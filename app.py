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

# Initialize session state
if "saved_report" not in st.session_state:
    st.session_state.saved_report = ""
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

# --- 3. Advanced CSS (Dynamic RTL/LTR + Background) ---
direction = "rtl" if is_ar else "ltr"
text_align = "right" if is_ar else "left"
font_family = "'Tajawal', 'Segoe UI', Tahoma, sans-serif" if is_ar else "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&family=Segoe+UI:wght@400;700&display=swap');
    

     .stApp {
        background: linear-gradient(270deg, #00c6ff, #0072ff, #00c6ff);
        background-size: 600% 600%;
        animation: gradientMove 10s ease infinite;
    }

    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
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
        box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
        line-height: 1.8;
        animation: fadeSlide 0.6s ease forwards;
        opacity: 0;
        transform: translateY(20px);
    }}

    @keyframes fadeSlide {{
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        transition: 0.3s;
    }}

    .stButton>button:hover {{
        transform: scale(1.03);
        box-shadow: 0px 6px 20px rgba(0,0,0,0.3);
    }}

    img {{
        filter: drop-shadow(0px 4px 12px rgba(0,0,0,0.4));
    }}

    .modal-overlay {{
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0,0,0,0.65);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease forwards;
    }}

    .modal-box {{
        width: 70%;
        max-height: 85vh;
        overflow-y: auto;
        background: #fff;
        border-radius: 18px;
        padding: 25px;
        position: relative;
        animation: scaleIn 0.35s ease forwards;
    }}

    .close-btn {{
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 22px;
        font-weight: bold;
        cursor: pointer;
    }}

    .close-btn:hover {{
        color: red;
        transform: scale(1.2);
    }}

    @keyframes fadeIn {{
        from {{opacity: 0;}}
        to {{opacity: 1;}}
    }}

    @keyframes scaleIn {{
        from {{
            transform: scale(0.8);
            opacity: 0;
        }}
        to {{
            transform: scale(1);
            opacity: 1;
        }}
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

# --- 6. Detailed Agronomic Logic (Bilingual, Expanded) ---
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
            html += """
<h3>✅ التقييم الفسيولوجي: مثالي</h3>
<p>تظهر العينة التي تم تحليلها <b>كثافة كلوروفيل ممتازة</b> ولا يوجد أي تدهور خلوي. الجهاز الوعائي يعمل بكفاءة.</p>
<h4>📋 توصيات استراتيجية مفصلة:</h4>
<ul>
<li><b>التوازن الغذائي:</b> حافظ على نسب N-P-K (مثلاً 1:1:1 في مرحلة النمو الخضري، ثم 1:2:2 بعد الإزهار). ركز على تطبيقات الكالسيوم-بورون (مثل نترات الكالسيوم 2-3 كجم/1000 م²) أثناء التزهير لتجنب الأزهار الميتة وتشقق الثمار.</li>
<li><b>المحفزات الحيوية:</b> استخدم الأحماض الأمينية (مثل 1 لتر/فدان) وهيومات البوتاسيوم (2-3 كجم/فدان) لتعزيز كفاءة امتصاص الجذور وتحسين مقاومة الإجهادات.</li>
<li><b>المراقبة الوقائية:</b> افحص الحقل كل 48 ساعة بحثاً عن كتل بيض الآفات المبكرة. ضع مصائد لاصقة صفراء لمراقبة الذبابة البيضاء والمن. استخدم شبكات حشرية على مداخل الصوب.</li>
<li><b>إدارة الري:</b> استخدم الري بالتنقيط لتجنب الرطوبة الزائدة على الأوراق. قم بالري صباحاً لتبخير الرطوبة خلال النهار. في الأراضي الثقيلة، أضف فترات جفاف بين الريات لتهوية الجذور.</li>
<li><b>توصيات مستقبلية:</b> قم بتحليل التربة سنوياً لتعديل برنامج التسميد. استخدم أصنافاً مقاومة للأمراض الشائعة في الموسم القادم.</li>
</ul>"""
        elif "Late_blight" in disease:
            html += """
<h3>🚨 إنذار مرضي: الندوة المتأخرة (فيتوفثورا)</h3>
<p><b>المسبب:</b> فطر بيضي <i>Phytophthora infestans</i> يزدهر في الرطوبة العالية (>90%) ودرجات حرارة معتدلة (15-25°م). يمكنه تدمير الحقول بالكامل خلال 7-10 أيام.</p>
<p><b>الأعراض التفصيلية:</b> بقع مائية خضراء داكنة على الأوراق، تتحول إلى بنية سوداء مع هالة صفراء. على الساق، تظهر بقع بنية مستطيلة. في الظروف الرطبة، ينمو عشب أبيض (الجراثيم) على السطح السفلي للأوراق. الثمار تصاب ببقع بنية زيتية.</p>
<h4>🛠️ خطة العمل الطارئة (المكافحة المتكاملة):</h4>
<p><b>1. التدخل الكيميائي الفوري (بالتناوب):</b></p>
<ul>
<li><b>ميتالاكسيل-إم + مانكوزيب</b> (ريدوميل جولد) 250 جم/100 لتر – للوقاية والعلاج المبكر.</li>
<li><b>سيموكسانيل + فاموكسادون</b> (تاكوس) – لعمل علاجي قوي.</li>
<li><b>بروباموكارب هيدروكلوريد</b> (بروليفي) 150 مل/100 لتر – لرعاية الجذور والساق.</li>
<li><b>فوسيتيل-ألومنيوم</b> 200 جم/100 لتر – محفز للمناعة.</li>
<li><b>الرش بالتناوب كل 5-7 أيام، مع إضافة مادة لاصقة (سيلكيت أو تاين).</b></li>
</ul>
<p><b>2. الإدارة الحقلية:</b></p>
<ul>
<li><b>الرطوبة:</b> أوقف الري بالرش فوراً. حوّل إلى الري بالتنقيط إن أمكن. زد التهوية في الصوب.</li>
<li><b>النظافة:</b> اقتلع النباتات المصابة بشدة واحرقها خارج الحقل. لا تقم بعمل كمبوست منها. تطهير الأدوات بالكحول أو هيبوكلوريت.</li>
<li><b>تناوب المحاصيل:</b> لا تزرع محاصيل عائلة الباذنجانيات (بطاطس، طماطم، فلفل) في نفس الحقل لمدة 3 سنوات.</li>
</ul>
<p><b>3. المكافحة الحيوية:</b> رش مستحضرات تحتوي على <i>Trichoderma harzianum</i> أو <i>Bacillus subtilis</i> للحد من تطور الفطر في التربة.</p>"""
        elif "Spider_mites" in disease:
            html += """
<h3>🕷️ تحليل الآفات: العنكبوت الأحمر ذو البقعتين (<i>Tetranychus urticae</i>)</h3>
<p><b>الملاحظات:</b> ثقوب في الخلايا الورقية تؤدي إلى اصفرار منقط (تبقع) ثم جفاف الأوراق. تتغذى العناكب على السطح السفلي للورقة وتنسج خيوطاً حريرية.</p>
<p><b>الظروف المساعدة:</b> ارتفاع الحرارة (>30°م) وانخفاض الرطوبة الجوية (<60%)، وكذلك الإجهاد المائي يزيد من شدة الإصابة.</p>
<h4>🛠️ المكافحة المتكاملة للآفات (IPM):</h4>
<p><b>1. المكافحة الكيميائية (بالتناوب لتجنب المقاومة):</b></p>
<ul>
<li><b>أبامكتين 1.8% EC:</b> 50 مل/100 لتر مع ضمان تغطية السطح السفلي للأوراق.</li>
<li><b>سبيروميسيفين</b> (أوبرون) 25 مل/100 لتر – ممتاز لمكافحة البيض والحوريات.</li>
<li><b>هيكسيثياوكس</b> (نيسورون) 15 مل/100 لتر – يثبط انسلاخ الحوريات.</li>
<li><b>زيت النيم</b> 2-3 مل/لتر – بديل طبيعي مع تأثير مانع للتغذية.</li>
</ul>
<p><b>2. المكافحة الفيزيائية والبيئية:</b></p>
<ul>
<li><b>الرش الضبابي:</b> زيادة الرطوبة حول النبات (رش الأوراق بالماء) يثبط تكاثر العناكب.</li>
<li><b>التبريد:</b> خفض درجة الحرارة في الصوب أو استخدام مراوح للتهوية.</li>
<li><b>إزالة الأعشاب الضارة:</b> لأنها عوائل بديلة للآفة.</li>
</ul>
<p><b>3. المكافحة الحيوية:</b> إطلاق المفترسات الطبيعية مثل <i>Phytoseiulus persimilis</i> (على الأقل 10 أفراد/م²) عند ظهور الإصابة المبكرة. تجنب المبيدات واسعة المجال التي تقتل هذه المفترسات.</p>"""
        elif "Virus" in disease or "mosaic" in disease or "YellowLeaf" in disease:
            html += """
<h3>🚫 التقييم الباثولوجي: استيطان فيروسي جهازي</h3>
<p><b>ملاحظة فنية:</b> الفيروسات جهازية، بمجرد الإصابة لا يوجد علاج كيميائي لأنسجة النبات المصابة. يعتمد النجاح على منع الانتشار والسيطرة على النواقل.</p>
<p><b>الأعراض:</b> تبرقش الأوراق (تناوب مناطق خضراء وصفراء)، تجعد، تقزم النبات، تشوه الثمار، ضعف عام.</p>
<h4>🛠️ استراتيجية السيطرة (لا علاج، فقط منع):</h4>
<p><b>1. إدارة النواقل (الحشرات):</b> السيطرة على الذبابة البيضاء (ناقل فيروس تجعد الأوراق الصفراء) والمن (ناقل فيروس الموزاييك).</p>
<ul>
<li>استخدم مبيدات جهازية مثل <b>إيميداكلوبريد</b> (كونفيدور 0.5 مل/لتر) أو <b>أسيتاميبريد</b> (موسبيلان 0.25 جم/لتر) بالتناوب مع مبيدات تماس (بيرميثرين).</li>
<li>انشر المصائد اللاصقة الصفراء (15-20 مصيدة/فدان) للمراقبة والكشف المبكر.</li>
<li>استخدم شبكات حشرية دقيقة (50 ميكرون) على مداخل الصوب وفتحات التهوية.</li>
</ul>
<p><b>2. الاستئصال:</b> اقتلع النباتات المصابة فوراً لأنها بؤرة لانتشار الفيروس. ضعها في أكياس محكمة وأخرجها خارج الحقل. لا تترك بقايا النباتات داخل التربة.</p>
<p><b>3. وقاية الزراعة الجديدة:</b> استخدم شتلات خالية من الفيروسات من مصادر موثوقة. تطهير الأدوات واليدين قبل العمل في الحقل. تجنب زراعة المحاصيل المتضررة بجانب محاصيل حساسة جديدة.</p>"""
        else:
            html += f"""
<h3>🍄 التشخيص: {disease_ar}</h3>
<p>بقع ميتة على الأوراق (نخرية) ناتجة على الأرجح عن مسببات فطرية أو بكتيرية. يعتمد العلاج على المسبب المحدد ولكن يمكن اتباع بروتوكول عام.</p>
<h4>🛠️ توصيات الخبراء للسيطرة:</h4>
<p><b>1. المكافحة الكيميائية (عند ظهور الأعراض):</b></p>
<ul>
<li><b>كلوروثالونيل</b> (برافو) 200 مل/100 لتر – فطري واسع المجال.</li>
<li><b>أزوكسيستروبين</b> (أميستار) 40 مل/100 لتر – فطري جهازي مع تأثير وقائي وعلاجي.</li>
<li><b>أوكسي كلورور النحاس</b> 300 جم/100 لتر – للكبح البكتيري والفطري (يستخدم بحذر لتجنب التسمم).</li>
<li><b>مانكوزيب</b> (مانزوكوب) 250 جم/100 لتر – فعال ضد الندوات المبكرة والمتأخرة.</li>
</ul>
<p><b>2. الإجراءات الثقافية:</b></p>
<ul>
<li>تقليم الأوراق السفلية والمصابة لتحسين التهوية وتقليل مصدر العدوى.</li>
<li>تجنب الري بالرش، واستخدم الري بالتنقيط.</li>
<li>تطبيق التغطية بالبلاستيك (mulching) لمنع تناثر التربة الملوثة على الأوراق.</li>
<li>تناوب المحاصيل مع نباتات غير عائلة (مثل البقوليات) لمدة عامين.</li>
</ul>
<p><b>3. المكافحة الحيوية:</b> رش مستحضرات تحتوي على <i>Bacillus subtilis</i> (سيريناد) أو <i>Trichoderma</i> لتثبيط نمو الفطريات الممرضة.</p>"""

        # Environmental Context Arabic (expanded)
        html += "<h4>🌍 عوامل الذكاء البيئي وتوصيات مكيفة:</h4>"
        if temp > 38:
            html += f"<p>⚠️ <b>إجهاد حراري ({temp} م°):</b> استخدم <b>سليكات البوتاسيوم</b> (2 مل/لتر) لتقوية جدر الخلايا وتقليل النتح. رش الأحماض الأمينية والجبرلين لتخفيف الإجهاد. زد فترات الري ليلاً لتبريد الجذور.</p>"
        elif temp < 10:
            html += f"<p>❄️ <b>إجهاد برودة ({temp} م°):</b> استخدم أغطية بلاستيكية ليلاً. رش سترات الكالسيوم لتعزيز صلابة النبات. قلل الري لتجنب تعفن الجذور.</p>"
        
        if soil == "طينية" and water in ["عالي", "مشبع بالمياه"]:
            html += "<p>⚠️ <b>ميكانيكا التربة:</b> خطر كبير لحدوث <b>نقص الأكسجين (Hypoxia)</b> وعفن الجذور في التربة الثقيلة. أضف مادة عضوية (كمبوست) لتحسين الصرف. زود فترات الجفاف بين الريات. استخدم مراوح تهوية في الصوب لزيادة الأكسجين حول الجذور.</p>"
        elif soil == "رملية" and water == "منخفض":
            html += "<p>💧 <b>إجهاد جفاف:</b> التربة الرملية تستنزف الماء بسرعة. النبات يقترب من نقطة الذبول الدائم. زد وتيرة الري مع تقليل الكمية (الري المتكرر الخفيف). أضف مادة حافظة للرطوبة مثل البوليمرات الماصة أو الكمبوست لتحسين احتفاظ التربة بالماء.</p>"
        elif soil == "طينية" and water == "منخفض":
            html += "<p>⚠️ <b>إجهاد جفاف في تربة ثقيلة:</b> التربة الطينية قد تتشقق وتجف بسرعة رغم قدرتها على الاحتفاظ بالماء. قم بالتغطية العضوية (القش) حول النباتات للحفاظ على رطوبة التربة ومنع التبخر.</p>"
        
        html += f"""<hr>
<p style="font-style: italic;"><b>القرار الهندسي النهائي:</b> مستوى الثقة {conf*100:.1f}%. التوصيات مبنية على البروتوكولات الزراعية الدولية وممارسات الخبراء.</p>
<p style="font-size: 0.9em;"><b>ملاحظة مهمة:</b> هذه التوصيات استشارية. راجع دائمًا مهندس زراعي معتمد لتحديد الجرعات حسب ظروفك الحقلية والتشريعات المحلية.</p>
</div>"""

    else:
        # English Version (expanded similarly)
        html = f"""<div class="report-container">
<h2 style="text-align: center;">AGRICULTURE CLINIC REPORT</h2>
<p style="text-align: center;">Generated by ENG/ AHMED ABD AL-HAFEZ</p>
<hr>
<p><b>Primary Diagnosis:</b> {disease_en}</p>
<p><b>Statistical Confidence:</b> {conf*100:.2f}%</p>
<p><b>Field Conditions:</b> Temp: {temp}°C | Soil: {soil} | Irrigation: {water}</p>
<hr>"""

        if "healthy" in disease:
            html += """
<h3>✅ Physiological Assessment: Optimal</h3>
<p>The analyzed specimen shows <b>excellent chlorophyll density</b> and no cellular degradation. The vascular system appears functional.</p>
<h4>📋 Detailed Strategic Recommendations:</h4>
<ul>
<li><b>Nutritional Balance:</b> Maintain N-P-K ratios (e.g., 1:1:1 during vegetative stage, then 1:2:2 after flowering). Focus on Calcium-Boron applications (e.g., Calcium nitrate 2-3 kg/1000 m²) during flowering to prevent blossom end rot and fruit cracking.</li>
<li><b>Biostimulants:</b> Apply Amino Acids (1 L/ha) and Potassium Humate (2-3 kg/ha) to enhance root absorption efficiency and improve stress tolerance.</li>
<li><b>Preventive Monitoring:</b> Scout the field every 48 hours for early pest egg clusters. Use yellow sticky traps to monitor whiteflies and aphids. Install insect nets on greenhouse openings.</li>
<li><b>Irrigation Management:</b> Use drip irrigation to avoid excess leaf moisture. Irrigate in the morning to allow foliage to dry during the day. On heavy soils, incorporate dry periods between irrigations to aerate roots.</li>
<li><b>Future Recommendations:</b> Conduct annual soil analysis to adjust fertilization programs. Use resistant cultivars for common diseases in the next season.</li>
</ul>"""
        elif "Late_blight" in disease:
            html += """
<h3>🚨 Pathogen Alert: Late Blight (<i>Phytophthora infestans</i>)</h3>
<p><b>Etiology:</b> An oomycete pathogen that thrives in high humidity (>90%) and moderate temperatures (15-25°C). It can destroy fields within 7-10 days.</p>
<p><b>Detailed Symptoms:</b> Dark, water-soaked lesions on leaves, turning brown-black with a yellow halo. On stems, elongated brown lesions. Under wet conditions, white mold (sporangia) appears on the underside of leaves. Fruits develop oily brown spots.</p>
<h4>🛠️ Emergency Action Plan (Integrated Management):</h4>
<p><b>1. Immediate Chemical Intervention (rotate products):</b></p>
<ul>
<li><b>Metalaxyl-M + Mancozeb</b> (Ridomil Gold) 250 g/100 L – for prevention and early curative action.</li>
<li><b>Cymoxanil + Famoxadone</b> (Tanos) – strong curative effect.</li>
<li><b>Propamocarb Hydrochloride</b> (Previcur) 150 ml/100 L – for root and stem protection.</li>
<li><b>Fosetyl-Aluminum</b> (Aliette) 200 g/100 L – induces plant resistance.</li>
<li><b>Apply every 5-7 days, alternating, with a sticker (e.g., Silwet).</b></li>
</ul>
<p><b>2. Field Management:</b></p>
<ul>
<li><b>Humidity:</b> Halt overhead irrigation immediately. Switch to drip if possible. Increase ventilation in greenhouses.</li>
<li><b>Sanitation:</b> Remove and burn severely infected plants. Do NOT compost them. Disinfect tools with alcohol or bleach.</li>
<li><b>Crop Rotation:</b> Do not plant Solanaceae crops (potato, tomato, pepper) in the same field for 3 years.</li>
</ul>
<p><b>3. Biological Control:</b> Apply products containing <i>Trichoderma harzianum</i> or <i>Bacillus subtilis</i> to suppress the pathogen in soil.</p>"""
        elif "Spider_mites" in disease:
            html += """
<h3>🕷️ Pest Analysis: Two-Spotted Spider Mite (<i>Tetranychus urticae</i>)</h3>
<p><b>Observations:</b> Punctured leaf cells leading to chlorotic stippling, then leaf desiccation. Mites feed on the abaxial surface and produce fine webbing.</p>
<p><b>Favorable Conditions:</b> High temperatures (>30°C), low humidity (<60%), and water stress exacerbate infestations.</p>
<h4>🛠️ Integrated Pest Management (IPM):</h4>
<p><b>1. Chemical Control (rotate to prevent resistance):</b></p>
<ul>
<li><b>Abamectin 1.8% EC:</b> 50 ml/100 L, ensure thorough coverage of lower leaf surfaces.</li>
<li><b>Spiromesifen</b> (Oberon) 25 ml/100 L – excellent against eggs and nymphs.</li>
<li><b>Hexythiazox</b> (Nissorun) 15 ml/100 L – inhibits molting of nymphs.</li>
<li><b>Neem Oil</b> 2-3 ml/L – a natural alternative with antifeedant effects.</li>
</ul>
<p><b>2. Physical and Environmental Control:</b></p>
<ul>
<li><b>Mist Spraying:</b> Increasing humidity around plants (misting leaves) suppresses mite reproduction.</li>
<li><b>Cooling:</b> Reduce greenhouse temperature or use fans for ventilation.</li>
<li><b>Weed Removal:</b> Eliminate alternative host plants.</li>
</ul>
<p><b>3. Biological Control:</b> Release predatory mites such as <i>Phytoseiulus persimilis</i> (at least 10 individuals/m²) at early infestation. Avoid broad‑spectrum pesticides that kill these predators.</p>"""
        elif "Virus" in disease or "mosaic" in disease or "YellowLeaf" in disease:
            html += """
<h3>🚫 Pathological Assessment: Systemic Viral Infection</h3>
<p><b>Technical Note:</b> Viruses are systemic; once infected, there is no chemical cure for plant tissue. Management focuses on preventing spread and controlling vectors.</p>
<p><b>Symptoms:</b> Mosaic (alternating green and yellow patches), leaf curl, stunting, fruit deformities, general decline.</p>
<h4>🛠️ Control Strategy (No Cure, Only Prevention):</h4>
<p><b>1. Vector Management:</b> Control whiteflies (vector of Tomato Yellow Leaf Curl Virus) and aphids (vector of mosaic viruses).</p>
<ul>
<li>Use systemic insecticides such as <b>Imidacloprid</b> (Confidor 0.5 ml/L) or <b>Acetamiprid</b> (Mospilan 0.25 g/L), alternating with contact products (permethrin).</li>
<li>Place yellow sticky traps (15-20 per acre) for monitoring and early detection.</li>
<li>Install fine mesh insect nets (50 micron) on greenhouse vents and entrances.</li>
</ul>
<p><b>2. Eradication:</b> Uproot infected plants immediately as they serve as virus reservoirs. Place them in sealed bags and remove from the field. Do not leave plant debris inside.</p>
<p><b>3. Protection for New Plantings:</b> Use virus‑free seedlings from reliable sources. Disinfect tools and hands before working in the field. Avoid planting new susceptible crops adjacent to infected fields.</p>"""
        else:
            html += f"""
<h3>🍄 Diagnosis: {disease_en}</h3>
<p>Necrotic leaf lesions likely caused by fungal or bacterial pathogens. A general control protocol is provided below.</p>
<h4>🛠️ Expert Recommendations for Control:</h4>
<p><b>1. Chemical Control (when symptoms appear):</b></p>
<ul>
<li><b>Chlorothalonil</b> (Bravo) 200 ml/100 L – broad‑spectrum fungicide.</li>
<li><b>Azoxystrobin</b> (Amistar) 40 ml/100 L – systemic fungicide with protective and curative action.</li>
<li><b>Copper Oxychloride</b> 300 g/100 L – for bacterial and fungal suppression (use cautiously to avoid phytotoxicity).</li>
<li><b>Mancozeb</b> (Manzate) 250 g/100 L – effective against early and late blights.</li>
</ul>
<p><b>2. Cultural Practices:</b></p>
<ul>
<li>Prune lower and infected leaves to improve air circulation and reduce inoculum.</li>
<li>Avoid overhead irrigation; use drip irrigation.</li>
<li>Apply plastic mulch to prevent soil splash onto leaves.</li>
<li>Rotate crops with non‑host families (e.g., legumes) for two years.</li>
</ul>
<p><b>3. Biological Control:</b> Apply products containing <i>Bacillus subtilis</i> (Serenade) or <i>Trichoderma</i> to suppress fungal pathogens.</p>"""

        # Environmental Context English (expanded)
        html += "<h4>🌍 Environmental Intelligence Factors & Tailored Recommendations:</h4>"
        if temp > 38:
            html += f"<p>⚠️ <b>Heat Stress ({temp}°C):</b> Apply <b>Potassium Silicate</b> (2 ml/L) to harden cell walls and reduce transpiration. Spray amino acids and gibberellins to alleviate stress. Increase night irrigation to cool roots.</p>"
        elif temp < 10:
            html += f"<p>❄️ <b>Cold Stress ({temp}°C):</b> Use plastic covers at night. Spray calcium citrate to strengthen plant cell walls. Reduce irrigation to avoid root rot.</p>"
        
        if soil == "Clay" and water in ["High", "Waterlogged"]:
            html += "<p>⚠️ <b>Soil Mechanics:</b> High risk of <b>Hypoxia</b> and root rot in heavy soil. Add organic matter (compost) to improve drainage. Increase dry periods between irrigations. Use ventilation fans in greenhouses to boost oxygen around roots.</p>"
        elif soil == "Sandy" and water == "Low":
            html += "<p>💧 <b>Drought Stress:</b> Sandy soils drain rapidly. Plant is nearing wilting point. Increase irrigation frequency with smaller amounts (light, frequent watering). Add moisture‑retaining materials like hydrogels or compost to improve water holding capacity.</p>"
        elif soil == "Clay" and water == "Low":
            html += "<p>⚠️ <b>Drought Stress in Heavy Soil:</b> Clay soils may crack and dry quickly despite their water‑holding capacity. Apply organic mulch (straw) around plants to conserve moisture and reduce evaporation.</p>"
        
        html += f"""<hr>
<p style="font-style: italic;"><b>Final Engineering Verdict:</b> Confidence level is {conf*100:.1f}%. Recommendations are based on international agronomic protocols and expert practices.</p>
<p style="font-size: 0.9em;"><b>Important Note:</b> These recommendations are advisory. Always consult a certified agricultural engineer for precise dosages based on your field conditions and local regulations.</p>
</div>"""
    return html

# Logo and header
col_logo, col_text = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=140)
    except:
        pass

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
        s_input_raw = st.selectbox(ui["soil_label"], ui["soil_options"])
        w_input_raw = st.selectbox(ui["water_label"], ui["water_options"])

with c2:
    st.subheader(ui["report_header"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=400, caption=f"ID: {uploaded_file.name}")
        
        if st.button(ui["btn_analyze"]):
            with st.spinner(ui["spinner"]):
                # Process image
                proc_img = img.convert("RGB").resize((224, 224))
                img_array = np.array(proc_img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                # Predict
                raw_preds = model.predict(img_array, verbose=0)
                best_idx = np.argmax(raw_preds)
                best_conf = float(np.max(raw_preds))
                label = class_names[best_idx]
                
                # Success message
                identified_text = arabic_classes.get(label, label) if is_ar else label.replace('___', ' | ')
                st.success(f"{identified_text} ✓")
                
                # Generate full report
                full_report = get_detailed_report(label, t_input, s_input_raw, w_input_raw, best_conf, is_ar)
                st.session_state.saved_report = full_report
                st.session_state.show_modal = True
                
                # Display modal (overlay)
                modal_html = f"""
                <div class="modal-overlay" id="modal" onclick="if(event.target.id=='modal') this.style.display='none'">
                    <div class="modal-box">
                        <div class="close-btn" onclick="document.getElementById('modal').style.display='none'">×</div>
                        {full_report}
                    </div>
                </div>
                """
                st.markdown(modal_html, unsafe_allow_html=True)
    
    # Display the saved report in the main area if it exists
    if st.session_state.saved_report:
        st.markdown(st.session_state.saved_report, unsafe_allow_html=True)
    else:
        st.info(ui["wait"])

st.markdown("---")
st.caption(ui["footer"])
