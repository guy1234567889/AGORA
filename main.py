import streamlit as st
import json
import os
import base64
import random
from datetime import datetime

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

def generate_bot_items(num_items=5):
    titles = [
        "רכיבי ארדואינו ומטריצות", "ספה תלת מושבית שחורה", "אייפון 12 (מסך שבור)", 
        "אופניים חשמליים", "קופסת צעצועים לגיל 3", "ספרים בנושא תכנות ב-Python", 
        "ראוטר ישן של בזק", "מכונת כביסה פתח עליון", "שולחן כתיבה מאיקאה", "אוסף כבלים RF ומתאמים"
    ]
    categories = ["רהיטים", "מוצרי חשמל", "ביגוד", "צעצועים", "שונות", "אלקטרוניקה"]
    locations = ["רחובות", "תל אביב", "חיפה", "ראשון לציון", "ירושלים", "נס ציונה", "אשדוד"]
    conditions = ["חדש לגמרי", "כמו חדש", "משומש - מצב טוב", "דורש תיקון"]
    
    new_bot_items = []
    for _ in range(num_items):
        new_bot_items.append({
            "id": str(random.randint(10000, 99999)),
            "title": random.choice(titles),
            "category": random.choice(categories),
            "location": random.choice(locations),
            "condition": random.choice(conditions),
            "description": "הפריט הועלה על ידי הבוט האוטומטי. כל הקודם זוכה!",
            "phone": f"05{random.randint(2,9)}{random.randint(1000000,9999999)}",
            "image": "",
            "status": "available",
            "comments": [],
            "is_bot": True
        })
    return new_bot_items

def simulate_bot_interactions():
    available_items = [item for item in st.session_state['items'] if item.get('status') != 'claimed']
    if not available_items:
        return 0
        
    interactions_count = random.randint(1, min(5, len(available_items)))
    selected_items = random.sample(available_items, interactions_count)
    
    bot_names = ["בוט_דני", "בוט_יעל", "בוט_משה", "בוט_שירה", "בוט_אלכס"]
    messages = [
        "היי, זה עדיין רלוונטי? אני יכול לבוא לאסוף היום בערב.",
        "שומר לי? אני אגיע מחר על הבוקר.",
        "רלוונטי? שלחתי לך הודעה בוואטסאפ.",
        "איזה יופי! בדיוק חיפשתי כזה. אפשר לאסוף בסופש?"
    ]
    
    for item in selected_items:
        if 'comments' not in item:
            item['comments'] = []
            
        buyer = random.choice(bot_names)
        msg = random.choice(messages)
        
        item['comments'].append({"user": buyer, "text": msg, "time": datetime.now().strftime("%H:%M")})
        
        if random.choice([True, False]):
            item['comments'].append({
                "user": "מוסר החפץ", 
                "text": "בכיף, שומר לך. דבר איתי כשאתה באזור.", 
                "time": datetime.now().strftime("%H:%M")
            })
            item['status'] = 'claimed'
            
    save_items(st.session_state['items'])
    return interactions_count

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #334155, #0f172a);
        background-size: 400% 400%; animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    header {background-color: transparent !important;}
    .stApp, .stMarkdown, p, div, h1, h2, h3 { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .product-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); border-radius: 16px; padding: 22px; margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s ease;
    }
    .product-card.claimed { border-color: rgba(239, 68, 68, 0.5); opacity: 0.8; }
    
    .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; background: linear-gradient(45deg, #FF512F, #DD2476); color: white; font-size: 0.8rem; margin-left: 6px; margin-bottom: 10px; font-weight: bold; }
    .location-badge { background: linear-gradient(45deg, #1CB5E0, #000851); }
    .claimed-badge { background: #ef4444 !important; box-shadow: 0 0 10px #ef4444; }
    
    .card-title { margin-top: 0; margin-bottom: 15px; font-size: 1.4rem; color: #ffffff; }
    .chat-bubble { background: rgba(0,0,0,0.3); padding: 8px 12px; border-radius: 12px; margin-bottom: 5px; font-size: 0.85rem; border-right: 3px solid #2196F3; }
    .chat-bubble.owner { border-right: 3px solid #4CAF50; background: rgba(76, 175, 80, 0.1); }
    </style>
""", unsafe_allow_html=True)

st.title("✨ לוח שיתוף חפצים")
st.divider()

menu = ["🛍️ הלוח המרכזי", "➕ פרסום מודעה חדשה", "🤖 מעבדת בוטים"]
choice = st.sidebar.radio("תפריט פעולות", menu)

if choice == "🛍️ הלוח המרכזי":
    all_items = st.session_state['items']
    cols = st.columns(3)
    
    for index, item in enumerate(reversed(all_items)):
        col = cols[index % 3] 
        with col:
            is_claimed = item.get('status') == 'claimed'
            card_class = "product-card claimed" if is_claimed else "product-card"
            status_badge = '<span class="badge claimed-badge">❌ נמסר</span>' if is_claimed else ""
            
            chat_html = ""
            for comment in item.get('comments', []):
                bubble_class = "chat-bubble owner" if comment['user'] == "מוסר החפץ" else "chat-bubble"
                chat_html += f"<div class='{bubble_class}'><strong>{comment['user']}:</strong> {comment['text']} <span style='color:#888; font-size:0.7rem;'>({comment['time']})</span></div>"
                
            # HTML String exactly left-aligned to avoid Markdown Code-Block interpretation
            card_html = f"""<div class="{card_class}">
<h3 class="card-title">{item.get('title', 'ללא שם')}</h3>
<div>
<span class="badge">{item.get('category', '')}</span>
<span class="badge location-badge">📍 {item.get('location', '')}</span>
{status_badge}
</div>
<p style="color: #cbd5e1; font-size: 0.95rem;">{item.get('description', '')}</p>
<div style="margin-top: 15px;">
{chat_html}
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)
            st.write("") 

elif choice == "➕ פרסום מודעה חדשה":
    with st.form("add_item_form", clear_on_submit=True):
        title = st.text_input("📌 כותרת")
        category = st.selectbox("📂 קטגוריה", ["רהיטים", "מוצרי חשמל", "אלקטרוניקה", "ביגוד", "צעצועים", "שונות"])
        location = st.text_input("📍 עיר איסוף", placeholder="לדוגמה: רחובות")
        description = st.text_area("📝 תיאור החפץ")
        
        if st.form_submit_button("🚀 פרסם מודעה", type="primary") and title and location:
            new_item = {
                "id": str(random.randint(10000, 99999)),
                "title": title, "category": category, "location": location, 
                "description": description, "status": "available", "comments": []
            }
            st.session_state['items'].append(new_item)
            save_items(st.session_state['items'])
            st.success("🎉 פורסם בהצלחה!")

elif choice == "🤖 מעבדת בוטים":
    st.markdown("### ⚙️ מעבדת בוטים - סימולציה חיה")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### יצירת מודעות")
        if st.button("🚀 בוט העלאת מוצרים (מייצר 5 מודעות)"):
            new_bots = generate_bot_items(5)
            st.session_state['items'].extend(new_bots)
            save_items(st.session_state['items'])
            st.success("הבוטים העלו 5 מודעות חדשות.")
            
    with col2:
        st.markdown("#### סימולציית תקשורת")
        st.write("מפעיל בוטים 'קונים' שיסרקו את הלוח, ישאירו תגובות לפריטים אקראיים, וחלקם יסגרו עסקה (יסמנו כנמסר).")
        if st.button("💬 בוט תקשורת (משא ומתן לייב)"):
            interactions = simulate_bot_interactions()
            if interactions > 0:
                st.success(f"בוצעה תקשורת על {interactions} פריטים. חזור ללוח לראות את הצ'אטים!")
            else:
                st.warning("אין פריטים פנויים בלוח לנהל עליהם משא ומתן.")
