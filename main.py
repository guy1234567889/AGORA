import streamlit as st
import json
import os
import base64
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="אגורה Pro - מתקדם", page_icon="♻️", layout="wide")

DATA_FILE = "agora_data.json"

# מילון קטגוריות ותתי-קטגוריות עשיר
CATEGORIES = {
    "רהיטים": ["ספות וסלון", "שולחנות וכיסאות", "ארונות ומדפים", "ריהוט לחדרי שינה"],
    "מוצרי חשמל": ["מכונות כביסה ומייבשים", "מקררים ומקפיאים", "מוצרי מטבח קטנים", "מזגנים ומאווררים"],
    "אלקטרוניקה ומעבדה": ["ציוד מדידה ו-RF", "בקרים ומיקרו-בקרים (ESP32/Arduino)", "רכיבים ואביזרים", "טלפונים ומחשבים"],
    "ביגוד ואופנה": ["ביגוד גברים", "ביגוד נשים", "הנעלה", "אקססוריז"],
    "צעצועים וילדים": ["משחקי קופסה", "צעצועי התפתחות", "ציוד לתינוקות", "עגלות וטיולונים"],
    "שונות": ["כלי עבודה", "ציוד ספורט", "ספרים ומגזינים", "אחר"]
}

# רשימת ערים בישראל עם קואורדינציות אמיתיות למפה
CITY_COORDS = {
    "רחובות": {"lat": 31.8944, "lon": 34.8094},
    "תל אביב": {"lat": 32.0853, "lon": 34.7818},
    "חיפה": {"lat": 32.7940, "lon": 34.9896},
    "ראשון לציון": {"lat": 31.9730, "lon": 34.7925},
    "ירושלים": {"lat": 31.7683, "lon": 35.2137},
    "נס ציונה": {"lat": 31.9287, "lon": 34.7994},
    "אשדוד": {"lat": 31.8044, "lon": 34.6553},
    "באר שבע": {"lat": 31.2529, "lon": 34.7915}
}

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
            # תיקון אחידות ID לפריטים ישנים
            for item in items:
                if 'id' not in item:
                    item['id'] = str(random.randint(100000, 999999))
                if 'sub_category' not in item:
                    item['sub_category'] = "כללי"
                if 'phone' not in item:
                    item['phone'] = "0501234567"
            return items
    return []

def save_items(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

if 'items' not in st.session_state:
    st.session_state['items'] = load_items()
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []

def generate_bot_items(num_items=10):
    bot_users = [
        {"name": "גיא_קדוש", "karma": 480, "verified": True},
        {"name": "ליאת_מנהלת", "karma": 350, "verified": True},
        {"name": "שירה_קליניקה", "karma": 190, "verified": False},
        {"name": "אלכס_מהנדס", "karma": 75, "verified": True}
    ]
    
    new_bot_items = []
    for _ in range(num_items):
        cat = random.choice(list(CATEGORIES.keys()))
        sub_cat = random.choice(CATEGORIES[cat])
        city = random.choice(list(CITY_COORDS.keys()))
        user = random.choice(bot_users)
        is_req = random.choice([True, False])
        
        new_bot_items.append({
            "id": str(random.randint(100000, 999999)),
            "type": "request" if is_req else "giveaway",
            "title": f"{sub_cat} במצב מצוין" if not is_req else f"מחפש בדחיפות {sub_cat}",
            "category": cat,
            "sub_category": sub_cat,
            "location": city,
            "lat": CITY_COORDS[city]["lat"] + random.uniform(-0.01, 0.01),
            "lon": CITY_COORDS[city]["lon"] + random.uniform(-0.01, 0.01),
            "condition": random.choice(["חדש לגמרי", "כמו חדש", "משומש - מצב טוב"]),
            "description": "הועלה אוטומטי מהמערכת. איסוף נוח, גמיש בשעות הערב.",
            "phone": f"05{random.randint(2,9)}{random.randint(1000000,9999999)}",
            "image": "", # תמונת דמה ויזואלית תטופל בתצוגה
            "status": "available",
            "views": random.randint(10, 250),
            "owner": user,
            "is_bot": True
        })
    return new_bot_items

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #090d16, #111827, #1e1b4b, #030712);
        background-size: 400% 400%; animation: gradientBG 20s ease infinite;
    }
    @keyframes gradientBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    header {background-color: transparent !important;}
    .stApp, .stMarkdown, p, div, h1, h2, h3, span { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .product-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px); border-radius: 16px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s ease, border-color 0.2s; position: relative;
    }
    .product-card:hover { border-color: #3b82f6; transform: translateY(-4px); }
    
    .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; background: rgba(59, 130, 246, 0.2); color: #93c5fd; font-size: 0.75rem; margin-left: 6px; border: 1px solid rgba(59, 130, 246, 0.4); }
    .hot-badge { background: linear-gradient(45deg, #ef4444, #f97316); color: white; border: none; font-weight: bold; }
    
    .user-info { font-size: 0.8rem; color: #94a3b8; display: flex; align-items: center; gap: 5px; margin-bottom: 8px; }
    .whatsapp-btn {
        display: block; text-align: center; background-color: #25D366; color: white !important;
        padding: 8px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; font-size: 0.9rem;
    }
    .whatsapp-btn:hover { background-color: #128C7E; }
    </style>
""", unsafe_allow_html=True)

st.title("♻️ אגורה Pro - פלטפורמת שיתוף חכמה")
st.divider()

menu = ["🛍️ לוח פריטים למסירה", "🗺️ מפה ארצית (יד 2 Style)", "🙏 לוח דרושים", "⭐ מועדפים", "➕ פרסם מודעה", "🤖 מעבדה"]
choice = st.sidebar.radio("ניווט ראשי", menu)

def render_card(item):
    owner = item.get('owner', {"name": "משתמש", "karma": 10, "verified": True})
    verified_icon = "✔️" if owner.get('verified') else ""
    views = item.get('views', 15)
    hot_tag = '<span class="badge hot-badge">🔥 מבוקש</span>' if views > 100 else ""
    phone = item.get('phone', '0501234567')
    
    # תמונת דמה ויזואלית לפי קטגוריה אם אין תמונה אמיתית
    img_html = f"""<div style="background: linear-gradient(135deg, #1e293b, #0f172a); height: 140px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 1.1rem; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.05);">
        📷 תמונת המחשה ({item.get('sub_category', 'כללי')})
    </div>"""
    if item.get('image'):
        try:
            img_html = f"<img src='data:image/png;base64,{item.get('image')}' style='width:100%; height:140px; object-fit:cover; border-radius:10px; margin-bottom:12px;'/>"
        except:
            pass

    card_html = f"""<div class="product-card">
{img_html}
<div class="user-info">
👤 {owner.get('name')} <span style="color:#fbbf24;">⭐ {owner.get('karma')}</span> <span style="color:#38bdf8;">{verified_icon}</span>
</div>
<h3 style="margin: 0 0 8px 0; color: #f8fafc; font-size: 1.2rem;">{item.get('title')}</h3>
<div style="margin-bottom: 8px;">
{hot_tag}
<span class="badge">{item.get('sub_category', item.get('category'))}</span>
<span class="badge" style="background:rgba(16, 185, 129, 0.2); color:#6ee7b7; border-color:rgba(16, 185, 129, 0.4);">📍 {item.get('location')}</span>
</div>
<p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 15px; height: 40px; overflow: hidden;">{item.get('description')}</p>
<div style="font-size: 0.75rem; color: #64748b; margin-bottom: 10px;">👁️ {views} צפיות</div>
<a href="https://wa.me/972{phone[1:] if phone.startswith('0') else phone}" target="_blank" class="whatsapp-btn">
💬 פנה בוואטסאפ ({phone})
</a>
</div>"""
    st.markdown(card_html, unsafe_allow_html=True)

if choice == "🛍️ לוח פריטים למסירה":
    st.subheader("לוח פריטים למסירה ארצי")
    
    # סרגלי סינון מתקדמים לפי קטגוריות ותתי קטגוריות
    c1, c2 = st.columns(2)
    with c1:
        selected_main_cat = st.selectbox("בחר קטגוריה ראשית", ["הכל"] + list(CATEGORIES.keys()))
    with c2:
        sub_options = ["הכל"]
        if selected_main_cat != "הכל":
            sub_options += CATEGORIES[selected_main_cat]
        selected_sub_cat = st.selectbox("בחר תת-קטגוריה", sub_options)
        
    all_items = [i for i in st.session_state['items'] if i.get('type', 'giveaway') == 'giveaway']
    
    if selected_main_cat != "הכל":
        all_items = [i for i in all_items if i.get('category') == selected_main_cat]
    if selected_sub_cat != "הכל":
        all_items = [i for i in all_items if i.get('sub_category') == selected_sub_cat]
        
    if not all_items:
        st.info("אין פריטים תחת הסינון הזה. נסה להיכנס למעבדה ולייצר נתונים!")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(all_items)):
            with cols[index % 3]:
                render_card(item)
                if st.button("❤️ שמור למועדפים", key=f"fav_board_{item['id']}"):
                    if item not in st.session_state['favorites']:
                        st.session_state['favorites'].append(item)
                        st.toast("נוסף למועדפים בהצלחה!")

elif choice == "🗺️ מפה ארצית (יד 2 Style)":
    st.subheader("מפת פריטים ארצית")
    st.write("צפה במיקום המדויק של החפצים הפעילים ברחבי הארץ:")
    
    map_data = []
    for item in st.session_state['items']:
        city = item.get('location', 'תל אביב')
        coords = CITY_COORDS.get(city, {"lat": 32.0853, "lon": 34.7818})
        map_data.append({
            "lat": coords["lat"] + random.uniform(-0.005, 0.005),
            "lon": coords["lon"] + random.uniform(-0.005, 0.005),
            "title": item.get('title')
        })
        
    if map_data:
        df_map = pd.DataFrame(map_data)
        st.map(df_map, latitude="lat", longitude="lon", size=30, color="#3b82f6")
    else:
        st.info("אין מספיק נתונים להצגה על המפה.")

elif choice == "🙏 לוח דרושים":
    st.subheader("לוח בקשות ודרושים")
    requests_items = [i for i in st.session_state['items'] if i.get('type') == 'request']
    if not requests_items:
        st.info("אין בקשות פעילות כרגע.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(requests_items)):
            with cols[index % 3]:
                render_card(item)

elif choice == "⭐ מועדפים":
    st.subheader("הפריטים ששמרת")
    if not st.session_state['favorites']:
        st.info("עדיין אין לך מועדפים.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(st.session_state['favorites']):
            with cols[index % 3]:
                render_card(item)
                if st.button("❌ הסר מהמועדפים", key=f"rem_{item['id']}"):
                    st.session_state['favorites'].remove(item)
                    st.rerun()

elif choice == "➕ פרסם מודעה":
    st.subheader("פרסום פריט חדש למערכת")
    with st.form("new_ad_form", clear_on_submit=True):
        ad_type = st.radio("סוג מודעה", ["מסירה (Giveaway)", "בקשה (Request)"])
        title = st.text_input("כותרת הפריט")
        
        c1, c2 = st.columns(2)
        with c1:
            main_cat = st.selectbox("קטגוריה ראשית", list(CATEGORIES.keys()))
        with c2:
            sub_cat = st.selectbox("תת-קטגוריה", CATEGORIES[main_cat])
            
        city = st.selectbox("עיר איסוף", list(CITY_COORDS.keys()))
        phone = st.text_input("מספר טלפון לוואטסאפ", value="0500000000")
        desc = st.text_area("תיאור מצב החפץ")
        uploaded_img = st.file_uploader("העלה תמונה אמיתית", type=["png", "jpg", "jpeg"])
        
        if st.form_submit_button("פרסם עכשיו", type="primary") and title:
            img_str = base64.b64encode(uploaded_img.read()).decode() if uploaded_img else ""
            coords = CITY_COORDS.get(city, {"lat": 32.0853, "lon": 34.7818})
            
            new_item = {
                "id": str(random.randint(100000, 999999)),
                "type": "request" if "בקשה" in ad_type else "giveaway",
                "title": title,
                "category": main_cat,
                "sub_category": sub_cat,
                "location": city,
                "lat": coords["lat"],
                "lon": coords["lon"],
                "description": desc,
                "phone": phone,
                "image": img_str,
                "status": "available",
                "views": 1,
                "owner": {"name": "אני", "karma": 50, "verified": True}
            }
            st.session_state['items'].append(new_item)
            save_items(st.session_state['items'])
            st.success("המודעה פורסמה בהצלחה!")

elif choice == "🤖 מעבדה":
    st.subheader("מעבדת בוטים וסימולציה")
    if st.button("🚀 הפעל בוט יצירת נתונים (15 פריטים עם תמונות ומיקומים)", type="primary"):
        new_bots = generate_bot_items(15)
        st.session_state['items'].extend(new_bots)
        save_items(st.session_state['items'])
        st.success("נוספו 15 פריטים חדשים עם ערים, קטגוריות ותתי-קטגוריות מפורטות!")
    if st.button("🗑️ איפוס מלא"):
        st.session_state['items'] = []
        st.session_state['favorites'] = []
        save_items([])
        st.warning("הכל אופס.")
