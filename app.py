# ╔══════════════════════════════════════════════════════════════╗
# ║              DevLife OS  —  by a Developer, for Developers   ║
# ║   Stack: Streamlit · SQLite · Plotly · Pandas                ║
# ╚══════════════════════════════════════════════════════════════╝

import streamlit as st
import sqlite3
import hashlib
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import os

# ──────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DevLife OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
#  GLOBAL STYLES
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #080c14 !important;
    color: #dce7f3 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1220 0%, #080c14 100%) !important;
    border-right: 1px solid #1a2540 !important;
}
section[data-testid="stSidebar"] * { color: #c5d3e8 !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 0.88rem !important; }

/* ── Metric ── */
div[data-testid="stMetricValue"]  { color: #38bdf8 !important; font-weight: 800 !important; font-size: 1.9rem !important; }
div[data-testid="stMetricLabel"]  { color: #64748b !important; font-size: 0.78rem !important; letter-spacing: .5px; text-transform: uppercase; }
div[data-testid="stMetricDelta"]  { color: #34d399 !important; }
div[data-testid="metric-container"] {
    background: #0d1627;
    border: 1px solid #1e2d48;
    border-radius: 12px;
    padding: 18px 20px;
}

/* ── Cards ── */
.dv-card {
    background: linear-gradient(135deg, #0d1627 0%, #0a1020 100%);
    border: 1px solid #1e2d48;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 18px;
    box-shadow: 0 4px 24px rgba(0,0,0,.35);
}
.dv-card-teal  { border-left: 4px solid #2dd4bf; }
.dv-card-blue  { border-left: 4px solid #38bdf8; }
.dv-card-green { border-left: 4px solid #34d399; }
.dv-card-amber { border-left: 4px solid #fbbf24; }
.dv-card-red   { border-left: 4px solid #f87171; }
.dv-card-purple{ border-left: 4px solid #a78bfa; }

/* ── Quote Banner ── */
.quote-banner {
    background: linear-gradient(100deg, #0f2040 0%, #0a1830 60%, #071528 100%);
    border: 1px solid #1e3a5f;
    border-left: 5px solid #38bdf8;
    border-radius: 12px;
    padding: 22px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.quote-banner::before {
    content: '"';
    position: absolute;
    top: -10px; left: 16px;
    font-size: 100px;
    color: rgba(56,189,248,.08);
    font-family: Georgia, serif;
    line-height: 1;
}
.quote-text {
    font-size: 1.05rem;
    font-style: italic;
    color: #bae6fd;
    line-height: 1.65;
    margin: 0 0 8px 0;
}
.quote-author {
    font-size: 0.78rem;
    color: #38bdf8;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.quote-category {
    font-size: 0.7rem;
    color: #475569;
    margin-top: 2px;
}

/* ── Progress bar ── */
.pb-wrap  { background: #111c30; border-radius: 99px; height: 9px; overflow: hidden; margin: 6px 0 3px; }
.pb-fill  { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #0ea5e9, #2dd4bf); }

/* ── Tag pills ── */
.pill {
    display: inline-block; padding: 2px 11px;
    border-radius: 99px; font-size: 0.7rem; font-weight: 600;
    margin: 2px; letter-spacing: .3px;
}
.pill-teal   { background: #2dd4bf18; color: #2dd4bf; border: 1px solid #2dd4bf44; }
.pill-blue   { background: #38bdf818; color: #38bdf8; border: 1px solid #38bdf844; }
.pill-green  { background: #34d39918; color: #34d399; border: 1px solid #34d39944; }
.pill-amber  { background: #fbbf2418; color: #fbbf24; border: 1px solid #fbbf2444; }
.pill-red    { background: #f8717118; color: #f87171; border: 1px solid #f8717144; }
.pill-purple { background: #a78bfa18; color: #a78bfa; border: 1px solid #a78bfa44; }
.pill-slate  { background: #47556918; color: #94a3b8; border: 1px solid #47556944; }

/* ── Section header ── */
.sec-header {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #38bdf8;
    border-bottom: 1px solid #1e2d48;
    padding-bottom: 8px;
    margin: 24px 0 14px;
}

/* ── Streak badge ── */
.streak { display:inline-block; background:linear-gradient(135deg,#f97316,#fbbf24); color:#000;
          font-weight:700; font-size:.72rem; padding:2px 9px; border-radius:99px; }

/* ── Habit row ── */
.habit-row {
    background: #0d1627; border: 1px solid #1e2d48; border-radius: 9px;
    padding: 10px 14px; margin: 4px 0; display:flex; align-items:center;
}
.habit-done { opacity:.45; text-decoration:line-through; }

/* ── Buttons ── */
.stButton > button {
    background: #0d1627 !important; color: #38bdf8 !important;
    border: 1px solid #38bdf8 !important; border-radius: 8px !important;
    font-weight: 500 !important; transition: all .25s ease !important;
}
.stButton > button:hover {
    background: #38bdf8 !important; color: #080c14 !important;
    box-shadow: 0 0 16px rgba(56,189,248,.35) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]  { background:#0d1627; border-radius:10px; padding:4px; gap:3px; }
.stTabs [data-baseweb="tab"]       { border-radius:7px; color:#64748b; font-weight:500; font-size:.84rem; }
.stTabs [aria-selected="true"]     { background:#1e2d48 !important; color:#38bdf8 !important; }

/* ── Inputs ── */
input, textarea, select, .stTextInput input, .stTextArea textarea {
    background: #0d1627 !important; border: 1px solid #1e2d48 !important;
    color: #dce7f3 !important; border-radius: 8px !important; font-family:'Inter',sans-serif !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] { background:#0d1627; border:1px solid #1e2d48; border-radius:10px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#080c14; }
::-webkit-scrollbar-thumb { background:#1e2d48; border-radius:99px; }

/* ── Logo text ── */
.logo-text { font-size:1.25rem; font-weight:800; color:#38bdf8; letter-spacing:-0.5px; }
.logo-sub  { font-size:.7rem; color:#475569; letter-spacing:1.5px; text-transform:uppercase; }

/* ── Greeting ── */
.greeting-name { color:#38bdf8; font-weight:800; }
.greeting-date { color:#475569; font-size:.85rem; }

/* ── Big number ── */
.big-number { font-size:2.6rem; font-weight:800; line-height:1; }

/* ── Mono ── */
.mono { font-family:'JetBrains Mono',monospace; }

hr { border-color: #1a2540 !important; }

/* ── hide streamlit default header ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  DATABASE
# ──────────────────────────────────────────────────────────────
DB_FILE = "devlife_os.db"

def conn():
    c = sqlite3.connect(DB_FILE, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'Developer',
            stack TEXT DEFAULT 'React / PHP / Python',
            created_at TEXT DEFAULT (date('now'))
        );
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, name TEXT, category TEXT, slot TEXT
        );
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, habit_id INTEGER,
            date TEXT, completed INTEGER DEFAULT 0,
            UNIQUE(user_id, habit_id, date)
        );
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, title TEXT, category TEXT,
            timeframe TEXT, progress INTEGER DEFAULT 0,
            deadline TEXT, status TEXT DEFAULT 'active'
        );
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, date TEXT,
            q1 TEXT, q2 TEXT, q3 TEXT, brain_dump TEXT,
            mood INTEGER DEFAULT 5, energy INTEGER DEFAULT 5,
            UNIQUE(user_id, date)
        );
        CREATE TABLE IF NOT EXISTS daily_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, date TEXT,
            deep_work_hrs REAL DEFAULT 0,
            coding_hrs REAL DEFAULT 0,
            exercise_mins INTEGER DEFAULT 0,
            sleep_hrs REAL DEFAULT 0,
            UNIQUE(user_id, date)
        );
        CREATE TABLE IF NOT EXISTS skill_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, skill TEXT,
            rating INTEGER, month INTEGER, year INTEGER,
            UNIQUE(user_id, skill, month, year)
        );
        """)
        
        # ── AUTOMATIC MIGRATIONS FOR OLD DATABASES ──
        cursor = db.cursor()
        
        # Patch the 'users' table if it's missing columns from an old run
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [row[1] for row in cursor.fetchall()]
        if "role" not in user_columns:
            db.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'Developer'")
        if "stack" not in user_columns:
            db.execute("ALTER TABLE users ADD COLUMN stack TEXT DEFAULT 'React / PHP / Python'")
            
        # Patch the 'habits' table if it's missing the 'slot' column
        cursor.execute("PRAGMA table_info(habits)")
        habit_columns = [row[1] for row in cursor.fetchall()]
        if "slot" not in habit_columns:
            db.execute("ALTER TABLE habits ADD COLUMN slot TEXT DEFAULT 'Morning'")

        # Patch the 'goals' table if it's missing the 'status' column (Fixes your current error)
        cursor.execute("PRAGMA table_info(goals)")
        goal_columns = [row[1] for row in cursor.fetchall()]
        if "status" not in goal_columns:
            db.execute("ALTER TABLE goals ADD COLUMN status TEXT DEFAULT 'active'")

init_db()

# ──────────────────────────────────────────────────────────────
#  AUTH
# ──────────────────────────────────────────────────────────────
def make_hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

DEFAULT_HABITS = [
    # (name, category, slot)
    # 🌅 Morning Routine — সকালের রুটিন
    ("No Phone First 30 Mins — ঘুম থেকে উঠে প্রথম ৩০ মিনিট ফোন না ধরা", "Mental", "Morning"),
    ("10 Min Stillness/Breathing — ১০ মিনিট চুপচাপ বসা বা প্রাণায়াম/Breathing", "Mental", "Morning"),
    ("Read 10 Verses of Quran — প্রতিদিন ১০ টি আয়াত কুরআন পাঠ", "Mental", "Morning"),  # <-- এখানে যুক্ত করা হয়েছে
    ("Physical Activation (15m) — শরীর সচল করা (১৫ মিনিট হালকা ব্যায়াম)", "Health", "Morning"),
    ("Deep Learning Block (60m) — গভীর মনোযোগ দিয়ে নতুন কিছু শেখা (১ ঘণ্টা)", "Coding", "Morning"),
    ("High-Protein Screenless Breakfast — স্ক্রিন ছাড়া পুষ্টিকর নাস্তা খাওয়া", "Health", "Morning"),
    ("Plan the day — write your MIT — দিনের পরিকল্পনা ও প্রধান কাজ নির্ধারণ", "Mental", "Morning"),

    # 💻 Work Routine — কাজের রুটিন
    ("Deep Work Block 1 (Hard Code) — কঠিন কোডিং ও লজিক সমাধান", "Coding", "Work"),
    ("Reactive Tasks Window — ইমেইল, মেসেজ ও কোড রিভিউ চেক করার সময়", "Coding", "Work"),
    ("Disconnect & Walk Lunch — মোবাইল-ল্যাপটপ ছাড়া দুপুরের খাবার ও হাঁটা", "Health", "Work"),
    ("Project / Build Time — পার্সোনাল প্রজেক্ট বা নতুন কিছু বিল্ড করার সময়", "Coding", "Work"),
    ("Shutdown Ritual executed — দিনের কাজ শেষ করার রিল্যাক্সিং রুটিন", "Mental", "Work"),

    # 💪 Fitness Routine — শারীরিক ব্যায়াম
    ("Post-Work Decompression Walk — কাজ শেষে মাথা ফ্রেশ করার জন্য হাঁটা", "Health", "Fitness"),
    ("Posterior Chain / Strength Training — পিঠ, কোমর ও শারীরিক শক্তির ব্যায়াম", "Health", "Fitness"),
    ("Wrist & posture stretch — কব্জি এবং বসার ভঙ্গি বা পোস্টার স্ট্রেচিং", "Health", "Fitness"),

    # 📖 Learning — পড়ালেখা
    ("Read 5 pages of a book — প্রতিদিন ৫ পৃষ্ঠা বই পাঠ", "Mental", "Learning"),  # <-- এখানে যুক্ত করা হয়েছে
    ("Read technical book — 30 min — টেকনিক্যাল বই পড়া (৩০ মিনিট)", "Coding", "Learning"),
    ("Write or post about what you learned — যা শিখলেন তা নিয়ে পোস্ট করা", "Coding", "Learning"),

    # 🌙 Night Routine — রাতের রুটিন
    ("Digital Sunset @ 9:00 PM — রাত ৯:০০ টায় সব ডিভাইস/স্ক্রিন বন্ধ করা", "Mental", "Night"),
    ("Night reflection — 3 questions — রাতের আত্মচিন্তন (৩টি প্রশ্ন)", "Mental", "Night"),
    ("In bed by 10:15 PM — রাত ১০:১৫ এর মধ্যে বিছানায় যাওয়া", "Health", "Night"),
]

def seed_habits(uid):
    with conn() as db:
        db.executemany(
            "INSERT INTO habits (user_id,name,category,slot) VALUES (?,?,?,?)",
            [(uid, n, c, s) for n, c, s in DEFAULT_HABITS],
        )

def register_user(username, password, role, stack):
    try:
        with conn() as db:
            cur = db.execute(
                "INSERT INTO users (username,password_hash,role,stack) VALUES (?,?,?,?)",
                (username, make_hash(password), role, stack),
            )
            seed_habits(cur.lastrowid)
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "Username already taken."

def login_user(username, password):
    with conn() as db:
        row = db.execute(
            "SELECT * FROM users WHERE username=? AND password_hash=?",
            (username, make_hash(password)),
        ).fetchone()
    return row


# ──────────────────────────────────────────────────────────────
#  QUOTES  (expanded, categorised, daily-rotating)
# ──────────────────────────────────────────────────────────────
QUOTES = [
    # Coding
    ("Code is the most leveraged skill in human history. One developer can build something used by millions.",
     "DevLife OS", "Coding"),
    ("Build things. Don't just learn things. Real skill lives in projects that break and force you to figure it out.",
     "DevLife OS", "Coding"),
    ("First make it work. Then make it right. Then make it fast — in that order, always.",
     "Kent Beck", "Coding"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.",
     "Harold Abelson", "Coding"),
    ("Simplicity is the soul of efficiency. Delete before you add.",
     "Austin Freeman", "Coding"),
    ("The best code is no code at all. Every line you write is a liability.",
     "Jeff Atwood", "Coding"),
    ("Talk is cheap. Show me the code.",
     "Linus Torvalds", "Coding"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
     "Martin Fowler", "Coding"),
    # Mindset
    ("Your brain is your IDE. Sleep, nutrition, and movement are not lifestyle choices — they are performance configuration.",
     "DevLife OS", "Mindset"),
    ("Small daily inputs create massive long-term outputs. The math of compounding always wins.",
     "DevLife OS", "Mindset"),
    ("Think in years, not weeks. The developer earning $200K is rarely more talented — they just have a longer time horizon.",
     "DevLife OS", "Mindset"),
    ("Depth beats breadth. Pick one stack, go uncomfortably deep, then learn everything adjacent fast.",
     "DevLife OS", "Mindset"),
    ("Identity before behaviour. Don't say 'I want to code.' Say 'I am someone who builds every day.'",
     "DevLife OS", "Mindset"),
    ("The gap between knowing and doing is where the life you want actually lives.",
     "DevLife OS", "Mindset"),
    ("Pressure is a privilege. It means something is at stake.",
     "Billie Jean King", "Mindset"),
    ("Do not wait; the time will never be just right. Start where you stand.",
     "Napoleon Hill", "Mindset"),
    ("You don't rise to the level of your goals. You fall to the level of your systems.",
     "James Clear", "Mindset"),
    # Health & Energy
    ("Sleep is not a cost. It is your nightly performance upgrade. Protect it like a production server.",
     "DevLife OS", "Health"),
    ("Movement is medicine for the brain. A 30-minute walk produces more creative output than an extra hour at the desk.",
     "DevLife OS", "Health"),
    ("Energy is the real currency — not time. A well-rested 5 hours beats a sleep-deprived 10, every single time.",
     "DevLife OS", "Health"),
    ("Take care of your body. It's the only place you have to live.",
     "Jim Rohn", "Health"),
    # Finance & Career
    ("A developer who earns $60K and invests 30% will outperform one who earns $120K and spends it all.",
     "DevLife OS", "Finance"),
    ("Your portfolio is your loudest voice. Ship work that speaks before you enter the room.",
     "DevLife OS", "Career"),
    ("The expert in anything was once a beginner who refused to quit.",
     "Helen Hayes", "Career"),
    ("Write about what you know before you feel ready. Teaching forces clarity that study alone never gives.",
     "DevLife OS", "Career"),
    ("Success is not about working hard in silence. Ship in public. Learn in public. Grow in public.",
     "DevLife OS", "Career"),
    # Philosophy
    ("We are what we repeatedly do. Excellence, then, is not an act but a habit.",
     "Aristotle", "Philosophy"),
    ("It does not matter how slowly you go as long as you do not stop.",
     "Confucius", "Philosophy"),
    ("The secret of getting ahead is getting started.",
     "Mark Twain", "Philosophy"),
    ("Discipline is the bridge between goals and accomplishment.",
     "Jim Rohn", "Philosophy"),
    ("An investment in knowledge pays the best interest.",
     "Benjamin Franklin", "Philosophy"),
]

CAT_PILL = {
    "Coding":     "pill-blue",
    "Mindset":    "pill-teal",
    "Health":     "pill-green",
    "Finance":    "pill-amber",
    "Career":     "pill-purple",
    "Philosophy": "pill-slate",
}

def daily_quote():
    """Return a deterministic daily quote, cycling through all."""
    idx = datetime.date.today().toordinal() % len(QUOTES)
    return QUOTES[idx]

def random_quote_by_cat(cat):
    pool = [q for q in QUOTES if q[2] == cat]
    return random.choice(pool) if pool else random.choice(QUOTES)


# ──────────────────────────────────────────────────────────────
#  UI HELPERS
# ──────────────────────────────────────────────────────────────
SLOT_ICONS = {"Morning": "🌅", "Work": "💻", "Fitness": "💪", "Learning": "📖", "Night": "🌙"}
CAT_COLORS = {
    "Mental": "#38bdf8", "Health": "#34d399", "Coding": "#a78bfa",
    "Morning": "#fbbf24", "Work": "#38bdf8", "Fitness": "#34d399",
    "Learning": "#2dd4bf", "Night": "#f87171",
    "Daily": "#38bdf8", "Weekly": "#34d399", "Monthly": "#a78bfa", "Yearly": "#fbbf24",
    "Coding_g": "#a78bfa", "Finance": "#fbbf24", "Health_g": "#34d399",
    "Learning_g": "#2dd4bf", "Social": "#f87171",
}

def pbar(pct, color="#38bdf8"):
    pct = min(max(float(pct), 0), 100)
    return (f'<div class="pb-wrap"><div class="pb-fill" '
            f'style="width:{pct:.1f}%;background:linear-gradient(90deg,{color},{color}aa)"></div></div>'
            f'<small style="color:#475569">{pct:.0f}%</small>')

def mbox(value, label, color="#38bdf8", delta=None):
    d = f'<div style="color:#34d399;font-size:.78rem;margin-top:2px">{delta}</div>' if delta else ""
    return (f'<div style="background:#0d1627;border:1px solid #1e2d48;border-radius:12px;'
            f'padding:18px 16px;text-align:center">'
            f'<div style="font-size:2rem;font-weight:800;color:{color}">{value}</div>'
            f'<div style="font-size:.72rem;color:#475569;letter-spacing:.8px;text-transform:uppercase;margin-top:4px">{label}</div>'
            f'{d}</div>')

def quote_card(text, author, category):
    pill_cls = CAT_PILL.get(category, "pill-slate")
    return f"""
    <div class="quote-banner">
        <p class="quote-text">{text}</p>
        <div style="display:flex;align-items:center;gap:10px;margin-top:8px">
            <span class="quote-author">— {author}</span>
            <span class="pill {pill_cls}">{category}</span>
        </div>
    </div>"""

def section(title):
    st.markdown(f'<div class="sec-header">{title}</div>', unsafe_allow_html=True)

def pill(label, cls="pill-blue"):
    return f'<span class="pill {cls}">{label}</span>'

def chart_theme(fig):
    fig.update_layout(
        paper_bgcolor="#080c14", plot_bgcolor="#0d1627",
        font=dict(color="#94a3b8", family="Inter"),
        legend=dict(bgcolor="#0d1627", bordercolor="#1e2d48"),
        margin=dict(t=36, b=20, l=16, r=16),
        xaxis=dict(gridcolor="#1e2d48", linecolor="#1e2d48"),
        yaxis=dict(gridcolor="#1e2d48", linecolor="#1e2d48"),
    )
    return fig


# ──────────────────────────────────────────────────────────────
#  DATA FUNCTIONS
# ──────────────────────────────────────────────────────────────
def get_habits(uid):
    with conn() as db:
        return db.execute("SELECT * FROM habits WHERE user_id=?", (uid,)).fetchall()

def ensure_today_logs(uid, today):
    with conn() as db:
        habits = db.execute("SELECT id FROM habits WHERE user_id=?", (uid,)).fetchall()
        for h in habits:
            db.execute(
                "INSERT OR IGNORE INTO habit_logs (user_id,habit_id,date,completed) VALUES (?,?,?,0)",
                (uid, h["id"], today),
            )

def get_logs(uid, today):
    with conn() as db:
        return db.execute("""
            SELECT hl.id, hl.completed, h.name, h.slot, h.category
            FROM habit_logs hl JOIN habits h ON hl.habit_id=h.id
            WHERE hl.user_id=? AND hl.date=?
            ORDER BY h.slot, h.name
        """, (uid, today)).fetchall()

def set_log(log_id, val):
    with conn() as db:
        db.execute("UPDATE habit_logs SET completed=? WHERE id=?", (val, log_id))

def streak(uid, habit_id):
    with conn() as db:
        rows = db.execute("""
            SELECT date FROM habit_logs WHERE user_id=? AND habit_id=? AND completed=1
            ORDER BY date DESC
        """, (uid, habit_id)).fetchall()
    if not rows:
        return 0
    dates = [datetime.date.fromisoformat(r["date"]) for r in rows]
    s, expected = 0, datetime.date.today()
    for d in dates:
        if d == expected or (s == 0 and d == expected - datetime.timedelta(days=1)):
            s += 1
            expected = d - datetime.timedelta(days=1)
        else:
            break
    return s

def comp_rate(uid, days=7):
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    with conn() as db:
        total_h = db.execute("SELECT COUNT(*) FROM habits WHERE user_id=?", (uid,)).fetchone()[0]
        if total_h == 0:
            return 0.0
        done = db.execute(
            "SELECT COUNT(*) FROM habit_logs WHERE user_id=? AND completed=1 AND date>=?",
            (uid, since),
        ).fetchone()[0]
    return round(done / (total_h * days) * 100, 1)

def get_goals(uid, timeframe=None, status="active"):
    with conn() as db:
        if timeframe:
            return db.execute(
                "SELECT * FROM goals WHERE user_id=? AND timeframe=? AND status=? ORDER BY deadline",
                (uid, timeframe, status),
            ).fetchall()
        return db.execute(
            "SELECT * FROM goals WHERE user_id=? AND status=? ORDER BY timeframe,deadline",
            (uid, status),
        ).fetchall()

def save_journal(uid, date, q1, q2, q3, bd, mood, energy):
    with conn() as db:
        db.execute("""
            INSERT INTO journal_entries (user_id,date,q1,q2,q3,brain_dump,mood,energy)
            VALUES (?,?,?,?,?,?,?,?)
            ON CONFLICT(user_id,date) DO UPDATE SET
            q1=excluded.q1,q2=excluded.q2,q3=excluded.q3,
            brain_dump=excluded.brain_dump,mood=excluded.mood,energy=excluded.energy
        """, (uid, date, q1, q2, q3, bd, mood, energy))

def get_journal(uid, date):
    with conn() as db:
        return db.execute(
            "SELECT * FROM journal_entries WHERE user_id=? AND date=?", (uid, date)
        ).fetchone()

def save_metrics(uid, date, dw, code, ex, sl):
    with conn() as db:
        db.execute("""
            INSERT INTO daily_metrics (user_id,date,deep_work_hrs,coding_hrs,exercise_mins,sleep_hrs)
            VALUES (?,?,?,?,?,?)
            ON CONFLICT(user_id,date) DO UPDATE SET
            deep_work_hrs=excluded.deep_work_hrs,coding_hrs=excluded.coding_hrs,
            exercise_mins=excluded.exercise_mins,sleep_hrs=excluded.sleep_hrs
        """, (uid, date, dw, code, ex, sl))

def get_metrics_df(uid, days=30):
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    with conn() as db:
        return pd.read_sql_query(
            "SELECT * FROM daily_metrics WHERE user_id=? AND date>=? ORDER BY date",
            db, params=(uid, since),
        )

def get_heatmap_df(uid, days=90):
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    with conn() as db:
        total = db.execute("SELECT COUNT(*) FROM habits WHERE user_id=?", (uid,)).fetchone()[0]
        df = pd.read_sql_query("""
            SELECT date, SUM(completed) as done FROM habit_logs
            WHERE user_id=? AND date>=? GROUP BY date ORDER BY date
        """, db, params=(uid, since))
    if df.empty or total == 0:
        return df
    df["pct"] = (df["done"] / total * 100).round(1)
    return df

def get_journal_df(uid, days=30):
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    with conn() as db:
        return pd.read_sql_query(
            "SELECT * FROM journal_entries WHERE user_id=? AND date>=? ORDER BY date",
            db, params=(uid, since),
        )

def get_skill_df(uid):
    with conn() as db:
        return pd.read_sql_query(
            "SELECT * FROM skill_ratings WHERE user_id=? ORDER BY year,month",
            db, params=(uid,),
        )

def save_skill(uid, skill, rating, month, year):
    with conn() as db:
        db.execute("""
            INSERT INTO skill_ratings (user_id,skill,rating,month,year) VALUES (?,?,?,?,?)
            ON CONFLICT(user_id,skill,month,year) DO UPDATE SET rating=excluded.rating
        """, (uid, skill, rating, month, year))


# ──────────────────────────────────────────────────────────────
#  AUTH PAGE
# ──────────────────────────────────────────────────────────────
def page_auth():
    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        st.markdown("""
        <div style="text-align:center;padding:40px 0 20px">
            <div style="font-size:3.5rem;margin-bottom:6px">⚡</div>
            <div style="font-size:2.2rem;font-weight:800;color:#38bdf8;letter-spacing:-1px">DevLife OS</div>
            <div style="color:#475569;font-size:.88rem;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px">
                Developer Success System
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show daily quote on login screen too
        qt, qa, qc = daily_quote()
        st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

        t_in, t_up = st.tabs(["🔑  Sign In", "🚀  Create Account"])

        with t_in:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("login_form"):
                u = st.text_input("Username", placeholder="your_username")
                p = st.text_input("Password", type="password", placeholder="••••••••")
                if st.form_submit_button("Login →", use_container_width=True):
                    user = login_user(u, p)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id   = user["id"]
                        st.session_state.username  = user["username"]
                        st.session_state.role      = user["role"]
                        st.session_state.stack     = user["stack"]
                        st.rerun()
                    else:
                        st.error("Wrong username or password.")

        with t_up:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("reg_form"):
                c1, c2 = st.columns(2)
                nu = c1.text_input("Username *")
                np1 = c2.text_input("Password *", type="password")
                np2 = st.text_input("Confirm Password *", type="password")
                role = st.selectbox("I am a …", [
                    "Junior Developer", "Mid-level Developer",
                    "Senior Developer", "Full-stack Developer", "Student",
                ])
                stack = st.multiselect("Primary Stack", [
                    "React", "PHP", "Python", "Laravel", "Next.js",
                    "Django", "FastAPI", "TypeScript", "Node.js", "Vue",
                ], default=["React", "PHP", "Python"])
                if st.form_submit_button("Create Account →", use_container_width=True):
                    if len(np1) < 6:
                        st.error("Password must be 6+ characters.")
                    elif np1 != np2:
                        st.error("Passwords do not match.")
                    elif not nu:
                        st.error("Username required.")
                    else:
                        ok, msg = register_user(nu, np1, role, ", ".join(stack))
                        st.success(msg) if ok else st.error(msg)


# ──────────────────────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────────────────────
def render_sidebar():
    uid   = st.session_state.user_id
    uname = st.session_state.username
    today = datetime.date.today().isoformat()
    ensure_today_logs(uid, today)
    logs  = get_logs(uid, today)
    total = len(logs)
    done  = sum(1 for l in logs if l["completed"])
    pct   = done / total * 100 if total else 0
    bar_color = "#34d399" if pct >= 75 else "#fbbf24" if pct >= 40 else "#f87171"

    with st.sidebar:
        st.markdown(f"""
        <div style="padding:16px 0 10px;text-align:center">
            <div style="font-size:2rem;margin-bottom:4px">⚡</div>
            <div class="logo-text">DevLife OS</div>
            <div class="logo-sub">Developer Success System</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#111c30;border:1px solid #1e2d48;border-radius:10px;
                    padding:12px 14px;margin:10px 0 6px">
            <div style="font-size:.9rem;font-weight:700;color:#dce7f3">👤 {uname}</div>
            <div style="font-size:.73rem;color:#475569;margin-top:2px">
                {st.session_state.role} · {st.session_state.stack[:30]}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center;margin:10px 0 4px">
            <div style="font-size:.68rem;color:#475569;letter-spacing:1px;text-transform:uppercase">Today</div>
            <div style="font-size:1.7rem;font-weight:800;color:{bar_color};line-height:1.1">{pct:.0f}%</div>
            <div style="background:#111c30;border-radius:99px;height:7px;overflow:hidden;margin:4px 0 2px">
                <div style="height:100%;border-radius:99px;background:{bar_color};width:{pct:.0f}%"></div>
            </div>
            <div style="font-size:.7rem;color:#475569">{done}/{total} habits</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        selected = st.radio("Navigate", [
            "🏠  Dashboard",
            "📋  Daily Routine",
            "🎯  Goals",
            "🔥  Habits",
            "📊  Reviews",
            "📚  Skills & Roadmap",
            "💰  Finance Tips",
            "👤  Profile",
        ], label_visibility="collapsed")
        st.markdown("---")

        # Mini quote in sidebar
        qt, qa, _ = random_quote_by_cat("Mindset")
        st.markdown(f"""
        <div style="background:#111c30;border:1px solid #1e2d48;border-radius:8px;
                    padding:10px 12px;margin-top:4px">
            <div style="font-size:.72rem;color:#94a3b8;font-style:italic;line-height:1.5">"{qt[:110]}…"</div>
            <div style="font-size:.65rem;color:#38bdf8;margin-top:5px">— {qa}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True):
            for k in ["logged_in","user_id","username","role","stack"]:
                st.session_state.pop(k, None)
            st.rerun()

    return selected.strip().split("  ", 1)[-1]  # clean label


# ──────────────────────────────────────────────────────────────
#  PAGE: DASHBOARD
# ──────────────────────────────────────────────────────────────
def page_dashboard():
    uid   = st.session_state.user_id
    uname = st.session_state.username
    today = datetime.date.today()
    today_str = today.isoformat()
    ensure_today_logs(uid, today_str)
    logs  = get_logs(uid, today_str)
    total = len(logs)
    done  = sum(1 for l in logs if l["completed"])
    pct   = round(done / total * 100) if total else 0

    hour  = datetime.datetime.now().hour
    greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"

    # Header
    st.markdown(f"""
    <div class="dv-card dv-card-blue" style="margin-top:4px">
        <h2 style="margin:0;font-size:1.6rem;font-weight:800;color:#dce7f3">
            {greet}, <span class="greeting-name">{uname}</span> 👋
        </h2>
        <p class="greeting-date" style="margin:5px 0 0">
            {today.strftime("%A, %B %d %Y")}
            &nbsp;·&nbsp; {st.session_state.role}
            &nbsp;·&nbsp; Stack: <span style="color:#38bdf8">{st.session_state.stack}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Daily rotating quote
    qt, qa, qc = daily_quote()
    st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

    # ── KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(mbox(f"{pct}%",                        "Today's Completion",  "#38bdf8"), unsafe_allow_html=True)
    c2.markdown(mbox(f"{done}/{total}",                "Habits Done Today",   "#34d399"), unsafe_allow_html=True)
    c3.markdown(mbox(f"{comp_rate(uid,7)}%",           "7-Day Average",       "#fbbf24"), unsafe_allow_html=True)
    c4.markdown(mbox(str(len(get_goals(uid))),         "Active Goals",        "#a78bfa"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    # ── Habit checklist
    with left:
        section("⚡  Today's Habit Checklist")
        if not logs:
            st.info("No habits found. They are seeded automatically on registration.")
        else:
            for slot, slot_name in [("Morning","Morning"),("Work","Work"),
                                    ("Fitness","Fitness"),("Learning","Learning"),("Night","Night")]:
                slot_logs = [l for l in logs if l["slot"] == slot]
                if not slot_logs:
                    continue
                st.markdown(f"**{SLOT_ICONS.get(slot,'')} {slot_name}**")
                for log in slot_logs:
                    cb, lbl = st.columns([1, 10])
                    checked = cb.checkbox("", value=bool(log["completed"]),
                                          key=f"dash_{log['id']}")
                    style = "color:#475569;text-decoration:line-through" if checked else "color:#dce7f3"
                    lbl.markdown(f'<span style="{style};font-size:.87rem">{log["name"]}</span>',
                                 unsafe_allow_html=True)
                    if checked != bool(log["completed"]):
                        set_log(log["id"], int(checked))
                        st.rerun()

    # ── Goals + Quick log
    with right:
        section("🎯  Active Goals")
        goals = get_goals(uid)
        if not goals:
            st.info("No goals yet — create some in Goals.")
        else:
            tf_colors = {"Daily":"#38bdf8","Weekly":"#34d399","Monthly":"#a78bfa","Yearly":"#fbbf24"}
            for g in list(goals)[:5]:
                gp = min(g["progress"], 100)
                color = tf_colors.get(g["timeframe"], "#38bdf8")
                st.markdown(f"""
                <div style="margin-bottom:14px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
                        <span style="font-size:.83rem;color:#dce7f3">{g['title']}</span>
                        <span class="pill pill-{'blue' if g['timeframe']=='Daily' else 'green' if g['timeframe']=='Weekly' else 'purple' if g['timeframe']=='Monthly' else 'amber'}">{g['timeframe']}</span>
                    </div>
                    {pbar(gp, color)}
                </div>""", unsafe_allow_html=True)

        section("📊  Quick Daily Log")
        with st.form("quick_log"):
            dw = st.slider("💻 Deep Work (hrs)", 0.0, 12.0, 3.0, 0.5)
            ex = st.slider("💪 Exercise (min)",  0, 180, 30, 5)
            sl = st.slider("😴 Sleep (hrs)",     4.0, 10.0, 7.5, 0.25)
            if st.form_submit_button("Save →", use_container_width=True):
                save_metrics(uid, today_str, dw, dw, ex, sl)
                st.success("Saved!")


# ──────────────────────────────────────────────────────────────
#  PAGE: DAILY ROUTINE
# ──────────────────────────────────────────────────────────────
def page_daily():
    uid = st.session_state.user_id
    st.markdown("## 📋 Daily Routine Tracker")

    sel     = st.date_input("Date", value=datetime.date.today(), max_value=datetime.date.today())
    sel_str = sel.isoformat()
    ensure_today_logs(uid, sel_str)

    t1, t2, t3 = st.tabs(["✅  Habits", "📝  Journal", "📊  Metrics"])

    with t1:
        logs  = get_logs(uid, sel_str)
        total = len(logs)
        done  = sum(1 for l in logs if l["completed"])
        pct_v = done / total * 100 if total else 0
        st.markdown(f"""<div class="dv-card dv-card-blue">
            <b style="color:#dce7f3">{done}/{total} habits — {sel.strftime("%b %d, %Y")}</b>
            {pbar(pct_v)}</div>""", unsafe_allow_html=True)

        for slot, _ in [("Morning",""),("Work",""),("Fitness",""),("Learning",""),("Night","")]:
            slot_logs = [l for l in logs if l["slot"] == slot]
            if not slot_logs:
                continue
            section(f"{SLOT_ICONS.get(slot,'')}  {slot} Routine")
            for log in slot_logs:
                with st.expander(f"{log['name']}  {'✅' if log['completed'] else '⬜'}"):
                    checked = st.checkbox("Mark complete", value=bool(log["completed"]),
                                          key=f"rout_{sel_str}_{log['id']}")
                    if st.button("Save", key=f"save_{sel_str}_{log['id']}"):
                        set_log(log["id"], int(checked))
                        st.success("Saved!")
                        st.rerun()

    with t2:
        section("📝  Daily Journal — 5 Developer Questions")
        ex = get_journal(uid, sel_str)

        # Quote for journaling context
        qt, qa, qc = random_quote_by_cat("Mindset")
        st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

        with st.form("journal_form"):
            c1, c2 = st.columns(2)
            with c1:
                q1 = st.text_area("🙏 What are you grateful for today?",           value=ex["q1"] if ex else "", height=90)
                q2 = st.text_area("🎯 What technical problem must you solve today?", value=ex["q2"] if ex else "", height=90)
                q3 = st.text_area("⚠️ What hard task are you avoiding in your codebase?", value=ex["q3"] if ex else "", height=90)
            with c2:
                bd = st.text_area("🧠 Brain Dump — ideas, thoughts, anything on your mind", value=ex["brain_dump"] if ex else "", height=200)
            mc, ec = st.columns(2)
            mood   = mc.slider("😊 Mood (1–10)",   1, 10, int(ex["mood"])   if ex else 7)
            energy = ec.slider("⚡ Energy (1–10)", 1, 10, int(ex["energy"]) if ex else 7)
            if st.form_submit_button("💾 Commit Journal Entry", use_container_width=True):
                save_journal(uid, sel_str, q1, q2, q3, bd, mood, energy)
                st.success("Journal saved!")

    with t3:
        section("📊  Log Performance Metrics")
        with conn() as db:
            em = db.execute(
                "SELECT * FROM daily_metrics WHERE user_id=? AND date=?", (uid, sel_str)
            ).fetchone()
        with st.form("metrics_form"):
            c1, c2 = st.columns(2)
            with c1:
                dw   = st.number_input("💻 Deep Work (hrs)",   0.0, 16.0, float(em["deep_work_hrs"])  if em else 0.0, 0.5)
                code = st.number_input("⌨️ Coding (hrs)",      0.0, 16.0, float(em["coding_hrs"])     if em else 0.0, 0.5)
            with c2:
                ex   = st.number_input("💪 Exercise (min)",    0,   300,  int(em["exercise_mins"])    if em else 0,   5)
                sl   = st.number_input("😴 Sleep (hrs)",       0.0, 12.0, float(em["sleep_hrs"])      if em else 7.0, 0.25)
            if st.form_submit_button("💾 Save Metrics", use_container_width=True):
                save_metrics(uid, sel_str, dw, code, ex, sl)
                st.success("Metrics saved!")


# ──────────────────────────────────────────────────────────────
#  PAGE: GOALS
# ──────────────────────────────────────────────────────────────
def page_goals():
    uid = st.session_state.user_id
    st.markdown("## 🎯 Goal Management")
    t1, t2, t3 = st.tabs(["📋  Active Goals", "➕  New Goal", "✅  Completed"])

    tf_icons  = {"Daily":"📅","Weekly":"📆","Monthly":"🗓️","Yearly":"🏆"}
    tf_pills  = {"Daily":"pill-blue","Weekly":"pill-green","Monthly":"pill-purple","Yearly":"pill-amber"}
    cat_pills = {"Coding":"pill-blue","Finance":"pill-amber","Health":"pill-green",
                 "Learning":"pill-teal","Social":"pill-red","General":"pill-slate"}

    with t1:
        tf = st.selectbox("Filter", ["All","Daily","Weekly","Monthly","Yearly"])
        goals = get_goals(uid) if tf == "All" else get_goals(uid, tf)

        if not goals:
            st.info("No active goals. Create one in the 'New Goal' tab.")
        else:
            for tf_label in (["Daily","Weekly","Monthly","Yearly"] if tf=="All" else [tf]):
                sub = [g for g in goals if g["timeframe"] == tf_label]
                if not sub:
                    continue
                section(f"{tf_icons.get(tf_label,'🎯')}  {tf_label} Goals")
                for g in sub:
                    gp = min(g["progress"], 100)
                    with st.expander(f"{g['title']}  —  {gp}%"):
                        st.markdown(
                            f'<span class="pill {cat_pills.get(g["category"],"pill-slate")}">{g["category"]}</span>'
                            f'<span class="pill {tf_pills.get(g["timeframe"],"pill-slate")}">{g["timeframe"]}</span>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(pbar(gp, CAT_COLORS.get(g["timeframe"],"#38bdf8")), unsafe_allow_html=True)
                        if g["deadline"]:
                            dl = datetime.date.fromisoformat(g["deadline"])
                            days_left = (dl - datetime.date.today()).days
                            dl_col = "#34d399" if days_left > 7 else "#fbbf24" if days_left >= 0 else "#f87171"
                            st.markdown(f'<span style="color:{dl_col};font-size:.83rem">⏰ '
                                        f'{"In " + str(days_left) + " days" if days_left >= 0 else str(abs(days_left)) + " days overdue"}'
                                        f'</span>', unsafe_allow_html=True)
                        uc, dc = st.columns(2)
                        with uc:
                            with st.form(f"upd_{g['id']}"):
                                nv = st.slider("Progress %", 0, 100, int(g["progress"]))
                                if st.form_submit_button("Update"):
                                    with conn() as db:
                                        db.execute("UPDATE goals SET progress=? WHERE id=? AND user_id=?",
                                                   (nv, g["id"], uid))
                                    st.success("Updated!")
                                    st.rerun()
                        with dc:
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button("✅ Complete", key=f"cmp_{g['id']}"):
                                with conn() as db:
                                    db.execute("UPDATE goals SET status='completed' WHERE id=? AND user_id=?",
                                               (g["id"], uid))
                                st.success("Goal completed! 🎉")
                                st.rerun()
                            if st.button("🗑 Delete", key=f"del_{g['id']}"):
                                with conn() as db:
                                    db.execute("DELETE FROM goals WHERE id=? AND user_id=?", (g["id"], uid))
                                st.rerun()

    with t2:
        section("➕  Create New Goal")
        # Career quote for motivation
        qt, qa, qc = random_quote_by_cat("Career")
        st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)
        with st.form("add_goal"):
            title    = st.text_input("Goal Title *", placeholder="e.g. Ship my first SaaS product")
            c1, c2 = st.columns(2)
            category  = c1.selectbox("Category", ["Coding","Finance","Health","Learning","Social","General"])
            timeframe = c2.selectbox("Timeframe", ["Daily","Weekly","Monthly","Yearly"])
            deadline  = st.date_input("Deadline", value=datetime.date.today() + datetime.timedelta(days=30))
            if st.form_submit_button("🚀 Create Goal", use_container_width=True):
                if not title:
                    st.error("Title required.")
                else:
                    with conn() as db:
                        db.execute("INSERT INTO goals (user_id,title,category,timeframe,progress,deadline) VALUES (?,?,?,?,0,?)",
                                   (uid, title, category, timeframe, deadline.isoformat()))
                    st.success(f"Goal '{title}' created!")
                    st.rerun()

    with t3:
        comp = get_goals(uid, status="completed")
        if not comp:
            st.info("No completed goals yet. Keep building!")
        else:
            st.markdown(f"**{len(comp)} goals completed 🏆**")
            for g in comp:
                st.markdown(f"""<div class="dv-card dv-card-green" style="padding:14px 18px;margin-bottom:8px">
                    <b style="color:#34d399">✅ {g['title']}</b>
                    <span class="pill {cat_pills.get(g['category'],'pill-slate')}">{g['category']}</span>
                    <span class="pill {tf_pills.get(g['timeframe'],'pill-slate')}">{g['timeframe']}</span>
                    <br><small style="color:#475569">Deadline: {g['deadline'] or 'N/A'} · Progress: {g['progress']}%</small>
                </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  PAGE: HABITS
# ──────────────────────────────────────────────────────────────
def page_habits():
    uid   = st.session_state.user_id
    today = datetime.date.today().isoformat()
    st.markdown("## 🔥 Habit Manager")
    habits = get_habits(uid)
    t1, t2 = st.tabs(["🔥  Streaks & Heatmap", "➕  Add / Remove"])

    with t1:
        if not habits:
            st.info("No habits found.")
        else:
            section("Current Streaks")
            cols = st.columns(3)
            for i, h in enumerate(habits):
                s = streak(uid, h["id"])
                color = "#fbbf24" if s >= 14 else "#34d399" if s >= 7 else "#38bdf8" if s >= 3 else "#475569"
                fire  = "🔥" if s >= 7 else "✨" if s >= 3 else ""
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="background:#0d1627;border:1px solid #1e2d48;border-radius:10px;
                                padding:12px;text-align:center;margin-bottom:10px">
                        <div style="font-size:.75rem;color:#94a3b8;margin-bottom:4px">{h['name'][:28]}</div>
                        <div style="font-size:1.5rem;font-weight:800;color:{color}">{s}</div>
                        <div style="font-size:.68rem;color:#475569">days {fire}</div>
                        <span class="pill {'pill-amber' if s>=14 else 'pill-green' if s>=7 else 'pill-blue' if s>=3 else 'pill-slate'}">{h['slot']}</span>
                    </div>""", unsafe_allow_html=True)

        section("90-Day Completion Heatmap")
        hmap = get_heatmap_df(uid, 90)
        if hmap.empty:
            st.info("Log habits to see your heatmap.")
        else:
            fig = px.bar(
                hmap, x="date", y="pct", color="pct",
                color_continuous_scale=[[0,"#0d1627"],[0.3,"#0c2d3f"],
                                        [0.6,"#0e5c70"],[1,"#2dd4bf"]],
                labels={"date":"Date","pct":"Completion %"},
                title="Daily Habit Completion — 90 days",
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(chart_theme(fig), use_container_width=True)

    with t2:
        section("➕  Add Custom Habit")
        with st.form("add_habit"):
            name = st.text_input("Habit Name *")
            c1, c2 = st.columns(2)
            cat  = c1.selectbox("Category", ["Mental","Health","Coding"])
            slot = c2.selectbox("Slot",     ["Morning","Work","Fitness","Learning","Night"])
            if st.form_submit_button("Add Habit", use_container_width=True):
                if not name:
                    st.error("Name required.")
                else:
                    with conn() as db:
                        db.execute("INSERT INTO habits (user_id,name,category,slot) VALUES (?,?,?,?)",
                                   (uid, name, cat, slot))
                    st.success("Habit added!")
                    st.rerun()

        section("🗑  Manage Habits")
        for h in habits:
            hc1, hc2 = st.columns([9, 2])
            hc1.markdown(f'{SLOT_ICONS.get(h["slot"],"")} {h["name"]} '
                         f'<span class="pill pill-slate">{h["slot"]}</span>',
                         unsafe_allow_html=True)
            if hc2.button("Remove", key=f"rm_{h['id']}"):
                with conn() as db:
                    db.execute("DELETE FROM habits WHERE id=? AND user_id=?", (h["id"], uid))
                    db.execute("DELETE FROM habit_logs WHERE habit_id=? AND user_id=?", (h["id"], uid))
                st.rerun()


# ──────────────────────────────────────────────────────────────
#   PAGE: REVIEWS
# ──────────────────────────────────────────────────────────────
def page_reviews():
    uid = st.session_state.user_id
    st.markdown("## 📊 Progress Reviews")
    t1, t2, t3 = st.tabs(["📅  Weekly", "🗓️  Monthly", "🏆  Yearly"])

    def render_review(days, label):
        hmap     = get_heatmap_df(uid, days)
        metrics  = get_metrics_df(uid, days)
        jdf      = get_journal_df(uid, days)
        
        wr       = comp_rate(uid, days)
        
        adw      = metrics["deep_work_hrs"].mean() if not metrics.empty else 0
        asl      = metrics["sleep_hrs"].mean()     if not metrics.empty else 0
        aex      = metrics["exercise_mins"].mean()  if not metrics.empty else 0

        # Quote for review context
        qt, qa, qc = random_quote_by_cat("Philosophy")
        st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(mbox(f"{wr}%",       f"{label} Habit Rate",  "#34d399"), unsafe_allow_html=True)
        c2.markdown(mbox(f"{adw:.1f}h",  "Avg Deep Work/Day",    "#38bdf8"), unsafe_allow_html=True)
        c3.markdown(mbox(f"{aex:.0f}m",  "Avg Exercise/Day",     "#34d399"), unsafe_allow_html=True)
        c4.markdown(mbox(f"{asl:.1f}h",  "Avg Sleep/Night",      "#a78bfa"), unsafe_allow_html=True)

        if not hmap.empty:
            section(f"Habit Completion — {label}")
            fig = px.bar(hmap, x="date", y="pct", color="pct",
                         color_continuous_scale=["#0d1627","#0e5c70","#2dd4bf"],
                         labels={"date":"Date","pct":"Completion %"})
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(chart_theme(fig), use_container_width=True, key=f"habit_chart_review_{label}")

        if not metrics.empty:
            section("Performance Metrics Trend")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=metrics["date"], y=metrics["deep_work_hrs"],
                                      name="Deep Work (hrs)", line=dict(color="#38bdf8", width=2)))
            fig2.add_trace(go.Scatter(x=metrics["date"], y=metrics["sleep_hrs"],
                                      name="Sleep (hrs)", line=dict(color="#a78bfa", width=2)))
            fig2.add_trace(go.Scatter(x=metrics["date"], y=metrics["exercise_mins"]/60,
                                      name="Exercise (hrs)", line=dict(color="#34d399", width=2)))
            st.plotly_chart(chart_theme(fig2), use_container_width=True, key=f"metrics_chart_review_{label}")

        if not jdf.empty and "mood" in jdf.columns:
            section("Mood & Energy Trends")
            jdf["mood"]   = pd.to_numeric(jdf["mood"], errors="coerce")
            jdf["energy"] = pd.to_numeric(jdf["energy"], errors="coerce")
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=jdf["date"], y=jdf["mood"],
                                      name="Mood", line=dict(color="#fbbf24"), mode="lines+markers"))
            fig3.add_trace(go.Scatter(x=jdf["date"], y=jdf["energy"],
                                      name="Energy", line=dict(color="#f87171"), mode="lines+markers"))
            fig3.update_yaxes(range=[0, 11])
            st.plotly_chart(chart_theme(fig3), use_container_width=True, key=f"mood_chart_review_{label}")

    with t1:
        st.markdown("### 📅 Weekly Review")
        render_review(7, "7-Day")
        goals_w = get_goals(uid, "Weekly")
        if goals_w:
            section("Weekly Goals")
            for g in goals_w:
                gp = min(g["progress"], 100)
                st.markdown(f"""<div style="margin-bottom:12px">
                    <b style="color:#dce7f3">{g['title']}</b>
                    <span class="pill pill-green">Weekly</span>
                    {pbar(gp, "#34d399")}
                </div>""", unsafe_allow_html=True)

    with t2:
        st.markdown("### 🗓️ Monthly Review")
        render_review(30, "30-Day")
        goals_m = get_goals(uid, "Monthly")
        if goals_m:
            section("Monthly Goals")
            for g in goals_m:
                gp = min(g["progress"], 100)
                st.markdown(f"""<div style="margin-bottom:12px">
                    <b style="color:#dce7f3">{g['title']}</b>
                    <span class="pill pill-purple">Monthly</span>
                    {pbar(gp, "#a78bfa")}
                </div>""", unsafe_allow_html=True)

    with t3:
        st.markdown("### 🏆 Yearly Review")
        render_review(365, "365-Day")

        # Skill self-rating tracker
        section("📈 Monthly Skill Self-Rating")
        SKILLS = ["React","PHP","Python","System Design","Testing",
                  "TypeScript","SQL","Algorithms","Communication","DevOps"]
        skills_df = get_skill_df(uid)
        nm, ny = datetime.date.today().month, datetime.date.today().year

        with st.form("skill_form"):
            st.markdown("**Rate your current level (1 = beginner · 10 = expert)**")
            cols = st.columns(5)
            ratings = {}
            for i, sk in enumerate(SKILLS):
                with cols[i % 5]:
                    ex_r = skills_df[
                        (skills_df["skill"]==sk) &
                        (skills_df["month"]==nm) &
                        (skills_df["year"]==ny)
                    ]
                    default = int(ex_r["rating"].iloc[0]) if not ex_r.empty else 5
                    ratings[sk] = st.slider(sk, 1, 10, default, key=f"sk_{sk}")
            if st.form_submit_button("💾 Save Skill Ratings", use_container_width=True):
                for sk, r in ratings.items():
                    save_skill(uid, sk, r, nm, ny)
                st.success("Skill ratings saved!")
                st.rerun()

        if not skills_df.empty:
            skills_df = skills_df.copy()
            skills_df["period"] = (skills_df["year"].astype(str) + "-" +
                                   skills_df["month"].astype(str).str.zfill(2))
            fig_sk = px.line(skills_df, x="period", y="rating", color="skill",
                             title="Skill Progression Over Time",
                             labels={"period":"Month","rating":"Rating","skill":"Skill"})
            fig_sk.update_yaxes(range=[0, 11])
            st.plotly_chart(chart_theme(fig_sk), use_container_width=True, key="skills_progression_line_chart")
# ──────────────────────────────────────────────────────────────
#  PAGE: SKILLS ROADMAP
# ──────────────────────────────────────────────────────────────
def page_skills():
    st.markdown("## 📚 Skills & Learning Roadmap")

    # Coding quote
    qt, qa, qc = random_quote_by_cat("Coding")
    st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

    roadmaps = {
        "⚛️  React / Frontend": [
            ("Core React & JSX",                     "Foundational"),
            ("Hooks: useState, useEffect, useRef…",  "Foundational"),
            ("State Management — Zustand / Redux",   "Intermediate"),
            ("React Router v6",                      "Intermediate"),
            ("TypeScript with React",                "Intermediate"),
            ("Performance — memo, lazy, Suspense",   "Advanced"),
            ("Testing: Jest + React Testing Library","Advanced"),
            ("Next.js — SSR, SSG, App Router",       "Advanced"),
            ("Build Tools: Vite / Webpack internals","Expert"),
            ("Accessibility & Web Standards",        "Expert"),
        ],
        "🐘  PHP / Laravel": [
            ("Core PHP & OOP Principles",            "Foundational"),
            ("Composer & Dependency Management",     "Foundational"),
            ("Laravel MVC, Routing, Middleware",     "Intermediate"),
            ("Eloquent ORM & Migrations",            "Intermediate"),
            ("REST API Design & Versioning",         "Intermediate"),
            ("Auth: Sanctum, Passport, Gates",       "Advanced"),
            ("Testing: PHPUnit & Pest",              "Advanced"),
            ("Queues, Jobs & Broadcasting",          "Advanced"),
            ("Docker & Cloud Deployment",            "Expert"),
            ("Performance, Caching & Security",      "Expert"),
        ],
        "🐍  Python": [
            ("Core Python & OOP",                    "Foundational"),
            ("Virtual Envs, pip & Packaging",        "Foundational"),
            ("FastAPI or Django REST",               "Intermediate"),
            ("SQLAlchemy / Django ORM",              "Intermediate"),
            ("Async Python: asyncio, httpx",         "Intermediate"),
            ("Testing with pytest",                  "Advanced"),
            ("Data Structures & Algorithms",         "Advanced"),
            ("Docker & CI/CD Pipelines",             "Advanced"),
            ("ML / Data Science OR DevOps path",     "Expert"),
            ("System Design at Scale",               "Expert"),
        ],
    }

    level_style = {
        "Foundational": ("pill-green",  "#34d399"),
        "Intermediate": ("pill-blue",   "#38bdf8"),
        "Advanced":     ("pill-purple", "#a78bfa"),
        "Expert":       ("pill-amber",  "#fbbf24"),
    }

    for stack_name, steps in roadmaps.items():
        with st.expander(f"📌 {stack_name} Roadmap"):
            for i, (topic, level) in enumerate(steps, 1):
                pc, color = level_style[level]
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;
                            border-radius:9px;margin:4px 0;background:#0d1627;border:1px solid #1e2d48">
                    <span style="color:{color};font-weight:700;font-family:'JetBrains Mono',monospace;
                                 min-width:26px;font-size:.8rem">{i:02d}</span>
                    <span style="color:#dce7f3;flex:1">{topic}</span>
                    <span class="pill {pc}">{level}</span>
                </div>""", unsafe_allow_html=True)

    section("📖  Essential Developer Reading List")
    books = [
        ("Clean Code",                    "Robert C. Martin", "Naming, functions, code quality"),
        ("The Pragmatic Programmer",      "Hunt & Thomas",    "Career philosophy and craft"),
        ("Designing Data-Intensive Apps", "Martin Kleppmann", "Systems architecture — essential"),
        ("You Don't Know JS",             "Kyle Simpson",     "Deep JavaScript mastery"),
        ("The Psychology of Money",       "Morgan Housel",    "Financial independence mindset"),
        ("Deep Work",                     "Cal Newport",      "Focus and productivity systems"),
        ("Atomic Habits",                 "James Clear",      "Habit formation backed by science"),
        ("The Mythical Man-Month",        "Fred Brooks",      "Engineering teams and delivery"),
    ]
    c1, c2 = st.columns(2)
    for i, (title, author, desc) in enumerate(books):
        with (c1 if i % 2 == 0 else c2):
            st.markdown(f"""<div class="dv-card dv-card-blue" style="padding:14px 16px;margin-bottom:8px">
                <b style="color:#dce7f3">{title}</b><br>
                <small style="color:#38bdf8">{author}</small><br>
                <small style="color:#475569">{desc}</small>
            </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  PAGE: FINANCE TIPS
# ──────────────────────────────────────────────────────────────
def page_finance():
    uid = st.session_state.user_id
    st.markdown("## 💰 Financial Independence for Developers")

    qt, qa, qc = random_quote_by_cat("Finance")
    st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

    t1, t2 = st.tabs(["💡  Rules & Income Streams", "🎯  Finance Goals"])

    with t1:
        section("Developer Financial Rules")
        rules = [
            ("🎯", "Save and invest at least 20% of every paycheck — before spending."),
            ("📈", "Invest in low-cost index funds: S&P 500 or global ETFs."),
            ("🚫", "Avoid lifestyle inflation. Every raise is an investment opportunity."),
            ("💻", "Build a side income stream before you need it: freelance, SaaS, or content."),
            ("🏦", "Build a 6-month emergency fund before aggressive investing."),
            ("📚", "Read The Psychology of Money. It rewires how you think about wealth."),
            ("🔢", "Track your net worth monthly. What gets measured gets improved."),
            ("⏰", "Start investing early. Time in market beats timing the market."),
            ("💡", "Learn to read a P&L statement. Build products, not just features."),
        ]
        for icon, rule in rules:
            st.markdown(f"""<div class="dv-card dv-card-green" style="padding:12px 16px;margin:5px 0">
                <span style="font-size:1.1rem">{icon}</span>
                <span style="color:#dce7f3;margin-left:10px">{rule}</span>
            </div>""", unsafe_allow_html=True)

        section("Developer Income Streams")
        streams = [
            ("💼", "Salary / Full-time",      "Stable primary income. Optimise for learning speed early on."),
            ("🔧", "Freelancing",             "High hourly rate. Start with one client in your current niche."),
            ("🚀", "SaaS Product",            "Asymmetric upside. Takes 12–24 months but compounds forever."),
            ("📝", "Technical Content",       "Blog, newsletter, YouTube. Builds reputation + passive income."),
            ("📦", "Open Source + Sponsors",  "Long game. Builds community trust and career leverage."),
            ("🎓", "Courses / Coaching",      "Leverage your expertise. Highest margin income stream."),
        ]
        c1, c2 = st.columns(2)
        for i, (icon, name, desc) in enumerate(streams):
            with (c1 if i % 2 == 0 else c2):
                st.markdown(f"""<div class="dv-card dv-card-blue" style="padding:14px 16px;margin-bottom:8px">
                    <span style="font-size:1rem">{icon} <b style="color:#dce7f3">{name}</b></span><br>
                    <small style="color:#475569">{desc}</small>
                </div>""", unsafe_allow_html=True)

    with t2:
        with conn() as db:
            fin_goals = db.execute(
                "SELECT * FROM goals WHERE user_id=? AND category='Finance' AND status='active'",
                (uid,),
            ).fetchall()
        if not fin_goals:
            st.info("No Finance goals yet. Create goals with Category = Finance in the Goals page.")
        else:
            for g in fin_goals:
                gp = min(g["progress"], 100)
                st.markdown(f"""<div class="dv-card dv-card-amber" style="margin-bottom:10px">
                    <b style="color:#fbbf24">{g['title']}</b>
                    <span class="pill pill-amber">{g['timeframe']}</span>
                    {pbar(gp, "#fbbf24")}
                    <small style="color:#475569">Deadline: {g['deadline'] or 'N/A'} · Progress: {gp}%</small>
                </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  PAGE: PROFILE
# ──────────────────────────────────────────────────────────────
def page_profile():
    uid  = st.session_state.user_id
    st.markdown("## 👤 Profile & Settings")

    with conn() as db:
        u = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

    if u:
        st.markdown(f"""<div class="dv-card dv-card-blue">
            <h3 style="margin:0;color:#38bdf8">@{u['username']}</h3>
            <p style="margin:5px 0;color:#475569">{u['role']}</p>
            <p style="margin:3px 0">
                <span class="pill pill-teal">Stack: {u['stack']}</span>
            </p>
            <p style="margin:5px 0;color:#475569;font-size:.8rem">Member since {u['created_at']}</p>
        </div>""", unsafe_allow_html=True)

    habits_count = len(get_habits(uid))
    comp_goals   = get_goals(uid, status="completed")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(mbox(habits_count,               "Active Habits",  "#34d399"), unsafe_allow_html=True)
    c2.markdown(mbox(len(comp_goals),            "Goals Done",     "#fbbf24"), unsafe_allow_html=True)
    c3.markdown(mbox(f"{comp_rate(uid,7)}%",     "7-Day Rate",     "#38bdf8"), unsafe_allow_html=True)
    c4.markdown(mbox(f"{comp_rate(uid,30)}%",    "30-Day Rate",    "#a78bfa"), unsafe_allow_html=True)

    section("Update Profile")
    with st.form("profile_form"):
        role_opts = ["Junior Developer","Mid-level Developer","Senior Developer",
                     "Full-stack Developer","Student"]
        cur_role  = u["role"] if u and u["role"] in role_opts else role_opts[0]
        new_role  = st.selectbox("Role", role_opts, index=role_opts.index(cur_role))
        new_stack = st.text_input("Stack", value=u["stack"] if u else "")
        if st.form_submit_button("Save Changes", use_container_width=True):
            with conn() as db:
                db.execute("UPDATE users SET role=?,stack=? WHERE id=?", (new_role, new_stack, uid))
            st.session_state.role  = new_role
            st.session_state.stack = new_stack
            st.success("Profile updated!")

    section("All Quotes Library")
    st.markdown("*Every quote in DevLife OS — rotating daily on your dashboard.*")
    cat_filter = st.selectbox("Filter by category",
                              ["All"] + sorted(set(q[2] for q in QUOTES)))
    pool = QUOTES if cat_filter == "All" else [q for q in QUOTES if q[2] == cat_filter]
    for text, author, cat in pool:
        pc = CAT_PILL.get(cat, "pill-slate")
        st.markdown(f"""
        <div style="background:#0d1627;border:1px solid #1e2d48;border-radius:9px;
                    padding:12px 16px;margin:5px 0">
            <span style="color:#bae6fd;font-style:italic;font-size:.87rem">"{text}"</span><br>
            <span style="color:#38bdf8;font-size:.73rem;font-weight:600">— {author}</span>
            <span class="pill {pc}" style="margin-left:8px">{cat}</span>
        </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  ROUTER
# ──────────────────────────────────────────────────────────────
PAGES = {
    "Dashboard":      page_dashboard,
    "Daily Routine":  page_daily,
    "Goals":          page_goals,
    "Habits":         page_habits,
    "Reviews":        page_reviews,
    "Skills & Roadmap": page_skills,
    "Finance Tips":   page_finance,
    "Profile":        page_profile,
}

def main():
    # Init session state
    for k, v in [("logged_in", False), ("user_id", None), ("username", ""),
                 ("role", "Developer"), ("stack", "React/PHP/Python")]:
        if k not in st.session_state:
            st.session_state[k] = v

    if not st.session_state.logged_in:
        page_auth()
        return

    selected = render_sidebar()  # clean page name
    # Match to PAGES dict
    matched = next((k for k in PAGES if k.lower() in selected.lower()), "Dashboard")
    PAGES[matched]()


if __name__ == "__main__":
    main()
