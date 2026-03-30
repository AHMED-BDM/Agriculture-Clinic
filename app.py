import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Pro Ag-Clinic AI", page_icon="🌿", layout="wide")

# --- 2. تهيئة الذاكرة (Session State) ---
# بنعرف المتغيرات دي في الأول عشان البرنامج يفتكرها طول ما المتصفح مفتوح
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None  # هنخزن هنا (المرض، النسبة)
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# --- 3. شريط اللغة الجانبي ---
with st.sidebar:
    st.title("🌐 Language / اللغة")
    lang = st.radio("Choose Language:", ["English", "العربية"])

is_ar = lang == "العربية"

# قاموس الواجهة
ui = {
    "title": "🌿 العيادة الزراعية الذكية" if is_ar else "🌿 Pro Ag-Clinic AI",
    "input_header": "📋 بيانات الحقل" if is_ar else "📋 Field Data",
    "upload_label": "ارفع صورة الورقة" if is_ar else "Upload Leaf Image",
    "temp": "الحرارة" if is_ar else "Temperature",
    "btn_analyze": "تحليل العينة" if is_ar else "ANALYZE SPECIMEN",
    "report_header": "🔍 التقرير الفني" if is_ar else "🔍 Technical Report",
    "footer": "© 2026 هندسة النظم الزراعية" if is_ar else "© 2026 Smart Agri-Systems"
}

# --- 4. الدعم البصري (CSS) ---
direction = "rtl" if is_ar else "ltr"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] {{
        direction: {direction};
        text-align: {"right" if is_ar else "left"};
        font-family: 'Tajawal', sans-serif;
    }}
    .report-card {{
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 10px solid #1b5e20;
        border-left: 10px solid #1b5e20;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #111;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. تحميل الموديل وكاش البيانات ---
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('Fplant_model.keras')

model = load_model()

class_names = [
    "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

arabic_names = {
    "Pepper__bell___Bacterial_spot": "فلفل حلو - تبقع بكتيري",
    "Pepper__bell___healthy": "فلفل حلو - سليم",
    "Potato___Early_blight": "بطاطس - ندوة مبكرة",
    "Potato___Late_blight": "بطاطس - ندوة متأخرة",
    "Potato___healthy": "بطاطس - سليم",
    "Tomato_Bacterial_spot": "طماطم - تبقع بكتيري",
    "Tomato_Early_blight": "طماطم - ندوة مبكرة",
    "Tomato_Late_blight": "طماطم - ندوة متأخرة",
    "Tomato_Leaf_Mold": "طماطم - عفن الأوراق",
    "Tomato_Septoria_leaf_spot": "طماطم - تبقع سبتوري",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "طماطم - العنكبوت الأحمر",
    "Tomato__Target_Spot": "طماطم - التبقع الهدفي",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "طماطم - فيروس تجعد الأوراق",
    "Tomato__Tomato_mosaic_virus": "طماطم - فيروس الموزاييك",
    "Tomato_healthy": "طماطم - سليم"
}

# --- 6. دالة إنشاء التقرير ---
def render_report(label, conf, t, s, w):
    name = arabic_names.get(label, label) if is_ar else label.replace("_", " ")
    
    if is_ar:
        return f"""<div class="report-card">
        <h2 style="color:#1b5e20; text-align:center;">تقرير التشخيص الزراعي</h2>
        <p><b>المرض المكتشف:</b> {name}</p>
        <p><b>نسبة الثقة:</b> {conf*100:.1f}%</p>
        <hr>
        <h4>💡 التوصيات الفنية:</h4>
        <ul>
            <li>استخدم مبيدات فطرية تحتوي على النحاس إذا كانت الإصابة بكتيرية.</li>
            <li>تحكم في الرطوبة المحيطة (مستوى الري الحالي: {w}).</li>
            <li>درجة الحرارة ({t}°م) {"تزيد من نشاط الفطر" if t > 25 else "مناسبة حالياً"}.</li>
        </ul>
        </div>"""
    else:
        return f"""<div class="report-card">
        <h2 style="color:#1b5e20; text-align:center;">Agronomic Diagnosis</h2>
        <p><b>Identified:</b> {name}</p>
        <p><b>Confidence:</b> {conf*100:.1f}%</p>
        <hr>
        <h4>💡 Management Plan:</h4>
        <ul>
            <li>Apply targeted fungicides based on {label} protocol.</li>
            <li>Monitor irrigation (Current: {w}).</li>
            <li>Temp {t}°C is {"conducive for pathogens" if t > 25 else "stable"}.</li>
        </ul>
        </div>"""

# --- 7. تصميم الواجهة ---
st.title(ui["title"])
st.markdown("---")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader(ui["input_header"])
    uploaded_file = st.file_uploader(ui["upload_label"], type=["jpg", "png", "jpeg"])
    
    # إذا تغيرت الصورة، امسح النتائج القديمة
    if uploaded_file:
        if st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.analysis_results = None
            st.session_state.last_uploaded_file = uploaded_file.name

    t_val = st.slider(ui["temp"], 0, 50, 25)
    s_val = st.selectbox("Soil" if not is_ar else "التربة", ["Clay", "Sandy"])
    w_val = st.selectbox("Water" if not is_ar else "الري", ["Low", "High"])

    if uploaded_file and st.button(ui["btn_analyze"]):
        with st.spinner("Analyzing..."):
            img = Image.open(uploaded_file).convert("RGB").resize((224, 224))
            img_arr = np.array(img) / 255.0
            pred = model.predict(np.expand_dims(img_arr, 0), verbose=0)
            
            # تخزين النتيجة في الذاكرة (هنا السر!)
            st.session_state.analysis_results = {
                "label": class_names[np.argmax(pred)],
                "conf": float(np.max(pred))
            }

with col2:
    st.subheader(ui["report_header"])
    if uploaded_file:
        st.image(uploaded_file, width=300)
        
        # عرض النتيجة من الذاكرة (حتى لو الصفحة عملت Refresh)
        if st.session_state.analysis_results:
            res = st.session_state.analysis_results
            report_html = render_report(res["label"], res["conf"], t_val, s_val, w_val)
            st.markdown(report_html, unsafe_allow_html=True)
        else:
            st.info("Press Analyze to generate report" if not is_ar else "اضغط على زر التحليل لإظهار التقرير")
    else:
        st.warning("Please upload an image first" if not is_ar else "يرجى رفع صورة أولاً")

st.markdown("---")
st.caption(ui["footer"])
