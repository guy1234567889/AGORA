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

# הזרקת קוד עיצוב (CSS) שדורס את העיצוב הרגיל של Streamlit
st.markdown("""
    <style>
    /* יישור לימין של כל האפליקציה */
    .stApp, .stMarkdown, p, div, h1, h2, h3 {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* עיצוב כרטיסיות המוצרים */
    .product-card {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #333;
        height: 100%;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.5);
        border-color: #4CAF50;
    }
    
    /* תגיות צבעוניות לקטגוריה ועיר */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-size: 0.8rem;
        margin-left: 5px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .location-badge {
        background-color: #2196F3;
    }
    
    /* עיצוב כותרות בתוך הכרטיסיה */
    .card-title {
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 1.3rem;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ לוח שיתוף חפצים")
st.markdown("<p style='font-size: 1.2rem; color: #888;'>פלטפורמה מודרנית למסירה ומציאת חפצים שווים.</p>", unsafe_allow_html=True)
st.divider()

# תפריט ניווט מעוצב בצד
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
        # יצירת מבנה גריד של 3 עמודות
        cols = st.columns(3)
        
        for index, item in enumerate(reversed(filtered_items)):
            col = cols[index % 3] # חלוקה שווה של המודעות בין 3 העמודות
            
            with col:
                # הזרקת ה-HTML של הכרטיסיה לתוך העמודה
                st.markdown(f"""
                <div class="product-card">
                    <h3 class="card-title">{item['title']}</h3>
                    <div>
                        <span class="badge">{item['category']}</span>
                        <span class="badge location-badge">📍 {item['location']}</span>
                    </div>
                    <p style="color: #bbb; font-size: 0.95rem;">{item['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # הצגת התמונה מתחת לטקסט
                if item.get('image'):
                    try:
                        st.image(base64.b64decode(item['image']), use_container_width=True)
                    except:
                        pass
                
                # כפתור ברוחב מלא בתוך העמודה
                st.button("💬 צור קשר", key=f"btn_{index}_{item['title']}", use_container_width=True)
                st.write("") # מרווח נשימה בין כרטיסיות

elif choice == "➕ פרסום מודעה חדשה":
    # מרכוז הטופס כדי שלא יימרח על כל המסך
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📝 העלאת חפץ חדש")
        # clear_on_submit מנקה את הטופס אוטומטית אחרי השליחה
        with st.form("add_item_form", clear_on_submit=True):
            title = st.text_input("📌 כותרת (מה אתה מוסר?)", placeholder="לדוגמה: ספה תלת מושבית במצב מצוין")
            
            c1, c2 = st.columns(2)
            with c1:
                category = st.selectbox("📂 קטגוריה", ["רהיטים", "מוצרי חשמל", "ביגוד", "צעצועים", "שונות"])
            with c2:
                location = st.text_input("📍 עיר איסוף", placeholder="לדוגמה: רחובות")
                
            description = st.text_area("📝 תיאור החפץ", placeholder="ספר על מצב החפץ, מתי אפשר לאסוף וכו'...")
            uploaded_image = st.file_uploader("📸 העלה תמונה (מומלץ!)", type=["png", "jpg", "jpeg"])
            
            # כפתור שליחה מודגש
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
