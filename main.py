import streamlit as st
import json
import os
import base64
import random
import math
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="אגורה Pro", page_icon="♻️", layout="wide", initial_sidebar_state="collapsed")

DATA_FILE = "agora_data.json"

CATEGORIES = {
    "📱 אלקטרוניקה, מחשבים ותקשורת": [
        "מכשירים סלולריים וטאבלטים", 
        "מחשבים ניידים", 
        "מחשבים נייחים", 
        "מסכים וטלוויזיות", 
        "ממירים וסטרימרים", 
        "קונסולות משחק", 
        "ציוד היקפי (מקלדות, עכברים)",
        "כבלים ומטענים"
    ],
    "🏠 חשמל ומוצרי בית": [
        "מקררים ומקפיאים", 
        "מכונות כביסה ומייבשים", 
        "מדיחי כלים", 
        "תנורים וכיריים", 
        "מזגנים ומאווררים", 
        "קוטלי יתושים ומזיקים", 
        "שואבי אבק", 
        "מוצרי מטבח קטנים (מיקסר, בלנדר)"
    ],
    "🛋️ רהיטים וציוד לבית": [
        "ספות ומערכות סלון", 
        "ספה בודדת", 
        "פינות אוכל ושולחנות", 
        "ארונות ומזנונים", 
        "מיטות ומזרנים", 
        "שידות וכונניות", 
        "ריהוט גן ומרפסת"
    ],
    "🚲 תחבורה וניידות": [
        "אופניים חשמליים", 
        "אופניים רגילים", 
        "קורקינטים חשמליים", 
        "קורקינטים רגילים", 
        "קסדות ואביזרי בטיחות"
    ],
    "🛠️ כלי עבודה, RF ומעבדה": [
        "ציוד מדידה ו-RF", 
        "רכיבים אלקטרוניים ובקרים (ESP32)", 
        "כלי עבודה חשמליים (מקדחות, מברגות)", 
        "כלי עבודה ידניים", 
        "ציוד ריתוך וציוד טכני"
    ],
    "👶 ילדים, תינוקות וצעצועים": [
        "עגלות וטיולונים", 
        "כיסאות בטיחות לרכב", 
        "משחקי קופסה וצעצועים", 
        "מיטות ולולים", 
        "בגדי תינוקות וילדים"
    ],
    "👕 אופנה, ביגוד ותכשיטים": [
        "בגדי נשים", 
        "בגדי גברים", 
        "הנעלה", 
        "תיקים ואקססוריז", 
        "שעונים ותכשיטים"
    ],
    "📦 פנאי, ספורט ושונות": [
        "ספרים ומגזינים", 
        "ציוד ספורט וכושר", 
        "ציוד קמפינג וטיולים", 
        "כלי נגינה", 
        "ציוד לחיות מחמד",
        "אחר"
    ]
}

AUTO_CAT_MAP = {
    "מחשב": ("📱 אלקטרוניקה, מחשבים ותקשורת", "מחשבים ניידים"),
    "לפטופ": ("📱 אלקטרוניקה, מחשבים ותקשורת", "מחשבים ניידים"),
    "סלולר": ("📱 אלקטרוניקה, מחשבים ותקשורת", "מכשירים סלולריים וטאבלטים"),
    "טלפון": ("📱 אלקטרוניקה, מחשבים ותקשורת", "מכשירים סלולריים וטאבלטים"),
    "ממיר": ("📱 אלקטרוניקה, מחשבים ותקשורת", "ממירים וסטרימרים"),
    "סטרימר": ("📱 אלקטרוניקה, מחשבים ותקשורת", "ממירים וסטרימרים"),
    "יתוש": ("🏠 חשמל ומוצרי בית", "קוטלי יתושים ומזיקים"),
    "קוטל": ("🏠 חשמל ומוצרי בית", "קוטלי יתושים ומזיקים"),
    "מקרר": ("🏠 חשמל ומוצרי בית", "מקררים ומקפיאים"),
    "ספה": ("🛋️ רהיטים וציוד לבית", "ספות ומערכות סלון"),
    "אופניים": ("🚲 תחבורה וניידות", "אופניים רגילים"),
    "קורקינט": ("🚲 תחבורה וניידות", "קורקינטים חשמליים"),
    "esp32": ("🛠️ כלי עבודה, RF ומעבדה", "רכיבים אלקטרוניים ובקרים (ESP32)"),
    "rf": ("🛠️ כלי עבודה, RF ומעבדה", "ציוד מדידה ו-RF")
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

CITY_POLYGONS = {
    "רחובות": [[31.918, 34.795], [31.922, 34.812], [31.908, 34.828], [31.882, 34.830], [31.866, 34.812], [31.870, 34.788], [31.895, 34.782]],
    "תל אביב": [[32.125, 34.770], [32.115, 34.825], [32.045, 34.815], [32.015, 34.765], [32.035, 34.742], [32.095, 34.740]]
}

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def validate_content(title, desc, main_cat):
    blocked_words = ["שטויות", "קללה", "דלורית", "זבל", "test", "בדיקה"]
    text_to_check = (title + " " + desc).lower()
    for word in blocked_words:
        if word in text_to_check: return False, f"המילה '{word}' חסומה."
    if len(title) < 3: return False, "כותרת המודעה קצרה מדי."
    return True, ""

def load_items():
    dummy_items = []
    cities = list(CITY_COORDS.keys())
    for main_cat, sub_cats in CATEGORIES.items():
        for sub_cat in sub_cats:
            city = random.choice(cities)
            coords = CITY_COORDS[city]
            dummy_items.append({
                "id": f"dummy_{random.randint(10000, 99999)}",
                "type": "giveaway",
                "title": f"מסירה: {sub_cat} במצב מצוין",
                "category": main_cat,
                "sub_category": sub_cat,
                "location": city,
                "lat": coords["lat"] + random.uniform(-0.01, 0.01),
                "lon": coords["lon"] + random.uniform(-0.01, 0.01),
                "description": f"פריט איכותי ששמור היטב מתת-הקטגוריה {sub_cat}. איסוף נוח בתיאום מראש.",
                "phone": "0526693881",
                "contact_pref": "שיחה רגילה או וואטסאפ",
                "image_url": "https://images.unsplash.com/photo-1584467735811-628b0fd4603d?w=600&q=80",
                "views": random.randint(1, 20),
                "owner": {"name": "צוות אגורה", "karma": 15, "verified": True}
            })
    return dummy_items

if 'items' not in st.session_state: st.session_state['items'] = load_items()
if 'favorites' not in st.session_state: st.session_state['favorites'] = []
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = {"name": "גיא", "phone": "0526693881", "city": "רחובות", "karma": 5}

st.markdown("""
    <style>
    .stApp { background: #f8fafc; color: #0f172a; direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
    div[role="radiogroup"] label, div[role="radiogroup"] div, p { color: #0f172a !important; }
    .product-card {
        background: #ffffff; border-radius: 20px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        border: 1px solid #e2e8f0; transition: transform 0.2s ease, box-shadow 0.2s;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); }
    .badge { display: inline-block; padding: 5px 12px; border-radius: 20px; background: #e0f2fe; color: #0284c7; font-size: 0.75rem; margin-left: 6px; font-weight: 600;}
    .user-info { font-size: 0.85rem; color: #64748b; margin-bottom: 12px; }
    .action-buttons { display: flex; gap: 10px; margin-top: 15px; }
    .wa-btn, .call-btn, .inapp-btn { flex: 1; text-align: center; color: white !important; padding: 10px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 0.9rem; transition: 0.2s;}
    .wa-btn { background: #25D366; } .wa-btn:hover { background: #16a34a; }
    .call-btn { background: #3b82f6; } .call-btn:hover { background: #2563eb; }
    .inapp-btn { background: #6366f1; } .inapp-btn:hover { background: #4f46e5; }
    .filter-bar-title { font-size: 1.4rem; font-weight: 700; margin-bottom: 20px; text-align: center; color: #1e293b; }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 30px !important; padding: 2px 10px !important;
    }
    div[data-baseweb="select"] span { color: #334155 !important; font-weight: 500 !important; }
    input[type="text"] {
        background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 30px !important; color: #334155 !important; padding: 10px 20px !important;
    }
    input::placeholder { color: #94a3b8 !important; }
    label { color: #475569 !important; font-weight: 600 !important; font-size: 0.85rem !important; margin-bottom: 5px !important; }
    .nav-bar { background: white; padding: 10px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 25px;}
    </style>
""", unsafe_allow_html=True)

st.title("♻️ אגורה Pro")

st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
menu_options = ["🏠 דף הבית", "📍 מפה", "🔍 סוכן חיפוש", "➕ סוכן העלאה", "❤️ שמורים"]
choice = st.radio("ניווט", menu_options, horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

def render_card(item, unique_key_prefix, extra_info=""):
    owner = item.get('owner', {"name": "משתמש אנונימי", "karma": 0})
    phone = item.get('phone', '')
    wa_num = phone[1:] if phone.startswith('0') else phone
    contact_pref = item.get('contact_pref', 'שיחה רגילה או וואטסאפ')
    img_src = item.get('image_url') or "https://images.unsplash.com/photo-1584467735811-628b0fd4603d?w=600&q=80"
    if item.get('image'):
        try: img_src = f"data:image/png;base64,{item.get('image')}"
        except: pass

    if contact_pref == "הודעות באפליקציה בלבד":
        buttons_html = f'<a href="#" class="inapp-btn">✉️ שלח הודעה באפליקציה</a>'
    elif contact_pref == "רק וואטסאפ":
        buttons_html = f'<a href="https://wa.me/972{wa_num}" target="_blank" class="wa-btn">💬 וואטסאפ בלבד</a>'
    else:
        buttons_html = f'<a href="https://wa.me/972{wa_num}" target="_blank" class="wa-btn">💬 וואטסאפ</a> <a href="tel:{phone}" class="call-btn">📞 התקשר</a>'

    card_html = f"""<div class="product-card">
<img src="{img_src}" style="width:100%; height:180px; object-fit:cover; border-radius:15px; margin-bottom:15px;"/>
<div class="user-info">👤 {owner.get('name')} <span style="color:#fbbf24;">{'⭐ ' + str(owner.get('karma')) if owner.get('karma') > 0 else '🌟 משתמש חדש'}</span></div>
<h3 style="margin: 0 0 10px 0; color: #0f172a; font-size: 1.3rem;">{item.get('title')}</h3>
<div style="margin-bottom: 12px;">
<span class="badge">{item.get('sub_category', item.get('category'))}</span>
<span class="badge" style="background:#dcfce7; color:#166534;">📍 {item.get('location')}</span>
{f'<span class="badge" style="background:#fef08a; color:#854d0e;">🚗 {extra_info}</span>' if extra_info else ''}
</div>
<p style="color: #475569; font-size: 0.9rem; margin-bottom: 15px; line-height: 1.5;">{item.get('description')}</p>
<div class="action-buttons">{buttons_html}</div>
</div>"""
    st.markdown(card_html, unsafe_allow_html=True)
    item_id = item.get('id', str(random.randint(1000,9999)))
    if st.button("❤️ שמור פריט", key=f"fav_{unique_key_prefix}_{item_id}", use_container_width=True):
        if item not in st.session_state['favorites']:
            st.session_state['favorites'].append(item)
            st.toast("נשמר בהצלחה!")

if choice == "🏠 דף הבית":
    st.markdown('<div class="filter-bar-title">מה תרצו לחפש היום?</div>', unsafe_allow_html=True)
    
    # ניהול מצב הקטגוריות מחוץ לטופס כדי לאפשר עדכון דינמי חלק
    if 'selected_main_cat' not in st.session_state:
        st.session_state['selected_main_cat'] = "הכל"

    f1, f2, f3, f4 = st.columns(4)
    
    def update_main_cat():
        st.session_state['selected_sub_cat'] = "הכל"

    selected_main_cat = f1.selectbox("סוג מוצר", ["הכל"] + list(CATEGORIES.keys()), key="selected_main_cat", on_change=update_main_cat)
    
    sub_options = ["הכל"] + (CATEGORIES[selected_main_cat] if selected_main_cat != "הכל" else [])
    if 'selected_sub_cat' not in st.session_state:
        st.session_state['selected_sub_cat'] = "הכל"
        
    selected_sub_cat = f2.selectbox("תת-קטגוריה", sub_options, key="selected_sub_cat")
    selected_loc = f3.selectbox("אזור / עיר", ["כל הארץ"] + list(CITY_COORDS.keys()))
    search_text = f4.text_input("חיפוש חופשי", placeholder="למשל: מחשב, ממיר...")
    
    st.divider()

    all_items = [i for i in st.session_state['items'] if i.get('type') == 'giveaway']
    if selected_main_cat != "הכל": 
        all_items = [i for i in all_items if i.get('category') == selected_main_cat]
    if selected_sub_cat != "הכל": 
        all_items = [i for i in all_items if i.get('sub_category') == selected_sub_cat]
    if selected_loc != "כל הארץ": 
        all_items = [i for i in all_items if i.get('location') == selected_loc]
    if search_text: 
        all_items = [i for i in all_items if search_text.lower() in (i.get('title','') + i.get('description','')).lower()]
        
    if not all_items: 
        st.info("אין פריטים התואמים לחיפוש שלך.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(reversed(all_items)):
            with cols[index % 3]: render_card(item, "home")

elif choice == "📍 מפה":
    st.subheader("מפה ארצית")
    selected_map_city = st.selectbox("🎯 התמקד בעיר:", ["כל הארץ"] + list(CITY_COORDS.keys()))
    map_center = [31.8944, 34.8094] if selected_map_city == "כל הארץ" else [CITY_COORDS[selected_map_city]["lat"], CITY_COORDS[selected_map_city]["lon"]]
    
    google_tiles = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
    m = folium.Map(
        location=map_center, zoom_start=8 if selected_map_city == "כל הארץ" else 13, 
        tiles=google_tiles, attr="Google", min_zoom=7, max_bounds=True,
        min_lat=29.4, max_lat=33.4, min_lon=34.2, max_lon=35.9
    )
    
    if selected_map_city != "כל הארץ" and selected_map_city in CITY_POLYGONS:
        folium.Polygon(locations=CITY_POLYGONS[selected_map_city], color="#3b82f6", weight=2, fill=True, fill_opacity=0.1).add_to(m)

    for idx, item in enumerate(st.session_state['items']):
        if selected_map_city != "כל הארץ" and item.get('location') != selected_map_city: continue
        lat = item.get('lat', map_center[0]) + (idx * 0.001 % 0.01)
        lon = item.get('lon', map_center[1]) + (idx * 0.001 % 0.01)
        phone = item.get('phone', '')
        wa_num = phone[1:] if phone.startswith('0') else phone
        img_src = item.get('image_url') or "https://images.unsplash.com/photo-1584467735811-628b0fd4603d?w=600&q=80"
        if item.get('image'):
            try: img_src = f"data:image/png;base64,{item.get('image')}"
            except: pass
            
        popup_html = f"""
        <div style="direction: rtl; text-align: right; width: 170px; font-family: 'Segoe UI', Tahoma, sans-serif;">
            <img src="{img_src}" style="width:100%; height:110px; object-fit:cover; border-radius:8px; margin-bottom:8px;"/>
            <b style="font-size:15px; color:#0f172a; display:block; margin-bottom:2px;">{item.get('title')}</b>
            <span style="color:#64748b; font-size:12px; display:block; margin-bottom:10px;">{item.get('category')}</span>
            <a href="https://wa.me/972{wa_num}" target="_blank" style="padding:6px; background:#25D366; color:white; border-radius:5px; text-decoration:none; font-size:13px; font-weight:bold; display:block; text-align:center;">לפניה בוואטסאפ</a>
        </div>
        """
        folium.CircleMarker(
            location=[lat, lon], radius=8, color="#3b82f6", fill=True, fill_color="#3b82f6", fill_opacity=0.9, tooltip="לחץ לצפייה"
        ).add_to(m).add_child(folium.Popup(popup_html, max_width=200))
        
    st_folium(m, width=1200, height=500)

elif choice == "🔍 סוכן חיפוש":
    st.markdown('<div class="filter-bar-title">🔍 חיפוש חכם לפי מרחק</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    user_city = c1.selectbox("📍 המיקום שלך:", list(CITY_COORDS.keys()), index=list(CITY_COORDS.keys()).index(st.session_state['current_user']['city']))
    search_query = c2.text_input("🔍 מה לחפש?", placeholder="למשל: מחשב, ממיר, קוטל יתושים...")
    if search_query:
        user_coords = CITY_COORDS[user_city]
        scored_items = []
        for item in st.session_state['items']:
            text_block = (item.get('title','') + item.get('description','') + item.get('category','')).lower()
            if search_query.lower() in text_block:
                dist = calculate_distance(user_coords['lat'], user_coords['lon'], item.get('lat', 0), item.get('lon', 0))
                scored_items.append((dist, item))
        scored_items.sort(key=lambda x: x[0])
        if not scored_items: st.warning("לא מצאנו פריטים תואמים.")
        else:
            st.success(f"מצאנו {len(scored_items)} פריטים, מסודרים מהקרוב לרחוק:")
            cols = st.columns(3)
            for index, (dist, item) in enumerate(scored_items):
                with cols[index % 3]: render_card(item, "agent", extra_info=f"{dist} ק\"מ ממך")

elif choice == "➕ סוכן העלאה":
    st.markdown('<div class="filter-bar-title">➕ איזה פריט תרצה למסור?</div>', unsafe_allow_html=True)
    title = st.text_input("מה שם הפריט?", placeholder="לדוגמה: קוטל יתושים, ממיר דיגיטלי...", key="upload_title")
    
    suggested_main, suggested_sub = "📦 פנאי, ספורט ושונות", "אחר"
    for keyword, (m_cat, s_cat) in AUTO_CAT_MAP.items():
        if keyword in title.lower(): suggested_main, suggested_sub = m_cat, s_cat; break
        
    with st.form("smart_upload_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        main_cat_idx = list(CATEGORIES.keys()).index(suggested_main) if suggested_main in CATEGORIES else 0
        main_cat = c1.selectbox("לאיזו קטגוריה הוא שייך?", list(CATEGORIES.keys()), index=main_cat_idx)
        
        sub_cat_idx = CATEGORIES[main_cat].index(suggested_sub) if suggested_sub in CATEGORIES[main_cat] else 0
        sub_cat = c2.selectbox("תת-קטגוריה:", CATEGORIES[main_cat], index=sub_cat_idx)
        
        c3, c4 = st.columns(2)
        city = c3.selectbox("מהי עיר האיסוף?", list(CITY_COORDS.keys()), index=list(CITY_COORDS.keys()).index(st.session_state['current_user']['city']))
        phone = c4.text_input("מספר טלפון לתיאום:", value=st.session_state['current_user']['phone'])
        contact_pref = st.radio("איך תעדיף שיפנו אליך בנוגע לפריט הזה?", ["שיחה רגילה או וואטסאפ", "רק וואטסאפ", "הודעות באפליקציה בלבד"], horizontal=True)
        desc = st.text_area("ספר קצת על מצב הפריט:")
        uploaded_img = st.file_uploader("תמונה (לא חובה)", type=["png", "jpg", "jpeg"])
        if st.form_submit_button("פרסם פריט", type="primary", use_container_width=True):
            is_valid, error_msg = validate_content(title, desc, main_cat)
            if not is_valid: st.error(f"המודעה נחסמה על ידי הסוכן: {error_msg}")
            else:
                img_str = base64.b64encode(uploaded_img.read()).decode() if uploaded_img else ""
                coords = CITY_COORDS.get(city)
                new_item = {
                    "id": f"usr_{random.randint(1000, 9999)}", "type": "giveaway", "title": title,
                    "category": main_cat, "sub_category": sub_cat, "location": city,
                    "lat": coords["lat"] + random.uniform(-0.01, 0.01), "lon": coords["lon"] + random.uniform(-0.01, 0.01),
                    "description": desc, "phone": phone, "contact_pref": contact_pref,
                    "image": img_str, "views": 0, "owner": {"name": st.session_state['current_user']['name'], "karma": st.session_state['current_user']['karma'], "verified": False} 
                }
                st.session_state['items'].insert(0, new_item)
                save_items(st.session_state['items'])
                st.balloons()
                st.success("הפריט הועלה בהצלחה למערכת!")

elif choice == "❤️ שמורים":
    st.subheader("פריטים ששמרתי")
    if not st.session_state['favorites']: st.info("אין פריטים ששמרת עדיין.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(st.session_state['favorites']):
            with cols[index % 3]:
                render_card(item, "favs")
                if st.button("❌ הסר", key=f"rem_{item.get('id')}", use_container_width=True):
                    st.session_state['favorites'].remove(item)
                    st.rerun()
