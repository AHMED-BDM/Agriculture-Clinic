import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import base64

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
    "footer": "© 2026 النظم الزراعية الذكية | قسم الزراعة الدقيقة" if is_ar else "© 2026 Smart Agri-Systems | Expert Module | Precision Agriculture Division",
    "export_pdf": "تصدير PDF" if is_ar else "Export PDF"
}

# Initialize session state
if "saved_report" not in st.session_state:
    st.session_state.saved_report = ""
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

# --- 3. Advanced CSS (Dynamic RTL/LTR + Professional Design) ---
direction = "rtl" if is_ar else "ltr"
text_align = "right" if is_ar else "left"
font_family = "'Tajawal', 'Segoe UI', Tahoma, sans-serif" if is_ar else "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("background.jpg")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Segoe+UI:wght@400;500;700&display=swap');
    
    /* Global Reset & Base */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    .stApp {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Overlay - more opaque for better readability */
    .stApp > div:first-child {{
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(2px);
    }}

    /* Sidebar - modern glassmorphism */
    .stSidebar {{
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0,0,0,0.05);
    }}

    /* Remove background from the logo column */
    div[data-testid="column"]:first-child {{
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
    }}
    
    /* Remove extra white rectangles */
    .stApp header {{
        background: transparent !important;
    }}
    .stApp .st-emotion-cache-1r6slb0 {{
        background: transparent !important;
    }}

    /* Main Columns - subtle cards */
    [data-testid="stColumn"] {{
        background: rgba(255, 255, 255, 0.88);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }}
    
    [data-testid="stColumn"]:hover {{
        box-shadow: 0 12px 28px rgba(0,0,0,0.1);
    }}

    /* All text in black */
    html, body, [class*="css"], .stMarkdown, .stSubheader, .stTitle, .stCaption,
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError,
    .stSelectbox, .stSlider, .stTextInput, label,
    .stSidebar * {{
        color: #000000 !important;
        font-family: {font_family};
        direction: {direction};
        text-align: {text_align};
    }}

    /* Headings with slight weight */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }}
    
    /* Report Container - premium card */
    .report-container {{
        background: #ffffff !important;
        border-radius: 28px;
        padding: 2rem;
        border: none;
        box-shadow: 0 20px 35px -10px rgba(0,0,0,0.15);
        line-height: 1.7;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .report-container:hover {{
        box-shadow: 0 25px 40px -12px rgba(0,0,0,0.2);
    }}
    
    /* Green accent borders */
    .report-container hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #1b5e20, #2e7d32, #1b5e20);
        margin: 1.2rem 0;
    }}
    
    /* Buttons - gradient with shadow */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white !important;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 40px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #2e7d32, #1b5e20);
    }}
    
    /* Image styling */
    img {{
        border-radius: 20px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }}
    
    img:hover {{
        transform: scale(1.02);
    }}
    
    /* Modal overlay */
    .modal-overlay {{
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0,0,0,0.75);
        backdrop-filter: blur(4px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.25s ease;
    }}
    
    .modal-box {{
        width: 75%;
        max-width: 1000px;
        max-height: 85vh;
        overflow-y: auto;
        background: #fff;
        border-radius: 32px;
        padding: 2rem;
        position: relative;
        animation: scaleIn 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
        box-shadow: 0 30px 40px rgba(0,0,0,0.3);
    }}
    
    .close-btn {{
        position: absolute;
        top: 1rem;
        right: 1.5rem;
        font-size: 1.8rem;
        font-weight: 700;
        cursor: pointer;
        color: #555;
        transition: all 0.2s;
        line-height: 1;
        background: rgba(0,0,0,0.05);
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        z-index: 10000;
    }}
    
    .close-btn:hover {{
        color: #d32f2f;
        background: rgba(0,0,0,0.1);
        transform: rotate(90deg);
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes scaleIn {{
        from {{
            transform: scale(0.95);
            opacity: 0;
        }}
        to {{
            transform: scale(1);
            opacity: 1;
        }}
    }}
    
    /* Fix for info box */
    .stInfo {{
        background: rgba(0,0,0,0.05) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        border-left: 6px solid #1b5e20 !important;
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        font-weight: 600 !important;
        background: rgba(0,0,0,0.02) !important;
        border-radius: 12px !important;
    }}
    
    /* Print styles for PDF export */
    @media print {{
        body * {{
            visibility: hidden;
        }}
        .report-container, .report-container * {{
            visibility: visible;
        }}
        .report-container {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            margin: 0;
            padding: 20px;
            box-shadow: none;
        }}
        .stApp, .stApp > div, [data-testid="stColumn"] {{
            background: white !important;
        }}
        .stButton, .stSidebar, .stMarkdown:has(button) {{
            display: none !important;
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

# --- 6. Detailed Agronomic Logic (Bilingual, Professional) ---
def get_detailed_report(disease, temp, soil, water, conf, is_ar):
    disease_en = disease.replace("_", " ")
    disease_ar = arabic_classes.get(disease, disease_en)
    
    if is_ar:
        html = f"""<div class="report-container">
<h2 style="text-align: center;">📋 تقرير العيادة الزراعية المعتمد</h2>
<p style="text-align: center; opacity:0.7;">المهندس الزراعي المعتمد: أحمد عبد الحافظ</p>
<hr>
<p><strong>التشخيص الأساسي:</strong> {disease_ar}</p>
<p><strong>دقة النموذج الإحصائي:</strong> {conf*100:.2f}%</p>
<p><strong>الظروف الحقلية المسجلة:</strong> درجة الحرارة: {temp}°C | نوع التربة: {soil} | مستوى الري: {water}</p>
<hr>"""

        if "healthy" in disease:
            html += """
<h3>✅ التقييم الفسيولوجي – سليم</h3>
<p>العينة المدروسة تظهر <strong>كفاءة تمثيل ضوئي ممتازة</strong> وغياب أي علامات إجهاد حيوي أو غير حيوي. الجهاز الوعائي يعمل بكفاءة عالية.</p>
<h4>📌 توصيات إستراتيجية للحفاظ على الصحة النباتية:</h4>
<ul>
<li><strong>التوازن الغذائي الدقيق:</strong> الحفاظ على نسب N-P-K متوازنة (1:1:1 خلال النمو الخضري، ثم 1:2:2 بعد التزهير). التركيز على إضافة الكالسيوم (نترات الكالسيوم 2-3 كجم/1000 م²) والبورون (حمض البوريك 0.5-1 جم/لتر) لضمان جودة الثمار.</li>
<li><strong>المنشطات الحيوية:</strong> تطبيق الأحماض الأمينية (1 لتر/فدان) وهيمات البوتاسيوم (2-3 كجم/فدان) لتحسين امتصاص الجذور وزيادة مقاومة الإجهادات البيئية.</li>
<li><strong>المراقبة الوقائية:</strong> الفحص الحقل المنتظم كل 48 ساعة لاكتشاف أي تجمعات مبكرة للآفات. استخدام المصائد اللاصقة الصفراء (15-20 مصيدة/فدان) لمراقبة الذبابة البيضاء والمن. تركيب شبكات حشرية (50 ميكرون) على مداخل الصوبات.</li>
<li><strong>إدارة الري:</strong> الري بالتنقيط للحفاظ على جفاف الأوراق. الري صباحاً للسماح بتبخر الرطوبة. في الأراضي الثقيلة، إدخال فترات جفاف بين الريات لتهوية الجذور وتجنب الإجهاد الناتج عن نقص الأكسجين.</li>
<li><strong>توصيات مستقبلية:</strong> تحليل التربة سنوياً لتعديل برامج التسميد. اعتماد أصناف مقاومة للأمراض السائدة في الموسم التالي.</li>
</ul>"""
        elif "Late_blight" in disease:
            html += """
<h3>🚨 إنذار مرضي – الندوة المتأخرة (Phytophthora infestans)</h3>
<p><strong>المسبب:</strong> فطر بيضي (Oomycete) يتطور بسرعة في الرطوبة الجوية &gt;90% ودرجات حرارة معتدلة (15-25°م). يمكنه القضاء على الحقل بالكامل خلال 7-10 أيام في الظروف الملائمة.</p>
<p><strong>الأعراض التفصيلية:</strong> بقع مائية خضراء داكنة على الأوراق، تتحول إلى بنية سوداء مع هالة صفراء. على الساق تظهر بقع بنية مستطيلة. في الأجواء الرطبة، ينمو عشب أبيض (الجراثيم) على السطح السفلي للأوراق. الثمار تصاب ببقع بنية زيتية لامعة.</p>
<h4>🛠️ خطة المكافحة المتكاملة (الطوارئ):</h4>
<p><strong>1. التدخل الكيميائي العاجل (بالتناوب لتجنب المقاومة):</strong></p>
<ul>
<li><strong>ميتالاكسيل-إم + مانكوزيب</strong> (ريدوميل جولد) 250 جم/100 لتر – وقائي وعلاجي مبكر.</li>
<li><strong>سيموكسانيل + فاموكسادون</strong> (تاكوس) – تأثير علاجي قوي.</li>
<li><strong>بروباموكارب هيدروكلوريد</strong> (بروليفي) 150 مل/100 لتر – يحمي الجذور والساق.</li>
<li><strong>فوسيتيل-ألومنيوم</strong> (أليت) 200 جم/100 لتر – منشط مناعي.</li>
<li><strong>الرش كل 5-7 أيام، بالتناوب، مع مادة لاصقة (سيلكيت 0.5 مل/لتر).</strong></li>
</ul>
<p><strong>2. الإدارة الحقلية:</strong></p>
<ul>
<li><strong>الرطوبة:</strong> وقف الري بالرش فوراً، التحول إلى الري بالتنقيط، زيادة التهوية في الصوب.</li>
<li><strong>النظافة:</strong> قلع النباتات المصابة بشدة وحرقها خارج الحقل. تطهير الأدوات بالكحول 70% أو هيبوكلوريت الصوديوم.</li>
<li><strong>الدورة الزراعية:</strong> عدم زراعة محاصيل العائلة الباذنجانية (بطاطس، طماطم، فلفل) في نفس الحقل لمدة 3 سنوات على الأقل.</li>
</ul>
<p><strong>3. المكافحة الحيوية:</strong> رش مستحضرات تحتوي على <em>Trichoderma harzianum</em> أو <em>Bacillus subtilis</em> للحد من استمرار الفطر في التربة.</p>"""
        elif "Spider_mites" in disease:
            html += """
<h3>🕷️ تحليل الآفة – العنكبوت الأحمر ذو البقعتين (Tetranychus urticae)</h3>
<p><strong>الملاحظات:</strong> ثقوب في الخلايا الورقية تؤدي إلى اصفرار منقط (تبقع) ثم جفاف الأوراق. تتغذى العناكب على السطح السفلي للأوراق وتنسج خيوطاً حريرية كثيفة.</p>
<p><strong>الظروف المساعدة:</strong> ارتفاع الحرارة (&gt;30°م) وانخفاض الرطوبة الجوية (&lt;60%)، بالإضافة إلى الإجهاد المائي يزيد من حدة الإصابة.</p>
<h4>🛠️ الإدارة المتكاملة للآفات (IPM):</h4>
<p><strong>1. المكافحة الكيميائية (بالتناوب لمنع المقاومة):</strong></p>
<ul>
<li><strong>أبامكتين 1.8% EC</strong> (فيرتيميك) 50 مل/100 لتر – يغطى السطح السفلي للأوراق.</li>
<li><strong>سبيروميسيفين</strong> (أوبرون) 25 مل/100 لتر – ممتاز ضد البيض والحوريات.</li>
<li><strong>هيكسيثياوكس</strong> (نيسورون) 15 مل/100 لتر – يثبط انسلاخ الحوريات.</li>
<li><strong>زيت النيم</strong> 2-3 مل/لتر – بديل طبيعي مانع للتغذية.</li>
</ul>
<p><strong>2. المكافحة الفيزيائية والبيئية:</strong></p>
<ul>
<li><strong>الرش الضبابي:</strong> رفع الرطوبة حول النبات (رش الأوراق بالماء) يثبط تكاثر العناكب.</li>
<li><strong>التبريد:</strong> خفض درجة الحرارة في الصوب أو استخدام مراوح للتهوية.</li>
<li><strong>إزالة الأعشاب الضارة:</strong> لأنها عوائل بديلة للآفة.</li>
</ul>
<p><strong>3. المكافحة الحيوية:</strong> إطلاق المفترسات الطبيعية مثل <em>Phytoseiulus persimilis</em> (10 أفراد/م²) عند أول ظهور للإصابة. تجنب المبيدات واسعة المجال التي تقتل هذه المفترسات.</p>"""
        elif "Virus" in disease or "mosaic" in disease or "YellowLeaf" in disease:
            html += """
<h3>🚫 تقييم باثولوجي – عدوى فيروسية جهازية</h3>
<p><strong>ملاحظة فنية:</strong> الفيروسات جهازية، بمجرد الإصابة لا يوجد علاج كيميائي لأنسجة النبات المصابة. النجاح يعتمد على منع الانتشار والسيطرة على النواقل.</p>
<p><strong>الأعراض:</strong> تبرقش الأوراق (تبادل مناطق خضراء وصفراء)، تجعد، تقزم النبات، تشوه الثمار، ضعف عام في النمو.</p>
<h4>🛠️ استراتيجية السيطرة (لا علاج، فقط منع):</h4>
<p><strong>1. إدارة النواقل (الحشرات):</strong> السيطرة على الذبابة البيضاء (ناقل فيروس تجعد الأوراق الصفراء) والمن (ناقل فيروس الموزاييك).</p>
<ul>
<li>استخدام مبيدات جهازية مثل <strong>إيميداكلوبريد</strong> (كونفيدور 0.5 مل/لتر) أو <strong>أسيتاميبريد</strong> (موسبيلان 0.25 جم/لتر) بالتناوب مع مبيدات تماس (بيرميثرين).</li>
<li>نشر المصائد اللاصقة الصفراء (15-20 مصيدة/فدان) للمراقبة والكشف المبكر.</li>
<li>تركيب شبكات حشرية دقيقة (50 ميكرون) على مداخل الصوبات وفتحات التهوية.</li>
</ul>
<p><strong>2. الاستئصال:</strong> قلع النباتات المصابة فوراً لأنها بؤرة لانتشار الفيروس. وضعها في أكياس محكمة وإخراجها خارج الحقل. عدم ترك بقايا النباتات داخل التربة.</p>
<p><strong>3. وقاية الزراعة الجديدة:</strong> استخدام شتلات خالية من الفيروسات من مصادر موثوقة. تطهير الأدوات واليدين قبل العمل في الحقل. تجنب زراعة المحاصيل الحساسة بجوار حقول مصابة.</p>"""
        else:
            html += f"""
<h3>🍄 التشخيص: {disease_ar}</h3>
<p>بقع نخرية على الأوراق ناتجة عن مسببات فطرية أو بكتيرية. يعتمد العلاج على المسبب الدقيق ولكن يمكن اتباع البروتوكول العام التالي.</p>
<h4>🛠️ توصيات الخبراء للسيطرة:</h4>
<p><strong>1. المكافحة الكيميائية (عند ظهور الأعراض):</strong></p>
<ul>
<li><strong>كلوروثالونيل</strong> (برافو) 200 مل/100 لتر – فطري واسع المجال.</li>
<li><strong>أزوكسيستروبين</strong> (أميستار) 40 مل/100 لتر – فطري جهازي وقائي وعلاجي.</li>
<li><strong>أوكسي كلورور النحاس</strong> 300 جم/100 لتر – للكبح البكتيري والفطري (يستخدم بحذر لتجنب التسمم).</li>
<li><strong>مانكوزيب</strong> (مانزوكوب) 250 جم/100 لتر – فعال ضد الندوات المبكرة والمتأخرة.</li>
</ul>
<p><strong>2. الإجراءات الثقافية:</strong></p>
<ul>
<li>تقليم الأوراق السفلية والمصابة لتحسين التهوية وتقليل مصدر العدوى.</li>
<li>تجنب الري بالرش، واستخدام الري بالتنقيط.</li>
<li>تطبيق التغطية بالبلاستيك (mulching) لمنع تناثر التربة الملوثة على الأوراق.</li>
<li>تناوب المحاصيل مع نباتات غير عائلة (مثل البقوليات) لمدة عامين.</li>
</ul>
<p><strong>3. المكافحة الحيوية:</strong> رش مستحضرات تحتوي على <em>Bacillus subtilis</em> (سيريناد) أو <em>Trichoderma</em> لتثبيط نمو الفطريات الممرضة.</p>"""

        # Environmental Context Arabic (expanded)
        html += "<h4>🌍 عوامل الذكاء البيئي وتوصيات مكيفة:</h4>"
        if temp > 38:
            html += f"<p>⚠️ <strong>إجهاد حراري ({temp}°م):</strong> استخدام <strong>سليكات البوتاسيوم</strong> (2 مل/لتر) لتقوية جدر الخلايا وتقليل النتح. رش الأحماض الأمينية والجبرلين لتخفيف الإجهاد. زيادة الري ليلاً لتبريد منطقة الجذور.</p>"
        elif temp < 10:
            html += f"<p>❄️ <strong>إجهاد برودة ({temp}°م):</strong> استخدام أغطية بلاستيكية ليلاً. رش سترات الكالسيوم لتعزيز صلابة النبات. تقليل الري لتجنب تعفن الجذور.</p>"
        
        if soil == "طينية" and water in ["عالي", "مشبع بالمياه"]:
            html += "<p>⚠️ <strong>ميكانيكا التربة:</strong> خطر مرتفع لحدوث <strong>نقص الأكسجين (Hypoxia)</strong> وعفن الجذور في التربة الثقيلة. إضافة مادة عضوية (كمبوست) لتحسين الصرف. إطالة فترات الجفاف بين الريات. استخدام مراوح تهوية في الصوب لزيادة الأكسجين حول الجذور.</p>"
        elif soil == "رملية" and water == "منخفض":
            html += "<p>💧 <strong>إجهاد جفاف:</strong> التربة الرملية تستنزف الماء بسرعة. النبات يقترب من نقطة الذبول الدائم. زيادة وتيرة الري مع تقليل الكمية (الري المتكرر الخفيف). إضافة مواد حافظة للرطوبة مثل البوليمرات الماصة أو الكمبوست لتحسين احتفاظ التربة بالماء.</p>"
        elif soil == "طينية" and water == "منخفض":
            html += "<p>⚠️ <strong>إجهاد جفاف في تربة ثقيلة:</strong> التربة الطينية قد تتشقق وتجف بسرعة رغم قدرتها على الاحتفاظ بالماء. التغطية العضوية (القش) حول النباتات للحفاظ على رطوبة التربة ومنع التبخر.</p>"
        
        html += f"""<hr>
<p style="font-style: italic;"><strong>القرار الهندسي النهائي:</strong> مستوى الثقة {conf*100:.1f}%. التوصيات تستند إلى البروتوكولات الزراعية الدولية وممارسات الخبراء المعتمدة.</p>
<p style="font-size: 0.9em;"><strong>ملاحظة مهمة:</strong> هذه التوصيات استشارية. يُرجى الرجوع إلى مهندس زراعي معتمد لتحديد الجرعات وفق ظروفك الحقلية والتشريعات المحلية.</p>
</div>"""

    else:
        # English Version (professional)
        html = f"""<div class="report-container">
<h2 style="text-align: center;">📋 CERTIFIED AGRICULTURE CLINIC REPORT</h2>
<p style="text-align: center; opacity:0.7;">Certified Agricultural Engineer: Ahmed Abd Al-Hafez</p>
<hr>
<p><strong>Primary Diagnosis:</strong> {disease_en}</p>
<p><strong>Statistical Confidence:</strong> {conf*100:.2f}%</p>
<p><strong>Field Conditions:</strong> Temperature: {temp}°C | Soil: {soil} | Irrigation: {water}</p>
<hr>"""

        if "healthy" in disease:
            html += """
<h3>✅ Physiological Assessment – Healthy</h3>
<p>The analyzed sample exhibits <strong>excellent photosynthetic efficiency</strong> and no signs of biotic or abiotic stress. The vascular system is fully functional.</p>
<h4>📌 Strategic Recommendations for Plant Health Maintenance:</h4>
<ul>
<li><strong>Precise Nutritional Balance:</strong> Maintain balanced N-P-K ratios (1:1:1 during vegetative stage, then 1:2:2 after flowering). Focus on Calcium (Calcium nitrate 2-3 kg/1000 m²) and Boron (Boric acid 0.5-1 g/L) applications during flowering to prevent blossom end rot and fruit cracking.</li>
<li><strong>Biostimulants:</strong> Apply Amino Acids (1 L/ha) and Potassium Humate (2-3 kg/ha) to enhance root absorption and improve stress tolerance.</li>
<li><strong>Preventive Monitoring:</strong> Scout the field every 48 hours for early pest egg masses. Use yellow sticky traps (15-20 per acre) to monitor whiteflies and aphids. Install insect-proof nets (50 mesh) on greenhouse openings.</li>
<li><strong>Irrigation Management:</strong> Use drip irrigation to avoid leaf wetness. Irrigate in the morning to allow foliage to dry. On heavy soils, incorporate dry periods between irrigations to aerate roots and prevent hypoxia.</li>
<li><strong>Future Recommendations:</strong> Conduct annual soil analysis to fine‑tune fertilization. Use resistant cultivars for prevalent diseases in the upcoming season.</li>
</ul>"""
        elif "Late_blight" in disease:
            html += """
<h3>🚨 Pathogen Alert – Late Blight (Phytophthora infestans)</h3>
<p><strong>Etiology:</strong> An oomycete pathogen that thrives in high humidity (>90%) and moderate temperatures (15-25°C). It can devastate fields within 7-10 days under favorable conditions.</p>
<p><strong>Detailed Symptoms:</strong> Dark, water-soaked lesions on leaves turning brown-black with a yellow halo. Elongated brown lesions on stems. Under humid conditions, white sporangial growth appears on leaf undersides. Fruits develop oily brown spots.</p>
<h4>🛠️ Integrated Management Plan (Emergency):</h4>
<p><strong>1. Immediate Chemical Intervention (rotate products):</strong></p>
<ul>
<li><strong>Metalaxyl-M + Mancozeb</strong> (Ridomil Gold) 250 g/100 L – preventive and early curative.</li>
<li><strong>Cymoxanil + Famoxadone</strong> (Tanos) – strong curative action.</li>
<li><strong>Propamocarb Hydrochloride</strong> (Previcur) 150 ml/100 L – protects roots and stems.</li>
<li><strong>Fosetyl-Aluminum</strong> (Aliette) 200 g/100 L – resistance inducer.</li>
<li><strong>Apply every 5-7 days, alternating, with a sticker (Silwet 0.5 ml/L).</strong></li>
</ul>
<p><strong>2. Field Management:</strong></p>
<ul>
<li><strong>Humidity:</strong> Halt overhead irrigation immediately; switch to drip. Increase greenhouse ventilation.</li>
<li><strong>Sanitation:</strong> Remove and burn severely infected plants. Disinfect tools with 70% alcohol or bleach.</li>
<li><strong>Crop Rotation:</strong> Avoid planting Solanaceae crops (potato, tomato, pepper) in the same field for at least 3 years.</li>
</ul>
<p><strong>3. Biological Control:</strong> Apply products containing <em>Trichoderma harzianum</em> or <em>Bacillus subtilis</em> to suppress soil‑borne inoculum.</p>"""
        elif "Spider_mites" in disease:
            html += """
<h3>🕷️ Pest Analysis – Two-Spotted Spider Mite (Tetranychus urticae)</h3>
<p><strong>Observations:</strong> Punctured leaf cells cause chlorotic stippling, followed by leaf desiccation. Mites feed on the abaxial surface and produce dense webbing.</p>
<p><strong>Favorable Conditions:</strong> High temperatures (>30°C), low humidity (<60%), and water stress exacerbate infestations.</p>
<h4>🛠️ Integrated Pest Management (IPM):</h4>
<p><strong>1. Chemical Control (rotate to avoid resistance):</strong></p>
<ul>
<li><strong>Abamectin 1.8% EC</strong> (Vertimec) 50 ml/100 L – ensure thorough coverage of lower leaf surfaces.</li>
<li><strong>Spiromesifen</strong> (Oberon) 25 ml/100 L – excellent against eggs and nymphs.</li>
<li><strong>Hexythiazox</strong> (Nissorun) 15 ml/100 L – inhibits nymph molting.</li>
<li><strong>Neem Oil</strong> 2-3 ml/L – natural antifeedant.</li>
</ul>
<p><strong>2. Physical and Environmental Control:</strong></p>
<ul>
<li><strong>Mist Spraying:</strong> Increase humidity around plants (misting leaves) to suppress mite reproduction.</li>
<li><strong>Cooling:</strong> Reduce greenhouse temperature or use fans for ventilation.</li>
<li><strong>Weed Removal:</strong> Eliminate alternative host plants.</li>
</ul>
<p><strong>3. Biological Control:</strong> Release predatory mites such as <em>Phytoseiulus persimilis</em> (10 individuals/m²) at early infestation. Avoid broad‑spectrum pesticides that kill these predators.</p>"""
        elif "Virus" in disease or "mosaic" in disease or "YellowLeaf" in disease:
            html += """
<h3>🚫 Pathological Assessment – Systemic Viral Infection</h3>
<p><strong>Technical Note:</strong> Viruses are systemic; once infected, there is no chemical cure for plant tissue. Success depends on preventing spread and controlling vectors.</p>
<p><strong>Symptoms:</strong> Mosaic (alternating green and yellow patches), leaf curl, stunting, fruit deformities, overall decline.</p>
<h4>🛠️ Control Strategy (No Cure, Only Prevention):</h4>
<p><strong>1. Vector Management:</strong> Control whiteflies (vector of Tomato Yellow Leaf Curl Virus) and aphids (vector of mosaic viruses).</p>
<ul>
<li>Use systemic insecticides such as <strong>Imidacloprid</strong> (Confidor 0.5 ml/L) or <strong>Acetamiprid</strong> (Mospilan 0.25 g/L), alternating with contact products (permethrin).</li>
<li>Place yellow sticky traps (15-20 per acre) for monitoring and early detection.</li>
<li>Install fine mesh insect nets (50 micron) on greenhouse vents and entrances.</li>
</ul>
<p><strong>2. Eradication:</strong> Uproot infected plants immediately as they serve as virus reservoirs. Place them in sealed bags and remove from the field. Do not leave plant debris inside.</p>
<p><strong>3. Protection for New Plantings:</strong> Use virus‑free seedlings from reliable sources. Disinfect tools and hands before working. Avoid planting new susceptible crops adjacent to infected fields.</p>"""
        else:
            html += f"""
<h3>🍄 Diagnosis: {disease_en}</h3>
<p>Necrotic leaf lesions likely caused by fungal or bacterial pathogens. A general control protocol is provided below.</p>
<h4>🛠️ Expert Recommendations for Control:</h4>
<p><strong>1. Chemical Control (when symptoms appear):</strong></p>
<ul>
<li><strong>Chlorothalonil</strong> (Bravo) 200 ml/100 L – broad‑spectrum fungicide.</li>
<li><strong>Azoxystrobin</strong> (Amistar) 40 ml/100 L – systemic fungicide with protective and curative action.</li>
<li><strong>Copper Oxychloride</strong> 300 g/100 L – for bacterial and fungal suppression (use cautiously to avoid phytotoxicity).</li>
<li><strong>Mancozeb</strong> (Manzate) 250 g/100 L – effective against early and late blights.</li>
</ul>
<p><strong>2. Cultural Practices:</strong></p>
<ul>
<li>Prune lower and infected leaves to improve air circulation and reduce inoculum.</li>
<li>Avoid overhead irrigation; use drip irrigation.</li>
<li>Apply plastic mulch to prevent soil splash onto leaves.</li>
<li>Rotate crops with non‑host families (e.g., legumes) for two years.</li>
</ul>
<p><strong>3. Biological Control:</strong> Apply products containing <em>Bacillus subtilis</em> (Serenade) or <em>Trichoderma</em> to suppress fungal pathogens.</p>"""

        # Environmental Context English (expanded)
        html += "<h4>🌍 Environmental Intelligence Factors & Tailored Recommendations:</h4>"
        if temp > 38:
            html += f"<p>⚠️ <strong>Heat Stress ({temp}°C):</strong> Apply <strong>Potassium Silicate</strong> (2 ml/L) to strengthen cell walls and reduce transpiration. Spray amino acids and gibberellins to alleviate stress. Increase night irrigation to cool roots.</p>"
        elif temp < 10:
            html += f"<p>❄️ <strong>Cold Stress ({temp}°C):</strong> Use plastic covers at night. Spray calcium citrate to strengthen plant cell walls. Reduce irrigation to avoid root rot.</p>"
        
        if soil == "Clay" and water in ["High", "Waterlogged"]:
            html += "<p>⚠️ <strong>Soil Mechanics:</strong> High risk of <strong>Hypoxia</strong> and root rot in heavy soil. Add organic matter (compost) to improve drainage. Increase dry periods between irrigations. Use ventilation fans in greenhouses to boost oxygen around roots.</p>"
        elif soil == "Sandy" and water == "Low":
            html += "<p>💧 <strong>Drought Stress:</strong> Sandy soils drain rapidly. Plant is nearing wilting point. Increase irrigation frequency with smaller amounts (light, frequent watering). Add moisture‑retaining materials like hydrogels or compost to improve water holding capacity.</p>"
        elif soil == "Clay" and water == "Low":
            html += "<p>⚠️ <strong>Drought Stress in Heavy Soil:</strong> Clay soils may crack and dry quickly despite their water‑holding capacity. Apply organic mulch (straw) around plants to conserve moisture and reduce evaporation.</p>"
        
        html += f"""<hr>
<p style="font-style: italic;"><strong>Final Engineering Verdict:</strong> Confidence level is {conf*100:.1f}%. Recommendations are based on international agronomic protocols and expert practices.</p>
<p style="font-size: 0.9em;"><strong>Important Note:</strong> These recommendations are advisory. Always consult a certified agricultural engineer for precise dosages based on your field conditions and local regulations.</p>
</div>"""
    return html

# Logo and header – remove background
col_logo, col_text = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=140)
    except:
        pass
# The rest of the header is handled by CSS; we don't need extra content here.

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
        
        # Export PDF button
        if st.button(ui["export_pdf"], key="pdf_btn"):
            st.markdown("""
            <script>
                window.print();
            </script>
            """, unsafe_allow_html=True)
        
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
                
                # Display modal (overlay) with close button using JavaScript
                modal_html = f"""
                <div id="modalOverlay" class="modal-overlay">
                    <div class="modal-box">
                        <div class="close-btn" onclick="document.getElementById('modalOverlay').style.display='none'">×</div>
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
