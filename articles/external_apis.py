"""
Shared HTTP helpers for Crossref and Semantic Scholar.

Used by orcidsearch.py (ingest) and items_classifier.py (batch classify) so each
DOI is not re-fetched unnecessarily: ingest can attach crossref_subjects and
fields_of_study to each publication record for later runs without extra calls.
"""

from __future__ import annotations

import re
from typing import Any

import requests

USER_AGENT = "SalvadoranArxivPubScript/1.0 (mailto:your@email.com)"


def strip_doi_prefix(doi: str | None) -> str:
    """Return bare DOI string for API paths, or '' if missing."""
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
    return s.strip()


def _clean_jats_abstract(raw: Any) -> str:
    if raw is None or raw == "N/A":
        return "N/A"
    if not isinstance(raw, str):
        return "N/A"
    text = re.sub(r"<[^>]+>", "", raw).strip()
    return text if text else "N/A"


def _crossref_subjects(message: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for s in message.get("subject") or []:
        if isinstance(s, dict):
            name = s.get("name")
            if isinstance(name, str) and name.strip():
                out.append(name.strip())
        elif isinstance(s, str) and s.strip():
            out.append(s.strip())
    return out


def fetch_crossref_work(doi: str, author_name: str) -> dict[str, Any]:
    """GET Crossref /works/{doi}; return abstract, affiliation, journal, subjects."""
    if not doi or doi == "N/A":
        return {
            "abstract": "N/A",
            "affiliation": "N/A",
            "journal": "N/A",
            "subjects": [],
        }

    raw_doi = strip_doi_prefix(doi)
    if not raw_doi:
        return {
            "abstract": "N/A",
            "affiliation": "N/A",
            "journal": "N/A",
            "subjects": [],
        }

    try:
        url = f"https://api.crossref.org/works/{raw_doi}"
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code != 200:
            return {
                "abstract": "N/A",
                "affiliation": "N/A",
                "journal": "N/A",
                "subjects": [],
            }

        data = response.json().get("message", {}) or {}

        abstract = _clean_jats_abstract(data.get("abstract"))

        affiliation = "N/A"
        crossref_authors = data.get("author") or []
        author_parts = author_name.lower().split()
        for ca in crossref_authors:
            if not isinstance(ca, dict):
                continue
            given = (ca.get("given") or "").lower()
            family = (ca.get("family") or "").lower()
            full = f"{given} {family}"
            if any(part in full for part in author_parts if len(part) > 2):
                affiliations = ca.get("affiliation") or []
                if affiliations and isinstance(affiliations[0], dict):
                    affiliation = affiliations[0].get("name", "N/A") or "N/A"
                break

        journal = "N/A"
        container = data.get("container-title") or []
        if container and isinstance(container[0], str):
            journal = (container[0] or "").strip() or "N/A"
        if journal == "N/A":
            short = data.get("short-container-title") or []
            if short and isinstance(short[0], str):
                journal = (short[0] or "").strip() or "N/A"

        subjects = _crossref_subjects(data if isinstance(data, dict) else {})

        return {
            "abstract": abstract,
            "affiliation": affiliation,
            "journal": journal,
            "subjects": subjects,
        }
    except Exception:
        return {
            "abstract": "N/A",
            "affiliation": "N/A",
            "journal": "N/A",
            "subjects": [],
        }


def fetch_semantic_scholar_work(doi: str, author_name: str) -> dict[str, Any]:
    """GET Semantic Scholar paper by DOI; same triple + fields_of_study."""
    if not doi or doi == "N/A":
        return {
            "abstract": "N/A",
            "affiliation": "N/A",
            "journal": "N/A",
            "fields_of_study": [],
        }

    raw_doi = strip_doi_prefix(doi)
    if not raw_doi:
        return {
            "abstract": "N/A",
            "affiliation": "N/A",
            "journal": "N/A",
            "fields_of_study": [],
        }

    fields = "abstract,authors.name,authors.affiliations,journal,venue,fieldsOfStudy"
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{raw_doi}?fields={fields}"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=15,
        )
        if response.status_code != 200:
            return {
                "abstract": "N/A",
                "affiliation": "N/A",
                "journal": "N/A",
                "fields_of_study": [],
            }

        data = response.json() or {}

        abstract = data.get("abstract")
        if isinstance(abstract, str) and abstract.strip():
            abstract = abstract.strip()
        else:
            abstract = "N/A"

        affiliation = "N/A"
        s2_authors = data.get("authors") or []
        author_parts = author_name.lower().split()
        for a in s2_authors:
            if not isinstance(a, dict):
                continue
            full = (a.get("name") or "").lower()
            if any(part in full for part in author_parts if len(part) > 2):
                affs = a.get("affiliations") or []
                if affs:
                    first = affs[0]
                    if isinstance(first, str) and first.strip():
                        affiliation = first.strip()
                    elif isinstance(first, dict):
                        cand = (first.get("name") or "").strip()
                        if cand:
                            affiliation = cand
                break

        journal = "N/A"
        j = data.get("journal") or {}
        if isinstance(j, dict):
            jname = (j.get("name") or "").strip()
            if jname:
                journal = jname
        if journal == "N/A":
            venue = (data.get("venue") or "").strip()
            if venue:
                journal = venue

        fos = data.get("fieldsOfStudy") or []
        fields_of_study: list[str] = []
        if isinstance(fos, list):
            for x in fos:
                if isinstance(x, str) and x.strip():
                    fields_of_study.append(x.strip())

        return {
            "abstract": abstract,
            "affiliation": affiliation,
            "journal": journal,
            "fields_of_study": fields_of_study,
        }
    except Exception:
        return {
            "abstract": "N/A",
            "affiliation": "N/A",
            "journal": "N/A",
            "fields_of_study": [],
        }


def fetch_semantic_scholar_fields_only(doi: str) -> list[str]:
    """Lightweight S2 lookup: only fieldsOfStudy (cheap follow-up for classification)."""
    raw_doi = strip_doi_prefix(doi)
    if not raw_doi:
        return []
    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/DOI:{raw_doi}"
        "?fields=fieldsOfStudy"
    )
    try:
        r = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=12,
        )
        if r.status_code != 200:
            return []
        fos = (r.json() or {}).get("fieldsOfStudy") or []
        if not isinstance(fos, list):
            return []
        return [x.strip() for x in fos if isinstance(x, str) and x.strip()]
    except Exception:
        return []
