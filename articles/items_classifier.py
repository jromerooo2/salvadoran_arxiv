"""
Publication discipline classifier using Crossref subjects, Semantic Scholar
fieldsOfStudy, and lightweight text signals (no local LLM).

Requirements:
    pip install requests

Ingest (orcidsearch.py) attaches ``crossref_subjects`` and ``fields_of_study`` when
available so batch runs can classify without repeating full metadata fetches.
Optional one cheap S2 call (fieldsOfStudy only) fills gaps for older JSON files.
"""

from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Iterable

_ARTICLES_DIR = os.path.dirname(os.path.abspath(__file__))
if _ARTICLES_DIR not in sys.path:
    sys.path.insert(0, _ARTICLES_DIR)

from external_apis import fetch_semantic_scholar_fields_only

# ── Configuration ─────────────────────────────────────────────────────────────
MAX_WORKERS = 4
CONTENT_JSON_PATH = os.path.join(
    os.path.dirname(__file__), "..", "src", "assets", "content.json"
)


def _load_disciplines_from_content() -> tuple[list[str], dict[str, str | None]]:
    """Return (sorted discipline names, {name: code}) from content.json subcategories."""
    with open(CONTENT_JSON_PATH, "r", encoding="utf-8") as f:
        content_obj = json.load(f)

    if not isinstance(content_obj, list):
        raise ValueError("Expected content.json to be a list of categories.")

    name_to_code: dict[str, str | None] = {}
    for category in content_obj:
        if not isinstance(category, dict):
            continue
        subcategories = category.get("subcategories")
        if not isinstance(subcategories, list):
            continue
        for sub in subcategories:
            if not isinstance(sub, dict):
                continue
            name = sub.get("subcategories_name")
            code = sub.get("subcategories_code")
            if isinstance(name, str) and name.strip():
                key = name.strip().lower()
                name_to_code[key] = (
                    code.strip() if isinstance(code, str) and code.strip() else None
                )

    if not name_to_code:
        raise ValueError("No subcategory names found in content.json.")

    sorted_names = sorted(name_to_code)
    return sorted_names, {n: name_to_code[n] for n in sorted_names}


DISCIPLINES, DISCIPLINES_CODES = _load_disciplines_from_content()
ALL_DISCIPLINE_KEYS = frozenset(DISCIPLINES_CODES.keys())

# Semantic Scholar coarse fields (lowercase) -> candidate disciplines (exact keys)
S2_SCOPE: dict[str, frozenset[str]] = {
    "physics": frozenset(
        {
            "astrophysics",
            "condensed matter",
            "general relativity and cosmology",
            "high energy physics",
            "nuclear physics",
            "quantum physics",
            "physics",
        }
    ),
    "mathematics": frozenset(
        {
            "algebra & number theory",
            "analysis & differential equations",
            "geometry & topology",
            "applied & computational mathematics",
            "probability & statistics",
            "combinatorics & discrete mathematics",
        }
    ),
    "biology": frozenset(
        {
            "molecular biology",
            "ecology & evolution",
            "cell biology",
            "neuroscience",
            "genetics & genomics",
        }
    ),
    "chemistry": frozenset(
        {
            "organic chemistry",
            "inorganic chemistry",
            "physical chemistry",
            "biochemistry",
            "materials & nanochemistry",
        }
    ),
    "medicine": frozenset(
        {
            "public health & epidemiology",
            "clinical & translational research",
            "nursing & allied health",
            "pharmacology & drug development",
            "global & community health",
            "biomedical informatics",
        }
    ),
    "engineering": frozenset(
        {
            "electrical & computer engineering",
            "mechanical engineering",
            "civil & environmental engineering",
            "chemical engineering",
            "biomedical engineering",
        }
    ),
    "computer science": frozenset(
        {
            "electrical & computer engineering",
            "mechanical engineering",
            "biomedical engineering",
            "biomedical informatics",
        }
    ),
    "materials science": frozenset({"materials & nanochemistry", "physical chemistry"}),
    "environmental science": frozenset(
        {"civil & environmental engineering", "ecology & evolution"}
    ),
    "education": frozenset(
        {
            "physics education",
            "mathematics education",
            "biology education",
            "chemistry education",
            "engineering education",
            "health sciences education",
        }
    ),
    "psychology": frozenset({"neuroscience", "clinical & translational research"}),
    "sociology": frozenset({"public health & epidemiology", "global & community health"}),
    "political science": frozenset({"global & community health"}),
    "economics": frozenset({"probability & statistics"}),
    "geography": frozenset({"ecology & evolution", "civil & environmental engineering"}),
    "agricultural and food sciences": frozenset(
        {"ecology & evolution", "molecular biology"}
    ),
    "history": frozenset({"physics education"}),  # weak; usually overridden by text
    "linguistics": frozenset(),
    "philosophy": frozenset(),
    "art": frozenset(),
    "business": frozenset(),
    "law": frozenset(),
    "geology": frozenset({"civil & environmental engineering", "ecology & evolution"}),
}

S2_SINGLE_DEFAULT: dict[str, str] = {
    "physics": "physics",
    "mathematics": "applied & computational mathematics",
    "biology": "molecular biology",
    "chemistry": "physical chemistry",
    "medicine": "clinical & translational research",
    "engineering": "mechanical engineering",
    "computer science": "electrical & computer engineering",
    "materials science": "materials & nanochemistry",
    "environmental science": "civil & environmental engineering",
    "education": "physics education",
    "psychology": "neuroscience",
    "sociology": "public health & epidemiology",
    "political science": "global & community health",
    "economics": "probability & statistics",
    "geography": "ecology & evolution",
    "agricultural and food sciences": "ecology & evolution",
    "geology": "civil & environmental engineering",
}

# Longer phrases first: (substring_lower, discipline_key)
_PHRASE_RULES_RAW: list[tuple[str, str]] = [
    ("quantum information", "quantum physics"),
    ("quantum computing", "quantum physics"),
    ("quantum error", "quantum physics"),
    ("qubit", "quantum physics"),
    ("tensor network", "quantum physics"),
    ("dark energy", "astrophysics"),
    ("dark matter", "astrophysics"),
    ("baryon acoustic", "astrophysics"),
    ("type ia supernova", "astrophysics"),
    ("supernova", "high energy physics"),
    ("neutron star merger", "high energy physics"),
    ("core-collapse supernova", "high energy physics"),
    ("neutrino fast flavor", "high energy physics"),
    ("neutrino flavor", "high energy physics"),
    ("neutrino", "high energy physics"),
    ("black hole", "astrophysics"),
    ("gravitational wave", "general relativity and cosmology"),
    ("general relativity", "general relativity and cosmology"),
    ("cosmological", "astrophysics"),
    ("inflationary", "astrophysics"),
    ("lattice qcd", "high energy physics"),
    ("standard model", "high energy physics"),
    ("higgs", "high energy physics"),
    ("large hadron collider", "high energy physics"),
    ("particle physics", "high energy physics"),
    ("quantum field theory", "high energy physics"),
    ("graphene", "condensed matter"),
    ("superconduct", "condensed matter"),
    ("condensed matter", "condensed matter"),
    ("many-body", "condensed matter"),
    ("nuclear structure", "nuclear physics"),
    ("nuclear reaction", "nuclear physics"),
    ("radioactive", "nuclear physics"),
    ("protein structure", "biochemistry"),
    ("enzyme", "biochemistry"),
    ("metabol", "biochemistry"),
    ("organic synthesis", "organic chemistry"),
    ("catalyst", "physical chemistry"),
    ("polymer", "materials & nanochemistry"),
    ("nanoparticle", "materials & nanochemistry"),
    ("genome-wide", "genetics & genomics"),
    ("crispr", "genetics & genomics"),
    ("single-cell", "cell biology"),
    ("neural circuit", "neuroscience"),
    ("brain imaging", "neuroscience"),
    ("ecosystem", "ecology & evolution"),
    ("biodiversity", "ecology & evolution"),
    ("epidemiolog", "public health & epidemiology"),
    ("randomized controlled trial", "clinical & translational research"),
    ("clinical trial", "clinical & translational research"),
    ("finite element", "mechanical engineering"),
    ("cfd", "mechanical engineering"),
    ("structural health", "civil & environmental engineering"),
    ("wastewater", "civil & environmental engineering"),
    ("machine learning", "electrical & computer engineering"),
    ("deep learning", "electrical & computer engineering"),
    ("neural network", "electrical & computer engineering"),
    ("reinforcement learning", "electrical & computer engineering"),
    ("control system", "electrical & computer engineering"),
    ("semiconductor", "electrical & computer engineering"),
    ("heat transfer", "mechanical engineering"),
    ("fluid dynamics", "mechanical engineering"),
    ("chemical reactor", "chemical engineering"),
    ("distillation column", "chemical engineering"),
    ("stem education", "physics education"),
    ("undergraduate physics", "physics education"),
    ("algebraic geometry", "geometry & topology"),
    ("differential geometry", "geometry & topology"),
    ("partial differential equation", "analysis & differential equations"),
    ("stochastic process", "probability & statistics"),
    ("graph theory", "combinatorics & discrete mathematics"),
    ("prime number", "algebra & number theory"),
    ("galois theory", "algebra & number theory"),
    ("health informatics", "biomedical informatics"),
    ("electronic health record", "biomedical informatics"),
]

PHRASE_RULES = sorted(_PHRASE_RULES_RAW, key=lambda x: len(x[0]), reverse=True)

# Keyword hints per discipline (substring match in blob)
DISCIPLINE_TERMS: dict[str, tuple[str, ...]] = {
    "astrophysics": (
        "cosmolog",
        "galaxy",
        "dark energy",
        "dark matter",
        "cmb",
        "exoplanet",
        "astrophys",
    ),
    "general relativity and cosmology": (
        "gravitational wave",
        "ligo",
        "black hole",
        "spacetime",
        "einstein",
        "horizon",
    ),
    "high energy physics": (
        "neutrino",
        "quark",
        "boson",
        "collider",
        "lhc",
        "particle",
        "hadron",
        "electroweak",
    ),
    "condensed matter": (
        "condensed",
        "superconduct",
        "graphene",
        "band gap",
        "phonon",
        "lattice",
    ),
    "nuclear physics": ("nuclear", "isotope", "fission", "fusion", "nucleon"),
    "quantum physics": (
        "quantum",
        "entanglement",
        "qubit",
        "decoherence",
        "hamiltonian",
    ),
    "physics": ("physics", "phys. rev", "physical review"),
    "algebra & number theory": ("algebra", "number theory", "galois", "ring theory"),
    "analysis & differential equations": (
        "pde",
        "ode",
        "sobolev",
        "harmonic analysis",
    ),
    "geometry & topology": ("topology", "manifold", "curvature", "cohomology"),
    "applied & computational mathematics": (
        "numerical",
        "finite element",
        "optimization",
        "simulation",
    ),
    "probability & statistics": (
        "bayesian",
        "markov",
        "regression",
        "stochastic",
        "inference",
    ),
    "combinatorics & discrete mathematics": (
        "combinator",
        "graph theory",
        "discrete",
    ),
    "molecular biology": ("mrna", "protein", "dna", "rna", "replication", "polymerase"),
    "cell biology": ("cell cycle", "mitochond", "cytoskeleton", "cellular"),
    "neuroscience": ("neuron", "synapse", "cortex", "eeg", "neuro"),
    "genetics & genomics": ("genome", "gene", "mutation", "sequencing", "allele"),
    "ecology & evolution": ("evolution", "species", "ecosystem", "selection", "habitat"),
    "organic chemistry": ("organic", "synthesis", "reagent", "stereochem"),
    "inorganic chemistry": ("inorganic", "coordination", "ligand", "metal complex"),
    "physical chemistry": ("spectroscop", "thermodynam", "kinetics", "electrochem"),
    "biochemistry": ("enzyme", "substrate", "pathway", "metabol"),
    "materials & nanochemistry": ("nanoparticle", "nanomaterial", "thin film", "polymer"),
    "electrical & computer engineering": (
        "circuit",
        "fpga",
        "microcontroller",
        "signal processing",
        "antenna",
        "wireless",
    ),
    "mechanical engineering": (
        "turbine",
        "robotics",
        "mechanical",
        "cfd",
        "heat exchanger",
    ),
    "civil & environmental engineering": (
        "concrete",
        "structural",
        "hydrology",
        "seismic",
        "wastewater",
    ),
    "chemical engineering": ("reactor", "distillation", "mass transfer", "catalyst bed"),
    "biomedical engineering": ("prosthetic", "biomaterial", "tissue engineering", "imaging"),
    "public health & epidemiology": (
        "epidemi",
        "population health",
        "outbreak",
        "vaccination",
    ),
    "clinical & translational research": (
        "clinical trial",
        "patient cohort",
        "diagnosis",
        "therapy",
    ),
    "nursing & allied health": ("nursing", "allied health", "patient care"),
    "pharmacology & drug development": ("pharmacokinetic", "drug", "dose", "clinical pharmac"),
    "global & community health": ("community health", "global health", "health equity"),
    "biomedical informatics": ("ehr", "informatics", "health record", "icd"),
    "physics education": ("physics education", "concept inventory", "undergraduate physics"),
    "mathematics education": ("mathematics education", "math anxiety", "calculus class"),
    "biology education": ("biology education", "biology lab"),
    "chemistry education": ("chemistry education", "general chemistry"),
    "engineering education": ("engineering education", "design course"),
    "health sciences education": ("medical education", "health professions education"),
}


def _normalize_list(val: Any) -> list[str]:
    if not val:
        return []
    if isinstance(val, str):
        return [val] if val.strip() else []
    if isinstance(val, list):
        return [str(x).strip() for x in val if isinstance(x, (str, int)) and str(x).strip()]
    return []


def _merge_scopes(fields_lower: Iterable[str]) -> frozenset[str] | None:
    scopes: list[frozenset[str]] = []
    for fos in fields_lower:
        key = fos.strip().lower()
        sc = S2_SCOPE.get(key)
        if sc is not None and len(sc) > 0:
            scopes.append(sc)
    if not scopes:
        return None
    out: set[str] = set()
    for s in scopes:
        out |= set(s)
    return frozenset(out)


def _phrase_match(blob: str) -> tuple[str, float] | None:
    for phrase, disc in PHRASE_RULES:
        if phrase in blob and disc in ALL_DISCIPLINE_KEYS:
            return disc, 0.88
    return None


def _score_terms(blob: str, candidates: frozenset[str] | None) -> tuple[str, float]:
    best_d = ""
    best_s = 0.0
    second = 0.0
    for d, terms in DISCIPLINE_TERMS.items():
        if candidates is not None and d not in candidates:
            continue
        s = sum(len(t) for t in terms if t in blob)
        if s > best_s:
            second = best_s
            best_s = s
            best_d = d
        elif s > second:
            second = s
    if best_s <= 0 or not best_d:
        return "", 0.0
    margin = (best_s - second) / max(best_s, 1.0)
    conf = min(0.93, 0.52 + 0.18 * margin + 0.01 * min(best_s, 40.0))
    return best_d, conf


def _default_from_s2(fields_lower: list[str]) -> tuple[str, float] | None:
    if len(fields_lower) == 1:
        d = S2_SINGLE_DEFAULT.get(fields_lower[0])
        if d and d in ALL_DISCIPLINE_KEYS:
            return d, 0.58
    return None


def classify_from_signals(
    title: str,
    abstract: str,
    journal: str,
    crossref_subjects: list[str] | None,
    fields_of_study: list[str] | None,
) -> dict[str, Any]:
    """
    Return discipline (content.json subcategory key, lowercased), confidence,
    and raw trace string. No HTTP performed.
    """
    subs = _normalize_list(crossref_subjects)
    fos = _normalize_list(fields_of_study)
    parts = [title, abstract, journal, " ".join(subs), " ".join(fos)]
    blob = " ".join(p for p in parts if isinstance(p, str)).lower()
    fields_lower = [f.lower() for f in fos]

    trace: list[str] = []

    pm = _phrase_match(blob)
    if pm:
        trace.append(f"phrase:{pm[0]}")
        return {"discipline": pm[0], "confidence": pm[1], "raw": "; ".join(trace)}

    scope = _merge_scopes(fields_lower)
    if scope is None:
        scope = ALL_DISCIPLINE_KEYS
        trace.append("scope:all")
    else:
        trace.append(f"scope:s2={','.join(fields_lower)}")

    disc, conf = _score_terms(blob, scope)
    if disc:
        trace.append(f"terms:{disc}")
        return {"discipline": disc, "confidence": conf, "raw": "; ".join(trace)}

    ddef = _default_from_s2(fields_lower)
    if ddef:
        trace.append(f"s2_default:{ddef[0]}")
        return {"discipline": ddef[0], "confidence": ddef[1], "raw": "; ".join(trace)}

    # Last pass: ignore S2 scope if it was too narrow and produced no hit
    if scope is not ALL_DISCIPLINE_KEYS:
        disc2, conf2 = _score_terms(blob, ALL_DISCIPLINE_KEYS)
        if disc2:
            trace.append(f"terms_global:{disc2}")
            return {"discipline": disc2, "confidence": conf2 * 0.92, "raw": "; ".join(trace)}

    return {"discipline": "n/a", "confidence": 0.0, "raw": "; ".join(trace) or "no_match"}


def classify_with_apis(
    title: str,
    abstract: str,
    journal: str = "",
    affiliation: str = "",
    doi: str = "",
    crossref_subjects: list[str] | None = None,
    fields_of_study: list[str] | None = None,
    fetch_s2_fields_if_empty: bool = True,
) -> dict[str, Any]:
    """
    Classify using stored API hints; optionally one lightweight S2 fieldsOfStudy
    request when hints are missing and DOI is available. ``affiliation`` is unused
    but kept for call-site compatibility.
    """
    fos = list(fields_of_study or [])
    if (
        fetch_s2_fields_if_empty
        and not fos
        and doi
        and str(doi).strip().upper() != "N/A"
    ):
        extra = fetch_semantic_scholar_fields_only(doi)
        if extra:
            fos = extra

    result = classify_from_signals(
        title, abstract, journal, crossref_subjects, fos
    )
    result["raw"] = (result.get("raw") or "") + (
        ";s2_fetch" if (fields_of_study or []) != fos and fos else ""
    )
    return result


def classify_batch(publications: list[dict], **kw: Any) -> list[dict]:
    results = []
    fetch = kw.get("fetch_s2_fields_if_empty", True)
    for i, pub in enumerate(publications, 1):
        print(f"  [{i}/{len(publications)}] Classifying: {pub.get('title', '')[:60]}...")
        classification = classify_with_apis(
            title=pub.get("title", ""),
            abstract=pub.get("abstract", ""),
            journal=pub.get("journal", ""),
            affiliation=pub.get("affiliation", ""),
            doi=pub.get("doi", ""),
            crossref_subjects=pub.get("crossref_subjects"),
            fields_of_study=pub.get("fields_of_study"),
            fetch_s2_fields_if_empty=fetch,
        )
        results.append({**pub, **classification})
        print(
            f"           → {classification['discipline']} "
            f"(confidence: {classification['confidence']:.2f})"
        )
    return results


def classify_batch_parallel(
    publications: list[dict],
    max_workers: int = MAX_WORKERS,
    fetch_s2_fields_if_empty: bool = True,
) -> list[dict]:
    if not publications:
        return []

    workers = max(1, min(max_workers, len(publications)))
    total = len(publications)
    results: list[dict | None] = [None] * total
    done = 0

    def _one(idx: int, pub: dict):
        classification = classify_with_apis(
            title=pub.get("title", ""),
            abstract=pub.get("abstract", ""),
            journal=pub.get("journal", ""),
            affiliation=pub.get("affiliation", ""),
            doi=pub.get("doi", ""),
            crossref_subjects=pub.get("crossref_subjects"),
            fields_of_study=pub.get("fields_of_study"),
            fetch_s2_fields_if_empty=fetch_s2_fields_if_empty,
        )
        return idx, pub, classification

    print(f"  Classifying {total} publications with {workers} parallel workers...")
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_one, i, p) for i, p in enumerate(publications)]
        for fut in as_completed(futures):
            idx, pub, classification = fut.result()
            results[idx] = {**pub, **classification}
            done += 1
            print(
                f"  [{done}/{total}] → {classification['discipline']:32s} "
                f"(conf: {classification['confidence']:.2f})  "
                f"{pub.get('title', '')[:45]}"
            )

    return [r for r in results if r is not None]


def classify_section_discipline(
    title: str,
    abstract: str,
    journal: str = "",
    affiliation: str = "",
) -> str:
    r = classify_with_apis(
        title,
        abstract,
        journal,
        affiliation,
        doi="",
        crossref_subjects=None,
        fields_of_study=None,
        fetch_s2_fields_if_empty=False,
    )
    return r["discipline"]


def infer_category_code_from_record(
    pub: dict,
    *,
    fetch_s2_if_needed: bool = True,
) -> str:
    """Return a ``subcategories_code`` value or '' if classification fails."""
    r = classify_with_apis(
        title=str(pub.get("title") or ""),
        abstract=str(pub.get("abstract") or ""),
        journal=str(pub.get("journal") or ""),
        affiliation=str(pub.get("affiliation") or ""),
        doi=str(pub.get("doi") or ""),
        crossref_subjects=pub.get("crossref_subjects"),
        fields_of_study=pub.get("fields_of_study"),
        fetch_s2_fields_if_empty=fetch_s2_if_needed,
    )
    disc = str(r.get("discipline", "")).strip().lower()
    code = DISCIPLINES_CODES.get(disc)
    return code if isinstance(code, str) and code.strip() else ""


def _load_publications_from_orcid_json(json_path: str) -> tuple[list[dict], dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    def _clean(v: Any) -> str:
        if not isinstance(v, str):
            return ""
        s = v.strip()
        return "" if s.upper() == "N/A" else s

    publications = []
    for pub in info.get("publications", []):
        if not isinstance(pub, dict):
            continue
        category = pub.get("category", "")
        if category and str(category).lower() != "uncategorized":
            continue

        publications.append(
            {
                "title": _clean(pub.get("title")),
                "abstract": _clean(pub.get("abstract")),
                "journal": _clean(pub.get("journal")),
                "affiliation": _clean(pub.get("affiliation")),
                "category": _clean(pub.get("category")),
                "doi": _clean(pub.get("doi")),
                "crossref_subjects": _normalize_list(pub.get("crossref_subjects")),
                "fields_of_study": _normalize_list(pub.get("fields_of_study")),
            }
        )
    return publications, info


def _normalize_doi_for_match(doi: Any) -> str:
    if not isinstance(doi, str):
        return ""
    s = doi.strip()
    if not s or s.upper() == "N/A":
        return ""
    lower = s.lower()
    for prefix in (
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
        "doi:",
    ):
        if lower.startswith(prefix):
            s = s[len(prefix) :]
            break
    return s.strip().lower()


def update_categories_in_file(json_path: str, results: list[dict]) -> dict[str, Any]:
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

    cats = sorted(
        {
            p["category"]
            for p in pubs
            if isinstance(p, dict)
            and isinstance(p.get("category"), str)
            and p["category"]
            and p["category"] != "uncategorized"
        }
    )
    data["author_categories"] = ", ".join(cats)
    data["total_publications"] = sum(1 for p in pubs if isinstance(p, dict))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"📝 Categories updated in {json_path}")
    print(
        f"   ✏️  {updated} changed | ✓ {unchanged} unchanged | "
        f"❓ {not_matched} not matched | 🏷️  author_categories: "
        f"{data['author_categories'] or '(none)'}"
    )
    if unmapped:
        print(
            f"   ⚠️  Disciplines without a code in DISCIPLINES_CODES: "
            f"{sorted(set(unmapped))}"
        )

    return {
        "updated": updated,
        "unchanged": unchanged,
        "not_matched": not_matched,
        "unmapped_disciplines": sorted(set(unmapped)),
    }


if __name__ == "__main__":
    items_dir = os.path.join(os.path.dirname(__file__), "items")
    items_paths = [
        os.path.join(items_dir, fname)
        for fname in os.listdir(items_dir)
        if fname.endswith("_publications.json")
    ]
    print("Found items files:")
    for p in items_paths:
        print("  ", p)

    for json_path in items_paths:
        print("=" * 60)
        print(f"Processing {json_path}")
        print("=" * 60)
        try:
            sample_publications, info = _load_publications_from_orcid_json(json_path)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error reading {json_path}: {e}")
            continue

        print("Publication Classifier — Crossref / Semantic Scholar signals")
        print(f"Author : {info.get('author')}")
        print(f"ORCID  : {info.get('orcid')}")
        print(f"Source : {info.get('source')}")
        print(
            f"Total  : {info.get('total_publications')} "
            f"({len(sample_publications)} loaded for classification)"
        )
        print(f"Workers: {MAX_WORKERS}")
        print("=" * 60)

        if not sample_publications:
            print("No uncategorized publications to classify. Skipping.")
            continue

        results = classify_batch_parallel(
            sample_publications,
            max_workers=MAX_WORKERS,
            fetch_s2_fields_if_empty=True,
        )

        print("\n── Writing categories back to file ──────────────────────")
        update_categories_in_file(json_path, results)
