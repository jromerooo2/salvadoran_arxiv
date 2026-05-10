"""
Publication discipline classifier using Ollama (local LLM).

Requirements:
    pip install ollama

Setup:
    1. Install Ollama: https://ollama.com/download
    2. Pull a model: ollama pull llama3
    3. Run the Ollama server (it starts automatically on most installs)
"""

import ollama
import json
import re
import os

# ── Configuration ─────────────────────────────────────────────────────────────
OLLAMA_MODEL = "llama3"          # Change to "mistral", "gemma3", etc. as needed
OLLAMA_HOST  = "http://localhost:11434"  # Default Ollama server address
CONTENT_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'assets', 'content.json')

def _load_disciplines_from_content():
    """Return (sorted discipline names, {name: code}) read from content.json.

    Only `subcategories[*].subcategories_name` / `subcategories_code` are read —
    top-level `category_name` / `category_code` values (e.g. "Physics", "phy",
    "Mathematics", "math", ...) are intentionally ignored.
    """
    with open(CONTENT_JSON_PATH, 'r', encoding='utf-8') as f:
        content_obj = json.load(f)

    if not isinstance(content_obj, list):
        raise ValueError("Expected content.json to be a list of categories.")

    name_to_code: dict[str, str | None] = {}
    for category in content_obj:
        if not isinstance(category, dict):
            continue
        subcategories = category.get('subcategories')
        if not isinstance(subcategories, list):
            continue
        for sub in subcategories:
            if not isinstance(sub, dict):
                continue
            name = sub.get('subcategories_name')
            code = sub.get('subcategories_code')
            if isinstance(name, str) and name.strip():
                key = name.strip().lower()
                name_to_code[key] = code.strip() if isinstance(code, str) and code.strip() else None

    if not name_to_code:
        raise ValueError("No subcategory names found in content.json.")

    sorted_names = sorted(name_to_code)
    return sorted_names, {n: name_to_code[n] for n in sorted_names}

DISCIPLINES, DISCIPLINES_CODES = _load_disciplines_from_content()
_DISCIPLINES_BULLETS = "\n".join(f"- {d}" for d in DISCIPLINES)
SYSTEM_PROMPT = f"""You are a scientific publication classifier.
Your task is to classify a publication into exactly ONE of these disciplines:
{_DISCIPLINES_BULLETS}

Rules:
- Reply ONLY with a valid JSON object, no extra text.
- The JSON must have two keys:
    "discipline": one of the disciplines above (lowercase, exact spelling)
    "confidence": a float from 0.0 to 1.0 indicating how certain you are
- If the publication clearly spans two disciplines, pick the most dominant one.
- If you cannot determine the discipline, use "N/A" for discipline and 0.0 for confidence.

Example output:
{{"discipline": "{DISCIPLINES[0]}", "confidence": 0.92}}
"""

# ── Core classifier ────────────────────────────────────────────────────────────

def classify_with_ollama(
    title: str,
    abstract: str,
    journal: str = "",
    affiliation: str = "",
    model: str = OLLAMA_MODEL,
) -> dict:
    """
    Classify a publication using a local Ollama model.

    Returns a dict with keys:
        discipline  – one of the five disciplines (or "N/A")
        confidence  – float 0–1
        raw         – the raw LLM response string (useful for debugging)
    """
    user_message = f"""Classify this publication:

Title:       {title}
Abstract:    {abstract}
Journal:     {journal or 'N/A'}
Affiliation: {affiliation or 'N/A'}
"""

    try:
        client = ollama.Client(host=OLLAMA_HOST)
        response = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            options={"temperature": 0},   # deterministic output
        )
        raw = response["message"]["content"].strip()
        result = _parse_response(raw)
        result["raw"] = raw
        return result

    except ollama.ResponseError as e:
        return {"discipline": "N/A", "confidence": 0.0, "raw": str(e),
                "error": f"Ollama API error: {e}"}
    except Exception as e:
        return {"discipline": "N/A", "confidence": 0.0, "raw": "",
                "error": f"Unexpected error: {e}"}


def _parse_response(text: str) -> dict:
    """Extract JSON from the model reply, tolerating minor formatting issues."""
    # Try direct JSON parse first
    try:
        data = json.loads(text)
        return _validate(data)
    except json.JSONDecodeError:
        pass

    # Fallback: extract the first {...} block
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return _validate(data)
        except json.JSONDecodeError:
            pass

    return {"discipline": "N/A", "confidence": 0.0}


def _validate(data: dict) -> dict:
    """Ensure discipline is one of the allowed values."""
    discipline = str(data.get("discipline", "N/A")).strip().lower()
    if discipline not in DISCIPLINES:
        discipline = "N/A"
    confidence = float(data.get("confidence", 0.0))
    confidence = max(0.0, min(1.0, confidence))
    return {"discipline": discipline, "confidence": confidence}


# ── Batch helper ───────────────────────────────────────────────────────────────

def classify_batch(publications: list[dict], model: str = OLLAMA_MODEL) -> list[dict]:
    """
    Classify a list of publications.

    Each item in `publications` should be a dict with keys:
        title, abstract, journal (optional), affiliation (optional)

    Returns the same list with 'discipline' and 'confidence' added to each item.
    """
    results = []
    for i, pub in enumerate(publications, 1):
        print(f"  [{i}/{len(publications)}] Classifying: {pub.get('title', '')[:60]}...")
        classification = classify_with_ollama(
            title=pub.get("title", ""),
            abstract=pub.get("abstract", ""),
            journal=pub.get("journal", ""),
            affiliation=pub.get("affiliation", ""),
            model=model,
        )
        results.append({**pub, **classification})
        print(f"           → {classification['discipline']} "
              f"(confidence: {classification['confidence']:.2f})")
        if classification.get("error"):
            print(f"           ! {classification['error']}")
            exit()
            
    return results


# ── Drop-in replacement for the original heuristic function ───────────────────

def classify_section_discipline(
    title: str,
    abstract: str,
    journal: str = "",
    affiliation: str = "",
) -> str:
    """
    Drop-in replacement for the original keyword-based classifier.
    Returns only the discipline string (or 'N/A'), matching the original API.
    """
    result = classify_with_ollama(title, abstract, journal, affiliation)
    return result["discipline"]


# ── Demo ───────────────────────────────────────────────────────────────────────

def _load_publications_from_orcid_json(json_path: str) -> list[dict]:
    """Build a `sample_publications`-style list from an ORCID + Crossref JSON file.

    Keeps only the fields the classifier consumes (title, abstract, journal,
    affiliation) and normalizes "N/A" / missing values to empty strings so the
    LLM prompt isn't polluted with placeholder text.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    def _clean(v):
        if not isinstance(v, str):
            return ""
        s = v.strip()
        return "" if s.upper() == "N/A" else s

    publications = []
    for pub in info.get("publications", []):
        if not isinstance(pub, dict):
            continue
        # append only if category is unclasified
        category = pub.get("category", "")
        if category and category.lower() != "uncategorized":
            continue

        publications.append({
            "title"      : _clean(pub.get("title")),
            "abstract"   : _clean(pub.get("abstract")),
            "journal"    : _clean(pub.get("journal")),
            "affiliation": _clean(pub.get("affiliation")),
            "category"   : _clean(pub.get("category")),
            'doi'        : _clean(pub.get("doi")),
        })
    return publications, info


def _normalize_doi_for_match(doi) -> str:
    """Lowercased DOI with common URL/`doi:` prefixes stripped, '' if unusable."""
    if not isinstance(doi, str):
        return ""
    s = doi.strip()
    if not s or s.upper() == "N/A":
        return ""
    lower = s.lower()
    for prefix in ("https://doi.org/", "http://doi.org/",
                   "https://dx.doi.org/", "http://dx.doi.org/", "doi:"):
        if lower.startswith(prefix):
            s = s[len(prefix):]
            break
    return s.strip().lower()


def update_categories_in_file(json_path: str, results: list[dict]) -> dict:
    """Rewrite each publication's `category` in `json_path` using `results`.

    For every classification result, look up the discipline code via
    `DISCIPLINES_CODES` and write it back to the matching publication's
    `category` field (matching first by normalized DOI, then by title).
    `author_categories` is re-derived from the updated codes so the file's
    metadata stays consistent.

    Returns a small report dict with counts of updated / unchanged / unmatched
    papers and any discipline names that did not map to a code.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pubs = data.get("publications", [])
    if not isinstance(pubs, list):
        raise ValueError(f"'publications' in {json_path} is not a list.")

    by_doi: dict[str, str] = {}
    by_title: dict[str, str] = {}
    unmapped: list[str] = []
    for r in results:
        discipline = str(r.get("discipline", "")).strip().lower()
        code = DISCIPLINES_CODES.get(discipline)
        if not code:
            if discipline and discipline != "n/a":
                unmapped.append(discipline)
            continue
        norm = _normalize_doi_for_match(r.get("doi"))
        if norm:
            by_doi[norm] = code
        title = str(r.get("title", "")).strip().lower()
        if title:
            by_title[title] = code

    updated = unchanged = not_matched = 0
    for pub in pubs:
        if not isinstance(pub, dict):
            continue
        norm = _normalize_doi_for_match(pub.get("doi"))
        new_code = by_doi.get(norm) if norm else None
        if not new_code:
            new_code = by_title.get(str(pub.get("title", "")).strip().lower())
        if not new_code:
            not_matched += 1
            continue
        if pub.get("category") == new_code:
            unchanged += 1
        else:
            pub["category"] = new_code
            updated += 1

    cats = sorted({
        p["category"] for p in pubs
        if isinstance(p, dict) and isinstance(p.get("category"), str)
        and p["category"] and p["category"] != "uncategorized"
    })
    data["author_categories"] = ", ".join(cats)
    data["total_publications"] = sum(1 for p in pubs if isinstance(p, dict))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"📝 Categories updated in {json_path}")
    print(f"   ✏️  {updated} changed | ✓ {unchanged} unchanged | "
          f"❓ {not_matched} not matched | 🏷️  author_categories: "
          f"{data['author_categories'] or '(none)'}")
    if unmapped:
        print(f"   ⚠️  Disciplines without a code in DISCIPLINES_CODES: "
              f"{sorted(set(unmapped))}")

    return {
        "updated": updated,
        "unchanged": unchanged,
        "not_matched": not_matched,
        "unmapped_disciplines": sorted(set(unmapped)),
    }


if __name__ == "__main__":

    json_path = "/root/software/salvadoran_arxiv/articles/items/Erick_Urquilla_ORCID_0009-0007-3861-3223_publications.json"

    try:
        sample_publications, info = _load_publications_from_orcid_json(json_path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading {json_path}: {e}")
        raise SystemExit(1)

    print("=" * 60)
    print("Publication Classifier — Ollama")
    print(f"Model : {OLLAMA_MODEL}")
    print(f"Author: {info.get('author')}")
    print(f"ORCID : {info.get('orcid')}")
    print(f"Source: {info.get('source')}")
    print(f"Total : {info.get('total_publications')} "
          f"({len(sample_publications)} loaded for classification)")
    print("=" * 60)

    if not sample_publications:
        print("No uncategorized publications to classify. Nothing to do.")
        raise SystemExit(0)

    results = classify_batch(sample_publications, model=OLLAMA_MODEL)

    print("\n── Summary ──────────────────────────────────────────────")
    for r in results:
        label = r["discipline"]
        conf  = f"{r['confidence']:.0%}"
        title = r["title"][:55]
        print(f"  {label} ({conf})  {title}")

    print("\n── Writing categories back to file ──────────────────────")
    update_categories_in_file(json_path, results)