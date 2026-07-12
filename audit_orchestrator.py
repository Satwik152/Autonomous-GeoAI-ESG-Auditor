import time
import sys
import os

try:
    import PyPDF2
    from geopy.geocoders import Nominatim
except ImportError:
    print("🚨 Missing libraries. Please run: pip install PyPDF2 geopy")
    sys.exit(1)

# Import our newly decoupled modular backend
try:
    from nlp_extractor import AutonomousESGAgent
    import geo_vision as gv
except ImportError as e:
    print(f"🚨 Import Error: {e}")
    sys.exit(1)

geolocator = Nominatim(user_agent="ey_terminal_agent_portfolio")

def extract_text_from_pdf(pdf_path):
    """Reads a real corporate PDF report and extracts raw text."""
    if not os.path.exists(pdf_path):
        return None
    document_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                document_text += text + "\n"
    return document_text

def run_autonomous_pipeline():
    print("\n" + "="*70)
    print("🤖 AUTONOMOUS ESG VERIFICATION AGENT INITIATED (TERMINAL MODE)")
    print("="*70)

    agent = AutonomousESGAgent()

    # 1. INGESTION
    print("\n[PHASE 1] AUTONOMOUS DOCUMENT INGESTION")
    pdf_filename = "real_report.pdf"
    
    document_text = extract_text_from_pdf(pdf_filename)
    if not document_text:
        print(f"⚠️ '{pdf_filename}' not found. Loading proxy corporate data...")
        document_text = "We planted over 50,000 native trees in Tauru of India to offset emissions."
    else:
        print(f"📄 Successfully ingested {pdf_filename}.")

    # 2. EXTRACTION
    print("\n[PHASE 2] AGENTIC CLAIM EXTRACTION")
    claims = agent.extract_claims(document_text)
    
    if not claims:
        print("✅ Agent found no actionable claims. Shutting down.")
        return

    # 3. VERIFICATION (Spatio-Temporal Delta Analysis)
    print("\n[PHASE 3] AUTONOMOUS SATELLITE VERIFICATION & REASONING")
    for i, item in enumerate(claims):
        print(f"\n--- Investigating Target {i+1}: {item['location_name']} ---")
        
        print(f"📍 Geocoding location: {item['location_name']}...")
        try:
            location = geolocator.geocode(item['location_name'], timeout=5)
            lat, lon = location.latitude, location.longitude
            print(f"   -> Coordinates locked: Lat {lat:.4f}, Lon {lon:.4f}")
        except:
            print("⚠️ Geocoding failed. Using proxy coordinates.")
            lat, lon = 28.2144, 76.9409 # Approx coordinates for Tauru
            
        print("🛰️ Triggering ArcGIS Satellite Tool (Current Telemetry)...")
        curr_img_path = gv.fetch_satellite_image(lat, lon)
        
        print("⏳ Fetching Historical Baseline Telemetry (Simulated)...")
        hist_img_path = gv.simulate_historical_imagery(curr_img_path)
        
        print("👁️ Agent executing Dual-Temporal Computer Vision analysis...")
        # We only need the percentage outputs for the terminal reasoning
        _, _, hist_pct = gv.run_computer_vision(hist_img_path)
        _, _, curr_pct = gv.run_computer_vision(curr_img_path)
        
        print(f"📊 Historical Cover: {hist_pct:.2f}% | Current Cover: {curr_pct:.2f}%")
        print(f"📉 Net Vegetation Delta: {curr_pct - hist_pct:+.2f}%")
        
        # Agent analyzes the Delta
        verdict = agent.verify_evidence(item['claim_text'], hist_pct, curr_pct)
        
        print("\n📝 === AGENT FINAL VERDICT ===")
        print(f"Status: {verdict['status']}")
        print(f"Reasoning: {verdict['reasoning']}")
        print("==============================")

    print("\n" + "="*70)
    print("✅ AGENT WORKFLOW COMPLETE. ZERO HUMAN INTERACTION REQUIRED.")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_autonomous_pipeline()