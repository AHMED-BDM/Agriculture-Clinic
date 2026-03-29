import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. Page Config ---
st.set_page_config(page_title="Smart Ag-Clinic", page_icon="🌿", layout="wide")

# --- 2. CSS Styles (Fixing Contrast & Text Visibility) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }

    /* This class ensures the advice is always readable with black text */
    .expert-card {
        background-color: #ffffff !important; 
        padding: 20px;
        border-radius: 10px;
        border-left: 10px solid #2e7d32;
        color: #000000 !important;
        margin-top: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    .expert-card h3, .expert-card h4, .expert-card b, .expert-card p, .expert-card li {
        color: #000000 !important;
        text-align: left;
    }

    .stButton>button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Load Model ---
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('Fplant_model.keras')

model = load_my_model()

# --- 4. Categories ---
class_names = [
    "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

# --- 5. Advice Logic (English Content) ---
def generate_report(disease, temp, soil, water, conf):
    disease_name = disease.replace("_", " ")
    
    # Building the HTML block
    report_html = f"""
    <div class="expert-card">
        <h3 style="color: #2e7d32 !important;">👨‍🌾 Agricultural Expert Report</h3>
        <p><b>Diagnosis:</b> {disease_name}</p>
        <p><b>Confidence:</b> {conf*100:.1f}%</p>
        <hr>
        <h4>🔍 Analysis & Treatment:</h4>
    """
    
    if "healthy" in disease:
        report_html += "<p>✅ Plant is healthy. Maintain current fertilization and irrigation schedule.</p>"
    elif "Late_blight" in disease:
        report_html += "<p>🚨 <b>Critical:</b> Late Blight detected. Immediate application of fungicides (e.g., Metalaxyl) is required.</p>"
    elif "Spider_mites" in disease:
        report_html += "<p>🕷️ <b>Pest:</b> Spider Mites detected. Use Acaricides and increase humidity.</p>"
    else:
        report_html += "<p>🍄 Fungal/Bacterial infection. Use copper-based sprays and improve air circulation.</p>"

    report_html += f"""
        <h4>🌍 Environment & Soil:</h4>
        <p>Current Temperature: {temp}°C | Soil: {soil} | Water: {water}</p>
    """
    
    if soil == "Clay" and water == "High":
        report_html += "<p>⚠️ <b>Risk:</b> High water in clay soil may cause Root Rot.</p>"

    report_html += "</div>"
    return report_html

# --- 6. Layout ---
st.title("🌿 Smart Agricultural Clinic")
st.markdown("AI-driven diagnosis for Tomato, Potato, and Pepper crops.")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📷 Input Data")
    img_file = st.file_uploader("Upload leaf image", type=["jpg", "jpeg", "png"])
    temp_val = st.slider("Temperature (°C)", 0, 50, 25)
    soil_type = st.selectbox("Soil Type", ["Clay", "Sandy", "Loamy"])
    water_val = st.selectbox("Water Status", ["Low", "Medium", "High"])

with col2:
    st.subheader("🔍 Analysis Results")
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=350)
        
        if st.button("RUN AI ANALYSIS"):
            with st.spinner('Processing...'):
                # Prep image
                test_img = img.convert("RGB").resize((224, 224))
                img_arr = np.array(test_img) / 255.0
                img_arr = np.expand_dims(img_arr, axis=0)
                
                # Predict
                preds = model.predict(img_arr, verbose=0)
                idx = np.argmax(preds)
                confidence = float(np.max(preds))
                disease = class_names[idx]
                
                # Show report - CRITICAL FIX HERE
                report_content = generate_report(disease, temp_val, soil_type, water_val, confidence)
                st.markdown(report_content, unsafe_allow_html=True)
    else:
        st.info("Upload an image to start.")
