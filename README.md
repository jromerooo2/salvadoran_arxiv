# Salvadoran Repository of Sciences — ssscience.org

A public, open repository that gathers the scientific output of Salvadoran
researchers around the world. The idea is simple: if a Salvadoran researcher
publishes scientific articles anywhere in the world, the repository
automatically collects those works from their ORCID, classifies them by
discipline, and displays them in a browsable catalog. There is no fee to be
listed and no fee to consult.

## What the site contains

- **Home.** General search bar (by title, author, journal, year, DOI,
  abstract) and an index of scientific disciplines (Physics, Mathematics,
  Biology, Chemistry, Medicine, Engineering, Computer Science, Education,
  etc., with subdisciplines like Astrophysics, Condensed Matter, Genomics,
  Bioengineering, and so on). Each subdiscipline links directly to its
  recent articles and to the researchers who have published in it.
- **Researchers.** List of registered Salvadoran researchers, with name,
  ORCID, most recent institutional affiliation, number of publications in
  the catalog, and their research fields.
- **Articles.** Full catalog of collected articles (title, author, journal,
  year, DOI, abstract).
- **People.** Public members of the community (name, title/affiliation,
  institutional email).
- **About / Contact.** Project mission and direct contacts.
- **"Not listed yet? Add your ORCID here" inbox.** Lets any Salvadoran
  researcher who is not yet listed submit their ORCID and email address to
  request inclusion in the repository.

## How it works, step by step, from receiving an ORCID

1. **ORCID submission.** A researcher visits the site, enters their ORCID
   and email address into the form, checks the confirmation that they are
   Salvadoran, and submits. The request reaches the repository
   administrators as an email through a **Formspree** endpoint. The email
   body contains exactly two lines: the ORCID and the submitter's email.
2. **Brief manual validation.** Administrators add the ORCID to
   `articles/orcid_comunidad`, the master list of Salvadoran ORCIDs the
   repository tracks.
3. **Automated publication collection (`articles/orcidsearch.py`).** For
   each ORCID in the list:
   - The **public ORCID API** is queried
     (`https://pub.orcid.org/v3.0/{orcid}/person` and `/works`) to obtain
     the author's name and the full list of their published works.
   - For each work, the DOI is extracted. Works without a DOI are
     discarded — they cannot be enriched or deduplicated reliably.
4. **Metadata enrichment.** Each article is completed with additional
   information by querying two external scientific APIs:
   - **Crossref** (`https://api.crossref.org/works/{doi}`): provides the
     abstract, journal name, author affiliations at the time of
     publication, and the publisher's official subject categories.
   - **Semantic Scholar**
     (`https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}`): used as a
     fallback when Crossref does not return abstract, journal, or
     affiliation, and to obtain the *fields of study* produced by Semantic
     Scholar's classification model.
5. **Automated discipline classification
   (`articles/items_classifier.py`).** Each article is assigned a
   subdiscipline code (for example `phy-astro` for Astrophysics,
   `bio-genom` for Genetics & Genomics, `eng-ece` for Electrical &
   Computer Engineering). The classifier combines five signals into a
   single decision:
   1. **Exact-phrase rules:** a dictionary of highly specific phrases
      (e.g. *"gravitational wave"* → General Relativity, *"neutrino"* →
      High Energy Physics, *"machine learning"* → Electrical & Computer
      Engineering, *"crispr"* → Genetics & Genomics). If any of these
      phrases appears in the title or abstract, the discipline is decided
      directly.
   2. **Semantic Scholar scope:** the *fields of study* returned by S2
      restrict the candidate disciplines (e.g. if S2 says *Physics*, only
      Physics subdisciplines are considered).
   3. **Crossref subjects:** the publisher's official categories are used
      as an additional cue inside that scope.
   4. **Term scoring:** each discipline has its own keyword dictionary; the
      classifier counts occurrences across title + abstract + journal +
      subjects + fields_of_study and picks the discipline with the highest
      score, computing a 0–1 confidence value at the same time.
   5. **Conservative defaults:** when only a single broad S2 field is
      present and no other signals match, a sensible per-discipline default
      is assigned (for example a lone *physics* tag falls back to general
      *physics*).

   The classifier is fully deterministic and uses no language models.
   Everything runs in Python with `requests`, on any machine, with no API
   keys.
6. **Storage.** The result per researcher is saved as a JSON file at
   `articles/items/{Name}_ORCID_{id}_publications.json`. Each file contains
   the author's metadata (name, ORCID, accumulated categories) and the
   list of publications (title, abstract, year, journal, affiliation, DOI,
   category). The process is idempotent: re-running it for the same ORCID
   does not duplicate existing DOIs and only adds new works.
7. **Site publication.** The frontend (Vue 3 + Vite, deployed on Vercel)
   imports every JSON file at build time and merges them into a single
   browsable list. The catalog is then available instantly on the site,
   sorted by year descending, with multi-field search and navigation by
   discipline and by researcher.

## External APIs and services

| API / Service | Use | Key required |
|---|---|---|
| **ORCID Public API** (`pub.orcid.org/v3.0`) | Author profile and list of works | No |
| **Crossref REST API** (`api.crossref.org/works`) | Abstract, journal, affiliation, publisher subjects | No |
| **Semantic Scholar Graph API** (`api.semanticscholar.org/graph/v1/paper`) | Fallback for abstract / affiliation, plus fields of study | No |
| **Formspree** (`formspree.io/f/xeedlegn`) | Inbox for ORCID submission requests from the site | No (free plan) |
| **Vercel** | Static hosting (Vite build, custom domain, HTTPS) | — |

The first three are open, free scientific APIs that require no registration
and no paid quota at the project's current volume.

## Tech stack

- **Frontend:** Vue 3, Vue Router, Tailwind CSS, Vite. Small static SPA
  deployed on Vercel.
- **Data backend:** Python scripts (no long-running server). All ingestion,
  enrichment, and classification logic runs offline, which keeps the site
  fast, cheap (no database, no server), and reproducible.
- **Persistence:** JSON files versioned in Git. There is no database. This
  makes it easy to audit exactly what data is published and allows the
  community to propose corrections via pull request.

## Repository layout

```
salvadoran_arxiv/
├── index.html                      # SPA entry point (Vite)
├── vite.config.js
├── vercel.json                     # SPA rewrite for Vercel (deep links)
├── public/                         # Static assets
├── src/
│   ├── App.vue                     # Layout (Navbar + router-view + Footer)
│   ├── main.js                     # Vue bootstrap
│   ├── router.js                   # Routes: /, /researchers, /articles, ...
│   ├── components/                 # Navbar, Footer, SearchBar, Tarjetas, OrcidSubmissionBox
│   ├── views/                      # Home, Researchers, Articles, People, About, Contact, SearchResults
│   ├── data/                       # Adapters that read articles/items/*.json
│   ├── assets/                     # content.json (taxonomy), logo
│   └── styles/
├── articles/
│   ├── orcid_comunidad             # Master list of tracked ORCIDs
│   ├── orcidsearch.py              # Ingestion: ORCID → Crossref/S2 → JSON
│   ├── items_classifier.py         # Deterministic discipline classifier
│   ├── external_apis.py            # HTTP helpers for Crossref and Semantic Scholar
│   └── items/                      # Per-author JSON (pipeline output)
└── comunidad/
    ├── people.json                 # Public members of the community
    └── extract_data.py
```

## Local development

### Frontend (Vue + Vite)

```bash
npm install
npm run dev        # Development server
npm run build      # Production build into dist/
npm run preview    # Serve the production build locally
```

### Data pipeline (Python)

```bash
pip install requests
cd articles
# Reads the ORCID list and creates/updates items/*.json
python orcidsearch.py
# (Re)classifies every existing item
python items_classifier.py
```

None of the scripts require API keys or paid accounts. New publications
appear on the site once the generated JSON is committed and deployed.

## Who is behind this

The repository was conceived and built by **Erick Urquilla** (PhD in
Physics, University of Tennessee, Knoxville) and **Juan Romero**
(Mechanical Engineering, Georgia Institute of Technology). It is part of
the broader effort of the Salvadoran international scientific community,
whose mission and origin story are described on the site's *About* page:
to make Salvadoran science visible and to connect researchers abroad with
universities and students back in El Salvador.

## Contact

For general inquiries and contributions: `elsalvador.stem@gmail.com`.
Community-specific and repository-specific contacts are listed on the
[Contact](https://www.sssciences.org/contact) page of the site.
