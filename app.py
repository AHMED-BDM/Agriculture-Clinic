import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. إعدادات واجهة المستخدم (Streamlit) ---
st.set_page_config(page_title="العيادة الزراعية الذكية", page_icon="🌿", layout="wide")

# --- 2. تحميل الموديل بطريقة ذكية (Caching) ---
@st.cache_resource
def load_my_model():
    # تأكد أن الملف موجود في نفس الفولدر على جيت هاب
    return tf.keras.models.load_model('Fplant_model.keras')

model = load_my_model()

# --- 3. فئات الأمراض (نفس الترتيب بتاعك) ---
class_names = [
    "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

# --- 4. قاموس العلاج الفوري (نفس بياناتك) ---
treatment = {
    "Pepper__bell___Bacterial_spot": "رش مبيد نحاسي",
    "Pepper__bell___healthy": "النبات سليم 🌿",
    "Potato___Early_blight": "رش مبيد فطري + إزالة الأوراق المصابة",
    "Potato___Late_blight": "تقليل الرطوبة + مبيد فطري قوي",
    "Potato___healthy": "النبات سليم 🌿",
    "Tomato_Bacterial_spot": "رش مبيد نحاسي",
    "Tomato_Early_blight": "رش مبيد فطري + إزالة الأوراق المصابة",
    "Tomato_Late_blight": "تقليل الرطوبة + مبيد نحاسي",
    "Tomato_Leaf_Mold": "تهوية جيدة + تقليل الري",
    "Tomato_Septoria_leaf_spot": "إزالة الأوراق المصابة + مبيد فطري",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "رش ماء + مبيد حشري",
    "Tomato__Target_Spot": "مبيد فطري مناسب",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "مكافحة الحشرات + إزالة النبات المصاب",
    "Tomato__Tomato_mosaic_virus": "إزالة النبات المصاب وتعقيم الأدوات",
    "Tomato_healthy": "النبات سليم 🌿"
}

# --- 5. دالة نصيحة المهندس الزراعي (نفس منطقك) ---
def ai_advice(disease, temp, soil, water, confidence):
    report = f"### 👨‍🌾 التقرير الفني للاستشاري الزراعي\n"
    report += f"**الحالة المرصودة:** {disease.replace('_', ' ')}  \n"
    report += f"**دقة القراءة الآلية:** {confidence*100:.1f}%  \n"
    report += "---\n"
    report += "🔍 **أولاً: التحليل المرضي والإجراءات العلاجية:**  \n\n"

    if "healthy" in disease:
        report += "✅ **الحالة العامة:** النبات في حالة نمو مثالية. لا توجد إصابات فطرية أو حشرية ظاهرة.  \n"
        report += "📍 **توصية المهندس:** استمر على برنامج التسميد المتوازن. نوصي بإضافة (مركبات الطحالب البحرية) كل 15 يوم لرفع المناعة.  \n"
    elif "Late_blight" in disease:
        report += "🚨 **تحذير (اللفحة المتأخرة):** هذا المرض 'مدمر' للمحصول وينتشر بسرعة البرق.  \n"
        report += "📍 **خطة التحرك:** 1. حرق النباتات المصابة بشدة. 2. الرش بمبيدات (ميتالاكسيل).  \n"
        if water == "كثير": report += "⚠️ **خطر:** امنع الري فوراً لمدة 48 ساعة.  \n"
    elif "Early_blight" in disease:
        report += "🍂 **تحليل (اللفحة المبكرة):** ناتجة عن تذبذب الري.  \n"
        report += "📍 **خطة التحرك:** 1. إزالة الأوراق السفلية. 2. رش (مانكوزيب).  \n"
    elif "Bacterial_spot" in disease:
        report += "🦠 **تحليل (التبقع البكتيري):** ري بالتنقيط فقط + رش (هيدروكسيد النحاس).  \n"
    elif "Spider_mites" in disease:
        report += "🕷️ **تحليل (العنكبوت الأحمر):** رش مبيد أكاروسي متخصص (أبامكتين).  \n"
    elif "Virus" in disease or "virus" in disease:
        report += "🚫 **تحليل (الفيروس):** قلع النبات المصاب فوراً ومكافحة الحشرات الناقلة.  \n"
    else:
        report += "🍄 **تحليل المرض:** إصابة فطرية تتطلب تهوية جيدة ورش وقائي نحاسي.  \n"

    report += "\n🌍 **ثانياً: إدارة البيئة والتربة:**  \n"
    if soil == "طينية" and water == "كثير":
        report += "- ⚠️ **خطر:** ري مكثف في تربة ثقيلة يسبب 'أعفان جذور'. توقف عن الري.  \n"
    elif soil == "رملية" and water == "قليل":
        report += "- 💧 **تنبيه:** التربة الرملية لا تمسك الماء، يفضل الري على فترات قصيرة.  \n"
    if temp > 38:
        report += f"- 🌡️ **إجهاد حراري:** رش (سليكات بوتاسيوم) لزيادة تحمل الحرارة.  \n"

    report += "\n---\n**💡 ملخص المهندس:** "
    report += "التشخيص دقيق جداً." if confidence > 0.85 else "يفضل الفحص الميداني للتأكد."
    return report

# --- 6. تصميم واجهة الموقع (Layout) ---
st.title("🌿 العيادة الزراعية الذكية")
st.markdown("استشارة فورية مدعومة بالذكاء الاصطناعي لتشخيص أمراض النبات")

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
        st.image(image, caption="الصورة المرفوعة", use_container_width=True)
        
        if st.button("🚀 تحليل الحالة الآن"):
            with st.spinner('جاري التحليل...'):
                # المعالجة
                img = image.convert("RGB").resize((224, 224))
                img_array = np.array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                # التوقع
                pred = model.predict(img_array, verbose=0)
                idx = np.argmax(pred)
                conf = float(np.max(pred))
                disease_name = class_names[idx]
                
                # عرض النتائج في بطاقات صغيرة
                c1, c2 = st.columns(2)
                c1.metric("المرض المكتشف", disease_name.replace("_", " "))
                c2.metric("دقة التشخيص", f"{conf*100:.1f}%")
                
                st.info(f"💊 **العلاج الفوري:** {treatment.get(disease_name, 'راجع المختص')}")
                
                # عرض تقرير الخبير (Markdown)
                advice_text = ai_advice(disease_name, temp_in, soil_in, water_in, conf)
                st.markdown(advice_text)
    else:
        st.info("يرجى رفع صورة للبدء.")