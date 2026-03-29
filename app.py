import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. إعدادات واجهة المستخدم ---
st.set_page_config(page_title="العيادة الزراعية الذكية", page_icon="🌿", layout="wide")

# --- تحسين المظهر وحل مشكلة لون الخط ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* تنسيق كارت النصائح لحل مشكلة الخط الأبيض */
    .advice-box {
        background-color: rgba(255, 255, 255, 0.9); /* خلفية بيضاء قوية */
        padding: 25px;
        border-radius: 15px;
        border-right: 8px solid #2e7d32;
        color: #1a1a1a !important; /* فرض اللون الأسود للنص */
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .advice-box h3, .advice-box h4, .advice-box b, .advice-box p, .advice-box span {
        color: #1a1a1a !important; /* ضمان أن كل العناوين بالأسود */
    }

    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تحميل الموديل ---
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('Fplant_model.keras')

model = load_my_model()

# --- 3. البيانات ---
class_names = [
    "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

# قاموس ترجمة الأسماء للعربية
arabic_names = {
    "Pepper__bell___Bacterial_spot": "فلفل - تبقع بكتيري",
    "Pepper__bell___healthy": "فلفل - سليم",
    "Potato___Early_blight": "بطاطس - ندوة مبكرة",
    "Potato___Late_blight": "بطاطس - ندوة متأخرة",
    "Potato___healthy": "بطاطس - سليم",
    "Tomato_Bacterial_spot": "طماطم - تبقع بكتيري",
    "Tomato_Early_blight": "طماطم - ندوة مبكرة",
    "Tomato_Late_blight": "طماطم - ندوة متأخرة",
    "Tomato_Leaf_Mold": "طماطم - عفن أوراق",
    "Tomato_Septoria_leaf_spot": "طماطم - تبقع سبتوري",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "طماطم - عنكبوت أحمر",
    "Tomato__Target_Spot": "طماطم - تبقع هدفي",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "طماطم - فيروس تجعد الأوراق",
    "Tomato__Tomato_mosaic_virus": "طماطم - فيروس الموزاييك",
    "Tomato_healthy": "طماطم - سليم"
}

# --- 4. دالة النصيحة الفنية ---
def ai_advice(disease, temp, soil, water, confidence):
    disease_ar = arabic_names.get(disease, disease)
    
    # بناء نص التقرير
    html_report = f"""
    <div class="advice-box">
        <h3 style="margin-top:0;">👨‍🌾 التقرير الفني للاستشاري الزراعي</h3>
        <p><b>الحالة المرصودة:</b> {disease_ar}</p>
        <p><b>دقة التشخيص:</b> {confidence*100:.1f}%</p>
        <hr style="border:0; border-top:1px solid #ccc;">
        
        <h4>🔍 أولاً: التحليل والإجراءات:</h4>
    """
    
    if "healthy" in disease:
        html_report += "<p>✅ النبات في حالة ممتازة. استمر في نظام التسميد الحالي مع مراقبة دورية.</p>"
    elif "Late_blight" in disease:
        html_report += "<p>🚨 <b>تحذير:</b> ندوة متأخرة. يجب الرش فوراً بمبيد يحتوي على (ميتالاكسيل). قلل الرطوبة فوراً.</p>"
    elif "Spider_mites" in disease:
        html_report += "<p>🕷️ <b>عنكبوت أحمر:</b> رش مبيد أكاروسي (أبامكتين) مع غسل الأوراق بالماء صباحاً.</p>"
    else:
        html_report += "<p>🍄 إصابة فطرية/بكتيرية. نوصي برش وقائي بمركبات النحاس وتحسين التهوية.</p>"

    html_report += "<h4>🌍 ثانياً: البيئة والتربة:</h4>"
    
    if soil == "طينية" and water == "كثير":
        html_report += "<p>⚠️ <b>خطر:</b> التربة الطينية تحتفظ بالماء؛ توقف عن الري لتجنب أعفان الجذور.</p>"
    
    if temp > 38:
        html_report += f"<p>🌡️ <b>إجهاد حراري ({temp}°C):</b> رش سليكات بوتاسيوم لزيادة تحمل النبات.</p>"

    html_report += f"<br><b>💡 ملخص:</b> {'التشخيص دقيق، ابدأ التنفيذ.' if confidence > 0.8 else 'يفضل التأكد بالعين المجردة.'}"
    html_report += "</div>"
    
    return html_report

# --- 5. واجهة المستخدم ---
st.title("🌿 العيادة الزراعية الذكية")
st.markdown("استشارة فورية مدعومة بالذكاء الاصطناعي")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📷 بيانات العينة")
    image_file = st.file_uploader("ارفع صورة ورقة النبات", type=["jpg", "png", "jpeg"])
    temp_in = st.slider("🌡️ درجة الحرارة", 0, 50, 25)
    soil_in = st.selectbox("🌱 نوع التربة", ["طينية", "رملية", "طميية"])
    water_in = st.selectbox("💧 حالة الري", ["قليل", "متوسط", "كثير"])
    
with col2:
    st.subheader("🔍 تقرير الفحص")
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="العينة المرصودة", use_container_width=True)
        
        if st.button("🚀 تحليل الحالة الآن"):
            with st.spinner('جاري التحليل...'):
                img = image.convert("RGB").resize((224, 224))
                img_array = np.array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                pred = model.predict(img_array, verbose=0)
                idx = np.argmax(pred)
                conf = float(np.max(pred))
                disease_name = class_names[idx]
                
                # عرض النتائج السريعة
                c1, c2 = st.columns(2)
                c1.metric("المرض", arabic_names.get(disease_name, disease_name))
                c2.metric("الثقة", f"{conf*100:.1f}%")
                
                # عرض التقرير الفني باستخدام HTML المحمي بـ CSS
                report_html = ai_advice(disease_name, temp_in, soil_in, water_in, conf)
                st.markdown(report_html, unsafe_allow_html=True)
    else:
        st.info("قم برفع صورة الورقة لبدء التقرير")
