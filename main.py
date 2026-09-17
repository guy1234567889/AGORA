import streamlit as st
import json
import os
import base64

# הגדרות עמוד
st.set_page_config(page_title="פרויקט אגורה", layout="centered")

DATA_FILE = "agora_data.json"

# פונקציות לטעינה ושמירה של נתונים (תחליף לדאטה-בייס)
def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

# טעינת הנתונים לזיכרון של Streamlit
if 'items' not in st.session_state:
    st.session_state['items'] = load_items()

st.title("♻️ פרויקט אגורה - שיתוף חפצים")
st.write("ברוכים הבאים ללוח! כאן תוכלו למצוא ולמסור חפצים.")
st.divider()

# תפריט ניווט
menu = ["לוח חפצים למסירה", "פרסום חפץ חדש"]
choice = st.sidebar.radio("ניווט", menu)

if choice == "לוח חפצים למסירה":
    st.sidebar.divider()
    st.sidebar.subheader("🔍 סינון מודעות")
    
    all_items = st.session_state['items']
    
    # חילוץ קטגוריות וערים קיימות למנוע הסינון
    categories = ["הכל"] + list(set([item['category'] for item in all_items]))
    locations = ["הכל"] + list(set([item['location'] for item in all_items]))
    
    selected_cat = st.sidebar.selectbox("סנן לפי קטגוריה", categories)
    selected_loc = st.sidebar.selectbox("סנן לפי עיר", locations)
    
    st.subheader("חפצים שמחכים לבית חדש")
    
    # הפעלת הסינון
    filtered_items = [
        item for item in all_items 
        if (selected_cat == "הכל" or item['category'] == selected_cat) and 
           (selected_loc == "הכל" or item['location'] == selected_loc)
    ]
    
    if not filtered_items:
        st.info("לא נמצאו חפצים התואמים לחיפוש שלך. נסה לשנות את הסינון.")
    else:
        # תצוגת המודעות
        for item in reversed(filtered_items):
            with st.container():
                st.write(f"### {item['title']}")
                st.write(f"**קטגוריה:** {item['category']} | **עיר איסוף:** {item['location']}")
                st.write(f"**תיאור:** {item['description']}")
                
                # הצגת תמונה אם קיימת
                if item.get('image'):
                    try:
                        st.image(base64.b64decode(item['image']), use_container_width=True)
                    except:
                        pass
                
                st.button("שלח הודעה למוסר", key=f"btn_{item['title']}_{item['location']}_{item.get('description', '')[:5]}")
                st.divider()

elif choice == "פרסום חפץ חדש":
    st.subheader("פרסם חפץ למסירה")
    
    with st.form("add_item_form"):
        title = st.text_input("מה אתה מוסר? (למשל: ספה תלת מושבית)")
        category = st.selectbox("קטגוריה", ["רהיטים", "מוצרי חשמל", "ביגוד", "צעצועים", "שונות"])
        location = st.text_input("עיר איסוף (למשל: רחובות)")
        description = st.text_area("תיאור מצב החפץ והערות נוספות")
        uploaded_image = st.file_uploader("העלה תמונה (אופציונלי)", type=["png", "jpg", "jpeg"])
        
        submitted = st.form_submit_button("פרסם בלוח")
        
        if submitted:
            if title and location:
                img_str = ""
                # המרת התמונה לטקסט כדי לשמור אותה בקובץ הנתונים
                if uploaded_image:
                    img_str = base64.b64encode(uploaded_image.read()).decode()
                    
                new_item = {
                    "title": title,
                    "category": category,
                    "location": location,
                    "description": description,
                    "image": img_str
                }
                
                # עדכון הזיכרון ושמירה לקובץ
                st.session_state['items'].append(new_item)
                save_items(st.session_state['items'])
                
                st.success("החפץ פורסם ונשמר בהצלחה! עבור ל'לוח חפצים למסירה' כדי לראות אותו.")
            else:
                st.error("אנא מלא לפחות את כותרת החפץ ועיר האיסוף.")
