"""
Publication Search Script — ORCID
Fetches scientific publications from ORCID public API using an ORCID ID.

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

    for group in works_data:
        summaries = group.get("work-summary", [])
        if not summaries:
            continue

        # Take the first summary (most complete)
        w = summaries[0]

        title   = w.get("title", {}).get("title", {}).get("value", "N/A")
        year_data = w.get("publication-date", {})
        year    = year_data.get("year", {}).get("value", "N/A") if year_data else "N/A"
        journal = w.get("journal-title", {}).get("value", "N/A") if w.get("journal-title") else "N/A"
        work_type = w.get("type", "N/A")

        # Extract DOI from external IDs
        doi = "N/A"
        ext_ids = w.get("external-ids", {}).get("external-id", [])
        for eid in ext_ids:
            if eid.get("external-id-type") == "doi":
                doi_val = eid.get("external-id-value", "")
                doi = f"https://doi.org/{doi_val}" if doi_val else "N/A"
                break

        papers.append({
            "title"  : title,
            "year"   : year,
            "journal": journal,
            "type"   : work_type,
            "doi"    : doi,
        })

    # Sort by year descending
    papers.sort(key=lambda x: x["year"] if x["year"] != "N/A" else "0000", reverse=True)

    return papers, author_name, orcid_id


# ── DISPLAY RESULTS ────────────────────────────────────────────────────────────
def display_results(papers, author_name, orcid_id):
    print(f"\n{'='*70}")
    print(f"  ORCID Publications — {author_name}")
    print(f"  ORCID ID : https://orcid.org/{orcid_id}")
    print(f"  Total    : {len(papers)}")
    print(f"{'='*70}\n")

    for i, paper in enumerate(papers, 1):
        print(f"[{i}] {paper['title']}")
        print(f"     Year   : {paper['year']}  |  Type: {paper['type']}")
        print(f"     Journal: {paper['journal']}")
        print(f"     DOI    : {paper['doi']}")
        print()


# ── SAVE TO JSON ───────────────────────────────────────────────────────────────
def save_results(papers, author_name, orcid_id):
    filename = f"items/{author_name.replace(' ', '_').replace(',', '')}_ORCID_{orcid_id}_publications.json"

    data = {
        "author"            : author_name,
        "orcid"             : f"https://orcid.org/{orcid_id}",
        "source"            : "ORCID",
        "total_publications": len(papers),
        "publications"      : papers,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Results saved to: {filename}")


# ── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    print("\n🔭 ORCID Publication Search Tool")
    print("─" * 40)
    orcid_input = input("  Enter ORCID ID (e.g. 0000-0001-5765-2061): ").strip()

    papers, author_name, orcid_id = search_orcid(orcid_input)

    if papers:
        display_results(papers, author_name, orcid_id)
        save = input("Save results to JSON file? (y/n): ").strip().lower()
        if save == "y":
            save_results(papers, author_name, orcid_id)
    else:
        print("⚠️  No publications found.")


if __name__ == "__main__":
    main()