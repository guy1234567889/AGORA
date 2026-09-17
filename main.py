import streamlit as st
import json
import os
import base64
import random
from datetime import datetime

st.set_page_config(page_title="אגורה Pro", page_icon="♻️", layout="wide")

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
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []

def generate_bot_items(num_items=10):
    titles_giveaway = [
        "רכיבי מיתוג RF ותואמי עכבה", "ספה תלת מושבית שחורה", "אייפון 13 פרו (ללא שריטות)", 
        "בקר ESP32 עם מודול Wi-Fi", "צעצועי התפתחות לילדים", "קוד פייתון לניתוח S-parameters (מודפס)", 
        "ראוטר סלולרי חכם", "מכונת כביסה פתח עליון", "שולחן עבודה מאיקאה", "אוסף כבלים ומתאמים בתדר גבוה"
    ]
    titles_request = [
        "מחפש רכיבי אלקטרוניקה לפרויקט", "דרוש מסך מחשב שעובד", "מחפשת הליכון או ציוד ריצה",
        "למישהו יש חלקי חילוף לרחפן?", "מחפש ספרי לימוד על פיתוח חומרה"
    ]
    categories = ["רהיטים", "מוצרי חשמל", "אלקטרוניקה", "ביגוד", "צעצועים", "שונות", "פיתוח ומעבדה"]
    locations = ["רחובות", "תל אביב", "חיפה", "ראשון לציון", "ירושלים", "נס ציונה", "אשדוד", "בטומי (איסוף מנמל תעופה)"]
    conditions = ["חדש לגמרי", "כמו חדש", "משומש - מצב טוב", "דורש תיקון"]
    bot_users = [
        {"name": "גיא_בוט", "karma": 450, "verified": True},
        {"name": "ליאת_בוט", "karma": 320, "verified": True},
        {"name": "שירה_בוט", "karma": 120, "verified": False},
        {"name": "אלכס_הצייד", "karma": 15, "verified": False}
    ]
    
    new_bot_items = []
    for _ in range(num_items):
        is_request = random.choice([True, False, False]) # 33% chance it's a request
        user = random.choice(bot_users)
        
        new_bot_items.append({
            "id": str(random.randint(100000, 999999)),
            "type": "request" if is_request else "giveaway",
            "title": random.choice(titles_request if is_request else titles_giveaway),
            "category": random.choice(categories),
            "location": random.choice(locations),
            "condition": random.choice(conditions),
            "description": "הועלה אוטומטית ממערכת הבוטים. גמיש בשעות האיסוף.",
            "phone": f"05{random.randint(2,9)}{random.randint(1000000,9999999)}",
            "image": "",
            "status": "available",
            "comments": [],
            "views": random.randint(5, 300),
            "owner": user,
            "is_bot": True
        })
    return new_bot_items

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #0b1120, #172554, #1e1b4b, #0f172a);
        background-size: 400% 400%; animation: gradientBG 20s ease infinite;
    }
    @keyframes gradientBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    header {background-color: transparent !important;}
    .stApp, .stMarkdown, p, div, h1, h2, h3, span { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .product-card {
        background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(16px); border-radius: 16px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4); border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s ease, border-color 0.2s; position: relative;
    }
    .product-card:hover { border-color: #3b82f6; transform: translateY(-5px); }
    .product-card.list-view { display: flex; align-items: center; justify-content: space-between; padding: 15px; }
    .product-card.request-card { border-right: 4px solid #f59e0b; }
    
    .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; background: rgba(59, 130, 246, 0.2); color: #93c5fd; font-size: 0.75rem; margin-left: 6px; border: 1px solid rgba(59, 130, 246, 0.4); }
    .hot-badge { background: linear-gradient(45deg, #ef4444, #f97316); color: white; border: none; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    
    .user-info { font-size: 0.8rem; color: #94a3b8; display: flex; align-items: center; gap: 5px; margin-bottom: 10px; }
    .karma-star { color: #fbbf24; }
    .verified-check { color: #38bdf8; }
    .meta-stats { font-size: 0.75rem; color: #64748b; position: absolute; bottom: 15px; left: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ מערכת אגורה Pro")
st.markdown("<p style='color: #94a3b8;'>הדור הבא של שיתוף חפצים: מוניטין, התראות חכמות, ולוח בקשות.</p>", unsafe_allow_html=True)
st.divider()

menu = ["🛍️ לוח פריטים למסירה", "🙏 לוח דרושים ובקשות", "⭐ המועדפים שלי", "➕ פרסום מודעה חדשה", "🤖 מעבדת אלגוריתמים"]
choice = st.sidebar.radio("ניווט מתקדם", menu)

def render_item_card(item, view_mode="grid"):
    # הזרקת נתוני מוניטין
    owner = item.get('owner', {"name": "אורח", "karma": 0, "verified": False})
    verified_icon = "✔️" if owner.get('verified') else ""
    views = item.get('views', random.randint(1, 50))
    hot_tag = '<span class="badge hot-badge">🔥 מבוקש מאוד</span>' if views > 100 else ""
    req_tag = '<span class="badge" style="background:#f59e0b;color:#fff;">בקשה לחפץ</span>' if item.get('type') == 'request' else ""
    
    card_class = "product-card request-card" if item.get('type') == 'request' else "product-card"
    if view_mode == "list": card_class += " list-view"

    card_html = f"""<div class="{card_class}">
<div>
<div class="user-info">
👤 {owner.get('name')} <span class="karma-star">⭐ {owner.get('karma')}</span> <span class="verified-check">{verified_icon}</span>
</div>
<h3 style="margin: 0 0 10px 0; color: #f8fafc; font-size: 1.3rem;">{item.get('title')}</h3>
<div style="margin-bottom: 10px;">
{hot_tag} {req_tag}
<span class="badge">📂 {item.get('category')}</span>
<span class="badge">📍 {item.get('location')}</span>
</div>
<p style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 25px;">{item.get('description')}</p>
<div class="meta-stats">👁️ {views} צפיות</div>
</div>
</div>"""
    st.markdown(card_html, unsafe_allow_html=True)

if choice in ["🛍️ לוח פריטים למסירה", "🙏 לוח דרושים ובקשות"]:
    is_requests_board = (choice == "🙏 לוח דרושים ובקשות")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        view_mode = st.radio("תצוגה", ["רשת (Grid)", "רשימה (List)"], horizontal=True)
    with col1:
        search_radius = st.slider("📍 רדיוס חיפוש (ק״מ מרחובות והסביבה)", 5, 100, 20)
    
    all_items = st.session_state['items']
    target_type = "request" if is_requests_board else "giveaway"
    filtered_items = [i for i in all_items if i.get('type', 'giveaway') == target_type]
    
    if not filtered_items:
        st.info("הלוח ריק כרגע. הפעל את הבוטים במעבדה כדי למלא אותו בנתונים!")
    else:
        if view_mode == "רשת (Grid)":
            cols = st.columns(3)
            for index, item in enumerate(reversed(filtered_items)):
                with cols[index % 3]:
                    render_item_card(item, "grid")
                    # כפתור מועדפים ווואטסאפ מחוץ ל-HTML כדי לשמור על אינטראקטיביות
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        if st.button("❤️", key=f"fav_{item['id']}"):
                            if item not in st.session_state['favorites']:
                                st.session_state['favorites'].append(item)
                                st.toast("נוסף למועדפים!")
                    with c2:
                        st.button("💬 צור קשר", key=f"contact_{item['id']}", use_container_width=True)
        else:
            for item in reversed(filtered_items):
                render_item_card(item, "list")
                st.button("❤️ שמור למועדפים", key=f"fav_list_{item['id']}")

elif choice == "⭐ המועדפים שלי":
    st.subheader("החפצים ששמרת")
    if not st.session_state['favorites']:
        st.info("עדיין לא שמרת פריטים. חזור ללוח ולחץ על ה-❤️!")
    else:
        cols = st.columns(3)
        for index, item in enumerate(st.session_state['favorites']):
            with cols[index % 3]:
                render_item_card(item, "grid")
                if st.button("❌ הסר", key=f"rem_{item['id']}"):
                    st.session_state['favorites'].remove(item)
                    st.rerun()

elif choice == "➕ פרסום מודעה חדשה":
    with st.form("add_item_form", clear_on_submit=True):
        ad_type = st.radio("סוג המודעה", ["מסירת חפץ (Giveaway)", "בקשת חפץ (Request)"])
        title = st.text_input("📌 כותרת")
        category = st.selectbox("📂 קטגוריה", ["רהיטים", "מוצרי חשמל", "אלקטרוניקה", "ביגוד", "צעצועים", "פיתוח ומעבדה", "שונות"])
        location = st.text_input("📍 עיר איסוף", value="רחובות")
        description = st.text_area("📝 פרטים נוספים")
        
        if st.form_submit_button("🚀 פרסם לאוויר", type="primary") and title:
            new_item = {
                "id": str(random.randint(100000, 999999)),
                "type": "request" if "בקשת" in ad_type else "giveaway",
                "title": title, "category": category, "location": location, 
                "description": description, "status": "available", "views": 0,
                "owner": {"name": "משתמש_אמיתי", "karma": 10, "verified": True}
            }
            st.session_state['items'].append(new_item)
            save_items(st.session_state['items'])
            st.success("🎉 פורסם בהצלחה!")

elif choice == "🤖 מעבדת אלגוריתמים":
    st.markdown("### ⚙️ מנוע הזרקת נתונים מתקדם")
    st.write("מייצר אקולוגיה שלמה: משתמשים עם מוניטין גבוה ונמוך, חפצים למסירה, ובקשות דרושים.")
    
    if st.button("🚀 הפעל סימולציית שוק חיה (מייצר 15 רשומות מגוונות)", type="primary"):
        new_bots = generate_bot_items(15)
        st.session_state['items'].extend(new_bots)
        save_items(st.session_state['items'])
        st.success("המערכת הוצפה בנתונים חדשים! עבור ללוח המסירה או ללוח הדרושים כדי לראות את התוצאות, כולל תגיות אש למודעות ויראליות.")
        
    if st.button("🗑️ איפוס מסד נתונים"):
        st.session_state['items'] = []
        st.session_state['favorites'] = []
        save_items([])
        st.warning("הלוח נוקה.")
