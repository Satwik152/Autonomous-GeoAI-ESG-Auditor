import streamlit as st
try:
    from geopy.geocoders import Nominatim
    from nlp_extractor import AutonomousESGAgent
    import geo_vision as gv
except ImportError as e:
    st.error(f"🚨 Missing backend module or library: {e}")
    st.stop()

st.set_page_config(
    page_title="GeoAI ESG Auditor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting Custom CSS for an Enterprise SaaS look
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
        html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; }
        .stButton>button { width: 100%; background: linear-gradient(135deg, #00b09b, #96c93d); color: white; font-weight: bold; border: none; border-radius: 8px; padding: 10px; transition: all 0.3s; }
        .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,176,155,0.4); }
        .fraud-alert { background-color: #450a0a; border-left: 6px solid #ef4444; padding: 15px; border-radius: 4px; color: #fca5a5; }
        .verified-alert { background-color: #064e3b; border-left: 6px solid #10b981; padding: 15px; border-radius: 4px; color: #6ee7b7; }
        .disclaimer { font-size: 0.8em; color: #94a3b8; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 Autonomous GeoAI ESG Auditor (Spatio-Temporal)")
st.markdown("An AI-driven agent that autonomously extracts corporate environmental claims and verifies them via **Before-and-After (Temporal) Satellite Delta Analysis**.")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📄 1. Input ESG Report")
    default_text = "GlobalCorp 2025 Impact Report:\n\nTo offset our remaining carbon emissions, we have invested heavily in global reforestation. Specifically, in March 2020, we successfully planted over 50,000 native trees in the Mato Grosso region of Brazil . We expect this to capture 10,000 tons of CO2."
    document_text = st.text_area("Corporate Document Text", value=default_text, height=300)
    run_audit = st.button("🚀 Launch Autonomous Audit Agent")

with col2:
    if run_audit:
        agent = AutonomousESGAgent()
        geolocator = Nominatim(user_agent="ey_streamlit_portfolio")
        
        with st.status("🤖 Agent actively analyzing claims...", expanded=True) as status:
            claims = agent.extract_claims(document_text)
            if not claims:
                status.update(label="No claims found.", state="error")
                st.stop()
                
            claim = claims[0]
            st.write(f"📍 Target identified: **{claim['location_name']}**")
            
            try:
                location = geolocator.geocode(claim['location_name'], timeout=5)
                lat, lon = location.latitude, location.longitude
                st.write(f"🔒 Coordinates locked: `{lat:.4f}, {lon:.4f}`")
            except:
                st.write("⚠️ Geocoding failed, using proxy coordinates.")
                lat, lon = 28.2144, 76.9409 # Approx coordinates for Tauru fallback
                
            baseline_yr = claim['baseline_year']
            target_yr = claim['target_year']
                
            # 100% AUTONOMOUS: Fetching data dynamically based on extracted text years
            st.write(f"⏳ Fetching Historical Baseline Telemetry ({baseline_yr})...")
            hist_img_path = gv.fetch_sentinel2_imagery(lat, lon, baseline_yr)

            st.write(f"🛰️ Fetching Post-Claim Satellite Telemetry ({target_yr})...")
            curr_img_path = gv.fetch_sentinel2_imagery(lat, lon, target_yr)
            
            st.write("👁️ Executing Dual-Temporal ExG Semantic Segmentation...")
            hist_img, hist_mask, hist_pct = gv.run_computer_vision(hist_img_path)
            curr_img, curr_mask, curr_pct = gv.run_computer_vision(curr_img_path)
            
            st.write("⚖️ Agent reasoning about Spatio-Temporal Delta...")
            verdict = agent.verify_evidence(claim['claim_text'], hist_pct, curr_pct)
            status.update(label="Audit Complete!", state="complete")
        
        st.subheader("🛰️ Spatio-Temporal Visual Evidence")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Target Region", claim['location_name'])
        m2.metric(f"Historical Baseline ({baseline_yr})", f"{hist_pct:.2f}%")
        m3.metric(f"Post-Claim Cover ({target_yr})", f"{curr_pct:.2f}%")
        m4.metric("Net Vegetation Delta", f"{curr_pct - hist_pct:+.2f}%", delta=f"{curr_pct - hist_pct:.2f}%")
        
        st.markdown(f"**1. Historical Baseline ({baseline_yr})**")
        h1, h2 = st.columns(2)
        with h1: st.image(hist_img, use_container_width=True)
        with h2: st.image(hist_mask, use_container_width=True)
        
        st.markdown(f"**2. Post-Claim Telemetry ({target_yr})**")
        c1, c2 = st.columns(2)
        with c1: st.image(curr_img, use_container_width=True)
        with c2: st.image(curr_mask, use_container_width=True)
            
        st.subheader("📝 Agent Final Verdict")
        if verdict['status'] == "FRAUD_DETECTED":
            st.markdown(f'<div class="fraud-alert"><strong>🚨 RED FLAG:</strong> {verdict["reasoning"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="verified-alert"><strong>✅ VERIFIED:</strong> {verdict["reasoning"]}</div>', unsafe_allow_html=True)
            
        st.markdown('<p class="disclaimer">Note: This pipeline utilizes authentic, time-stamped European Space Agency (ESA) Sentinel-2 satellite telemetry via EOX and ArcGIS World Imagery to ensure mathematical and ethical data integrity during the spatio-temporal delta verification.</p>', unsafe_allow_html=True)
    else:
        st.info("👈 Paste a corporate report on the left and click 'Launch Autonomous Audit Agent' to begin the pipeline.")
