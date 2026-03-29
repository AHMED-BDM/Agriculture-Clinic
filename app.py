import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. UI Configuration ---
st.set_page_config(page_title="Smart Ag-Clinic", page_icon="🌿", layout="wide")

# --- Custom CSS for Professional Look and High Contrast ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }

    /* Fixed Advice Card for High Readability */
    .expert-card {
        background-color: #ffffff; /* Solid White Background */
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #2e7d32;
        color: #1a1a1a !important; /* Force Dark Text */
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .expert-card h3, .expert-card h4, .expert-card b, .expert-card p, .expert-card li {
        color: #1a1a1a !important;
    }

    .stButton>button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Model Loading (Cached) ---
@st.cache_resource
def load_my_model():
    # Ensure Fplant_model.keras is in the same directory on GitHub
    return tf.keras.models.load_model('Fplant_model.keras')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Error loading model: {e}")

# --- 3. Class Names ---
class_names = [
    "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

# --- 4. Expert AI Advice Logic ---
def generate_expert_report(disease, temp, soil, water, confidence):
    disease_display = disease.replace("_", " ")
    
    report = f"""
    <div class="expert-card">
        <h3 style="margin-top:0;">👨‍🌾 Agricultural Consultant Technical Report</h3>
        <p><b>Detected Condition:</b> {disease_display}</p>
        <p><b>Analysis Confidence:</b> {confidence*100:.1f}%</p>
        <hr>
        
        <h4>🔍 Part I: Pathological Analysis & Treatment</h4>
    """
    
    if "healthy" in disease:
        report += """
        <p>✅ <b>Status:</b> The plant is in optimal physiological condition. No signs of fungal or viral infection detected.</p>
        <ul>
            <li><b>Nutrition:</b> Maintain balanced NPK fertigation.</li>
            <li><b>Immunity:</b> Apply seaweed extract every 15 days to enhance resistance to climatic stress.</li>
        </ul>
        """
    elif "Late_blight" in disease:
        report += """
        <p>🚨 <b>Critical Warning:</b> Late Blight (Phytophthora infestans) is a highly destructive pathogen.</p>
        <ul>
            <li><b>Chemical Control:</b> Immediate application of systemic fungicides containing Metalaxyl or Mancozeb.</li>
            <li><b>Cultural Practice:</b> Remove and burn infected foliage immediately. Reduce humidity by skipping irrigation cycles.</li>
        </ul>
        """
    elif "Early_blight" in disease:
        report += """
        <p>🍂 <b>Analysis:</b> Early Blight usually indicates nitrogen deficiency or fluctuating moisture.</p>
        <ul>
            <li><b>Treatment:</b> Use Chlorothalonil or Azoxystrobin based fungicides.</li>
            <li><b>Pro-tip:</b> Prune lower leaves to prevent soil-borne spores from splashing onto the plant.</li>
        </ul>
        """
    elif "Spider_mites" in disease:
        report += """
        <p>🕷️ <b>Pest Alert:</b> Red Spider Mites thrive in hot, dry conditions.</p>
        <ul>
            <li><b>Action:</b> Spray specialized acaricides like Abamectin. Focus on the underside of the leaves.</li>
            <li><b>Environment:</b> Increase ambient humidity if possible to disrupt their breeding cycle.</li>
        </ul>
        """
    elif "Virus" in disease or "virus" in disease:
        report += """
        <p>🚫 <b>Viral Infection:</b> No chemical cure exists for the plant itself.</p>
        <ul>
            <li><b>Eradication:</b> Uproot the infected plant immediately to prevent spread.</li>
            <li><b>Vector Control:</b> Control Whiteflies and Aphids using systemic insecticides (Imidacloprid).</li>
        </ul>
        """
    else:
        report += "<p>🍄 <b>Fungal Spotting:</b> Apply copper-based fungicides and improve air circulation.</p>"

    report += "<h4>🌍 Part II: Environmental & Soil Management</h4>"
    
    # Environmental Intelligence
    if soil == "Clay" and water == "High":
        report += "<p>⚠️ <b>Warning:</b> Heavy soil with high water saturation leads to <b>Root Rot</b>. Stop irrigation immediately.</p>"
    elif soil == "Sandy" and water == "Low":
        report += "<p>💧 <b>Alert:</b> Sandy soil leaches nutrients quickly. Use frequent, short irrigation pulses.</p>"
    
    if temp > 35:
        report += f"<p>🌡️ <b>Heat Stress ({temp}°C):</b> High temperatures inhibit photosynthesis. Apply Potassium Silicate to strengthen cell walls.</p>"
    
    report += f"<br><b>💡 Consultant Summary:</b> {'Diagnosis is highly reliable, proceed with action plan.' if confidence > 0.85 else 'Visual verification recommended due to moderate confidence.'}"
    report += "</div>"
    
    return report

# --- 5. Main App Layout ---
st.title("🌿 Smart Agricultural Clinic")
st.markdown("Professional AI-powered diagnosis for Tomato, Potato, and Pepper crops.")
st.markdown("---")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📷 Sample Input")
    image_file = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    temp_val = st.slider("🌡️ Ambient Temperature (°C)", 0, 50, 25)
    soil_type = st.selectbox("🌱 Soil Type", ["Clay", "Sandy", "Loamy"])
    water_status = st.selectbox("💧 Irrigation Status", ["Low", "Medium", "High"])
    
with col2:
    st.subheader("🔍 Diagnostic Results")
    
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Sample", width=350)
        
        if st.button("🚀 RUN ANALYSIS"):
            with st.spinner('Analyzing plant pathology...'):
                # Image Preprocessing
                img = image.convert("RGB").resize((224, 224))
                img_array = np.array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                # Model Prediction
                predictions = model.predict(img_array, verbose=0)
                idx = np.argmax(predictions)
                conf = float(np.max(predictions))
                disease = class_names[idx]
                
                # Display Metrics
                m1, m2 = st.columns(2)
                m1.metric("Condition", disease.split("___")[-1].replace("_", " "))
                m2.metric("Confidence", f"{conf*100:.1f}%")
                
                # Generate and Render High-Contrast Report
                expert_html = generate_expert_report(disease, temp_val, soil_type, water_status, conf)
                st.markdown(expert_html, unsafe_allow_html=True)
    else:
        st.info("Please upload a leaf photo to receive a consultation.")

st.markdown("---")
st.caption("AI Consultant v2.0 | Developed for Precision Agriculture")
