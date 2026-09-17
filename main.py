import streamlit as st
import json
import os
import base64
import random

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

# מחולל בוטים - מייצר נתונים פיקטיביים
def generate_bot_items(num_items=5):
    titles = [
        "רכיבי ארדואינו ומטריצות", "ספה תלת מושבית שחורה", "אייפון 12 (מסך שבור)", 
        "אופניים חשמליים (ללא סוללה)", "קופסת צעצועים לגיל 3", "ספרים בנושא תכנות ב-Python", 
        "ראוטר ישן של בזק", "מכונת כביסה פתח עליון", "שולחן כתיבה מאיקאה", "אוסף כבלים RF ומתאמים"
    ]
    categories = ["רהיטים", "מוצרי חשמל", "ביגוד", "צעצועים", "שונות", "אלקטרוניקה"]
    locations = ["רחובות", "תל אביב", "חיפה", "ראשון לציון", "ירושלים", "נס ציונה", "אשדוד"]
    conditions = ["חדש לגמרי", "כמו חדש", "משומש - מצב טוב", "דורש תיקון"]
    
    new_bot_items = []
    for _ in range(num_items):
        new_bot_items.append({
            "title": random.choice(titles),
            "category": random.choice(categories),
            "location": random.choice(locations),
            "condition": random.choice(conditions),
            "description": "הפריט הועלה על ידי הבוט האוטומטי שלנו. כל הקודם זוכה! לא שומר לאף אחד, פשוט לבוא ולקחת.",
            "phone": f"05{random.randint(2,9)}{random.randint(1000000,9999999)}",
            "image": "",
            "is_bot": True
        })
    return new_bot_items

# הזרקת קוד עיצוב CSS 
st.markdown("""
    <style>
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
    header {background-color: transparent !important;}
    .stApp, .stMarkdown, p, div, h1, h2, h3 {
        direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @keyframes floatIn {
        0% { opacity: 0; transform: translateY(40px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .product-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px; padding: 22px; margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        height: 100%;
        animation: floatIn 0.6s ease-out forwards;
    }
    .product-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(76, 175, 80, 0.5);
    }
    .badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        background: linear-gradient(45deg, #FF512F, #DD2476);
        color: white; font-size: 0.8rem; margin-left: 6px; margin-bottom: 10px; font-weight: bold;
    }
    .location-badge { background: linear-gradient(45deg, #1CB5E0, #000851); }
    .condition-badge { background: linear-gradient(45deg, #00b09b, #96c93d); }
    .card-title { margin-top: 0; margin-bottom: 15px; font-size: 1.4rem; color: #ffffff; }
    .whatsapp-btn {
        display: block; text-align: center; background-color: #25D366; color: white !important;
        padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 15px;
        transition: background-color 0.3s;
    }
    .whatsapp-btn:hover { background-color: #128C7E; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ לוח שיתוף חפצים")
st.markdown("<p style='font-size: 1.2rem; color: #e2e8f0;'>מערכת מתקדמת עם סימולציית בוטים חיה.</p>", unsafe_allow_html=True)
st.divider()

menu = ["🛍️ הלוח המרכזי", "➕ פרסום מודעה חדשה", "🤖 מעבדת בוטים"]
choice = st.sidebar.radio("תפריט פעולות", menu)

if choice == "🛍️ הלוח המרכזי":
    st.sidebar.divider()
    st.sidebar.markdown("### 🔍 סינון מתקדם")
    
    all_items = st.session_state['items']
    categories = ["הכל"] + list(set([item.get('category', '') for item in all_items]))
    locations = ["הכל"] + list(set([item.get('location', '') for item in all_items]))
    
    selected_cat = st.sidebar.selectbox("📂 קטגוריה", categories)
    selected_loc = st.sidebar.selectbox("📍 עיר", locations)
    
    filtered_items = [
        item for item in all_items 
        if (selected_cat == "הכל" or item.get('category') == selected_cat) and 
           (selected_loc == "הכל" or item.get('location') == selected_loc)
    ]
    
    if not filtered_items:
        st.info("לא מצאנו חפצים מתאימים. הלוח ריק? הפעל את הבוטים!")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(filtered_items)):
            col = cols[index % 3] 
            with col:
                phone_display = item.get('phone', 'לא צוין')
                condition_display = item.get('condition', 'לא צוין')
                
                # HTML מעודכן עם כפתור וואטסאפ וירטואלי
                st.markdown(f"""
                <div class="product-card">
                    <h3 class="card-title">{item.get('title', 'ללא שם')}</h3>
                    <div>
                        <span class="badge">{item.get('category', '')}</span>
                        <span class="badge location-badge">📍 {item.get('location', '')}</span>
                        <span class="badge condition-badge">✨ {condition_display}</span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">{item.get('description', '')}</p>
                    <a href="https://wa.me/972{phone_display[1:] if phone_display.startswith('0') else phone_display}" target="_blank" class="whatsapp-btn">
                        💬 וואטסאפ למוסר ({phone_display})
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                if item.get('image'):
                    try:
                        st.image(base64.b64decode(item['image']), use_container_width=True)
                    except:
                        pass
                st.write("") 

elif choice == "➕ פרסום מודעה חדשה":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📝 העלאת חפץ חדש")
        with st.form("add_item_form", clear_on_submit=True):
            title = st.text_input("📌 כותרת", placeholder="לדוגמה: אוסצילוסקופ ישן")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                category = st.selectbox("📂 קטגוריה", ["רהיטים", "מוצרי חשמל", "אלקטרוניקה", "ביגוד", "צעצועים", "שונות"])
            with c2:
                location = st.text_input("📍 עיר איסוף", placeholder="לדוגמה: רחובות")
            with c3:
                condition = st.selectbox("✨ מצב", ["חדש לגמרי", "כמו חדש", "משומש - מצב טוב", "דורש תיקון"])
            
            phone = st.text_input("📱 טלפון ליצירת קשר", placeholder="050-0000000")
            description = st.text_area("📝 תיאור החפץ")
            uploaded_image = st.file_uploader("📸 העלה תמונה", type=["png", "jpg", "jpeg"])
            
            submitted = st.form_submit_button("🚀 פרסם מודעה", type="primary", use_container_width=True)
            
            if submitted and title and location:
                img_str = base64.b64encode(uploaded_image.read()).decode() if uploaded_image else ""
                new_item = {
                    "title": title, "category": category, "location": location, 
                    "condition": condition, "phone": phone, "description": description, "image": img_str
                }
                st.session_state['items'].append(new_item)
                save_items(st.session_state['items'])
                st.success("🎉 פורסם בהצלחה!")

elif choice == "🤖 מעבדת בוטים":
    st.markdown("### ⚙️ סימולציית עומסים ובוטים")
    st.write("כאן תוכל להזריק עשרות מודעות פיקטיביות למערכת בלחיצת כפתור כדי לבחון את העיצוב, הסינון, ומהירות הטעינה.")
    
    col1, col2 = st.columns(2)
    with col1:
        num_to_generate = st.slider("כמה מודעות הבוט יעלה?", 1, 20, 5)
        if st.button("🚀 הפעל בוט העלאות עכשיו", type="primary"):
            new_bots = generate_bot_items(num_to_generate)
            st.session_state['items'].extend(new_bots)
            save_items(st.session_state['items'])
            st.success(f"הבוט העלה {num_to_generate} מודעות חדשות בהצלחה! חזור ללוח המרכזי כדי לראות אותן.")
            
    with col2:
        st.write("פעולות תחזוקה:")
        if st.button("🗑️ מחיקת כל הנתונים בלוח (איפוס מלא)"):
            st.session_state['items'] = []
            save_items([])
            st.warning("הלוח אופס לגמרי.")
