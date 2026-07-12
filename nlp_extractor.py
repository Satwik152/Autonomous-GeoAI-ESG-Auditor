import time
import spacy
import re
from datetime import datetime

# 🚀 ENTERPRISE UPGRADE: Location Sanitizer (Override Dictionary)
# Maps obscure, small, or commonly mis-geocoded locations to their exact administrative hierarchy.
LOCATION_OVERRIDES = {
    "tauru": "Taoru, Haryana, India",
    "wadi ad-dawasir": "Wadi ad-Dawasir, Riyadh Province, Saudi Arabia"
}

def load_nlp_model():
    """Loads the AI model for text extraction."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        raise Exception("🚨 spaCy model not found. Please run: python -m spacy download en_core_web_sm")

class AutonomousESGAgent:
    """Agent that processes text and evaluates visual evidence."""
    
    def extract_claims(self, document_text):
        time.sleep(1)
        nlp = load_nlp_model()
        doc = nlp(document_text)
        
        # 🚀 ENTERPRISE UPGRADE: Global Pre-check for Overrides
        # We scan the raw text first. If we find a known tricky location, we force the correct geocoding string instantly.
        doc_lower = document_text.lower()
        forced_location = None
        for key, precise_location in LOCATION_OVERRIDES.items():
            if key in doc_lower:
                forced_location = precise_location
                break
        
        # Extract Cities/Regions first
        cities = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC'] and len(ent.text) > 3]
        
        # Fallback to Regex for specific pattern matching ("in [City] of [Country]")
        match = re.search(r'in\s+(?:the\s+)?([A-Z][a-zA-Z\s]+?)(?:\s+of\s+([A-Z][a-zA-Z\s]+?))?(?=\.|\,|$|\sWe)', document_text)
        if match:
            city_region = match.group(1).replace(" region", "").strip()
            country = match.group(2).strip() if match.group(2) else ""
            
            if country:
                cities.append(f"{city_region}, {country}")
            else:
                cities.append(city_region)
            
        # Dynamic Temporal Extraction
        years = re.findall(r'\b(20[1-2][0-9])\b', document_text)
        claim_year = int(years[-1]) if years else datetime.now().year
        baseline_year = str(claim_year - 1)
        target_year = str(claim_year if claim_year <= datetime.now().year else "current")

        if forced_location or cities:
            # Grab the forced location first, otherwise use the NLP one
            loc_name = forced_location if forced_location else cities[-1].strip()
            
            # Find the sentence containing the claim
            claim_text = "Environmental restoration project"
            for sent in doc.sents:
                search_word = loc_name.split(',')[0].strip()
                if search_word.lower() in sent.text.lower():
                    claim_text = sent.text.strip()
                    break
                    
            return [{
                "claim_text": claim_text, 
                "location_name": loc_name,
                "baseline_year": baseline_year,
                "target_year": target_year
            }]
        return []

    def verify_evidence(self, claim_text, historical_cover, current_cover):
        """Evaluates the DELTA (change) in vegetation with a confidence score."""
        time.sleep(1)
        delta = current_cover - historical_cover
        
        # Calculate Confidence: Higher delta = higher confidence in verification
        confidence = min(abs(delta) * 50, 95.0) 
        
        if delta < -0.5:
            return {
                "status": "FRAUD_DETECTED",
                "confidence": f"{confidence:.1f}%",
                "reasoning": f"Temporal analysis shows a significant vegetation decrease of {delta:+.2f}%. Claim of restoration is contradicted by detected land degradation."
            }
        elif delta < 0.1:
            return {
                "status": "NEUTRAL",
                "confidence": f"{confidence:.1f}%",
                "reasoning": f"Temporal analysis shows a minor delta of {delta:+.2f}%. No significant restoration confirmed, but no major degradation detected."
            }
        else:
            return {
                "status": "VERIFIED",
                "confidence": f"{confidence:.1f}%",
                "reasoning": f"Temporal satellite analysis confirms a {delta:+.2f}% net increase in vegetation, successfully detecting and verifying the localized restoration claim."
            }