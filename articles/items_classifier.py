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

# ── Configuration ─────────────────────────────────────────────────────────────

OLLAMA_MODEL = "llama3"          # Change to "mistral", "gemma3", etc. as needed
OLLAMA_HOST  = "http://localhost:11434"  # Default Ollama server address

DISCIPLINES = [
    "physics",
    "chemistry",
    "biology",
    "health sciences",
    "engineering",
]

SYSTEM_PROMPT = """You are a scientific publication classifier.
Your task is to classify a publication into exactly ONE of these disciplines:
- physics
- chemistry
- biology
- health sciences
- engineering

Rules:
- Reply ONLY with a valid JSON object, no extra text.
- The JSON must have two keys:
    "discipline": one of the five disciplines above (lowercase, exact spelling)
    "confidence": a float from 0.0 to 1.0 indicating how certain you are
- If the publication clearly spans two disciplines, pick the most dominant one.
- If you cannot determine the discipline, use "N/A" for discipline and 0.0 for confidence.

Example output:
{"discipline": "biology", "confidence": 0.92}
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

if __name__ == "__main__":
    sample_publications = [
        {
            "title": "Quantum entanglement in topological superconductors",
            "abstract": (
                "We investigate quantum entanglement properties of Majorana fermions "
                "in topological superconducting nanowires under an external magnetic field. "
                "Using density matrix renormalization group methods, we characterize the "
                "entanglement spectrum and its connection to bulk topological invariants."
            ),
            "journal": "Physical Review Letters",
            "affiliation": "Department of Physics, MIT",
        },
        {
            "title": "CRISPR-Cas9 genome editing in mammalian stem cells",
            "abstract": (
                "We report efficient CRISPR-Cas9-mediated genome editing in human "
                "induced pluripotent stem cells. Our protocol achieves >80% on-target "
                "efficiency with minimal off-target effects, enabling precise correction "
                "of disease-associated mutations."
            ),
            "journal": "Nature Cell Biology",
            "affiliation": "Broad Institute, Cambridge MA",
        },
        {
            "title": "Palladium-catalyzed cross-coupling of aryl halides",
            "abstract": (
                "A novel palladium catalyst system for Suzuki–Miyaura cross-coupling "
                "reactions of sterically hindered aryl chlorides is described. The catalyst "
                "exhibits exceptional turnover numbers and broad substrate scope, including "
                "electron-rich and electron-poor arenes."
            ),
            "journal": "Journal of the American Chemical Society",
            "affiliation": "Department of Chemistry, Stanford University",
        },
        {
            "title": "Deep learning for early detection of diabetic retinopathy",
            "abstract": (
                "A convolutional neural network trained on 128,000 retinal fundus images "
                "achieves AUC 0.99 for detection of diabetic retinopathy, outperforming "
                "general ophthalmologists. Prospective clinical validation across three "
                "hospital networks confirmed diagnostic accuracy."
            ),
            "journal": "JAMA Ophthalmology",
            "affiliation": "Stanford Medical Center",
        },
        {
            "title": "Topology optimization of additive-manufactured aerospace structures",
            "abstract": (
                "We present a density-based topology optimization framework for metal "
                "additive manufacturing of load-bearing aerospace components. Finite element "
                "analysis-driven design iterations reduce structural mass by 34% while "
                "satisfying fatigue and buckling constraints."
            ),
            "journal": "International Journal of Mechanical Sciences",
            "affiliation": "School of Aerospace Engineering, Georgia Tech",
        },
    ]

    print("=" * 60)
    print("Publication Classifier — Ollama")
    print(f"Model: {OLLAMA_MODEL}")
    print("=" * 60)

    results = classify_batch(sample_publications, model=OLLAMA_MODEL)

    print("\n── Summary ──────────────────────────────────────────────")
    for r in results:
        label = r["discipline"].upper().ljust(16)
        conf  = f"{r['confidence']:.0%}"
        title = r["title"][:55]
        print(f"  {label} ({conf})  {title}")