🌍 Autonomous GeoAI ESG Auditor

An AI-driven Spatio-Temporal Verification Engine for Corporate Sustainability Claims

📌 Overview

The Autonomous GeoAI ESG Auditor is an enterprise-grade AI pipeline designed to detect corporate "greenwashing." It autonomously extracts environmental restoration claims from unstructured corporate reports, locates the exact geographic project site, and fetches multi-temporal satellite telemetry to mathematically verify if ecological restoration actually occurred.

This tool bridges the gap between static text claims and live global satellite data, providing an objective, mathematical truth (with confidence scoring) that corporate disclosures often lack.

🏗️ System Architecture

The system is built as a decoupled, modular architecture designed for scalability and API-resilience:

Phase 1: NLP Ingestion Engine (nlp_extractor.py) Uses spaCy and dynamic Regex to parse unstructured text, extract geospatial entities, and calculate temporal baselines. Includes a custom Location Sanitizer to resolve Geocoding centroid ambiguities.

Phase 2: Geospatial API Router (geo_vision.py) Intelligently routes requests between the ESA Sentinel-2 EOX Archive (for historical baseline telemetry) and ArcGIS World Imagery (for live/current telemetry) based on the extracted temporal claim.

Phase 3: Computer Vision Verification Engine Employs HSV-based semantic segmentation to isolate vegetation canopies and calculates a mathematically rigorous Spatio-Temporal Delta ($\Delta$) with a built-in statistical noise-tolerance buffer.

💻 Tech Stack

Frontend: Streamlit

NLP & Extraction: Python, spaCy, Regex

Geospatial & Vision: geopy (Nominatim), matplotlib, numpy, ESA Sentinel-2 API, ArcGIS API

🚀 How to Run Locally


Install the dependencies:

pip install -r requirements.txt


Note: Ensure the en_core_web_sm spaCy model is installed. If not, run: python -m spacy download en_core_web_sm

Launch the Streamlit Dashboard:

streamlit run app.py




⚖️ Verification Logic (Audit Trail)

To ensure professional transparency and account for satellite sensor variance, the engine uses the following threshold logic:

$\Delta < -0.5\%$: FRAUD DETECTED (Significant degradation)

$-0.5\% \le \Delta < 0.1\%$: NEUTRAL (Statistical noise / No significant change)

$\Delta \ge 0.1\%$: VERIFIED (Localized greening confirmed)

Built as a portfolio project showcasing the intersection of Natural Language Processing, Geospatial Intelligence, and ESG Assurance.