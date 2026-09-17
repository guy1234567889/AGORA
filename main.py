import streamlit as st
import json
import os
import base64
import random
import pandas as pd

st.set_page_config(page_title="אגורה Pro", page_icon="♻️", layout="wide")

DATA_FILE = "agora_data.json"

CATEGORIES = {
    "רהיטים": ["ספות וסלון", "שולחנות וכיסאות", "ארונות ומדפים", "ריהוט לחדרי שינה"],
    "מוצרי חשמל": ["מכונות כביסה ומייבשים", "מקררים ומקפיאים", "מוצרי מטבח קטנים", "מזגנים ומאווררים"],
    "אלקטרוניקה ומעבדה": ["ציוד מדידה ו-RF", "בקרים ומיקרו-בקרים (ESP32/Arduino)", "רכיבים ואביזרים", "טלפונים ומחשבים"],
    "ביגוד ואופנה": ["ביגוד גברים", "ביגוד נשים", "הנעלה", "אקססוריז"],
    "צעצועים וילדים": ["משחקי קופסה", "צעצועי התפתחות", "ציוד לתינוקות", "עגלות וטיולונים"],
    "שונות": ["כלי עבודה", "ציוד ספורט", "ספרים ומגזינים", "אחר"]
}

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

CATEGORY_IMAGES = {
    "רהיטים": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80",
    "מוצרי חשמל": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=80",
    "אלקטרוניקה ומעבדה": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80",
    "ביגוד ואופנה": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=600&q=80",
    "צעצועים וילדים": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?auto=format&fit=crop&w=600&q=80",
    "שונות": "https://images.unsplash.com/photo-1584467735811-628b0fd4603d?auto=format&fit=crop&w=600&q=80"
}

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
            for idx, item in enumerate(items):
                if 'id' not in item or not item['id']:
                    item['id'] = f"item_{idx}_{random.randint(1000,9999)}"
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

def generate_bot_items():
    bot_users = [
        {"name": "גיא_קדוש", "karma": 480, "verified": True},
        {"name": "ליאת_מנהלת", "karma": 350, "verified": True},
        {"name": "שירה_קליניקה", "karma": 190, "verified": False},
        {"name": "אלכס_מהנדס", "karma": 75, "verified": True}
    ]
    
    new_bot_items = []
    # ייצור פריט אחד לפחות מכל תת-קטגוריה כדי להבטיח כיסוי מלא של כל המערכת
    for cat, sub_list in CATEGORIES.items():
        for sub_cat in sub_list:
            city = random.choice(list(CITY_COORDS.keys()))
            user = random.choice(bot_users)
            is_req = random.choice([True, False, False])
            
            new_bot_items.append({
                "id": f"bot_{random.randint(100000, 999999)}",
                "type": "request" if is_req else "giveaway",
                "title": f"{sub_cat} במצב מעולה" if not is_req else f"דרוש בדחיפות {sub_cat}",
                "category": cat,
                "sub_category": sub_cat,
                "location": city,
                "lat": CITY_COORDS[city]["lat"] + random.uniform(-0.01, 0.01),
                "lon": CITY_COORDS[city]["lon"] + random.uniform(-0.01, 0.01),
                "condition": random.choice(["חדש לגמרי", "כמו חדש", "משומש"]),
                "description": f"פריט איכותי מקטגוריית {cat} ({sub_cat}). איסוף נוח בתיאום.",
                "phone": f"05{random.randint(2,9)}{random.randint(1000000,9999999)}",
                "image_url": CATEGORY_IMAGES.get(cat, ""),
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
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px); border-radius: 16px; padding: 18px; margin-bottom: 20px;
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

menu_options = [
    "🛍️ לוח פריטים למסירה", 
    "🗺️ מפה ארצית וחפצים לפי עיר", 
    "🙏 פריטים דרושים", 
    "❤️ פריטים שמעניינים אותי", 
    "➕ פרסם מודעה", 
    "🤖 מעבדה"
]
choice = st.selectbox("🧭 תפריט ניווט מהיר", menu_options, label_visibility="collapsed")
st.divider()

def render_card(item, unique_key_prefix):
    owner = item.get('owner', {"name": "משתמש", "karma": 10, "verified": True})
    verified_icon = "✔️" if owner.get('verified') else ""
    views = item.get('views', 15)
    hot_tag = '<span class="badge hot-badge">🔥 מבוקש</span>' if views > 100 else ""
    phone = item.get('phone', '0501234567')
    
    img_src = item.get('image_url') or CATEGORY_IMAGES.get(item.get('category'), "https://images.unsplash.com/photo-1584467735811-628b0fd4603d?auto=format&fit=crop&w=600&q=80")
    if item.get('image'):
        try:
            img_src = f"data:image/png;base64,{item.get('image')}"
        except:
            pass

    card_html = f"""<div class="product-card">
<img src="{img_src}" style="width:100%; height:150px; object-fit:cover; border-radius:10px; margin-bottom:12px; border:1px solid rgba(255,255,255,0.1);"/>
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
    
    # כפתור שמירה בטוח עם מפתח ייחודי לחלוטין
    item_id = item.get('id', str(random.randint(1000,9999)))
    if st.button("❤️ שמור", key=f"fav_{unique_key_prefix}_{item_id}"):
        if item not in st.session_state['favorites']:
            st.session_state['favorites'].append(item)
            st.toast("נוסף לפריטים שמעניינים אותי!")

if choice == "🛍️ לוח פריטים למסירה":
    st.subheader("🛍️ לוח פריטים למסירה")
    
    c1, c2 = st.columns(2)
    with c1:
        selected_main_cat = st.selectbox("📂 בחר קטגוריה ראשית", ["הכל"] + list(CATEGORIES.keys()))
    with c2:
        sub_options = ["הכל"]
        if selected_main_cat != "הכל":
            sub_options += CATEGORIES[selected_main_cat]
        selected_sub_cat = st.selectbox("📂 בחר תת-קטגוריה", sub_options)
        
    all_items = [i for i in st.session_state['items'] if i.get('type', 'giveaway') == 'giveaway']
    
    if selected_main_cat != "הכל":
        all_items = [i for i in all_items if i.get('category') == selected_main_cat]
    if selected_sub_cat != "הכל":
        all_items = [i for i in all_items if i.get('sub_category') == selected_sub_cat]
        
    if not all_items:
        st.info("אין פריטים תחת הסינון הזה. כנס למעבדה ולייצר נתונים!")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(all_items)):
            with cols[index % 3]:
                render_card(item, "board")

elif choice == "🗺️ מפה ארצית וחפצים לפי עיר":
    st.subheader("🗺️ מפה ארצית וסינון לפי עיר")
    st.write("בחר עיר מהרשימה כדי לראות בדיוק אילו פריטים מחכים לך באזור:")
    
    selected_city_filter = st.selectbox("בחר עיר לצפייה בפריטים", ["הכל"] + list(CITY_COORDS.keys()))
    
    map_data = []
    for item in st.session_state['items']:
        city = item.get('location', 'תל אביב')
        coords = CITY_COORDS.get(city, {"lat": 32.0853, "lon": 34.7818})
        map_data.append({
            "lat": coords["lat"] + random.uniform(-0.003, 0.003),
            "lon": coords["lon"] + random.uniform(-0.003, 0.003),
            "name": item.get('title'),
            "city": city
        })
        
    if map_data:
        st.map(pd.DataFrame(map_data), latitude="lat", longitude="lon", size=40, color="#3b82f6")
    
    st.divider()
    st.subheader(f"פריטים בעיר: {selected_city_filter}")
    city_items = st.session_state['items'] if selected_city_filter == "הכל" else [i for i in st.session_state['items'] if i.get('location'] == selected_city_filter]
    
    if not city_items:
        st.info("אין פריטים רשומים בעיר זו כרגע.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(city_items)):
            with cols[index % 3]:
                render_card(item, "city_map")

elif choice == "🙏 פריטים דרושים":
    st.subheader("🙏 פריטים דרושים ובקשות מהקהילה")
    requests_items = [i for i in st.session_state['items'] if i.get('type') == 'request']
    if not requests_items:
        st.info("אין בקשות פעילות כרגע.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(requests_items)):
            with cols[index % 3]:
                render_card(item, "requests")

elif choice == "❤️ פריטים שמעניינים אותי":
    st.subheader("❤️ פריטים שמעניינים אותי")
    if not st.session_state['favorites']:
        st.info("עדיין לא שמרת פריטים.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(st.session_state['favorites']):
            with cols[index % 3]:
                render_card(item, "favs")
                if st.button("❌ הסר", key=f"rem_{item.get('id', random.randint(1000,9999))}"):
                    st.session_state['favorites'].remove(item)
                    st.rerun()

elif choice == "➕ פרסם מודעה":
    st.subheader("➕ פרסום פריט חדש למערכת")
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
        uploaded_img = st.file_uploader("העלה תמונה אמיתית (אופציונלי)", type=["png", "jpg", "jpeg"])
        
        if st.form_submit_button("פרסם עכשיו", type="primary") and title:
            img_str = base64.b64encode(uploaded_img.read()).decode() if uploaded_img else ""
            coords = CITY_COORDS.get(city, {"lat": 32.0853, "lon": 34.7818})
            
            new_item = {
                "id": f"user_{random.randint(100000, 999999)}",
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
                "image_url": CATEGORY_IMAGES.get(main_cat, ""),
                "status": "available",
                "views": 1,
                "owner": {"name": "אני", "karma": 50, "verified": True}
            }
            st.session_state['items'].append(new_item)
            save_items(st.session_state['items'])
            st.success("המודעה פורסמה בהצלחה!")

elif choice == "🤖 מעבדה":
    st.subheader("🤖 מעבדת בוטים ונתונים")
    if st.button("🚀 טען פריטים מכל הקטגוריות ותתי-הקטגוריות", type="primary"):
        new_bots = generate_bot_items()
        st.session_state['items'].extend(new_bots)
        save_items(st.session_state['items'])
        st.success(f"נוספו בהצלחה {len(new_bots)} פריטים המכסים את כל הקטגוריות ותתי-הקטגוריות במערכת!")
    if st.button("🗑️ איפוס מסד נתונים"):
        st.session_state['items'] = []
        st.session_state['favorites'] = []
        save_items([])
        st.warning("הכל אופס.")
