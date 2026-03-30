import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. Page Configuration ---
st.set_page_config(page_title="Pro Ag-Clinic AI", page_icon="🌿", layout="wide")

# --- 2. Language Setup ---
with st.sidebar:
    st.title("🌐 Language / اللغة")
    lang = st.radio("Choose Interface Language:", ["English", "العربية"])

is_ar = lang == "العربية"

# UI Dictionaries
ui = {
    "title": "🌿 العيادة الزراعية الذكية الاحترافية" if is_ar else "🌿 Professional Agriculture AI Clinic",
    "subtitle": "نظام التحليل المرضي والاستشارة الفنية الدقيقة" if is_ar else "Detailed Pathological Analysis & Expert Consultation System",
    "input_header": "📋 إدخال بيانات الحقل" if is_ar else "📋 Input Field Data",
    "upload_label": "ارفع صورة الورقة المصابة (JPG/PNG)" if is_ar else "Upload Leaf Specimen (JPG/PNG)",
    "env_expander": "مستشعرات البيئة (إدخال يدوي)" if is_ar else "Environment Sensors (Manual Entry)",
    "temp": "درجة الحرارة المحيطة (مئوية)" if is_ar else "Ambient Temperature (°C)",
    "soil_label": "تكوين التربة" if is_ar else "Soil Composition",
    "soil_options": ["طينية", "رملية", "طميية", "غرينية"] if is_ar else ["Clay", "Sandy", "Loamy", "Silty"],
    "water_label": "مستوى الري/الرطوبة" if is_ar else "Irrigation/Moisture Level",
    "water_options": ["منخفض", "متوسط", "عالي", "مشبع بالمياه"] if is_ar else ["Low", "Medium", "High", "Waterlogged"],
    "report_header": "🔍 التقرير الفني للتحليل" if is_ar else "🔍 Technical Analysis Report",
    "btn_analyze": "بدء التحليل العميق" if is_ar else "EXECUTE DEEP ANALYSIS",
    "spinner": "جاري استدعاء قاعدة البيانات الزراعية..." if is_ar else "Accessing Agricultural Knowledge Base...",
    "wait": "في انتظار رفع صورة العينة للتشخيص..." if is_ar else "Awaiting leaf specimen for diagnosis...",
    "footer": "© 2026 النظم الزراعية الذكية | قسم الزراعة الدقيقة" if is_ar else "© 2026 Smart Agri-Systems | Expert Module | Precision Agriculture Division"
}

# --- 3. Advanced CSS (Dynamic RTL/LTR) ---
direction = "rtl" if is_ar else "ltr"
text_align = "right" if is_ar else "left"
font_family = "'Tajawal', 'Segoe UI', Tahoma, sans-serif" if is_ar else "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&family=Segoe+UI:wght@400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: {font_family};
        direction: {direction};
        text-align: {text_align};
    }}

    .report-container {{
        background-color: #ffffff !important;
        color: #111111 !important;
        padding: 30px;
        border-radius: 15px;
        border-left: 12px solid #1b5e20;
        border-right: 12px solid #1b5e20;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
        line-height: 1.8;
        text-align: {text_align};
        direction: {direction};
    }}

    .report-container h2, .report-container h3, .report-container h4 {{
        color: #1b5e20 !important;
        margin-top: 20px;
        font-weight: bold;
    }}

    .report-container b {{
        color: #000000 !important;
    }}

    .stButton>button {{
        width: 100%;
        background-color: #1b5e20;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. Model Loading ---
@st.cache_resource
def load_agri_model():
    return tf.keras.models.load_model('Fplant_model.keras')

model = load_agri_model()

# --- 5. Class Mapping & Translations ---
class_names = [
    "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

arabic_classes = {
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
    "Tomato_Spider_mites_Two_spotted_spider_mite": "طماطم - العنكبوت الأحمر ذو البقعتين",
    "Tomato__Target_Spot": "طماطم - التبقع الهدفي",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "طماطم - فيروس تجعد واصفرار الأوراق",
    "Tomato__Tomato_mosaic_virus": "طماطم - فيروس الموزاييك",
    "Tomato_healthy": "طماطم - سليم"
}

# --- 6. Detailed Agronomic Logic (Bilingual) ---
def get_detailed_report(disease, temp, soil, water, conf, is_ar):
    disease_en = disease.replace("_", " ")
    disease_ar = arabic_classes.get(disease, disease_en)
    
    if is_ar:
        html = f"""<div class="report-container">
<h2 style="text-align: center;">تقرير العيادة الزراعية المعتمد</h2>
<p style="text-align: center;">تم الإنشاء بواسطة المهندس/ أحمد عبد الحافظ</p>
<hr>
<p><b>التشخيص الأساسي:</b> {disease_ar}</p>
<p><b>دقة التشخيص الإحصائي:</b> {conf*100:.2f}%</p>
<p><b>الظروف الحقلية:</b> الحرارة: {temp} م° | التربة: {soil} | الري: {water}</p>
<hr>"""

        if "healthy" in disease:
            html += """<h3>✅ التقييم الفسيولوجي: مثالي</h3>
<p>تظهر العينة التي تم تحليلها <b>كثافة كلوروفيل ممتازة</b> ولا يوجد أي تدهور خلوي. الجهاز الوعائي يعمل بكفاءة.</p>
<h4>توصيات استراتيجية:</h4>
<ul>
<li><b>التوازن الغذائي:</b> حافظ على نسب N-P-K. ركز على تطبيقات الكالسيوم-بورون أثناء التزهير.</li>
<li><b>المحفزات الحيوية:</b> استخدم الأحماض الأمينية وهيومات البوتاسيوم لتعزيز كفاءة امتصاص الجذور.</li>
<li><b>المراقبة الوقائية:</b> افحص الحقل كل 48 ساعة بحثاً عن كتل بيض الآفات المبكرة.</li>
</ul>"""
        elif "Late_blight" in disease:
            html += """<h3>🚨 إنذار مرضي: الندوة المتأخرة (فيتوفثورا)</h3>
<p><b>المسبب:</b> فطر بيضي يزدهر في الرطوبة العالية (>90%). يمكنه تدمير الحقول بالكامل خلال 7-10 أيام.</p>
<h4>🛠️ خطة العمل الطارئة:</h4>
<p><b>1. التدخل الكيميائي الفوري:</b>
<ul>
<li><b>ميتالاكسيل-إم + مانكوزيب</b> (مثل ريدوميل جولد) بمعدل 250 جم/100 لتر.</li>
<li><b>سيموكسانيل + فاموكسادون</b> للعمل العلاجي للإصابات المبكرة.</li>
</ul></p>
<p><b>2. الإدارة الحقلية:</b>
<ul>
<li><b>الرطوبة:</b> أوقف الري بالرش فوراً وحول إلى التنقيط إن أمكن.</li>
<li><b>النظافة:</b> اقتلع النباتات المصابة بشدة واحرقها خارج الحقل. لا تقم بعمل كمبوست منها.</li>
</ul></p>"""
        elif "Spider_mites" in disease:
            html += """<h3>🕷️ تحليل الآفات: العنكبوت الأحمر</h3>
<p><b>الملاحظات:</b> ثقوب في الخلايا الورقية تؤدي إلى اصفرار منقط. تتغذى العناكب على السطح السفلي للورقة.</p>
<h4>🛠️ المكافحة المتكاملة للآفات (IPM):</h4>
<p><b>1. المكافحة الكيميائية:</b>
<ul>
<li><b>أبامكتين 1.8% EC:</b> رش بمعدل 50 مل/100 لتر مع ضمان تغطية السطح السفلي.</li>
<li><b>سبيروميسيفين:</b> ممتاز لمكافحة البيض والحوريات.</li>
</ul></p>
<p><b>2. المكافحة الفيزيائية:</b>
<ul>
<li><b>الرش الضبابي:</b> زيادة الرطوبة حول النبات يثبط تكاثر العناكب.</li>
</ul></p>"""
        elif "Virus" in disease or "mosaic" in disease or "YellowLeaf" in disease:
            html += """<h3>🚫 التقييم الباثولوجي: استيطان فيروسي</h3>
<p><b>ملاحظة فنية:</b> الفيروسات جهازية. بمجرد الإصابة، لا يوجد علاج كيميائي لأنسجة النبات.</p>
<h4>🛠️ استراتيجية السيطرة:</h4>
<p><b>1. إدارة النواقل (الحشرات):</b> السيطرة على الذبابة البيضاء والمن.
<ul>
<li>استخدم مبيدات جهازية مثل <b>إيميداكلوبريد</b> أو <b>أسيتاميبريد</b>.</li>
<li>انشر المصائد اللاصقة الصفراء للمراقبة.</li>
</ul></p>
<p><b>2. الاستئصال:</b> اقتلع النباتات المصابة فوراً لأنها بؤرة لانتشار الفيروس.</p>"""
        else:
            html += f"""<h3>🍄 التشخيص: {disease_ar}</h3>
<p>بقع ميتة ناتجة على الأرجح عن مسببات فطرية أو بكتيرية.</p>
<h4>🛠️ توصيات الخبراء:</h4>
<ul>
<li><b>مبيدات فطرية:</b> استخدم <b>كلوروثالونيل</b> أو <b>أزوكسيستروبين</b>.</li>
<li><b>المعالجة النحاسية:</b> رش <b>أوكسي كلورور النحاس</b> (300 جم/100 لتر) للكبح البكتيري.</li>
</ul>"""

        # Environmental Context Arabic
        html += "<h4>🌍 عوامل الذكاء البيئي:</h4>"
        if temp > 38:
            html += f"<p>⚠️ <b>إجهاد حراري ({temp} م°):</b> استخدم <b>سليكات البوتاسيوم</b> لتقوية جدر المانع وتقليل النتح.</p>"
        
        if soil == "طينية" and water in ["عالي", "مشبع بالمياه"]:
            html += "<p>⚠️ <b>ميكانيكا التربة:</b> خطر كبير لحدوث <b>نقص الأكسجين (Hypoxia)</b> وعفن الجذور في التربة الثقيلة.</p>"
        elif soil == "رملية" and water == "منخفض":
            html += "<p>💧 <b>إجهاد جفاف:</b> التربة الرملية تستنزف الماء بسرعة. النبات يقترب من نقطة الذبول الدائم.</p>"

        html += f"""<hr>
<p style="font-style: italic;"><b>الحكم الهندسي النهائي:</b> مستوى الثقة {conf*100:.1f}%. التوصيات مبنية على البروتوكولات الزراعية الدولية.</p>
</div>"""

    else:
        # English Version
        html = f"""<div class="report-container">
<h2 style="text-align: center;">AGRICULTURE CLINIC REPORT</h2>
<p style="text-align: center;">Generated by ENG/ AHMED ABD AL-HAFEZ</p>
<hr>
<p><b>Primary Diagnosis:</b> {disease_en}</p>
<p><b>Statistical Confidence:</b> {conf*100:.2f}%</p>
<p><b>Field Conditions:</b> Temp: {temp}°C | Soil: {soil} | Irrigation: {water}</p>
<hr>"""

        if "healthy" in disease:
            html += """<h3>✅ Physiological Assessment: Optimal</h3>
<p>The analyzed specimen shows <b>excellent chlorophyll density</b> and no cellular degradation. The vascular system appears functional.</p>
<h4>Strategic Recommendations:</h4>
<ul>
<li><b>Nutritional Balance:</b> Maintain N-P-K ratios. Focus on Calcium-Boron applications during flowering.</li>
<li><b>Biostimulants:</b> Apply Amino Acids and Humic Acid to enhance root absorption efficiency.</li>
<li><b>Monitoring:</b> Scout the field every 48 hours for early pest egg clusters.</li>
</ul>"""
        elif "Late_blight" in disease:
            html += """<h3>🚨 Pathogen Alert: Late Blight (Phytophthora infestans)</h3>
<p><b>Etiology:</b> An oomycete pathogen that thrives in high humidity (>90%). It can destroy fields within 7-10 days.</p>
<h4>🛠️ Emergency Action Plan:</h4>
<p><b>1. Immediate Chemical Intervention:</b>
<ul>
<li><b>Metalaxyl-M + Mancozeb</b> (e.g., Ridomil Gold) at 250g/100L.</li>
<li><b>Cymoxanil + Famoxadone</b> for curative action on early lesions.</li>
<li><b>Propamocarb Hydrochloride</b> for root and stem protection.</li>
</ul></p>
<p><b>2. Field Management:</b>
<ul>
<li><b>Humidity:</b> Halt overhead irrigation immediately. Switch to drip.</li>
<li><b>Sanitation:</b> Remove and burn infected plants. Do NOT compost.</li>
</ul></p>"""
        elif "Spider_mites" in disease:
            html += """<h3>🕷️ Pest Analysis: Two-Spotted Spider Mite</h3>
<p><b>Observations:</b> Punctured leaf cells leading to chlorotic stippling. Mites feed on the abaxial surface.</p>
<h4>🛠️ Integrated Pest Management (IPM):</h4>
<p><b>1. Chemical Control:</b>
<ul>
<li><b>Abamectin 1.8% EC:</b> Apply at 50ml/100L. Ensure thorough coverage.</li>
<li><b>Spiromesifen:</b> Excellent for controlling eggs and nymphs.</li>
</ul></p>
<p><b>2. Physical Control:</b>
<ul>
<li><b>Mist Spraying:</b> Increasing humidity inhibits mite reproduction.</li>
</ul></p>"""
        elif "Virus" in disease or "mosaic" in disease or "YellowLeaf" in disease:
            html += """<h3>🚫 Pathological Assessment: Viral Colonization</h3>
<p><b>Technical Note:</b> Viruses are systemic. Once infected, there is no chemical cure for the plant tissue.</p>
<h4>🛠️ Control Strategy:</h4>
<p><b>1. Vector Management:</b> Control Whiteflies and Aphids.
<ul>
<li>Apply <b>Imidacloprid</b> or <b>Acetamiprid</b>.</li>
<li>Use yellow sticky traps for monitoring.</li>
</ul></p>
<p><b>2. Eradication:</b> Uproot infected plants immediately as they are reservoirs.</p>"""
        else:
            html += f"""<h3>🍄 Diagnosis: {disease_en}</h3>
<p>Necrotic lesions likely caused by fungal/bacterial pathogens.</p>
<h4>🛠️ Expert Recommendations:</h4>
<ul>
<li><b>Fungicides:</b> Apply <b>Chlorothalonil</b> or <b>Azoxystrobin</b>.</li>
<li><b>Copper Treatment:</b> Apply <b>Copper Oxychloride</b> (300g/100L) for bacterial suppression.</li>
</ul>"""

        # Environmental Context English
        html += "<h4>🌍 Environmental Intelligence Factors:</h4>"
        if temp > 38:
            html += f"<p>⚠️ <b>Heat Stress ({temp}°C):</b> Apply <b>Potassium Silicate</b> to harden cell walls and reduce transpiration.</p>"
        
        if soil == "Clay" and water in ["High", "Waterlogged"]:
            html += "<p>⚠️ <b>Soil Mechanics:</b> High risk of <b>Hypoxia</b> and root rot in heavy soil.</p>"
        elif soil == "Sandy" and water == "Low":
            html += "<p>💧 <b>Drought Stress:</b> Sandy soils drain rapidly. Plant is nearing wilting point.</p>"

        html += f"""<hr>
<p style="font-style: italic;"><b>Final Engineering Verdict:</b> Confidence level is {conf*100:.1f}%. Recommendation based on international agronomic protocols.</p>
</div>"""
    return html

# --- 7. App Layout ---
st.title(ui["title"])
st.markdown(ui["subtitle"])
st.markdown("---")

c1, c2 = st.columns([1, 1.4], gap="large")

with c1:
    st.subheader(ui["input_header"])
    uploaded_file = st.file_uploader(ui["upload_label"], type=["jpg","jpeg","png"])
    
    with st.expander(ui["env_expander"]):
        t_input = st.slider(ui["temp"], 0, 55, 26)
        
        # Determine current index based on language to avoid selectbox mapping errors
        s_input_raw = st.selectbox(ui["soil_label"], ui["soil_options"])
        w_input_raw = st.selectbox(ui["water_label"], ui["water_options"])

with c2:
    st.subheader(ui["report_header"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=400, caption=f"ID: {uploaded_file.name}")
        
        if st.button(ui["btn_analyze"]):
            with st.spinner(ui["spinner"]):
                # Process
                proc_img = img.convert("RGB").resize((224, 224))
                img_array = np.array(proc_img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                # Predict
                raw_preds = model.predict(img_array, verbose=0)
                best_idx = np.argmax(raw_preds)
                best_conf = float(np.max(raw_preds))
                label = class_names[best_idx]
                
                # Success Info
                identified_text = arabic_classes.get(label, label) if is_ar else label.replace('___', ' | ')
                st.success(f"{identified_text} ✓")
                
                # Detailed Report Rendering
                full_report = get_detailed_report(label, t_input, s_input_raw, w_input_raw, best_conf, is_ar)
                st.markdown(full_report, unsafe_allow_html=True)
    else:
        st.info(ui["wait"])

st.markdown("---")
st.caption(ui["footer"])
