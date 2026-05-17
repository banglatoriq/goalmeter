import streamlit as st
import sqlite3
import hashlib
import datetime
import pandas as pd
import plotly.express as px
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DevLife OS",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INSPIRATIONAL CYBERPUNK COLOR PALETTE & UI/UX CSS ---
st.markdown("""
<style>
    /* Main background and font */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }
    
    /* Custom Card Design for UI/UX */
    .dev-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }
    
    .motivational-banner {
        background: linear-gradient(90deg, #0D9488 0%, #115E59 100%);
        padding: 20px;
        border-radius: 12px;
        color: #FFFFFF;
        border-left: 5px solid #2DD4BF;
        margin-bottom: 25px;
    }
    
    /* Metric styling adjustments */
    div[data-testid="stMetricValue"] {
        color: #2DD4BF !important;
        font-weight: 800;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 14px;
    }
    
    /* Button enhancement */
    .stButton>button {
        background-color: #0F172A;
        color: #2DD4BF;
        border: 1px solid #2DD4BF;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2DD4BF;
        color: #0F172A;
        box-shadow: 0 0 12px rgba(45, 212, 191, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE SETUP & ARCHITECTURE ---
DB_FILE = "devlife_os.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                slot TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                habit_id INTEGER,
                date TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                UNIQUE(user_id, habit_id, date),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                deadline TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT UNIQUE NOT NULL,
                q1 TEXT, q2 TEXT, q3 TEXT,
                mood INTEGER, energy INTEGER, brain_dump TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        conn.commit()

init_db()

# --- AUTHENTICATION FUNCTIONS ---
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def register_user(username, password):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, make_hash(password)))
            conn.commit()
            user_id = cursor.lastrowid
            seed_default_habits(user_id)
            return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, make_hash(password)))
        return cursor.fetchone()

def seed_default_habits(user_id):
    defaults = [
        ("সকালে ঘুম থেকে উঠে প্রথম ৩০ মিনিট ফোন না ধরা", "Mental", "Morning"),
        ("১০ মিনিট নিরবতা বা প্রাণায়াম/Breathing", "Mental", "Morning"),
        ("শরীর সচল করা (১৫ মিনিট হালকা ব্যায়াম)", "Health", "Morning"),
        ("Deep Learning Block (১ ঘণ্টা গভীর পড়ালেখা)", "Coding", "Morning"),
        ("স্ক্রিন ছাড়া পুষ্টিকর প্রাতঃরাশ/Breakfast", "Health", "Morning"),
        ("Deep Work Block 1 (কঠিন কোডিং ও লজিক সমাধান)", "Coding", "Work"),
        ("Reactive Tasks (ইমেইল, মেসেজ ও রিভিউ)", "Coding", "Work"),
        ("দুপুরের খাবারে স্ক্রিন থেকে সম্পূর্ণ দূরে থাকা ও হাঁটা", "Health", "Work"),
        ("পার্সোনাল প্রজেক্ট / নতুন কিছু বিল্ড করার সময়", "Coding", "Work"),
        ("দিনের কাজ শেষ করার রিল্যাক্সিং রুটিন (Shutdown)", "Mental", "Work"),
        ("স্ট্রেন্থ ট্রেনিং বা শারীরিক সুস্থতার ব্যায়াম", "Health", "Fitness"),
        ("রাত ৯:০০ টায় সব স্ক্রিন অফ বা নাইট মোড (Digital Sunset)", "Health", "Night"),
        ("কাজ শেষে মাইন্ড ফ্রেশ করার জন্য হাঁটা", "Health", "Fitness")
    ]
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO habits (user_id, name, category, slot) VALUES (?, ?, ?, ?)", 
                           [(user_id, name, cat, slot) for name, cat, slot in defaults])
        conn.commit()

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = ""

# --- AUTHENTICATION INTERFACE ---
if not st.session_state['logged_in']:
    st.title("🧭 DevLife OS")
    st.subheader("আপনার জীবনকে একটি গোছানো এবং সফল ইঞ্জিনিয়ারিং সিস্টেমে রূপান্তর করুন।")
    
    auth_mode = st.radio("মোড সিলেক্ট করুন:", ["Login", "Register"], horizontal=True)
    
    with st.form("auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(auth_mode)
        
        if submit:
            if auth_mode == "Register":
                if register_user(username, password):
                    st.success("অ্যাকাউন্ট তৈরি হয়েছে! এবার Login মোড সিলেক্ট করে প্রবেশ করুন।")
                else:
                    st.error("এই ইউজারনেমটি ইতিমধ্যে ব্যবহার করা হয়েছে।")
            else:
                user = login_user(username, password)
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user['id']
                    st.session_state['username'] = user['username']
                    st.rerun()
                else:
                    st.error("সঠিক ইউজারনেম বা পাসওয়ার্ড দিন।")
    st.stop()

# --- MAIN APP ARCHITECTURE (LOGGED IN) ---
user_id = st.session_state['user_id']
today = datetime.date.today().strftime("%Y-%m-%d")

# Sidebar Workspace Navigation
st.sidebar.title(f"🚀 {st.session_state['username']}@devlife_os")
menu = st.sidebar.radio(
    "কন্ট্রোল প্যানেল", 
    ["ড্যাশবোর্ড (Dashboard)", "রুটিন ট্র্যাকার (Routine Tracker)", "লক্ষ্য নির্ধারণ (Goal Architecture)", "রিপোর্ট ও অ্যানালিটিক্স (Advanced Reports)"]
)

if st.sidebar.button("System Shutdown (Logout)"):
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = ""
    st.rerun()

# --- MODULE 1: DASHBOARD ---
if menu == "ড্যাশবোর্ড (Dashboard)":
    st.title("🧭 মূল ড্যাশবোর্ড")
    st.write(f"📅 **আজকের তারিখ:** {datetime.date.today().strftime('%A, %B %d, %Y')}")
    
    # DEV-CENTRIC MOTIVATIONAL SPEECH GENERATOR
    speeches = [
        "কোড হোক বা জীবন—যেকোনো বড় সিস্টেমের শক্তি লুকিয়ে থাকে তার ফাউন্ডেশনের ওপর। আজকের ছোট ইনপুটটিই আগামীকালের বড় আউটপুট তৈরি করবে। ডোন্ট স্কিপ দ্য প্রসেস!",
        "টিউটোরিয়াল দেখা সহজ, কিন্তু আসল স্কিল তৈরি হয় যখন কোড ব্রেক করে আর আপনি সেটা নিজে ডিবাগ করেন। আজ অন্তত একটা কঠিন প্রবলেম ফেস করুন!",
        "আপনার ব্রেইনই আপনার সবচেয়ে বড় কাজের টুল (IDE)। পর্যাপ্ত ঘুম, ভালো খাবার আর শারীরিক মুভমেন্ট কোনো অপশন নয়—এটি আপনার পারফরম্যান্স কনফিগারেশন!",
        "মার্কেটে হাজারটা জিনিস জানা ডেভলপারের অভাব নেই। কিন্তু যারা যেকোনো একটি স্ট্যাক গভীরভাবে জানে এবং প্র্যাক্টিক্যাল প্রজেক্ট বিল্ড করে, জয় তাদেরই হয়। গো ডিপ!",
        "আজকের অলসতা মানে আগামীকালের সিস্টেম ক্র্যাশ। আপনার সিস্টেমের রানিং টাইম আপনার হাতে। মেক ইট কাউন্ট!"
    ]
    
    st.markdown(f"""
    <div class="motivational-banner">
        <h4>🔥 আজকের মনোবল বুস্টার (Daily Engineering Boost)</h4>
        <p style="font-size: 16px; font-style: italic; margin-bottom: 0;">"{random.choice(speeches)}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    with get_db_connection() as conn:
        total_habits = conn.execute("SELECT COUNT(*) FROM habits WHERE user_id = ?", (user_id,)).fetchone()[0]
        completed_today = conn.execute("SELECT COUNT(*) FROM habit_logs WHERE user_id = ? AND date = ? AND completed = 1", (user_id, today)).fetchone()[0]
    
    completion_rate = (completed_today / total_habits) * 100 if total_habits > 0 else 0
    
    # Main Metrics Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("আজকের কাজ সম্পন্ন হওয়ার হার (Completion)", f"{completion_rate:.1f}%", f"{completed_today}/{total_habits} অভীষ্ট লক্ষ্য")
    with col2:
        st.metric("আজকের কাজের গতি (Momentum)", "চমৎকার (Optimal)" if completion_rate > 50 else "ধীরগতির (Degraded)", "রুটিন ট্র্যাকিং এর ওপর ভিত্তি করে")
    with col3:
        st.metric("মানসিক প্রস্তুতি (Mindset Status)", "কনফিগারড (Ready)", "মস্তিষ্কের কর্মক্ষমতা সচল")

    st.markdown("---")
    
    # Priority Tasks Display
    st.markdown('<div class="dev-card">', unsafe_with_html=True)
    st.subheader("🎯 আজকের প্রধান কাজ ও মিশন (Top Objectives)")
    with get_db_connection() as conn:
        active_goals = conn.execute("SELECT * FROM goals WHERE user_id = ? AND progress < 100 LIMIT 3", (user_id,)).fetchall()
    
    if active_goals:
        for goal in active_goals:
            st.markdown(f"- **[{goal['category']}]** {goal['title']} — অগ্রগতি: `{goal['progress']}%`")
    else:
        st.info("বর্তমানে কোনো সক্রিয় লক্ষ্য নেই। নতুন মিশন সেট করতে বামদিকের 'লক্ষ্য নির্ধারণ' মেনুতে যান।")
    st.markdown('</div>', unsafe_with_html=True)

    st.info("💡 **মনে রাখুন:** আপনার পরিচয় আপনার আচরণের আগে আসে। আপনি শুধু টাস্ক কমপ্লিট করছেন না, আপনি নিজেকে একজন মাস্টার ইঞ্জিনিয়ার হিসেবে গড়ে তুলছেন।")

# --- MODULE 2: ROUTINE TRACKER ---
elif menu == "রুটিন ট্র্যাকার (Routine Tracker)":
    st.title("🌅 ডেইলি রুটিন ইঞ্জিন")
    
    with get_db_connection() as conn:
        all_habits = conn.execute("SELECT * FROM habits WHERE user_id = ?", (user_id,)).fetchall()
        for habit in all_habits:
            conn.execute("INSERT OR IGNORE INTO habit_logs (user_id, habit_id, date, completed) VALUES (?, ?, ?, 0)", 
                         (user_id, habit['id'], today))
        conn.commit()

    tab1, tab2, tab3 = st.tabs(["⚡ রুটিন চেকলিস্ট (Checklists)", "📝 আজকের আত্মচিন্তন (Deep Journaling)", "🧠 মাথার অতিরিক্ত চিন্তা ঝেড়ে ফেলা (Brain Dump)"])
    
    with tab1:
        st.subheader("আপনার দৈনন্দিন রুটিন ফ্রেমওয়ার্ক")
        with get_db_connection() as conn:
            logs = conn.execute("""
                SELECT hl.id, h.name, h.slot, hl.completed 
                FROM habit_logs hl 
                JOIN habits h ON hl.habit_id = h.id 
                WHERE hl.user_id = ? AND hl.date = ?
            """, (user_id, today)).fetchall()
            
        slots = [("Morning", "সকাল বেলার প্রস্তুতি"), ("Work", "কাজের সময় ও ফোকাস ব্লক"), ("Fitness", "শারীরিক সুস্থতা"), ("Night", "দিনের সমাপ্তি ও ঘুম")]
        for slot_key, slot_name in slots:
            st.write(f"#### 🕐 {slot_name}")
            slot_logs = [log for log in logs if log['slot'] == slot_key]
            
            for log in slot_logs:
                is_checked = bool(log['completed'])
                cb = st.checkbox(log['name'], value=is_checked, key=f"habit_{log['id']}")
                if cb != is_checked:
                    with get_db_connection() as conn:
                        conn.execute("UPDATE habit_logs SET completed = ? WHERE id = ?", (1 if cb else 0, log['id']))
                        conn.commit()
                    st.rerun()
                    
    with tab2:
        st.subheader("ডেভেলপার রিফ্লেকশন নোট")
        with get_db_connection() as conn:
            existing_j = conn.execute("SELECT * FROM journal_entries WHERE user_id = ? AND date = ?", (user_id, today)).fetchone()
            
        with st.form("journal_form"):
            q1 = st.text_area("১. আজকে কোডিং বা টেকনিক্যাল কোন জটিল সমস্যার সমাধান করলেন?", value=existing_j['q1'] if existing_j else "")
            q2 = st.text_area("২. নতুন কোন কোড আর্কিটেকচার বা ক্লিন প্যাটার্ন আজ শিখলেন বা অ্যাপ্লাই করলেন?", value=existing_j['q2'] if existing_j else "")
            q3 = st.text_area("৩. নিজের কোডবেস বা ক্যারিয়ারের কোন কঠিন কাজটা আপনি এড়িয়ে যাওয়ার চেষ্টা করছেন?", value=existing_j['q3'] if existing_j else "")
            
            col_m, col_e = st.columns(2)
            with col_m:
                mood = st.slider("আজকের মেজাজ বা মানসিক অবস্থা (Mood: 1-10)", 1, 10, int(existing_j['mood']) if existing_j and existing_j['mood'] else 5)
            with col_e:
                energy = st.slider("আজকের এনার্জি বা কর্মক্ষমতা (Energy: 1-10)", 1, 10, int(existing_j['energy']) if existing_j and existing_j['energy'] else 5)
                
            if st.form_submit_button("চিন্তাগুলো সেভ করুন (Commit Entry)"):
                with get_db_connection() as conn:
                    conn.execute("""
                        INSERT INTO journal_entries (user_id, date, q1, q2, q3, mood, energy) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(date) DO UPDATE SET q1=excluded.q1, q2=excluded.q2, q3=excluded.q3, mood=excluded.mood, energy=excluded.energy
                    """, (user_id, today, q1, q2, q3, mood, energy))
                    conn.commit()
                st.success("আজকের রিফ্লেকশন ডাটাবেজে যুক্ত হয়েছে।")
                
    with tab3:
        st.subheader("মানসিক লোড কমানোর ক্যাশ মেমোরি (Brain Dump)")
        with get_db_connection() as conn:
            existing_bd = conn.execute("SELECT brain_dump FROM journal_entries WHERE user_id = ? AND date = ?", (user_id, today)).fetchone()
            
        bd_text = st.text_area("কাজের মাঝে মাথায় আসা যেকোনো এলোমেলো চিন্তা বা আইডিয়া এখানে লিখে মাথা হালকা করুন (যাতে ফোকাস নষ্ট না হয়):", 
                               value=existing_bd['brain_dump'] if (existing_bd and existing_bd['brain_dump']) else "", height=250)
        if st.button("মেমোরি ফ্লাশ করুন (Save Storage)"):
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO journal_entries (user_id, date, brain_dump) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(date) DO UPDATE SET brain_dump=excluded.brain_dump
                """, (user_id, today, bd_text))
                conn.commit()
            st.success("মানসিক ট্র্যাকিং সেভ করা হয়েছে।")

# --- MODULE 3: GOAL ARCHITECTURE ---
elif menu == "লক্ষ্য নির্ধারণ (Goal Architecture)":
    st.title("🎯 লং-টার্ম গোল ও মিশন কন্ট্রোল")
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        st.subheader("নতুন মিশন সেট করুন")
        with st.form("new_goal_form"):
            title = st.text_input("লক্ষ্য বা টার্গেটের নাম")
            category = st.selectbox("ক্যাটাগরি", ["Coding", "Finance", "Health", "Learning", "Social"])
            timeframe = st.selectbox("সময়সীমার ধরন", ["Daily", "Weekly", "Monthly", "Yearly"])
            deadline = st.date_input("ডেডলাইন বা শেষ সময়")
            if st.form_submit_button("মিশন চালু করুন") and title:
                with get_db_connection() as conn:
                    conn.execute("INSERT INTO goals (user_id, title, category, timeframe, progress, deadline) VALUES (?, ?, ?, ?, 0, ?)",
                                 (user_id, title, category, timeframe, deadline.strftime("%Y-%m-%d")))
                    conn.commit()
                st.success("নতুন গোল পাইপলাইনে যুক্ত হয়েছে।")
                st.rerun()

    with col_g2:
        st.subheader("সক্রিয় লক্ষ্যসমূহ")
        with get_db_connection() as conn:
            goals = conn.execute("SELECT * FROM goals WHERE user_id = ?", (user_id,)).fetchall()
        if not goals:
            st.info("বর্তমানে কোনো সক্রিয় দীর্ঘমেয়াদী লক্ষ্য নেই।")
        else:
            for g in goals:
                with st.expander(f"[{g['category']}] {g['title']} - {g['timeframe']}"):
                    prog = st.slider("কাজের অগ্রগতি (%)", 0, 100, int(g['progress']), key=f"prog_{g['id']}")
                    if prog != g['progress']:
                        with get_db_connection() as conn:
                            conn.execute("UPDATE goals SET progress = ? WHERE id = ?", (prog, g['id']))
                            conn.commit()
                        st.rerun()
                    if st.button("মিশন ডিলিট করুন", key=f"del_{g['id']}"):
                        with get_db_connection() as conn:
                            conn.execute("DELETE FROM goals WHERE id = ?", (g['id'],))
                            conn.commit()
                        st.rerun()

# --- MODULE 4: ADVANCED REPORTS & ANALYTICS ---
elif menu == "রিপোর্ট ও বোঝাপড়া (Advanced Reports)":
    st.title("📅 সময়ের সাথে কাজের প্রোগ্রেস ও রিপোর্ট")
    
    with get_db_connection() as conn:
        log_df = pd.read_sql_query("""
            SELECT hl.date, hl.completed, h.name as habit_name, h.category
            FROM habit_logs hl
            JOIN habits h ON hl.habit_id = h.id
            WHERE hl.user_id = ?
        """, conn, params=(user_id,))
        
        journal_df = pd.read_sql_query("""
            SELECT date, mood, energy FROM journal_entries WHERE user_id = ?
        """, conn, params=(user_id,))

    if log_df.empty:
        st.warning("রিপোর্ট জেনারেট করার জন্য এখনো পর্যাপ্ত ডাটা নেই। কিছুদিন রুটিন ট্র্যাক করুন।")
    else:
        st.write("আপনার কাজের অগ্রগতির ফ্রিকোয়েন্সি সিলেক্ট করুন:")
        timeframe_option = st.selectbox(
            "রিপোর্টের সময়সীমা নির্বাচন করুন", 
            ["Daily (দৈনিক)", "Weekly (সাপ্তাহিক)", "Monthly (মাসিক)", "Quarterly (ত্রৈমাসিক)", "Half-Yearly (ষাণ্মাসিক)", "Yearly (বার্ষিক)"]
        )
        
        # Mapping timeframe selection to Pandas Frequency Strings
        clean_option = timeframe_option.split(" ")[0]
        freq_mapping = {
            "Daily": "D",
            "Weekly": "W-MON", 
            "Monthly": "ME",   
            "Quarterly": "QE", 
            "Half-Yearly": "2QE", 
            "Yearly": "YE"     
        }
        pd_freq = freq_mapping[clean_option]

        log_df['date'] = pd.to_datetime(log_df['date'])
        
        # Time aggregation processing
        time_grouped = log_df.groupby(pd.Grouper(key='date', freq=pd_freq)).agg(
            total_tasks=('completed', 'count'),
            completed_tasks=('completed', 'sum')
        ).reset_index()
        
        time_grouped['completion_rate'] = (time_grouped['completed_tasks'] / time_grouped['total_tasks']) * 100
        time_grouped['period'] = time_grouped['date'].dt.strftime('%Y-%m-%d')
        
        st.markdown(f"### 📈 {clean_option} ধারাবাহিকতা রিপোর্ট")
        
        # Chart 1: Core Habit Metric Chart
        fig_time = px.bar(
            time_grouped, x='period', y='completion_rate', 
            text='completion_rate',
            labels={'period': 'সময়কাল', 'completion_rate': 'সাফল্যের হার (%)'},
            title=f"রুটিন সফলতার গ্রাফ ({clean_option})", 
            template="plotly_dark", color='completion_rate', color_continuous_scale="Teal"
        )
        fig_time.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_time, use_container_width=True)

        # Detailed Grid Data
        st.write(f"**{clean_option} বিস্তারিত ডাটা টেবিল (এখান থেকে ডাউনলোড করতে পারবেন):**")
        st.dataframe(time_grouped[['period', 'total_tasks', 'completed_tasks', 'completion_rate']].style.format({'completion_rate': "{:.2f}%"}), use_container_width=True)

        st.markdown("---")
        
        # Chart 2: Mood and Energy Tracking over selective periods
        if not journal_df.empty and not journal_df['mood'].isna().all():
            st.subheader(f"🧠 {clean_option} মেজাজ ও শক্তির গড় গ্রাফ (Bio-Trends)")
            journal_df['date'] = pd.to_datetime(journal_df['date'])
            journal_df['mood'] = pd.to_numeric(journal_df['mood'], errors='coerce')
            journal_df['energy'] = pd.to_numeric(journal_df['energy'], errors='coerce')
            
            journal_grouped = journal_df.groupby(pd.Grouper(key='date', freq=pd_freq))[['mood', 'energy']].mean().reset_index()
            journal_grouped['period'] = journal_grouped['date'].dt.strftime('%Y-%m-%d')
            journal_grouped = journal_grouped.dropna(subset=['mood', 'energy'])
            
            if not journal_grouped.empty:
                fig_bio = px.line(
                    journal_grouped, x='period', y=['mood', 'energy'], markers=True,
                    labels={'value': 'গড় স্কোর (1-10)', 'period': 'সময়কাল'},
                    title=f"মানসিক অবস্থা ও কাজের শক্তির ট্রেন্ডস ({clean_option} Average)", template="plotly_dark"
                )
                st.plotly_chart(fig_bio, use_container_width=True)
            else:
                st.info("আপনার দৈনিক মানসিক অবস্থা ট্র্যাক করার জন্য রুটিন ট্র্যাকারের 'আজকের আত্মচিন্তন' ট্যাবটি নিয়মিত পূরণ করুন।")
