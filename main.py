import streamlit as st

# הגדרות בסיסיות לעמוד
st.set_page_config(page_title="פרויקט אגורה", layout="centered")

# יצירת "מסד נתונים" זמני בזיכרון של האפליקציה לשמירת החפצים
if 'items' not in st.session_state:
    st.session_state['items'] = []

st.title("♻️ פרויקט אגורה - שיתוף חפצים")
st.write("ברוכים הבאים ללוח! כאן תוכלו למצוא חפצים למסירה או לפרסם חפצים שאתם כבר לא צריכים.")

st.divider()

# יצירת תפריט ניווט צדדי
menu = ["לוח חפצים למסירה", "פרסום חפץ חדש"]
choice = st.sidebar.radio("ניווט", menu)

if choice == "לוח חפצים למסירה":
    st.subheader("חפצים שמחכים לבית חדש")
    
    # בדיקה אם יש חפצים להציג
    if len(st.session_state['items']) == 0:
        st.info("עדיין אין חפצים למסירה. תהיה הראשון לפרסם!")
    else:
        # מעבר על כל החפצים והצגתם
        for item in reversed(st.session_state['items']):
            with st.container():
                st.write(f"### {item['title']}")
                st.write(f"**קטגוריה:** {item['category']} | **עיר איסוף:** {item['location']}")
                st.write(f"**תיאור מצב החפץ:** {item['description']}")
                st.button("שלח הודעה למוסר", key=item['title']) # כפתור דמיון ליצירת קשר
                st.divider()

elif choice == "פרסום חפץ חדש":
    st.subheader("פרסם חפץ למסירה")
    
    # טופס להזנת פרטי החפץ
    with st.form("add_item_form"):
        title = st.text_input("מה אתה מוסר? (למשל: ספה תלת מושבית)")
        category = st.selectbox("קטגוריה", ["רהיטים", "מוצרי חשמל", "ביגוד", "שונות"])
        location = st.text_input("עיר איסוף (למשל: רחובות, תל אביב)")
        description = st.text_area("תיאור מצב החפץ והערות נוספות")
        
        submitted = st.form_submit_button("פרסם בלוח")
        
        if submitted:
            if title and location:
                # שמירת הנתונים
                new_item = {
                    "title": title,
                    "category": category,
                    "location": location,
                    "description": description
                }
                st.session_state['items'].append(new_item)
                st.success("החפץ פורסם בהצלחה! עבור ל'לוח חפצים למסירה' כדי לראות אותו.")
            else:
                st.error("אנא מלא לפחות את כותרת החפץ ועיר האיסוף.")
