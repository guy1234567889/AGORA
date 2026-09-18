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
USERS_FILE = "agora_users.json"

CATEGORIES = {
    "רהיטים": ["ספות וסלון", "שולחנות וכיסאות", "ארונות ומדפים", "ריהוט לחדרי שינה"],
    "מוצרי חשמל": ["מכונות כביסה ומייבשים", "מקררים ומקפיאים", "מוצרי מטבח קטנים", "מזגנים ומאווררים"],
    "אלקטרוניקה ומעבדה": ["ציוד מדידה ו-RF", "בקרים ומיקרו-בקרים", "רכיבים ואביזרים", "טלפונים ומחשבים"],
    "ביגוד ואופנה": ["ביגוד גברים", "ביגוד נשים", "הנעלה", "אקססוריז"],
    "צעצועים וילדים": ["משחקי קופסה", "צעצועי התפתחות", "ציוד לתינוקות", "עגלות וטיולונים"],
    "שונות": ["כלי עבודה", "ציוד ספורט", "ספרים ומגזינים", "אחר"]
}

AUTO_CAT_MAP = {
    "אופניים": ("שונות", "ציוד ספורט"),
    "מחשב": ("אלקטרוניקה ומעבדה", "טלפונים ומחשבים"),
    "מקרר": ("מוצרי חשמל", "מקררים ומקפיאים"),
    "ספה": ("רהיטים", "ספות וסלון"),
    "חולצה": ("ביגוד ואופנה", "ביגוד גברים"),
    "esp32": ("אלקטרוניקה ומעבדה", "בקרים ומיקרו-בקרים"),
    "קוטל": ("מוצרי חשמל", "מוצרי מטבח קטנים")
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
        if word in text_to_check:
            return False, f"המילה '{word}' חסומה לפרסום או אינה תואמת לכללי הקהילה."
    if len(title) < 2:
        return False, "כותרת המודעה קצרה מדי."
    return True, ""

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
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = {"name": "גיא", "phone": "0526693881", "city": "רחובות", "karma": 5}

st.markdown("""
    <style>
    .stApp { background: #f8fafc; color: #0f172a; direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
    input, textarea, div[data-baseweb="select"] { background-color: #ffffff !important; color: #0f172a !important; }
    .stTextInput input, .stTextArea textarea { color: #0f172a !important; background-color: #ffffff !important; }
    
    .product-card {
        background: #ffffff; border-radius: 20px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        border: 1px solid #f1f5f9;
    }
    .badge { display: inline-block; padding: 5px 12px; border-radius: 20px; background: #e0f2fe; color: #0284c7; font-size: 0.75rem; margin-left: 6px; font-weight: 600;}
    .user-info { font-size: 0.85rem; color: #64748b; margin-bottom: 12px; }
    .action-buttons { display: flex; gap: 10px; margin-top: 15px; }
    .wa-btn { flex: 1; text-align: center; background: #25D366; color: white !important; padding: 10px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 0.9rem;}
    .call-btn { flex: 1; text-align: center; background: #3b82f6; color: white !important; padding: 10px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 0.9rem;}
    .inapp-btn { flex: 1; text-align: center; background: #6366f1; color: white !important; padding: 10px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 0.9rem;}
    .nav-bar { background: white; padding: 10px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 25px;}
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); text-align: center; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

st.title("♻️ אגורה Pro")

st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
menu_options = ["🏠 דף הבית", "📍 מפה", "🔍 סוכן חיפוש", "➕ סוכן העלאה", "❤️ שמורים", "📊 ניהול ועסקים"]
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

    buttons_html = ""
    if contact_pref == "הודעות באפליקציה בלבד":
        buttons_html = f'<a href="#" class="inapp-btn">✉️ שלח הודעה באפליקציה</a>'
    elif contact_pref == "רק וואטסאפ":
        buttons_html = f'<a href="https://wa.me/972{wa_num}" target="_blank" class="wa-btn">💬 וואטסאפ בלבד</a>'
    else:
        buttons_html = f"""
        <a href="https://wa.me/972{wa_num}" target="_blank" class="wa-btn">💬 וואטסאפ</a>
        <a href="tel:{phone}" class="call-btn">📞 התקשר</a>
        """

    card_html = f"""<div class="product-card">
<img src="{img_src}" style="width:100%; height:180px; object-fit:cover; border-radius:15px; margin-bottom:15px;"/>
<div class="user-info">
👤 {owner.get('name')} <span style="color:#fbbf24;">{'⭐ ' + str(owner.get('karma')) if owner.get('karma') > 0 else '🌟 משתמש חדש'}</span>
</div>
<h3 style="margin: 0 0 10px 0; color: #0f172a; font-size: 1.3rem;">{item.get('title')}</h3>
<div style="margin-bottom: 12px;">
<span class="badge">{item.get('sub_category', item.get('category'))}</span>
<span class="badge" style="background:#dcfce7; color:#166534;">📍 {item.get('location')}</span>
{f'<span class="badge" style="background:#fef08a; color:#854d0e;">🚗 {extra_info}</span>' if extra_info else ''}
</div>
<p style="color: #475569; font-size: 0.9rem; margin-bottom: 15px; line-height: 1.5;">{item.get('description')}</p>
<div class="action-buttons">
{buttons_html}
</div>
</div>"""
    st.markdown(card_html, unsafe_allow_html=True)
    
    item_id = item.get('id', str(random.randint(1000,9999)))
    if st.button("❤️ שמור פריט", key=f"fav_{unique_key_prefix}_{item_id}", use_container_width=True):
        if item not in st.session_state['favorites']:
            st.session_state['favorites'].append(item)
            st.toast("נשמר בהצלחה!")

if choice == "🏠 דף הבית":
    st.subheader("לוח פריטים למסירה")
    c1, c2 = st.columns(2)
    selected_main_cat = c1.selectbox("קטגוריה", ["הכל"] + list(CATEGORIES.keys()))
    sub_options = ["הכל"] + (CATEGORIES[selected_main_cat] if selected_main_cat != "הכל" else [])
    selected_sub_cat = c2.selectbox("תת-קטגוריה", sub_options)
        
    all_items = [i for i in st.session_state['items'] if i.get('type') == 'giveaway']
    if selected_main_cat != "הכל": 
        all_items = [i for i in all_items if i.get('category') == selected_main_cat]
    if selected_sub_cat != "הכל": 
        all_items = [i for i in all_items if i.get('sub_category') == selected_sub_cat]
        
    if not all_items: st.info("אין פריטים בסינון זה.")
    cols = st.columns(3)
    for index, item in enumerate(reversed(all_items)):
        with cols[index % 3]: render_card(item, "home")

elif choice == "📍 מפה":
    st.subheader("מפה ארצית")
    selected_map_city = st.selectbox("🎯 התמקד בעיר:", ["כל הארץ"] + list(CITY_COORDS.keys()))
    map_center = [31.8944, 34.8094] if selected_map_city == "כל הארץ" else [CITY_COORDS[selected_map_city]["lat"], CITY_COORDS[selected_map_city]["lon"]]
    m = folium.Map(location=map_center, zoom_start=8 if selected_map_city == "כל הארץ" else 13, tiles="OpenStreetMap")
    
    if selected_map_city != "כל הארץ" and selected_map_city in CITY_POLYGONS:
        folium.Polygon(locations=CITY_POLYGONS[selected_map_city], color="#3b82f6", weight=2, fill=True, fill_opacity=0.1).add_to(m)

    for idx, item in enumerate(st.session_state['items']):
        if selected_map_city != "כל הארץ" and item.get('location') != selected_map_city: continue
        lat = item.get('lat', map_center[0]) + (idx * 0.001 % 0.01)
        lon = item.get('lon', map_center[1]) + (idx * 0.001 % 0.01)
        folium.Marker(location=[lat, lon], tooltip=item.get('title')).add_to(m)
        
    st_folium(m, width=1200, height=500)

elif choice == "🔍 סוכן חיפוש":
    st.markdown("### 🔍 איזה פריט אתה מחפש?")
    st.write("הסוכן ימצא את הפריטים הקרובים אליך ביותר, ויחשב את המרחק המדויק בקילומטרים.")
    
    c1, c2 = st.columns(2)
    user_city = c1.selectbox("📍 המיקום שלך:", list(CITY_COORDS.keys()), index=list(CITY_COORDS.keys()).index(st.session_state['current_user']['city']))
    search_query = c2.text_input("🔍 מה לחפש?", placeholder="למשל: בקר ESP32, ספה, אופניים...")
        
    if search_query:
        user_coords = CITY_COORDS[user_city]
        scored_items = []
        for item in st.session_state['items']:
            text_block = (item.get('title','') + item.get('description','') + item.get('category','')).lower()
            if search_query.lower() in text_block:
                dist = calculate_distance(user_coords['lat'], user_coords['lon'], item.get('lat', 0), item.get('lon', 0))
                scored_items.append((dist, item))
                
        scored_items.sort(key=lambda x: x[0])
        
        if not scored_items:
            st.warning("לא מצאנו פריטים תואמים.")
        else:
            st.success(f"מצאנו {len(scored_items)} פריטים, מסודרים מהקרוב לרחוק:")
            cols = st.columns(3)
            for index, (dist, item) in enumerate(scored_items):
                with cols[index % 3]:
                    render_card(item, "agent", extra_info=f"{dist} ק\"מ ממך")

elif choice == "➕ סוכן העלאה":
    st.markdown("### ➕ איזה פריט אתה כבר לא צריך ותרצה להעלות?")
    
    title = st.text_input("מה שם הפריט?", placeholder="לדוגמה: אופניים חשמליים", key="upload_title")
    
    suggested_main = "שונות"
    suggested_sub = "אחר"
    for keyword, (m_cat, s_cat) in AUTO_CAT_MAP.items():
        if keyword in title.lower():
            suggested_main = m_cat
            suggested_sub = s_cat
            break
            
    with st.form("smart_upload_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        main_cat = c1.selectbox("לאיזו קטגוריה הוא שייך?", list(CATEGORIES.keys()), index=list(CATEGORIES.keys()).index(suggested_main))
        sub_cat = c2.selectbox("תת-קטגוריה:", CATEGORIES[main_cat], index=CATEGORIES[main_cat].index(suggested_sub) if suggested_sub in CATEGORIES[main_cat] else 0)
        
        c3, c4 = st.columns(2)
        city = c3.selectbox("מהי עיר האיסוף?", list(CITY_COORDS.keys()), index=list(CITY_COORDS.keys()).index(st.session_state['current_user']['city']))
        phone = c4.text_input("מספר טלפון לתיאום:", value=st.session_state['current_user']['phone'])
        
        contact_pref = st.radio("איך תעדיף שיפנו אליך בנוגע לפריט הזה?", ["שיחה רגילה או וואטסאפ", "רק וואטסאפ", "הודעות באפליקציה בלבד"], horizontal=True)
        
        desc = st.text_area("ספר קצת על מצב הפריט:")
        uploaded_img = st.file_uploader("תמונה (לא חובה)", type=["png", "jpg", "jpeg"])
        
        if st.form_submit_button("פרסם פריט", type="primary", use_container_width=True):
            is_valid, error_msg = validate_content(title, desc, main_cat)
            
            if not is_valid:
                st.error(f"המודעה נחסמה על ידי הסוכן: {error_msg}")
            else:
                img_str = base64.b64encode(uploaded_img.read()).decode() if uploaded_img else ""
                coords = CITY_COORDS.get(city)
                new_item = {
                    "id": f"usr_{random.randint(1000, 9999)}",
                    "type": "giveaway",
                    "title": title,
                    "category": main_cat,
                    "sub_category": sub_cat,
                    "location": city,
                    "lat": coords["lat"] + random.uniform(-0.01, 0.01),
                    "lon": coords["lon"] + random.uniform(-0.01, 0.01),
                    "description": desc,
                    "phone": phone,
                    "contact_pref": contact_pref,
                    "image": img_str,
                    "views": 0,
                    "owner": {"name": st.session_state['current_user']['name'], "karma": st.session_state['current_user']['karma'], "verified": False} 
                }
                st.session_state['items'].insert(0, new_item)
                save_items(st.session_state['items'])
                st.balloons()
                st.success("הפריט הועלה בהצלחה למערכת!")

elif choice == "❤️ שמורים":
    st.subheader("פריטים ששמרתי")
    if not st.session_state['favorites']:
        st.info("אין פריטים שמורים עדיין.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(st.session_state['favorites']):
            with cols[index % 3]:
                render_card(item, "favs")
                if st.button("❌ הסר", key=f"rem_{item.get('id')}", use_container_width=True):
                    st.session_state['favorites'].remove(item)
                    st.rerun()

elif choice == "📊 ניהול ועסקים":
    st.subheader("📊 דשבורד ניהולי ומדדי צמיחה לעסקים")
    total_users = len(st.session_state['users_db'] if 'users_db' in st.session_state else []) + 124
    total_items = len(st.session_state['items'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>👥 משתמשים רשומים</h3><h2>{total_users}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>📦 פריטים בלוח</h3><h2>{total_items}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>📈 חשיפות החודש</h3><h2>{total_items * 18 + 430}</h2></div>', unsafe_allow_html=True)
