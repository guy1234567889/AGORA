import streamlit as st
import json
import os
import base64

# הגדרות עמוד מורחבות לעיצוב מודרני ופריסה רחבה
st.set_page_config(page_title="אגורה החדש", page_icon="♻️", layout="wide")

DATA_FILE = "agora_data.json"

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

if 'items' not in st.session_state:
    st.session_state['items'] = load_items()

# הזרקת קוד עיצוב (CSS) מתקדם עם אנימציות ורקע זז
st.markdown("""
    <style>
    /* רקע אנימטיבי שזז לאט (Gradient Animation) */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #334155, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* הסתרת הרקע הלבן/שחור הרגיל של החלק העליון */
    header {background-color: transparent !important;}

    /* יישור לימין של כל האפליקציה */
    .stApp, .stMarkdown, p, div, h1, h2, h3 {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* אנימציית כניסה לכרטיסיות (החלקה למעלה) */
    @keyframes floatIn {
        0% { opacity: 0; transform: translateY(40px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* עיצוב כרטיסיות המוצרים - סטייל זכוכית (Glassmorphism) */
    .product-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.1);
        height: 100%;
        animation: floatIn 0.8s ease-out forwards;
    }
    
    /* אפקט ריחוף עם העכבר */
    .product-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* תגיות צבעוניות וזוהרות לקטגוריה ועיר */
    .badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        background: linear-gradient(45deg, #FF512F, #DD2476);
        color: white;
        font-size: 0.85rem;
        margin-left: 8px;
        margin-bottom: 15px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(221, 36, 118, 0.4);
    }
    .location-badge {
        background: linear-gradient(45deg, #1CB5E0, #000851);
        box-shadow: 0 4px 10px rgba(28, 181, 224, 0.4);
    }
    
    /* כותרות בתוך הכרטיסיה */
    .card-title {
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.5rem;
        color: #ffffff;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ לוח שיתוף חפצים")
st.markdown("<p style='font-size: 1.2rem; color: #e2e8f0; text-shadow: 1px 1px 2px #000;'>פלטפורמה דינמית למסירה ומציאת חפצים שווים.</p>", unsafe_allow_html=True)
st.divider()

# תפריט ניווט 
menu = ["🛍️ הלוח המרכזי", "➕ פרסום מודעה חדשה"]
choice = st.sidebar.radio("תפריט פעולות", menu)

if choice == "🛍️ הלוח המרכזי":
    st.sidebar.divider()
    st.sidebar.markdown("### 🔍 סינון מתקדם")
    
    all_items = st.session_state['items']
    categories = ["הכל"] + list(set([item['category'] for item in all_items]))
    locations = ["הכל"] + list(set([item['location'] for item in all_items]))
    
    selected_cat = st.sidebar.selectbox("📂 קטגוריה", categories)
    selected_loc = st.sidebar.selectbox("📍 עיר", locations)
    
    filtered_items = [
        item for item in all_items 
        if (selected_cat == "הכל" or item['category'] == selected_cat) and 
           (selected_loc == "הכל" or item['location'] == selected_loc)
    ]
    
    if not filtered_items:
        st.info("לא מצאנו חפצים מתאימים. נסה לשנות את הסינון!")
    else:
        # פריסת גריד
        cols = st.columns(3)
        
        for index, item in enumerate(reversed(filtered_items)):
            col = cols[index % 3] 
            
            with col:
                st.markdown(f"""
                <div class="product-card">
                    <h3 class="card-title">{item['title']}</h3>
                    <div>
                        <span class="badge">{item['category']}</span>
                        <span class="badge location-badge">📍 {item['location']}</span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">{item['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if item.get('image'):
                    try:
                        st.image(base64.b64decode(item['image']), use_container_width=True)
                    except:
                        pass
                
                st.button("💬 צור קשר עם המוסר", key=f"btn_{index}_{item['title']}", use_container_width=True)
                st.write("") 

elif choice == "➕ פרסום מודעה חדשה":
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📝 העלאת חפץ חדש")
        with st.form("add_item_form", clear_on_submit=True):
            title = st.text_input("📌 כותרת (מה אתה מוסר?)", placeholder="לדוגמה: ספה תלת מושבית")
            
            c1, c2 = st.columns(2)
            with c1:
                category = st.selectbox("📂 קטגוריה", ["רהיטים", "מוצרי חשמל", "ביגוד", "צעצועים", "שונות"])
            with c2:
                location = st.text_input("📍 עיר איסוף", placeholder="לדוגמה: רחובות")
                
            description = st.text_area("📝 תיאור החפץ", placeholder="ספר על מצב החפץ, מתי אפשר לאסוף...")
            uploaded_image = st.file_uploader("📸 העלה תמונה (מומלץ!)", type=["png", "jpg", "jpeg"])
            
            submitted = st.form_submit_button("🚀 פרסם מודעה באוויר", type="primary", use_container_width=True)
            
            if submitted:
                if title and location:
                    img_str = ""
                    if uploaded_image:
                        img_str = base64.b64encode(uploaded_image.read()).decode()
                        
                    new_item = {
                        "title": title,
                        "category": category,
                        "location": location,
                        "description": description,
                        "image": img_str
                    }
                    
                    st.session_state['items'].append(new_item)
                    save_items(st.session_state['items'])
                    
                    st.success("🎉 החפץ פורסם בהצלחה! תוכל לראות אותו בלוח המרכזי.")
                else:
                    st.error("⚠️ חובה למלא כותרת ועיר איסוף.")
