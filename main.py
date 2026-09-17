import streamlit as st
import json
import os
import base64
import random
import pandas as pd
import folium
from streamlit_folium import st_folium

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

# גבולות גיאוגרפיים אמיתיים (פוליגונים) לערים המרכזיות במקום עיגולים פשוטים
CITY_POLYGONS = {
    "רחובות": [
        [31.918, 34.795], [31.922, 34.812], [31.908, 34.828],
        [31.882, 34.830], [31.866, 34.812], [31.870, 34.788], [31.895, 34.782]
    ],
    "תל אביב": [
        [32.125, 34.770], [32.115, 34.825], [32.045, 34.815],
        [32.015, 34.765], [32.035, 34.742], [32.095, 34.740]
    ],
    "ראשון לציון": [
        [31.995, 34.775], [32.000, 34.815], [31.950, 34.825],
        [31.940, 34.780], [31.965, 34.755]
    ]
}

CATEGORY_IMAGES = {
    "רהיטים": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80",
    "מוצרי חשמל": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=80",
    "אלקטרוניקה ומעבדה": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80",
    "ביגוד ואופנה": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=600&q=80",
    "צעצועים וילדים": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?auto=format&fit=crop&w=600&q=80",
    "שונות": "https://images.unsplash.com/photo-1584467735811-628b0fd4603d?auto=format&fit=crop&w=600&q=80"
}

def generate_all_category_items():
    bot_users = [
        {"name": "גיא_קדוש", "karma": 480, "verified": True},
        {"name": "ליאת_מנהלת", "karma": 350, "verified": True},
        {"name": "שירה_קליניקה", "karma": 190, "verified": False},
        {"name": "אלכס_מהנדס", "karma": 75, "verified": True}
    ]
    
    generated = []
    # ייצור של מספר פריטים לכל תת-קטגוריה כדי להבטיח מאגר עשיר ומלא לחלוטין בכל קטגוריה
    for cat, sub_list in CATEGORIES.items():
        for sub_cat in sub_list:
            for _ in range(2):  # שני פריטים לכל תת-קטגוריה לפחות
                city = random.choice(list(CITY_COORDS.keys()))
                user = random.choice(bot_users)
                is_req = random.choice([True, False, False])
                
                generated.append({
                    "id": f"item_{random.randint(100000, 999999)}",
                    "type": "request" if is_req else "giveaway",
                    "title": f"{sub_cat} איכותי במצב מעולה" if not is_req else f"דרוש בדחיפות: {sub_cat}",
                    "category": cat,
                    "sub_category": sub_cat,
                    "location": city,
                    "lat": CITY_COORDS[city]["lat"],
                    "lon": CITY_COORDS[city]["lon"],
                    "condition": random.choice(["חדש לגמרי", "כמו חדש", "משומש"]),
                    "description": f"פריט מצוין מקטגוריית {cat} תחת תת-קטגוריה {sub_cat}. איסוף נוח בתיאום מראש.",
                    "phone": f"05{random.randint(2,9)}{random.randint(1000000,9999999)}",
                    "image_url": CATEGORY_IMAGES.get(cat, ""),
                    "status": "available",
                    "views": random.randint(10, 250),
                    "owner": user,
                    "is_bot": True
                })
    return generated

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
            if items and len(items) > 30:
                return items
    return generate_all_category_items()

def save_items(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

if 'items' not in st.session_state:
    st.session_state['items'] = load_items()
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []

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
    "🗺️ מפה ארצית אינטראקטיבית", 
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
    
    item_id = item.get('id', str(random.randint(1000,9999)))
    if st.button("❤️ שמור", key=f"fav_{unique_key_prefix}_{item_id}"):
        if item not in st.session_state['favorites']:
            st.session_state['favorites'].append(item)
            st.toast("נוסף לפריטים שמעניינים אותי!")

if choice == "🛍️ לוח פריטים למסירה":
    st.subheader("🛍️ לוח פריטים למסירה לפי קטגוריות ותתי-קטגוריות")
    
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
        all_items = [i for i in all_items if i.get('category'] == selected_main_cat]
    if selected_sub_cat != "הכל":
        all_items = [i for i in all_items if i.get('sub_category'] == selected_sub_cat]
        
    if not all_items:
        st.info("אין פריטים תחת הסינון הזה.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(all_items)):
            with cols[index % 3]:
                render_card(item, "board")

elif choice == "🗺️ מפה ארצית אינטראקטיבית":
    st.subheader("🗺️ מפה ארצית אינטראקטיבית וגבולות אזוריים")
    
    selected_map_city = st.selectbox("🎯 בחר אזור / עיר להתמקדות במפה:", ["כל הארץ"] + list(CITY_COORDS.keys()))
    
    st.markdown("🔵 **כחול:** פריטים למסירה | 🔴 **אדום:** פריטים דרושים | *לחץ על כל נקודה במפה לפרטי החפץ*")
    
    if selected_map_city == "כל הארץ":
        map_center = [31.8944, 34.8094]
        zoom_level = 8
        displayed_items = st.session_state['items']
    else:
        map_center = [CITY_COORDS[selected_map_city]["lat"], CITY_COORDS[selected_map_city]["lon"]]
        zoom_level = 13
        displayed_items = [i for i in st.session_state['items'] if i.get('location') == selected_map_city]
    
    m = folium.Map(location=map_center, zoom_start=zoom_level, tiles="OpenStreetMap")
    
    # ציור גבול עירוני אמיתי (פוליגון) במקום עיגול פשוט אם קיים לעיר
    if selected_map_city != "כל הארץ" and selected_map_city in CITY_POLYGONS:
        folium.Polygon(
            locations=CITY_POLYGONS[selected_map_city],
            color="#2563eb",
            weight=3,
            fill=True,
            fill_color="#3b82f6",
            fill_opacity=0.15,
            popup=f"גבול מוניציפלי: {selected_map_city}"
        ).add_to(m)

    for idx, item in enumerate(displayed_items):
        base_lat = item.get('lat', map_center[0])
        base_lon = item.get('lon', map_center[1])
        
        lat = base_lat + (idx * 0.0012 % 0.02) - 0.01
        lon = base_lon + (idx * 0.0015 % 0.02) - 0.01
        
        title = item.get('title', 'ללא כותרת')
        loc = item.get('location', 'ישראל')
        cat = item.get('sub_category', item.get('category', ''))
        
        popup_html = f"""
        <div style="direction: rtl; text-align: right; font-family: sans-serif; width: 200px;">
            <b style="font-size: 1rem; color: #1e293b;">{title}</b><br>
            <span style="color: #64748b; font-size: 0.85rem;">📍 {loc} | {cat}</span>
        </div>
        """
        
        marker_color = "red" if item.get('type') == 'request' else "blue"
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=title,
            icon=folium.Icon(color=marker_color, icon="info-sign")
        ).add_to(m)
        
    st_folium(m, width=1200, height=550)
    
    st.divider()
    st.subheader(f"📌 פריטים באזור: {selected_map_city}")
    
    if not displayed_items:
        st.info("אין פריטים באזור זה כרגע.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(displayed_items)):
            with cols[index % 3]:
                render_card(item, "map_city")

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
                item_id = item.get('id', random.randint(1000,9999))
                if st.button("❌ הסר", key=f"rem_{item_id}"):
                    st.session_state['favorites'].remove(item)
                    save_items(st.session_state['items'])
                    st.rerun()

elif choice == "➕ פרסם מודעה":
    st.subheader("➕ פרסם פריט חדש למערכת")
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
                "lat": coords["lat"] + random.uniform(-0.01, 0.01),
                "lon": coords["lon"] + random.uniform(-0.01, 0.01),
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
    st.write("כאן תוכל לאפס את הנתונים ולייצר מחדש מאגר עשיר הכולל בדיוק פריטים מלאים לכל תת-קטגוריה במערכת.")
    if st.button("🚀 טען מחדש את כל הקטגוריות ותתי-הקטגוריות", type="primary"):
        st.session_state['items'] = generate_all_category_items()
        save_items(st.session_state['items'])
        st.success("המאגר אופס ונוצר מחדש בהצלחה עם כיסוי מלא של 100% מכל הקטגוריות!")
    if st.button("🗑️ איפוס מלא של הלוח"):
        st.session_state['items'] = []
        st.session_state['favorites'] = []
        save_items([])
        st.warning("הלוח אופס לגמרי.")
