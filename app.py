import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. Page Configuration ---
st.set_page_config(page_title="Pro Ag-Clinic AI", page_icon="🌿", layout="wide")

# --- 2. Session State Initialization (لحفظ التقرير من المسح) ---
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'last_file' not in st.session_state:
    st.session_state.last_file = None

# --- 3. Language Setup ---
with st.sidebar:
    # إضافة اللوجو في القائمة الجانبية
    try:
        logo = Image.open(r"C:\Users\Admin\Downloads\cd658e2d-2bc7-4014-adbf-ddf32587ae42.png") 
        st.image(logo, use_container_width=True)
    except:
        st.error(r"⚠️ لم يتم العثور على ملف C:\Users\Admin\Downloads\cd658e2d-2bc7-4014-adbf-ddf32587ae42.png")
        
    st.title("🌐 Language / اللغة")
    lang = st.radio("Choose Interface Language:", ["English", "العربية"])

is_ar = lang == "العربية"

# UI Dictionaries
ui = {
    "title": "العيادة الزراعية الذكية الاحترافية" if is_ar else "Professional Agriculture AI Clinic",
    "subtitle": "نظام التحليل المرضي والاستشارة الفنية الدقيقة" if is_ar else "Detailed Pathological Analysis & Expert Consultation System",
    "input_header": "📋 إدخال بيانات الحقل" if is_ar else "📋 Input Field Data",
    "upload_label": "ارفع صورة الورقة المصابة" if is_ar else "Upload Leaf Specimen",
    "env_expander": "مستشعرات البيئة" if is_ar else "Environment Sensors",
    "temp": "درجة الحرارة" if is_ar else "Temperature",
    "btn_analyze": "بدء التحليل العميق" if is_ar else "EXECUTE DEEP ANALYSIS",
    "report_header": "🔍 التقرير الفني للتحليل" if is_ar else "🔍 Technical Analysis Report",
    "wait": "في انتظار رفع صورة العينة..." if is_ar else "Awaiting leaf specimen...",
    "footer": "© 2026 العيادة الزراعية الذكية | مهندس أحمد عبد الحافظ" if is_ar else "© 2026 Smart Agri-Clinic | Eng. Ahmed Abd Al-Hafez"
}

# --- 4. Advanced CSS ---
direction = "rtl" if is_ar else "ltr"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Tajawal', sans-serif;
        direction: {direction};
        text-align: {"right" if is_ar else "left"};
    }}
    .report-container {{
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 12px solid #1b5e20;
        border-left: 12px solid #1b5e20;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
        color: #111;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. Model & Logic (Simplified for brevity) ---
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('Fplant_model.keras')

model = load_model()
class_names = ["Pepper__bell___Bacterial_spot", "Pepper__bell___healthy", "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy", "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight", "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot", "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot", "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus", "Tomato_healthy"]

# --- 6. App Layout ---

# الهيدر الرئيسي: اللوجو بجانب العنوان
head_col1, head_col2 = st.columns([1, 4])
with head_col1:
    try:
        st.image("logo.png", width=150)
    except: pass
with head_col2:
    st.title(ui["title"])
    st.write(ui["subtitle"])

st.markdown("---")

c1, c2 = st.columns([1, 1.4], gap="large")

with c1:
    st.subheader(ui["input_header"])
    uploaded_file = st.file_uploader(ui["upload_label"], type=["jpg","jpeg","png"])
    
    # تصحيح: مسح التقرير فقط إذا تم رفع صورة جديدة
    if uploaded_file and st.session_state.last_file != uploaded_file.name:
        st.session_state.analysis_results = None
        st.session_state.last_file = uploaded_file.name

    with st.expander(ui["env_expander"]):
        t_input = st.slider(ui["temp"], 0, 55, 26)
        s_input = st.selectbox("التربة" if is_ar else "Soil", ["Clay", "Sandy"])
        w_input = st.selectbox("الري" if is_ar else "Water", ["Low", "High"])

    if uploaded_file and st.button(ui["btn_analyze"]):
        with st.spinner("Analyzing..."):
            img = Image.open(uploaded_file).convert("RGB").resize((224, 224))
            img_arr = np.array(img) / 255.0
            preds = model.predict(np.expand_dims(img_arr, 0), verbose=0)
            
            # حفظ النتيجة في الذاكرة
            st.session_state.analysis_results = {
                "label": class_names[np.argmax(preds)],
                "conf": float(np.max(preds))
            }

with c2:
    st.subheader(ui["report_header"])
    if uploaded_file:
        st.image(uploaded_file, width=350, caption="Sample Image")
        
        # عرض التقرير من الذاكرة (هنا يتحقق الثبات عند تغيير اللغة)
        if st.session_state.analysis_results:
            res = st.session_state.analysis_results
            
            # عرض النتيجة بشكل مبسط (يمكنك دمج دالة get_detailed_report هنا)
            label_display = res["label"].replace("_", " ")
            conf_val = res["conf"] * 100
            
            st.markdown(f"""
            <div class="report-container">
                <h3 style="color:#1b5e20;">التشخيص: {label_display}</h3>
                <p><b>نسبة الثقة:</b> {conf_val:.2f}%</p>
                <hr>
                <p><b>توصية المهندس:</b> يرجى اتباع بروتوكول المكافحة المعتمد لدرجة حرارة {t_input} م°.</p>
                <p style="font-size: 0.8em; color: gray;">تم التحليل بواسطة نظام العيادة الذكية</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("اضغط على زر التحليل" if is_ar else "Click Analyze Button")
    else:
        st.info(ui["wait"])

st.markdown("---")
st.caption(ui["footer"])
