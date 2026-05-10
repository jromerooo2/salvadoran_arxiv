"""
Publication Search Script — ORCID + Crossref
Fetches publications from ORCID and enriches them with abstracts and
affiliation at time of publication via Crossref.

Requirements:
    pip install requests

No API key needed.

Usage:
    python search_orcid.py
    Enter ORCID ID when prompted, e.g.: 0000-0001-5765-2061
    Or full URL:                         https://orcid.org/0000-0001-5765-2061
"""

import requests
import json
import re
import time
import os
import random

# ── FETCH ABSTRACT + AFFILIATION FROM CROSSREF ────────────────────────────────
def fetch_details_from_crossref(doi, author_name):
    """Fetch abstract and affiliation for a given DOI using the Crossref API."""
    if not doi or doi == "N/A":
        return "N/A", "N/A"

    raw_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")

    try:
        url = f"https://api.crossref.org/works/{raw_doi}"
        headers = {"User-Agent": "PublicationSearchScript/1.0 (mailto:your@email.com)"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json().get("message", {})

            # Abstract — clean JATS XML tags if present
            abstract = data.get("abstract", "N/A")
            abstract = re.sub(r"<[^>]+>", "", abstract).strip() if abstract != "N/A" else "N/A"

            # Affiliation — search among all authors for a name match
            affiliation = "N/A"
            crossref_authors = data.get("author", [])
            author_parts = author_name.lower().split()

            for ca in crossref_authors:
                given  = ca.get("given",  "").lower()
                family = ca.get("family", "").lower()
                full   = f"{given} {family}"

                # Match if any part of the ORCID author name appears in this author entry
                if any(part in full for part in author_parts if len(part) > 2):
                    affiliations = ca.get("affiliation", [])
                    if affiliations:
                        affiliation = affiliations[0].get("name", "N/A")
                    break

            return abstract, affiliation

    except Exception:
        pass

    return "N/A", "N/A"


# ── ORCID SEARCH ───────────────────────────────────────────────────────────────
def search_orcid(orcid_id):
    """Fetch publications from ORCID public API by ORCID ID."""

    # Normalize: strip URL if user pastes full ORCID URL
    orcid_id = orcid_id.strip()
    orcid_id = orcid_id.replace("https://orcid.org/", "").replace("http://orcid.org/", "")

    # Validate format: 0000-0000-0000-0000
    if not re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", orcid_id):
        print("❌ Invalid ORCID format. Expected: 0000-0000-0000-0000")
        return [], None, None

    headers = {"Accept": "application/json"}

    # Step 1: Get author name from profile
    print(f"\n🔍 Fetching ORCID profile for: {orcid_id} ...")
    profile_url = f"https://pub.orcid.org/v3.0/{orcid_id}/person"
    response = requests.get(profile_url, headers=headers)

    author_name = "Unknown"
    if response.status_code == 200:
        person = response.json()
        given  = person.get("name", {}).get("given-names", {}).get("value", "")
        family = person.get("name", {}).get("family-name", {}).get("value", "")
        author_name = f"{given} {family}".strip()
        print(f"✅ Profile found: {author_name} (ORCID: {orcid_id})")
    else:
        print(f"⚠️  Could not fetch profile (status {response.status_code}). Proceeding with works...")

    # Step 2: Get list of works
    print(f"🔍 Fetching publications ...")
    works_url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    response = requests.get(works_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ ORCID works error: {response.status_code}")
        return [], author_name, orcid_id

    works_data = response.json().get("group", [])
    papers = []
    total = len(works_data)
    skipped = 0

    for idx, group in enumerate(works_data, 1):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue

        w = summaries[0]

        title     = w.get("title", {}).get("title", {}).get("value", "N/A")
        year_data = w.get("publication-date", {})
        pub_year  = year_data.get("year", {}).get("value", "N/A") if year_data else "N/A"
        journal   = w.get("journal-title", {}).get("value", "N/A") if w.get("journal-title") else "N/A"

        # Extract DOI
        doi = "N/A"
        ext_ids = w.get("external-ids", {}).get("external-id", [])
        for eid in ext_ids:
            if eid.get("external-id-type") == "doi":
                doi_val = eid.get("external-id-value", "")
                doi = f"https://doi.org/{doi_val}" if doi_val else "N/A"
                break

        # ── Skip articles without a DOI ──────────────────────────────────────
        if doi == "N/A":
            print(f"  [{idx}/{total}] ⏭️  Skipping (no DOI): {title[:60]}")
            skipped += 1
            continue

        # Fetch abstract and affiliation from Crossref
        print(f"  [{idx}/{total}] Fetching details for: {title[:60]}...")
        abstract, affiliation = fetch_details_from_crossref(doi, author_name)
        
        # Remove leading "Abstract" or variants (case-insensitive, optional colon/space/dot)
        if abstract != "N/A":
            abstract = re.sub(r'^\s*abstract[:\.\s-]*', '', abstract, flags=re.IGNORECASE).lstrip()
 
        time.sleep(0.2)  # Be polite to the API

        # # ── ASSIGN CATEGORY ─────────────────────────────────────────────────────
        # # for simplicity, we will assing them randomly
        # # Load category codes from ../src/assets/content.json (relative to this script)

        # content_json_path = os.path.join(os.path.dirname(__file__), "../src/assets/content.json")
        # try:
        #     with open(content_json_path, "r", encoding="utf-8") as f:
        #         toc = json.load(f)
        #     category_codes = []
        #     for cat in toc:
        #         for sub in cat.get("subcategories", []):
        #             code = sub.get("subcategories_code")
        #             if code:
        #                 category_codes.append(code)
        # except Exception as e:
        #     print(f"Category code loading error: {e}")
        #     category_codes = ["phy-phys", "chem-org", "bio-bio", "health-phe", "eng-ece"]  # fallback

        # category = random.choice(category_codes) if category_codes else ""
        category = ""
        # # ───────────────────────────────────────────────────────────────────────

        papers.append({
            "title"      : title,
            "abstract"   : abstract,
            "year"       : pub_year,
            "journal"    : journal,
            "affiliation": affiliation,
            "doi"        : doi,
            'category'   : category,
        })

    # Sort by year descending
    papers.sort(key=lambda x: x["year"] if x["year"] != "N/A" else "0000", reverse=True)

    print(f"\n  ✅ {len(papers)} articles saved | ⏭️  {skipped} skipped (no DOI)")
    return papers, author_name, orcid_id


# ── DISPLAY RESULTS ────────────────────────────────────────────────────────────
def display_results(papers, author_name, orcid_id):
    print(f"\n{'='*70}")
    print(f"  ORCID Publications — {author_name}")
    print(f"  ORCID ID : https://orcid.org/{orcid_id}")
    print(f"  Total    : {len(papers)}")
    print(f"{'='*70}\n")

    for i, paper in enumerate(papers, 1):
        abstract_preview = (
            paper['abstract'][:150] + "..."
            if paper['abstract'] != "N/A" and len(paper['abstract']) > 150
            else paper['abstract']
        )

        print(f"[{i}] {paper['title']}")
        print(f"     Year        : {paper['year']}")
        print(f"     Journal     : {paper['journal']}")
        print(f"     Affiliation : {paper['affiliation']}")
        print(f"     DOI         : {paper['doi']}")
        print(f"     Abstract    : {abstract_preview}")
        print()


# ── SAVE TO JSON ───────────────────────────────────────────────────────────────
def _normalize_doi(doi):
    """Return a canonical lowercase DOI for deduplication.

    Strips common URL prefixes and surrounding whitespace. Returns an empty
    string for missing / empty / "N/A" values so callers can treat them as
    "no usable DOI".
    """
    if not isinstance(doi, str):
        return ""
    s = doi.strip()
    if not s or s.upper() == "N/A":
        return ""
    lower = s.lower()
    for prefix in ("https://doi.org/", "http://doi.org/",
                   "https://dx.doi.org/", "http://dx.doi.org/",
                   "doi:"):
        if lower.startswith(prefix):
            s = s[len(prefix):]
            break
    return s.strip().lower()


def save_results(papers, author_name, orcid_id, author_categories):
    filename = f"items/{author_name.replace(' ', '_').replace(',', '')}_ORCID_{orcid_id}_publications.json"

    # ── Load existing file (if any) so we can merge instead of overwriting ──
    existing_meta = None
    existing_pubs = []
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing_meta = json.load(f)
            raw_pubs = existing_meta.get("publications", []) if isinstance(existing_meta, dict) else []
            if isinstance(raw_pubs, list):
                existing_pubs = raw_pubs
        except (OSError, json.JSONDecodeError) as e:
            backup = filename + ".bak"
            print(f"⚠️  Could not read existing file '{filename}' ({e}).")
            try:
                os.rename(filename, backup)
                print(f"   Existing file backed up to: {backup}")
            except OSError:
                pass
            existing_meta = None
            existing_pubs = []

    existing_dois = {
        _normalize_doi(p.get("doi"))
        for p in existing_pubs
        if isinstance(p, dict) and _normalize_doi(p.get("doi"))
    }

    # ── Dedupe incoming papers against the existing DOIs ────────────────────
    added = []
    duplicates = 0
    no_doi = 0
    for paper in papers:
        norm = _normalize_doi(paper.get("doi") if isinstance(paper, dict) else None)
        if not norm:
            # Cannot dedupe safely — skip to avoid silently duplicating on re-runs.
            no_doi += 1
            continue
        if norm in existing_dois:
            duplicates += 1
            continue
        existing_dois.add(norm)
        added.append(paper)

    merged_pubs = existing_pubs + added

    # Re-derive author_categories from the merged set so metadata stays in sync
    # with the publications list. Fall back to the supplied value if empty.
    merged_cats = sorted({
        p["category"] for p in merged_pubs
        if isinstance(p, dict) and isinstance(p.get("category"), str)
        and p["category"] and p["category"] != ""
    })
    merged_cats_str = ", ".join(merged_cats) if merged_cats else (author_categories or "")

    # ── Build the output, preserving any extra keys from the existing file ──
    if isinstance(existing_meta, dict):
        data = dict(existing_meta)
        data["author"]             = existing_meta.get("author") or author_name
        data["orcid"]              = existing_meta.get("orcid") or f"https://orcid.org/{orcid_id}"
        data["source"]             = existing_meta.get("source") or "ORCID + Crossref"
        data["author_categories"]  = merged_cats_str
        data["total_publications"] = len(merged_pubs)
        data["publications"]       = merged_pubs
    else:
        data = {
            "author"            : author_name,
            "orcid"             : f"https://orcid.org/{orcid_id}",
            "source"            : "ORCID + Crossref",
            "total_publications": len(merged_pubs),
            "author_categories" : merged_cats_str,
            "publications"      : merged_pubs,
        }

    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    if isinstance(existing_meta, dict):
        print(f"✅ Updated: {filename}")
        msg = f"   ➕ {len(added)} new added | ⏭️  {duplicates} duplicate DOI(s) skipped"
        if no_doi:
            msg += f" | ⚠️  {no_doi} skipped (no DOI, cannot dedupe)"
        msg += f" | 📚 total: {len(merged_pubs)}"
        print(msg)
    else:
        msg = f"✅ Created: {filename} ({len(merged_pubs)} papers"
        if no_doi:
            msg += f", {no_doi} skipped without DOI"
        msg += ")"
        print(msg)


def extract_categories_string(papers):
    """
    Extracts unique categories from the list of paper dicts and
    returns them as a single string separated by ', '.
    """
    unique_categories = set()
    for paper in papers:
        cat = paper.get('category')
        if cat and cat != "":
            unique_categories.add(cat)
    return ', '.join(sorted(unique_categories))

# ── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    print("\n🔭 ORCID Publication Search Tool")
    print("─" * 40)

    with open("orcid_comunidad", "r", encoding="utf-8") as f:
        orcid_ids = [line.strip() for line in f if line.strip()]

    for orcid_input in orcid_ids:
        print(f"Processing ORCID ID: {orcid_input}")
        papers, author_name, orcid_id = search_orcid(orcid_input)
        author_categories = extract_categories_string(papers)

        if papers:
            display_results(papers, author_name, orcid_id)
            save_results(papers, author_name, orcid_id, author_categories)
        else:
            print(f"⚠️  No publications found for ORCID ID {orcid_input}.")

    # Prevent main() from re-running below, as we moved the logic to this loop.
    return

if __name__ == "__main__":
    main()