import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. إعدادات واجهة المستخدم (Streamlit) ---
st.set_page_config(page_title="العيادة الزراعية الذكية", page_icon="🌿", layout="wide")

# --- إضافة CSS احترافي لدعم العربية (RTL) وتحسين المظهر ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stAlert {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        border-color: #1b5e20;
    }
    .advice-card {
        background-color: #f1f8e9;
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #7cb342;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تحميل الموديل بطريقة ذكية (Caching) ---
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('Fplant_model.keras')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"⚠️ جاري تحميل النظام أو يوجد خطأ في ملف الموديل: {e}")

# --- 3. فئات الأمراض وترجمتها للعربية ---
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
    "Pepper__bell___Bacterial_spot": "فلفل - تبقع بكتيري",
    "Pepper__bell___healthy": "فلفل - سليم ومعافى",
    "Potato___Early_blight": "بطاطس - الندوة المبكرة (اللفحة المبكرة)",
    "Potato___Late_blight": "بطاطس - الندوة المتأخرة (اللفحة المتأخرة)",
    "Potato___healthy": "بطاطس - سليم ومعافى",
    "Tomato_Bacterial_spot": "طماطم - تبقع بكتيري",
    "Tomato_Early_blight": "طماطم - الندوة المبكرة",
    "Tomato_Late_blight": "طماطم - الندوة المتأخرة",
    "Tomato_Leaf_Mold": "طماطم - عفن الأوراق",
    "Tomato_Septoria_leaf_spot": "طماطم - تبقع الأوراق السبتوري",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "طماطم - إصابة بالعنكبوت الأحمر",
    "Tomato__Target_Spot": "طماطم - التبقع الهدفي",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "طماطم - فيروس تجعد واصفرار الأوراق",
    "Tomato__Tomato_mosaic_virus": "طماطم - فيروس الموزاييك",
    "Tomato_healthy": "طماطم - سليم ومعافى"
}

# --- 4. دالة الاستشاري الزراعي (موسعة واحترافية) ---
def ai_advice(disease, temp, soil, water, confidence):
    report = ""
    
    # 1. التشخيص المبدئي
    if "healthy" in disease:
        report += "### ✅ تقرير الحالة: ممتاز\n"
        report += "النبات في حالة فسيولوجية ونمو مثالية، ولا توجد أي علامات لإصابات فطرية، حشرية، أو فيروسية ظاهرة على العينة.\n\n"
        report += "**💡 نصائح المهندس للحفاظ على الإنتاجية:**\n"
        report += "- **التسميد:** استمر على البرنامج المتوازن (NPK). يفضل رش أحماض أمينية مع طحالب بحرية مرة كل 15 يوماً لرفع مناعة النبات ضد التغيرات المناخية.\n"
        report += "- **المتابعة:** استمر في الفحص الدوري، خاصة للأسطح السفلية للأوراق حيث تبدأ معظم الإصابات الحشرية.\n"
    
    elif "Late_blight" in disease:
        report += "### 🚨 تقرير الحالة: خطير عاجل (الندوة المتأخرة)\n"
        report += "هذا الفطر (Phytophthora infestans) يعتبر من أخطر الأمراض المدمرة والمسببة لخسائر فادحة في وقت قصير جداً.\n\n"
        report += "**🛠️ خطة المكافحة الشاملة:**\n"
        report += "1. **مكافحة زراعية:** التخلص الفوري من الأوراق والنباتات المصابة بشدة بحرقها خارج الحقل. لا تتركها على الأرض أبداً.\n"
        report += "2. **مكافحة كيميائية:** الرش الفوري والمكثف بمبيدات جهازية ووقائية. نوصي بالمواد الفعالة: (ميتالاكسيل + مانكوزيب) أو (سيموكسانيل) أو (أزوكسي ستروبين). يتم الرش وتكراره بعد 5 أيام باختلاف المادة الفعالة.\n"
    
    elif "Early_blight" in disease:
        report += "### 🍂 تقرير الحالة: إصابة فطرية (الندوة المبكرة)\n"
        report += "مرض فطري (Alternaria solani) يظهر غالباً بسبب تذبذب درجات الحرارة والرطوبة العالية، ونقص التسميد البوتاسي يجعله أسرع انتشاراً.\n\n"
        report += "**🛠️ خطة المكافحة الشاملة:**\n"
        report += "1. **مكافحة زراعية:** إزالة الأوراق السفلية المصابة والقريبة من سطح التربة لتخفيف الرطوبة حول ساق النبات وتحسين التهوية.\n"
        report += "2. **مكافحة كيميائية:** استخدام مبيدات فطرية تحتوي على (ديفينوكونازول)، (أزوكسي ستروبين)، أو رش وقائي بـ (المانكوزيب).\n"
        report += "3. **تسميد:** رفع معدل البوتاسيوم في الري لتقوية جدر الخلايا النباتية.\n"

    elif "Bacterial_spot" in disease:
        report += "### 🦠 تقرير الحالة: إصابة بكتيرية (التبقع البكتيري)\n"
        report += "مرض بكتيري ينتشر بسرعة مع رزاز الماء والرياح. الجروح الناتجة عن التقليم أو الحشرات تسهل دخوله.\n\n"
        report += "**🛠️ خطة المكافحة:**\n"
        report += "1. ممنوع تماماً الري بالرش العُلوي، اعتمد على الري بالتنقيط أو الغمر المحكوم.\n"
        report += "2. الرش الفوري بمركبات النحاس (مثل هيدروكسيد النحاس أو أوكسي كلورور النحاس) وممكن خلطها مع مضاد حيوي زراعي (كاسوجاميسين) لنتائج أسرع.\n"

    elif "Spider_mites" in disease:
        report += "### 🕷️ تقرير الحالة: آفة أكاروسية (العنكبوت الأحمر)\n"
        report += "هذه الآفة تمتص العصارة الخلوية وتدمر كلوروفيل الورقة. تنشط جداً في الأجواء الحارة والجافة.\n\n"
        report += "**🛠️ خطة المكافحة:**\n"
        report += "1. **مكافحة كيميائية:** رش مبيد أكاروسي متخصص (أبامكتين) أو (سبيروميسيفين). **هام جداً:** يجب توجيه الرش للسطح السفلي للورقة حيث يختبئ العنكبوت.\n"
        report += "2. **مكافحة زراعية:** غسيل النباتات بالماء (في الصباح الباكر) يقلل من أعدادها بشكل ملحوظ لأنها تكره الرطوبة العالية.\n"

    elif "Virus" in disease or "YellowLeaf__Curl" in disease or "mosaic" in disease:
        report += "### 🚫 تقرير الحالة: إصابة فيروسية\n"
        report += "الأمراض الفيروسية ليس لها علاج مباشر يفيد الورقة المصابة، وتنتقل عن طريق الحشرات الثاقبة الماصة (مثل الذبابة البيضاء والمن).\n\n"
        report += "**🛠️ خطة التحرك الصارمة:**\n"
        report += "1. تقليع النباتات المصابة بالكامل فوراً (وضعها في كيس وحرقها) لتجنب انتقال العدوى لباقي الحقل.\n"
        report += "2. رش مبيد حشري جهازي (أسيتامبريد أو إيميداكلوبريد) للقضاء على الحشرة الناقلة للفيروس.\n"
        report += "3. تعقيم أدوات التقليم بمحلول هيبوكلوريت الصوديوم.\n"

    else:
        report += "### 🍄 تقرير الحالة: إصابة فطرية مسببة لتبقعات أو عفن\n"
        report += "غالباً ما تكون ناتجة عن سوء التهوية وكثافة المجموع الخضري مع زيادة الرطوبة.\n\n"
        report += "**🛠️ خطة المكافحة:**\n"
        report += "1. تقليم الأوراق السفلية لتحسين التهوية.\n"
        report += "2. رش مبيد فطري وقائي-علاجي يحتوي على (كلوروثالونيل) أو مركبات نحاسية.\n"

    # 2. نصائح التربة والمناخ (مبنية على اختيارات المستخدم)
    report += "\n---\n### 🌍 ثانياً: إدارة البيئة، الري، والتربة\n"
    
    if water == "كثير":
        if soil == "طينية":
            report += "⚠️ **تحذير هام بخصوص الري:** التربة الطينية تحتفظ بالمياه لفترات طويلة. الري الكثير حالياً يسبب اختناق الجذور ويزيد من احتمالية تعفنها (Root Rot)، وهو ما يهيئ بيئة مثالية لانتشار الفطريات. **توصية:** أوقف الري فوراً حتى تجف الطبقة السطحية بنسبة 50%.\n"
        else:
            report += "💧 **ملاحظة الري:** الري الغزير يشجع الأمراض الفطرية. نرجو تقليل كميات المياه وضبط فترات الري.\n"
    elif water == "قليل":
        if soil == "رملية":
            report += "💧 **تنبيه الري:** التربة الرملية تفقد الماء والعناصر بسرعة. يفضل تقسيم الري لجرعات صغيرة ومتقاربة، مع الاهتمام بـ (حقن الفولفيك أسيد) لزيادة احتفاظ التربة بالمياه والتسميد.\n"
        else:
            report += "⚠️ إجهاد العطش يضعف مناعة النبات ويجعله عرضة للحشرات (مثل العنكبوت الأحمر). يرجى انتظام الري.\n"

    if temp > 35:
        report += f"🌡️ **الإجهاد الحراري ({temp} مئوية):** الحرارة العالية تجعل النبات يغلق ثغوره ويوقف النمو. \n- **توصية:** يجب الري في فترات الصباح الباكر جداً أو ليلاً. نوصي برش (سليكات البوتاسيوم) أو (مستخلص طحالب بحرية) لرفع إجهاد الحرارة عن النبات.\n"
    elif temp < 15:
        report += f"❄️ **برودة الجو ({temp} مئوية):** الحرارة المنخفضة تبطئ من امتصاص الفسفور.\n- **توصية:** رش مركبات طاقة وفوسفور ورقي، وتقليل معدلات الري.\n"
    else:
        report += f"🌤️ **الحرارة ({temp} مئوية):** تعتبر درجات الحرارة الحالية مناسبة ومثالية للنمو.\n"

    report += "\n---\n**💡 ملاحظة الاستشاري:** "
    report += "التشخيص موثوق، ابدأ في تطبيق التوصيات فوراً." if confidence > 0.85 else "جودة الصورة أو زاوية الالتقاط تجعل دقة التحليل متوسطة. نوصي بمقارنة الأعراض على أرض الواقع بما تم ذكره، أو إعادة الفحص بصورة أوضح."
    
    return report

# --- 5. تصميم واجهة الموقع (Layout) ---
st.title("🌿 العيادة الزراعية الذكية")
st.markdown("<p style='font-size: 20px; color: #555;'>استشارة فورية مدعومة بالذكاء الاصطناعي لتشخيص أمراض (الطماطم، البطاطس، الفلفل) وتقديم روشتة العلاج المتكاملة.</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("📋 1. بيانات الحقل والعينة")
    image_file = st.file_uploader("📷 ارفع صورة واضحة لورقة النبات المصابة", type=["jpg", "png", "jpeg"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    temp_in = st.slider("🌡️ درجة حرارة الجو التقريبية (°C)", 0, 50, 25)
    soil_in = st.selectbox("🌱 نوع التربة في الحقل", ["طينية", "رملية", "طميية (صفراء)"])
    water_in = st.selectbox("💧 حالة الرطوبة والري الحالية", ["قليل (عطش)", "متوسط (منتظم)", "كثير (غزير)"])
    
with col2:
    st.subheader("🔍 2. نتيجة الفحص والتقرير الفني")
    
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="العينة قيد الفحص", width=300)
        
        if st.button("🚀 تحليل الحالة واستخراج الروشتة"):
            with st.spinner('👨‍🌾 المهندس الذكي يقوم بفحص العينة وتحليل المعطيات...'):
                try:
                    # المعالجة
                    img = image.convert("RGB").resize((224, 224))
                    img_array = np.array(img) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)
                    
                    # التوقع
                    pred = model.predict(img_array, verbose=0)
                    idx = np.argmax(pred)
                    conf = float(np.max(pred))
                    disease_en = class_names[idx]
                    disease_ar = arabic_names.get(disease_en, disease_en)
                    
                    # عرض النتائج في بطاقات صغيرة وجميلة
                    c1, c2 = st.columns(2)
                    c1.success(f"**التشخيص الآلي:**\n\n {disease_ar}")
                    if conf > 0.8:
                        c2.info(f"**دقة اليقين:**\n\n %{conf*100:.1f} (عالية)")
                    else:
                        c2.warning(f"**دقة اليقين:**\n\n %{conf*100:.1f} (متوسطة)")
                    
                    # عرض تقرير الخبير (Markdown)
                    advice_text = ai_advice(disease_en, temp_in, soil_in, water_in, conf)
                    st.markdown(f"<div class='advice-card'>{advice_text}</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"حدث خطأ غير متوقع أثناء الفحص: {e}")
    else:
        st.info("💡 **تعليمات:** يرجى إدخال بيانات الحقل على اليمين، ثم رفع صورة واضحة للورقة ليتمكن النظام من استخراج التقرير.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>تم التطوير لدعم المزارعين والمهندسين الزراعيين | العيادة الزراعية الذكية © 2024</p>", unsafe_allow_html=True)
