# ╔══════════════════════════════════════════════════════════════╗
# ║              DevLife OS  —  by a Developer, for Developers   ║
# ║   Stack: Streamlit · SQLite · Plotly · Pandas                ║
# ╚══════════════════════════════════════════════════════════════╝

import streamlit as st
import streamlit.components.v1 as components
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
    overflow-y: auto !important;
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

/* ── hide streamlit default header/footer ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hide native Streamlit sidebar completely ── */
section[data-testid="stSidebar"] { display: none !important; }
button[data-testid="collapsedControl"],
[data-testid="collapsedControl"] { display: none !important; }
.main .block-container { padding-left: 1rem !important; max-width: 100% !important; }

/* ── Sidebar nav radio items — bigger click targets ── */
section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio label {
    padding: 8px 12px !important;
    border-radius: 8px !important;
    transition: background .15s ease !important;
    cursor: pointer !important;
    font-size: 0.88rem !important;
    display: block !important;
    width: 100% !important;
    margin: 1px 0 !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: #1e2d48 !important;
}
section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 0.88rem !important;
    line-height: 1.4 !important;
}
/* Hide the radio circle dot — make it look like a nav list */
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}
section[data-testid="stSidebar"] .stMarkdownContainer p {
    font-size: 0.82rem !important;
    line-height: 1.5 !important;
}

/* ── Sidebar user card ── */
.sb-user-card {
    background: #111c30;
    border: 1px solid #1e2d48;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 8px 0 6px;
}

/* ── Sidebar progress area ── */
.sb-progress {
    margin: 6px 0 4px;
    padding: 8px 10px;
    background: #0a1020;
    border-radius: 10px;
    border: 1px solid #1a2540;
}

/* ── Sidebar mini quote ── */
.sb-quote {
    background: #111c30;
    border: 1px solid #1e2d48;
    border-radius: 8px;
    padding: 10px 12px;
    margin-top: 4px;
}

/* ── Admin login gate ── */
.admin-gate {
    background: linear-gradient(135deg, #1a0d0d 0%, #0f0808 100%);
    border: 1px solid #f87171;
    border-radius: 14px;
    padding: 32px 36px;
    max-width: 420px;
    margin: 40px auto;
    text-align: center;
}
.admin-gate-icon { font-size: 3rem; margin-bottom: 10px; }
.admin-gate-title { font-size: 1.4rem; font-weight: 800; color: #f87171; margin-bottom: 6px; }
.admin-gate-sub { font-size: .85rem; color: #64748b; margin-bottom: 20px; }

/* ── Admin badge ── */
.admin-badge {
    display: inline-block;
    background: linear-gradient(90deg, #f87171, #fbbf24);
    color: #080c14;
    font-size: .6rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 1px 7px;
    border-radius: 99px;
    margin-left: 6px;
    vertical-align: middle;
}

/* ── Outcompete accent buttons ── */
.btn-fire > button {
    background: linear-gradient(135deg, #f43127, #ff6b35) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
    box-shadow: 0 0 18px rgba(244,49,39,.4) !important;
    transition: all .25s ease !important;
}
.btn-fire > button:hover {
    background: linear-gradient(135deg, #ff6b35, #f43127) !important;
    box-shadow: 0 0 28px rgba(244,49,39,.6) !important;
}
.btn-gold > button {
    background: linear-gradient(135deg, #fcb302, #f97316) !important;
    color: #080c14 !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
    box-shadow: 0 0 18px rgba(252,179,2,.35) !important;
    transition: all .25s ease !important;
}
.btn-gold > button:hover {
    box-shadow: 0 0 28px rgba(252,179,2,.55) !important;
}
/* ── Outcompete journal section cards ── */
.oc-section {
    background: linear-gradient(135deg, #0d1627 0%, #0a1020 100%);
    border: 1px solid #1e2d48;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.oc-section-fire  { border-left: 4px solid #f43127; }
.oc-section-gold  { border-left: 4px solid #fcb302; }
.oc-section-teal  { border-left: 4px solid #2dd4bf; }
.oc-section-blue  { border-left: 4px solid #38bdf8; }
/* ── Mindset checkbox row ── */
.mindset-row {
    background: #0d1627; border: 1px solid #1e2d48; border-radius: 9px;
    padding: 10px 14px; margin: 5px 0;
}
/* ── 1% better tracker ── */
.one-pct-bar {
    background: linear-gradient(90deg, #f43127, #fcb302, #34d399);
    height: 8px; border-radius: 99px;
}

/* ── Admin panel ── */
.admin-card {
    background: linear-gradient(135deg, #1a0d0d 0%, #0f0808 100%);
    border: 1px solid #4a1a1a;
    border-left: 4px solid #f87171;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)




# ──────────────────────────────────────────────────────────────
#  LANGUAGE / TRANSLATION SYSTEM
# ──────────────────────────────────────────────────────────────
TRANSLATIONS = {
    # Auth
    "sign_in":           {"en": "🔑  Sign In",            "bn": "🔑  সাইন ইন"},
    "create_account":    {"en": "🚀  Create Account",     "bn": "🚀  অ্যাকাউন্ট তৈরি"},
    "username":          {"en": "Username",                "bn": "ইউজারনেম"},
    "password":          {"en": "Password",                "bn": "পাসওয়ার্ড"},
    "confirm_password":  {"en": "Confirm Password *",      "bn": "পাসওয়ার্ড নিশ্চিত *"},
    "login_btn":         {"en": "Login →",                "bn": "লগইন →"},
    "create_btn":        {"en": "Create Account →",       "bn": "অ্যাকাউন্ট তৈরি করুন →"},
    "wrong_creds":       {"en": "Wrong username or password.", "bn": "ইউজারনেম বা পাসওয়ার্ড ভুল।"},
    "pw_short":          {"en": "Password must be 6+ characters.", "bn": "পাসওয়ার্ড কমপক্ষে ৬ অক্ষরের হতে হবে।"},
    "pw_mismatch":       {"en": "Passwords do not match.", "bn": "পাসওয়ার্ড মেলেনি।"},
    "username_required": {"en": "Username required.",     "bn": "ইউজারনেম দিন।"},
    "account_created":   {"en": "Account created!",       "bn": "অ্যাকাউন্ট তৈরি হয়েছে!"},
    "username_taken":    {"en": "Username already taken.", "bn": "এই ইউজারনেম আগেই নেওয়া হয়েছে।"},
    "i_am_a":            {"en": "I am a …",               "bn": "আমি একজন …"},
    "primary_stack":     {"en": "Primary Stack",           "bn": "প্রধান স্ট্যাক"},
    # Sidebar / Nav
    "nav_dashboard":     {"en": "🏠  Dashboard",          "bn": "🏠  ড্যাশবোর্ড"},
    "nav_daily":         {"en": "📋  Daily Routine",      "bn": "📋  দৈনন্দিন রুটিন"},
    "nav_goals":         {"en": "🎯  Goals",              "bn": "🎯  লক্ষ্য"},
    "nav_habits":        {"en": "🔥  Habits",             "bn": "🔥  অভ্যাস"},
    "nav_reviews":       {"en": "📊  Reviews",            "bn": "📊  পর্যালোচনা"},
    "nav_skills":        {"en": "📚  Skills & Roadmap",   "bn": "📚  দক্ষতা ও রোডম্যাপ"},
    "nav_finance":       {"en": "💰  Finance Tips",       "bn": "💰  আর্থিক টিপস"},
    "nav_profile":       {"en": "👤  Profile",            "bn": "👤  প্রোফাইল"},
    "nav_admin":         {"en": "🛡️  Admin Panel",        "bn": "🛡️  অ্যাডমিন প্যানেল"},
    "logout":            {"en": "🚪  Logout",             "bn": "🚪  লগআউট"},
    "today":             {"en": "Today",                   "bn": "আজ"},
    # Dashboard
    "good_morning":      {"en": "Good morning",            "bn": "শুভ সকাল"},
    "good_afternoon":    {"en": "Good afternoon",          "bn": "শুভ অপরাহ্ন"},
    "good_evening":      {"en": "Good evening",            "bn": "শুভ সন্ধ্যা"},
    "todays_completion": {"en": "Today's Completion",      "bn": "আজকের সম্পূর্ণতা"},
    "habits_done_today": {"en": "Habits Done Today",       "bn": "আজকের সম্পন্ন অভ্যাস"},
    "7_day_avg":         {"en": "7-Day Average",           "bn": "৭ দিনের গড়"},
    "active_goals":      {"en": "Active Goals",            "bn": "সক্রিয় লক্ষ্য"},
    "todays_habits":     {"en": "⚡  Today's Habit Checklist","bn": "⚡  আজকের অভ্যাস তালিকা"},
    "active_goals_sec":  {"en": "🎯  Active Goals",        "bn": "🎯  সক্রিয় লক্ষ্যসমূহ"},
    "quick_log":         {"en": "📊  Quick Daily Log",     "bn": "📊  দ্রুত দৈনিক লগ"},
    "deep_work_hrs":     {"en": "💻 Deep Work (hrs)",      "bn": "💻 গভীর কাজ (ঘণ্টা)"},
    "exercise_min":      {"en": "💪 Exercise (min)",       "bn": "💪 ব্যায়াম (মিনিট)"},
    "sleep_hrs":         {"en": "😴 Sleep (hrs)",          "bn": "😴 ঘুম (ঘণ্টা)"},
    "save":              {"en": "Save →",                  "bn": "সংরক্ষণ →"},
    "saved":             {"en": "Saved!",                  "bn": "সংরক্ষিত!"},
    "no_habits_msg":     {"en": "No habits found. Seeded automatically on registration.",
                          "bn": "কোনো অভ্যাস নেই। নিবন্ধনের সময় স্বয়ংক্রিয়ভাবে যোগ হবে।"},
    "no_goals_msg":      {"en": "No goals yet — create some in Goals.",
                          "bn": "এখনো লক্ষ্য নেই — লক্ষ্য পাতায় তৈরি করুন।"},
    # Goals page
    "goal_management":   {"en": "## 🎯 Goal Management",  "bn": "## 🎯 লক্ষ্য ব্যবস্থাপনা"},
    "active_goals_tab":  {"en": "📋  Active Goals",       "bn": "📋  সক্রিয় লক্ষ্য"},
    "new_goal_tab":      {"en": "➕  New Goal",            "bn": "➕  নতুন লক্ষ্য"},
    "completed_tab":     {"en": "✅  Completed",           "bn": "✅  সম্পন্ন"},
    "goal_title_lbl":    {"en": "Goal Title *",            "bn": "লক্ষ্যের শিরোনাম *"},
    "category":          {"en": "Category",                "bn": "বিভাগ"},
    "timeframe":         {"en": "Timeframe",               "bn": "সময়সীমা"},
    "deadline":          {"en": "Deadline (optional)",     "bn": "শেষ তারিখ (ঐচ্ছিক)"},
    "create_goal_btn":   {"en": "🚀 Create Goal",          "bn": "🚀 লক্ষ্য তৈরি"},
    "update":            {"en": "Update",                   "bn": "আপডেট"},
    "complete":          {"en": "✅ Complete",              "bn": "✅ সম্পন্ন"},
    "delete":            {"en": "🗑 Delete",               "bn": "🗑 মুছুন"},
    "progress_pct":      {"en": "Progress %",              "bn": "অগ্রগতি %"},
    "no_active_goals":   {"en": "No active goals. Create one in the 'New Goal' tab.",
                          "bn": "কোনো সক্রিয় লক্ষ্য নেই। 'নতুন লক্ষ্য' ট্যাবে তৈরি করুন।"},
    "filter":            {"en": "Filter",                   "bn": "ফিল্টার"},
    # Habits page
    "habit_manager":     {"en": "## 🔥 Habit Manager",    "bn": "## 🔥 অভ্যাস ব্যবস্থাপক"},
    "streaks_heatmap":   {"en": "🔥  Streaks & Heatmap",  "bn": "🔥  ধারা ও হিটম্যাপ"},
    "add_remove":        {"en": "➕  Add / Remove",        "bn": "➕  যোগ / সরান"},
    "add_custom_habit":  {"en": "➕  Add Custom Habit",    "bn": "➕  কাস্টম অভ্যাস যোগ"},
    "habit_name":        {"en": "Habit Name *",            "bn": "অভ্যাসের নাম *"},
    "add_habit_btn":     {"en": "Add Habit",               "bn": "অভ্যাস যোগ"},
    "name_required":     {"en": "Name required.",          "bn": "নাম দিন।"},
    "habit_added":       {"en": "Habit added!",            "bn": "অভ্যাস যোগ হয়েছে!"},
    "remove":            {"en": "Remove",                  "bn": "সরান"},
    "manage_habits":     {"en": "🗑  Manage Habits",       "bn": "🗑  অভ্যাস পরিচালনা"},
    "current_streaks":   {"en": "Current Streaks",         "bn": "বর্তমান ধারাসমূহ"},
    # Reviews
    "progress_reviews":  {"en": "## 📊 Progress Reviews", "bn": "## 📊 অগ্রগতি পর্যালোচনা"},
    "weekly_tab":        {"en": "📅  Weekly",              "bn": "📅  সাপ্তাহিক"},
    "monthly_tab":       {"en": "🗓️  Monthly",             "bn": "🗓️  মাসিক"},
    "yearly_tab":        {"en": "🏆  Yearly",              "bn": "🏆  বার্ষিক"},
    "habit_rate":        {"en": "Habit Rate",              "bn": "অভ্যাসের হার"},
    "avg_deep_work":     {"en": "Avg Deep Work/Day",       "bn": "গড় গভীর কাজ/দিন"},
    "avg_exercise":      {"en": "Avg Exercise/Day",        "bn": "গড় ব্যায়াম/দিন"},
    "avg_sleep":         {"en": "Avg Sleep/Night",         "bn": "গড় ঘুম/রাত"},
    # Profile
    "profile_settings":  {"en": "## 👤 Profile & Settings","bn": "## 👤 প্রোফাইল ও সেটিংস"},
    "active_habits_kpi": {"en": "Active Habits",           "bn": "সক্রিয় অভ্যাস"},
    "goals_done":        {"en": "Goals Done",              "bn": "সম্পন্ন লক্ষ্য"},
    "7_day_rate":        {"en": "7-Day Rate",              "bn": "৭ দিনের হার"},
    "30_day_rate":       {"en": "30-Day Rate",             "bn": "৩০ দিনের হার"},
    "update_profile":    {"en": "Update Profile",          "bn": "প্রোফাইল আপডেট"},
    "role_lbl":          {"en": "Role",                    "bn": "ভূমিকা"},
    "stack_lbl":         {"en": "Stack",                   "bn": "স্ট্যাক"},
    "save_changes":      {"en": "Save Changes",            "bn": "পরিবর্তন সংরক্ষণ"},
    "profile_updated":   {"en": "Profile updated!",        "bn": "প্রোফাইল আপডেট হয়েছে!"},
    "quotes_library":    {"en": "All Quotes Library",      "bn": "সকল উদ্ধৃতি লাইব্রেরি"},
    "filter_by_cat":     {"en": "Filter by category",      "bn": "বিভাগ অনুযায়ী ফিল্টার"},
    "member_since":      {"en": "Member since",            "bn": "সদস্যপদ শুরু"},
    # Daily routine
    "daily_routine_title":{"en": "## 📋 Daily Routine Tracker","bn": "## 📋 দৈনন্দিন রুটিন ট্র্যাকার"},
    "habits_tab":        {"en": "✅  Habits",              "bn": "✅  অভ্যাস"},
    "journal_tab":       {"en": "📝  Journal",             "bn": "📝  জার্নাল"},
    "metrics_tab":       {"en": "📊  Metrics",             "bn": "📊  মেট্রিক্স"},
    "journal_title":     {"en": "📝  Daily Journal — 5 Developer Questions",
                          "bn": "📝  দৈনিক জার্নাল — ৫টি ডেভেলপার প্রশ্ন"},
    "q1":                {"en": "🙏 What are you grateful for today?",
                          "bn": "🙏 আজ আপনি কীসের জন্য কৃতজ্ঞ?"},
    "q2":                {"en": "🎯 What technical problem must you solve today?",
                          "bn": "🎯 আজ কোন টেকনিক্যাল সমস্যা সমাধান করতে হবে?"},
    "q3":                {"en": "⚠️ What hard task are you avoiding in your codebase?",
                          "bn": "⚠️ কোডবেসে কোন কঠিন কাজটি এড়িয়ে যাচ্ছেন?"},
    "brain_dump":        {"en": "🧠 Brain Dump — ideas, thoughts, anything on your mind",
                          "bn": "🧠 মনের কথা — যেকোনো ভাবনা বা ধারণা লিখুন"},
    "mood":              {"en": "😊 Mood (1–10)",           "bn": "😊 মেজাজ (১–১০)"},
    "energy":            {"en": "⚡ Energy (1–10)",         "bn": "⚡ শক্তি (১–১০)"},
    "commit_journal":    {"en": "💾 Commit Journal Entry",  "bn": "💾 জার্নাল এন্ট্রি সংরক্ষণ"},
    "journal_saved":     {"en": "Journal saved!",           "bn": "জার্নাল সংরক্ষিত!"},
    "log_metrics":       {"en": "📊  Log Performance Metrics","bn": "📊  পারফরম্যান্স মেট্রিক্স লগ"},
    "coding_hrs":        {"en": "⌨️ Coding (hrs)",          "bn": "⌨️ কোডিং (ঘণ্টা)"},
    "save_metrics_btn":  {"en": "💾 Save Metrics",          "bn": "💾 মেট্রিক্স সংরক্ষণ"},
    "mark_complete":     {"en": "Mark complete",            "bn": "সম্পন্ন হিসেবে চিহ্নিত করুন"},
    "date_lbl":          {"en": "Date",                    "bn": "তারিখ"},
    # Finance
    "finance_title":     {"en": "## 💰 Financial Independence for Developers",
                          "bn": "## 💰 ডেভেলপারদের আর্থিক স্বাধীনতা"},
    "rules_income":      {"en": "💡  Rules & Income Streams","bn": "💡  নিয়ম ও আয়ের উৎস"},
    "finance_goals_tab": {"en": "🎯  Finance Goals",        "bn": "🎯  আর্থিক লক্ষ্য"},
    "no_finance_goals":  {"en": "No Finance goals yet. Create goals with Category = Finance in the Goals page.",
                          "bn": "আর্থিক লক্ষ্য নেই। লক্ষ্য পাতায় Finance বিভাগে তৈরি করুন।"},
    # Skills
    "skills_title":      {"en": "## 📚 Skills & Learning Roadmap",
                          "bn": "## 📚 দক্ষতা ও শেখার রোডম্যাপ"},
    "save_skill_ratings":{"en": "💾 Save Skill Ratings",   "bn": "💾 দক্ষতা রেটিং সংরক্ষণ"},
    "skill_ratings_saved":{"en": "Skill ratings saved!",   "bn": "দক্ষতা রেটিং সংরক্ষিত!"},
}

def t(key):
    """Return translated string for the active language (en / bn)."""
    lang = st.session_state.get("lang", "en")
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("en", key))

# ──────────────────────────────────────────────────────────────
#  DATABASE
# ──────────────────────────────────────────────────────────────
# Use absolute path so DB persists regardless of working directory
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "devlife_os.db")

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
        
        # ── BULLETPROOF AUTOMATIC MIGRATIONS ──
        # এই ব্লকটি পুরনো ডাটাবেজে কোনো কলাম মিসিং থাকলে তা স্বয়ংক্রিয়ভাবে ইনজেক্ট করে দেবে
        try:
            db.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'Developer'")
        except sqlite3.OperationalError:
            pass
            
        try:
            db.execute("ALTER TABLE users ADD COLUMN stack TEXT DEFAULT 'React / PHP / Python'")
        except sqlite3.OperationalError:
            pass
            
        try:
            db.execute("ALTER TABLE habits ADD COLUMN slot TEXT DEFAULT 'Morning'")
        except sqlite3.OperationalError:
            pass

        try:
            db.execute("ALTER TABLE goals ADD COLUMN status TEXT DEFAULT 'active'")
        except sqlite3.OperationalError:
            pass

        try:
            db.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        # ── New Outcompete journal columns ──
        for col_def in [
            "nightly_review TEXT DEFAULT ''",
            "tomorrow_plan TEXT DEFAULT ''",
            "info_capture TEXT DEFAULT ''",
            "mindset_risk INTEGER DEFAULT 0",
            "mindset_compare INTEGER DEFAULT 0",
        ]:
            col_name = col_def.split()[0]
            try:
                db.execute(f"ALTER TABLE journal_entries ADD COLUMN {col_def}")
            except sqlite3.OperationalError:
                pass

        # ── New Outcompete metrics columns ──
        for col_def in [
            "quick_decisions INTEGER DEFAULT 5",
            "focus_pct INTEGER DEFAULT 50",
            "one_pct_better INTEGER DEFAULT 50",
        ]:
            try:
                db.execute(f"ALTER TABLE daily_metrics ADD COLUMN {col_def}")
            except sqlite3.OperationalError:
                pass

        # Auto-promote user named 'admin' to admin
        try:
            db.execute("UPDATE users SET is_admin=1 WHERE username='admin'")
        except Exception:
            pass

init_db()

# ──────────────────────────────────────────────────────────────
#  AUTH
# ──────────────────────────────────────────────────────────────
def make_hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

DEFAULT_HABITS = [
    # (name, category, slot)
    # ─── Outcompete Framework: Non-Negotiable Daily Habits ───

    # 🌅 Morning
    ("Plan 3 Top Priorities (Eat the Frog) — সকালে ৩টি সবচেয়ে গুরুত্বপূর্ণ কাজ ঠিক করুন", "Mental", "Morning"),
    ("Phone-Free First Hour — ঘুম থেকে উঠে প্রথম ১ ঘণ্টা ফোন ছাড়া থাকুন", "Mental", "Morning"),

    # 💻 Work / Focus
    ("60-90 Min Deep Work Block — নীরব ফোন, কোনো বাধা ছাড়া গভীর মনোযোগে কাজ", "Coding", "Work"),
    ("Complete the Hardest Task First — দিনের সবচেয়ে কঠিন কাজটি আগে শেষ করুন", "Coding", "Work"),

    # 📖 Learning
    ("30-60 Min Quality Learning — Business, Psychology, Tech বা Finance বই পড়ুন", "Mental", "Learning"),
    ("Share / Teach One Thing Learned Today — আজ যা শিখলেন তা একজনকে শেখান বা শেয়ার করুন", "Coding", "Learning"),

    # 💪 Fitness & Health
    ("25-30 Min Physical Exercise — হাঁটা, জগিং বা পুশ-আপ করুন", "Health", "Fitness"),
    ("10-15 Min Meditation / Stillness — ধ্যান বা চুপচাপ বসে মন শান্ত করুন", "Mental", "Fitness"),

    # 🤝 Networking & Comms
    ("Send One Important Email / Message on Time — সময়মতো একটি গুরুত্বপূর্ণ বার্তা পাঠান", "Mental", "Work"),
    ("Send a Thank-You or Networking Message — একজন পরিচিতকে ধন্যবাদ বা নেটওয়ার্কিং বার্তা পাঠান", "Mental", "Work"),

    # 🌙 Night / Review
    ("7-8 Hours Quality Sleep Setup — রাত ১০:৩০ এর মধ্যে ঘুমের প্রস্তুতি নিন", "Health", "Night"),
    ("Limit Low-Quality Social Media / Scrolling — অর্থহীন স্ক্রলিং সীমিত রাখুন", "Mental", "Night"),
]

def seed_habits(db, uid):
    """Insert default habits for a new user using an existing db connection."""
    db.executemany(
        "INSERT OR IGNORE INTO habits (user_id,name,category,slot) VALUES (?,?,?,?)",
        [(uid, n, c, s) for n, c, s in DEFAULT_HABITS],
    )

def register_user(username, password, role, stack):
    if not username or not username.strip():
        return False, "Username is required."
    try:
        with conn() as db:
            cur = db.execute(
                "INSERT INTO users (username,password_hash,role,stack) VALUES (?,?,?,?)",
                (username.strip(), make_hash(password), role, stack),
            )
            uid = cur.lastrowid
            seed_habits(db, uid)   # ← same connection/transaction
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

def save_journal(uid, date, q1, q2, q3, bd, mood, energy,
                  nightly_review="", tomorrow_plan="", info_capture="",
                  mindset_risk=0, mindset_compare=0):
    with conn() as db:
        db.execute("""
            INSERT INTO journal_entries
              (user_id,date,q1,q2,q3,brain_dump,mood,energy,
               nightly_review,tomorrow_plan,info_capture,mindset_risk,mindset_compare)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(user_id,date) DO UPDATE SET
            q1=excluded.q1,q2=excluded.q2,q3=excluded.q3,
            brain_dump=excluded.brain_dump,mood=excluded.mood,energy=excluded.energy,
            nightly_review=excluded.nightly_review,tomorrow_plan=excluded.tomorrow_plan,
            info_capture=excluded.info_capture,mindset_risk=excluded.mindset_risk,
            mindset_compare=excluded.mindset_compare
        """, (uid, date, q1, q2, q3, bd, mood, energy,
              nightly_review, tomorrow_plan, info_capture,
              int(mindset_risk), int(mindset_compare)))

def get_journal(uid, date):
    with conn() as db:
        return db.execute(
            "SELECT * FROM journal_entries WHERE user_id=? AND date=?", (uid, date)
        ).fetchone()

def save_metrics(uid, date, dw, code, ex, sl,
                  quick_decisions=5, focus_pct=50, one_pct_better=50):
    with conn() as db:
        db.execute("""
            INSERT INTO daily_metrics
              (user_id,date,deep_work_hrs,coding_hrs,exercise_mins,sleep_hrs,
               quick_decisions,focus_pct,one_pct_better)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(user_id,date) DO UPDATE SET
            deep_work_hrs=excluded.deep_work_hrs,coding_hrs=excluded.coding_hrs,
            exercise_mins=excluded.exercise_mins,sleep_hrs=excluded.sleep_hrs,
            quick_decisions=excluded.quick_decisions,focus_pct=excluded.focus_pct,
            one_pct_better=excluded.one_pct_better
        """, (uid, date, dw, code, ex, sl, quick_decisions, focus_pct, one_pct_better))

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

        # Language toggle (available before login)
        lang_col1, lang_col2, lang_col3 = st.columns([2, 2, 2])
        with lang_col2:
            lang_choice = st.radio(
                "🌐",
                ["English", "বাংলা"],
                index=0 if st.session_state.get("lang", "en") == "en" else 1,
                horizontal=True,
                key="auth_lang_radio",
                label_visibility="collapsed",
            )
            st.session_state.lang = "en" if lang_choice == "English" else "bn"

        # Show daily quote on login screen too
        qt, qa, qc = daily_quote()
        st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

        t_in, t_up = st.tabs([t("sign_in"), t("create_account")])

        with t_in:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("login_form"):
                u = st.text_input(t("username"), placeholder="your_username")
                p = st.text_input(t("password"), type="password", placeholder="••••••••")
                if st.form_submit_button(t("login_btn"), use_container_width=True):
                    user = login_user(u, p)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id   = user["id"]
                        st.session_state.username  = user["username"]
                        st.session_state.role      = user["role"]
                        st.session_state.stack     = user["stack"]
                        st.rerun()
                    else:
                        st.error(t("wrong_creds"))

        with t_up:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("reg_form"):
                c1, c2 = st.columns(2)
                nu = c1.text_input(t("username") + " *")
                np1 = c2.text_input(t("password") + " *", type="password")
                np2 = st.text_input(t("confirm_password"), type="password")
                role = st.selectbox(t("i_am_a"), [
                    "Junior Developer", "Mid-level Developer",
                    "Senior Developer", "Full-stack Developer", "Student",
                ])
                stack = st.multiselect(t("primary_stack"), [
                    "React", "PHP", "Python", "Laravel", "Next.js",
                    "Django", "FastAPI", "TypeScript", "Node.js", "Vue",
                ], default=["React", "PHP", "Python"])
                if st.form_submit_button(t("create_btn"), use_container_width=True):
                    if len(np1) < 6:
                        st.error(t("pw_short"))
                    elif np1 != np2:
                        st.error(t("pw_mismatch"))
                    elif not nu:
                        st.error(t("username_required"))
                    else:
                        ok, msg = register_user(nu, np1, role, ", ".join(stack))
                        st.success(msg) if ok else st.error(msg)


# ──────────────────────────────────────────────────────────────
#  TOP NAVBAR  (fixed header — pure Streamlit session_state nav)
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

    # ── Admin check ──
    with conn() as db:
        u_row = db.execute("SELECT is_admin FROM users WHERE id=?", (uid,)).fetchone()
    is_admin_user = bool(u_row and u_row["is_admin"])
    st.session_state.is_admin = is_admin_user

    # ── Page definitions ──
    PAGE_MAP = {
        "dashboard": t("nav_dashboard"),
        "daily":     t("nav_daily"),
        "goals":     t("nav_goals"),
        "habits":    t("nav_habits"),
        "reviews":   t("nav_reviews"),
        "skills":    t("nav_skills"),
        "finance":   t("nav_finance"),
        "journal":   "📝  Journal",
        "profile":   t("nav_profile"),
    }
    if is_admin_user:
        PAGE_MAP["admin"] = t("nav_admin")

    # ── Active page (session state only — no URL changes) ──
    if "active_page" not in st.session_state:
        st.session_state.active_page = "dashboard"
    active = st.session_state.active_page

    # ── Hidden nav buttons (zero-height container, invisible to user) ──
    # Each button has a unique key. JS clicks them to trigger Streamlit reruns.
    st.markdown(
        '<div style="position:absolute;width:1px;height:1px;overflow:hidden;opacity:0;pointer-events:none">',
        unsafe_allow_html=True,
    )
    for key in list(PAGE_MAP.keys()) + ["__logout__"]:
        if st.button(f"_nav_{key}", key=f"_navbtn_{key}"):
            if key == "__logout__":
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
            else:
                st.session_state.active_page = key
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Build navbar HTML ──
    admin_badge = (
        '<span style="display:inline-block;background:linear-gradient(90deg,#f87171,#fbbf24);'
        'color:#080c14;font-size:.5rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;'
        'padding:1px 5px;border-radius:99px;margin-left:4px;vertical-align:middle">ADMIN</span>'
        if is_admin_user else ""
    )

    # Desktop nav items
    nav_items_html = ""
    for key, label in PAGE_MAP.items():
        is_act = (key == active)
        style = (
            "background:#1e2d48;color:#38bdf8;font-weight:700;box-shadow:inset 0 -2px 0 #38bdf8;"
            if is_act else "color:#94a3b8;"
        )
        nav_items_html += (
            f'<button class="nb-link" data-page="{key}" '
            f'style="display:inline-flex;align-items:center;padding:5px 10px;border-radius:7px;'
            f'font-size:.78rem;font-weight:500;border:none;cursor:pointer;background:transparent;'
            f'white-space:nowrap;transition:background .15s,color .15s;flex-shrink:0;{style}">'
            f'{label}</button>'
        )

    # Mobile nav items (larger tap targets)
    mob_items_html = ""
    for key, label in PAGE_MAP.items():
        is_act = (key == active)
        style = "background:#1e2d48;color:#38bdf8;font-weight:700;" if is_act else "color:#94a3b8;"
        mob_items_html += (
            f'<button class="mob-link" data-page="{key}" '
            f'style="display:block;width:100%;padding:11px 14px;border-radius:8px;'
            f'font-size:.9rem;font-weight:500;border:none;cursor:pointer;background:transparent;'
            f'text-align:left;transition:background .15s,color .15s;{style}">'
            f'{label}</button>'
        )
    mob_items_html += (
        '<button class="mob-link" data-page="__logout__" '
        'style="display:block;width:100%;padding:11px 14px;border-radius:8px;'
        'font-size:.9rem;font-weight:600;border:none;cursor:pointer;background:transparent;'
        'text-align:left;color:#f87171;margin-top:6px;border-top:1px solid #1a2540;padding-top:13px;">'
        '🚪 Logout</button>'
    )

    navbar_html = f"""
<style>
#dv-navbar {{
    position:fixed; top:0; left:0; right:0; height:56px;
    background:linear-gradient(90deg,#080c14 0%,#0d1220 100%);
    border-bottom:1px solid #1a2540;
    display:flex; align-items:center; padding:0 16px; gap:4px;
    z-index:99999; box-shadow:0 2px 20px rgba(0,0,0,.6);
    font-family:'Inter',-apple-system,sans-serif;
}}
.nb-logo {{ display:flex;align-items:center;gap:7px;margin-right:10px;flex-shrink:0; }}
.nb-logo-icon {{ font-size:1.3rem;line-height:1; }}
.nb-logo-text {{ font-size:.95rem;font-weight:800;color:#38bdf8;letter-spacing:-.4px;white-space:nowrap; }}
.nb-sep {{ width:1px;height:28px;background:#1e2d48;margin:0 8px;flex-shrink:0; }}
.nb-links {{ display:flex;align-items:center;gap:2px;flex:1;overflow-x:auto;scrollbar-width:none; }}
.nb-links::-webkit-scrollbar {{ display:none; }}
.nb-link:hover {{ background:#1e2d48 !important; color:#dce7f3 !important; }}
.nb-right {{ display:flex;align-items:center;gap:8px;flex-shrink:0;margin-left:auto; }}
.nb-user {{ display:flex;flex-direction:column;align-items:flex-end;line-height:1.3; }}
.nb-username {{ font-size:.78rem;font-weight:700;color:#dce7f3;white-space:nowrap; }}
.nb-role {{ font-size:.62rem;color:#475569;white-space:nowrap; }}
.nb-progress {{ display:flex;align-items:center;gap:5px;background:#0d1627;border:1px solid #1e2d48;border-radius:8px;padding:4px 9px; }}
.nb-pct {{ font-size:.82rem;font-weight:800;line-height:1; }}
.nb-track {{ width:40px;height:4px;background:#1a2540;border-radius:99px;overflow:hidden; }}
.nb-fill {{ height:100%;border-radius:99px; }}
.nb-count {{ font-size:.6rem;color:#475569;white-space:nowrap; }}
.nb-logout-btn {{
    padding:5px 10px;border-radius:7px;font-size:.73rem;font-weight:600;
    color:#f87171;border:1px solid #4a1a1a;background:#1a0d0d;
    white-space:nowrap;flex-shrink:0;cursor:pointer;
    font-family:'Inter',sans-serif;transition:background .15s;
}}
.nb-logout-btn:hover {{ background:#2a1010; }}
#dv-mob-toggle {{
    display:none;background:#0d1627;border:1px solid #1e2d48;
    border-radius:8px;padding:6px 9px;cursor:pointer;flex-shrink:0;margin-left:4px;
}}
#dv-mob-toggle span {{
    display:block;width:18px;height:2px;background:#38bdf8;
    border-radius:2px;margin:3px 0;transition:all .2s;
}}
#dv-mob-menu {{
    display:none;position:fixed;top:56px;left:0;right:0;
    background:#0d1220;border-bottom:1px solid #1a2540;
    padding:8px 12px 14px;z-index:99998;flex-direction:column;gap:2px;
    box-shadow:0 8px 24px rgba(0,0,0,.5);
}}
.mob-link:hover {{ background:#1e2d48 !important; color:#38bdf8 !important; }}
@media(max-width:768px) {{
    .nb-links {{ display:none !important; }}
    .nb-user  {{ display:none !important; }}
    .nb-sep   {{ display:none !important; }}
    #dv-mob-toggle {{ display:block !important; }}
}}
</style>

<div id="dv-navbar">
  <div class="nb-logo">
    <span class="nb-logo-icon">⚡</span>
    <span class="nb-logo-text">DevLife OS</span>
  </div>
  <div class="nb-sep"></div>
  <div class="nb-links">{nav_items_html}</div>
  <div class="nb-right">
    <div class="nb-user">
      <span class="nb-username">{uname}{admin_badge}</span>
      <span class="nb-role">{st.session_state.role[:24]}</span>
    </div>
    <div class="nb-progress">
      <span class="nb-pct" style="color:{bar_color}">{pct:.0f}%</span>
      <div class="nb-track">
        <div class="nb-fill" style="background:{bar_color};width:{pct:.0f}%"></div>
      </div>
      <span class="nb-count">{done}/{total}</span>
    </div>
    <button class="nb-logout-btn" data-page="__logout__">🚪 Logout</button>
  </div>
  <button id="dv-mob-toggle" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</div>

<div id="dv-mob-menu">{mob_items_html}</div>

<div style="height:64px"></div>

<script>
(function() {{
  // ── Click any nav button → find the matching hidden Streamlit button and click it ──
  function navigate(pageKey) {{
    // Close mobile menu if open
    var mob = document.getElementById('dv-mob-menu');
    if (mob) mob.style.display = 'none';
    mobOpen = false;

    // Find the hidden Streamlit button whose label is "_nav_<pageKey>"
    // Streamlit renders buttons as <button> with the label as text content
    var allBtns = document.querySelectorAll('button');
    for (var i = 0; i < allBtns.length; i++) {{
      var btn = allBtns[i];
      if (btn.textContent.trim() === '_nav_' + pageKey) {{
        btn.click();
        return;
      }}
    }}
  }}

  // Wire up desktop nav buttons
  document.querySelectorAll('.nb-link, .nb-logout-btn').forEach(function(btn) {{
    btn.addEventListener('click', function(e) {{
      e.preventDefault();
      navigate(btn.getAttribute('data-page'));
    }});
  }});

  // Wire up mobile nav buttons
  document.querySelectorAll('.mob-link').forEach(function(btn) {{
    btn.addEventListener('click', function(e) {{
      e.preventDefault();
      navigate(btn.getAttribute('data-page'));
    }});
  }});

  // Mobile hamburger toggle
  var mobOpen = false;
  var mobToggle = document.getElementById('dv-mob-toggle');
  if (mobToggle) {{
    mobToggle.addEventListener('click', function() {{
      mobOpen = !mobOpen;
      var mob = document.getElementById('dv-mob-menu');
      if (mob) mob.style.display = mobOpen ? 'flex' : 'none';
    }});
  }}
}})();
</script>
"""

    st.markdown(navbar_html, unsafe_allow_html=True)
    return active


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
    greet_key = "good_morning" if hour < 12 else "good_afternoon" if hour < 17 else "good_evening"
    greet = t(greet_key)

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
    c1.markdown(mbox(f"{pct}%",                        t("todays_completion"),  "#38bdf8"), unsafe_allow_html=True)
    c2.markdown(mbox(f"{done}/{total}",                t("habits_done_today"),   "#34d399"), unsafe_allow_html=True)
    c3.markdown(mbox(f"{comp_rate(uid,7)}%",           t("7_day_avg"),           "#fbbf24"), unsafe_allow_html=True)
    c4.markdown(mbox(str(len(get_goals(uid))),         t("active_goals"),        "#a78bfa"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    # ── Habit checklist
    with left:
        section(t("todays_habits"))
        if not logs:
            st.info(t("no_habits_msg"))
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
        section(t("active_goals_sec"))
        goals = get_goals(uid)
        if not goals:
            st.info(t("no_goals_msg"))
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

        section(t("quick_log"))
        with st.form("quick_log"):
            dw = st.slider(t("deep_work_hrs"), 0.0, 12.0, 3.0, 0.5)
            cd = st.slider(t("coding_hrs"),    0.0, 12.0, 3.0, 0.5)
            ex = st.slider(t("exercise_min"),  0, 180, 30, 5)
            sl = st.slider(t("sleep_hrs"),     4.0, 10.0, 7.5, 0.25)
            opb_dash = st.slider(t("one_pct_better"), 1, 100, 50,
                                 help="How much 1% better are you today?")
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            saved_ql = st.form_submit_button(t("save"), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if saved_ql:
                save_metrics(uid, today_str, dw, cd, ex, sl, one_pct_better=opb_dash)
                st.success(t("saved"))


# ──────────────────────────────────────────────────────────────
#  PAGE: DAILY ROUTINE
# ──────────────────────────────────────────────────────────────
def page_daily():
    uid = st.session_state.user_id
    st.markdown(t("daily_routine_title"))

    sel     = st.date_input(t("date_lbl"), value=datetime.date.today(), max_value=datetime.date.today())
    sel_str = sel.isoformat()
    ensure_today_logs(uid, sel_str)

    tab1, tab2, tab3 = st.tabs([t("habits_tab"), t("journal_tab"), t("metrics_tab")])

    with tab1:
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
                    checked = st.checkbox(t("mark_complete"), value=bool(log["completed"]),
                                          key=f"rout_{sel_str}_{log['id']}")
                    if st.button(t("save"), key=f"save_{sel_str}_{log['id']}"):
                        set_log(log["id"], int(checked))
                        st.success(t("saved"))
                        st.rerun()

    with tab2:
        st.markdown(f'''<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
            <span style="font-size:1.3rem">📝</span>
            <span style="font-size:1.1rem;font-weight:800;color:#dce7f3">{t("journal_title")}</span>
        </div>''', unsafe_allow_html=True)
        ex = get_journal(uid, sel_str)

        # Motivational quote
        qt, qa, qc = random_quote_by_cat("Mindset")
        st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

        with st.form("journal_form"):
            # ── Section A: Nightly Review ──
            st.markdown('''<div class="oc-section oc-section-fire">
                <div style="font-size:.7rem;font-weight:700;letter-spacing:1.4px;
                            text-transform:uppercase;color:#f43127;margin-bottom:10px">
                    🌙 Nightly Review — দিন শেষের হিসাব
                </div>''', unsafe_allow_html=True)
            nr_val = ex["nightly_review"] if ex and ex["nightly_review"] else ""
            nightly_review = st.text_area(
                t("j_accomplished"),
                value=nr_val, height=90,
                placeholder="I shipped the auth module, fixed 2 bugs, reviewed 3 PRs…",
            )
            imp_val = ex["q3"] if ex and ex["q3"] else ""
            q3 = st.text_area(
                t("j_improve"),
                value=imp_val, height=80,
                placeholder="Tomorrow I need to focus more on deep work before checking messages…",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Section B: Tomorrow's Plan ──
            st.markdown('''<div class="oc-section oc-section-gold">
                <div style="font-size:.7rem;font-weight:700;letter-spacing:1.4px;
                            text-transform:uppercase;color:#fcb302;margin-bottom:10px">
                    🎯 Tomorrow's Plan — আগের রাতের পরিকল্পনা
                </div>''', unsafe_allow_html=True)
            tp_val = ex["tomorrow_plan"] if ex and ex["tomorrow_plan"] else ""
            tomorrow_plan = st.text_area(
                t("j_tomorrow_plan"),
                value=tp_val, height=90,
                placeholder="1. Complete the payment API\n2. Write unit tests\n3. Review team PRs",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Section C: Information Capture ──
            st.markdown('''<div class="oc-section oc-section-teal">
                <div style="font-size:.7rem;font-weight:700;letter-spacing:1.4px;
                            text-transform:uppercase;color:#2dd4bf;margin-bottom:10px">
                    🔗 Information Capture
                </div>''', unsafe_allow_html=True)
            ic_val = ex["info_capture"] if ex and ex["info_capture"] else ""
            info_capture = st.text_area(
                t("j_capture"),
                value=ic_val, height=80,
                placeholder="https://... | Learned: async generators in Python | Task: update README",
            )
            bd_val = ex["brain_dump"] if ex and ex["brain_dump"] else ""
            bd = st.text_area(
                t("brain_dump"),
                value=bd_val, height=80,
                placeholder="Any ideas, random thoughts, things on your mind…",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Section D: Mood, Energy & Mindset Check ──
            st.markdown('''<div class="oc-section oc-section-blue">
                <div style="font-size:.7rem;font-weight:700;letter-spacing:1.4px;
                            text-transform:uppercase;color:#38bdf8;margin-bottom:10px">
                    🧠 Mindset Check + Vitals
                </div>''', unsafe_allow_html=True)
            mc, ec = st.columns(2)
            mood   = mc.slider(t("mood"),   1, 10, int(ex["mood"])   if ex else 7)
            energy = ec.slider(t("energy"), 1, 10, int(ex["energy"]) if ex else 7)

            # Gratitude (q1) and focus problem (q2) kept as compact fields
            gc, fc = st.columns(2)
            q1_val = ex["q1"] if ex and ex["q1"] else ""
            q2_val = ex["q2"] if ex and ex["q2"] else ""
            q1 = gc.text_area(t("q1"), value=q1_val, height=70,
                               placeholder="I am grateful for…")
            q2 = fc.text_area(t("q2"), value=q2_val, height=70,
                               placeholder="The one technical problem I must solve…")

            # Mindset checkboxes
            risk_default    = bool(ex["mindset_risk"])    if ex else False
            compare_default = bool(ex["mindset_compare"]) if ex else False
            mindset_risk    = st.checkbox(t("j_risk"),    value=risk_default)
            mindset_compare = st.checkbox(t("j_compare"), value=compare_default)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Save button — fire accent ──
            st.markdown('<div class="btn-fire">', unsafe_allow_html=True)
            submitted = st.form_submit_button(t("j_save"), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if submitted:
                save_journal(uid, sel_str, q1, q2, q3, bd, mood, energy,
                             nightly_review=nightly_review,
                             tomorrow_plan=tomorrow_plan,
                             info_capture=info_capture,
                             mindset_risk=mindset_risk,
                             mindset_compare=mindset_compare)
                st.success(t("journal_saved"))

    with tab3:
        section(t("log_metrics"))
        with conn() as db:
            em = db.execute(
                "SELECT * FROM daily_metrics WHERE user_id=? AND date=?", (uid, sel_str)
            ).fetchone()

        def _em(col, default):
            try:
                return em[col] if em and em[col] is not None else default
            except (IndexError, KeyError):
                return default

        with st.form("metrics_form"):
            # ── Core performance ──
            st.markdown('''<div class="oc-section oc-section-blue">
                <div style="font-size:.7rem;font-weight:700;letter-spacing:1.4px;
                            text-transform:uppercase;color:#38bdf8;margin-bottom:10px">
                    ⏱ Core Performance
                </div>''', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                dw   = st.number_input(t("deep_work_hrs"), 0.0, 16.0, float(_em("deep_work_hrs", 0.0)), 0.5)
                code = st.number_input(t("coding_hrs"),    0.0, 16.0, float(_em("coding_hrs",    0.0)), 0.5)
            with c2:
                ex_v = st.number_input(t("exercise_min"),  0,   300,  int(_em("exercise_mins",   0)),   5)
                sl   = st.number_input(t("sleep_hrs"),     0.0, 12.0, float(_em("sleep_hrs",     7.0)), 0.25)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Deep Work & Execution quality ──
            st.markdown('''<div class="oc-section oc-section-fire">
                <div style="font-size:.7rem;font-weight:700;letter-spacing:1.4px;
                            text-transform:uppercase;color:#f43127;margin-bottom:10px">
                    🔥 Deep Work & Execution Quality
                </div>''', unsafe_allow_html=True)
            qd = st.slider(
                t("quick_decisions"), 1, 10, int(_em("quick_decisions", 5)),
                help="How many quick, decisive decisions did you make today without overthinking?",
            )
            fp = st.slider(
                t("focus_vs_distract"), 0, 100, int(_em("focus_pct", 50)),
                help="Estimate: what % of your work time was truly focused vs distracted/complaining?",
            )
            # Visual focus bar
            fp_color = "#34d399" if fp >= 70 else "#fcb302" if fp >= 40 else "#f43127"
            st.markdown(
                f'''<div style="background:#111c30;border-radius:99px;height:8px;overflow:hidden;margin:4px 0 8px">
                    <div style="height:100%;border-radius:99px;background:{fp_color};width:{fp}%"></div>
                </div>
                <small style="color:#475569">{fp}% focused execution</small>''',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # ── 1% Better tracker ──
            st.markdown('''<div class="oc-section oc-section-gold">
                <div style="font-size:.7rem;font-weight:700;letter-spacing:1.4px;
                            text-transform:uppercase;color:#fcb302;margin-bottom:10px">
                    📈 1% Better Daily Growth
                </div>''', unsafe_allow_html=True)
            opb = st.slider(
                t("one_pct_better"), 1, 100, int(_em("one_pct_better", 50)),
                help="On a scale of 1-100, how much better are you today vs yesterday?",
            )
            opb_color = "#34d399" if opb >= 70 else "#fcb302" if opb >= 40 else "#f43127"
            st.markdown(
                f'''<div style="background:#111c30;border-radius:99px;height:8px;overflow:hidden;margin:4px 0 8px">
                    <div style="height:100%;border-radius:99px;
                                background:linear-gradient(90deg,#f43127,#fcb302,{opb_color});
                                width:{opb}%"></div>
                </div>
                <small style="color:#475569">{opb}/100 — 1% better today</small>''',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Save button — gold accent ──
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            submitted_m = st.form_submit_button(t("save_metrics_btn"), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if submitted_m:
                save_metrics(uid, sel_str, dw, code, ex_v, sl,
                             quick_decisions=qd, focus_pct=fp, one_pct_better=opb)
                st.success(t("saved"))


# ──────────────────────────────────────────────────────────────
#  PAGE: GOALS
# ──────────────────────────────────────────────────────────────
def page_goals():
    uid = st.session_state.user_id
    st.markdown(t("goal_management"))
    t1, t2, t3 = st.tabs([t("active_goals_tab"), t("new_goal_tab"), t("completed_tab")])

    tf_icons  = {"Daily":"📅","Weekly":"📆","Monthly":"🗓️","Yearly":"🏆"}
    tf_pills  = {"Daily":"pill-blue","Weekly":"pill-green","Monthly":"pill-purple","Yearly":"pill-amber"}
    cat_pills = {"Coding":"pill-blue","Finance":"pill-amber","Health":"pill-green",
                 "Learning":"pill-teal","Social":"pill-red","General":"pill-slate"}

    with t1:
        tf = st.selectbox(t("filter"), ["All","Daily","Weekly","Monthly","Yearly"])
        goals = get_goals(uid) if tf == "All" else get_goals(uid, tf)

        if not goals:
            st.info(t("no_active_goals"))
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
                                nv = st.slider(t("progress_pct"), 0, 100, int(g["progress"]))
                                if st.form_submit_button(t("update")):
                                    with conn() as db:
                                        db.execute("UPDATE goals SET progress=? WHERE id=? AND user_id=?",
                                                   (nv, g["id"], uid))
                                    st.success(t("saved"))
                                    st.rerun()
                        with dc:
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button(t("complete"), key=f"cmp_{g['id']}"):
                                with conn() as db:
                                    db.execute("UPDATE goals SET status='completed' WHERE id=? AND user_id=?",
                                               (g["id"], uid))
                                st.success("Goal completed! 🎉")
                                st.rerun()
                            if st.button(t("delete"), key=f"del_{g['id']}"):
                                with conn() as db:
                                    db.execute("DELETE FROM goals WHERE id=? AND user_id=?", (g["id"], uid))
                                st.rerun()

    with t2:
        section("➕  Create New Goal")
        qt, qa, qc = random_quote_by_cat("Career")
        st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)
        with st.form("add_goal"):
            title     = st.text_input(t("goal_title_lbl"), placeholder="e.g. Ship my first SaaS product")
            c1, c2   = st.columns(2)
            category  = c1.selectbox(t("category"), ["Coding","Finance","Health","Learning","Social","General"])
            timeframe = c2.selectbox(t("timeframe"), ["Daily","Weekly","Monthly","Yearly"])
            deadline  = st.date_input(t("deadline"), value=datetime.date.today() + datetime.timedelta(days=30))
            if st.form_submit_button(t("create_goal_btn"), use_container_width=True):
                if not title:
                    st.error(t("name_required"))
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
    st.markdown(t("habit_manager"))
    habits = get_habits(uid)
    t1, t2 = st.tabs([t("streaks_heatmap"), t("add_remove")])

    with t1:
        if not habits:
            st.info(t("no_habits_msg"))
        else:
            section(t("current_streaks"))
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
        section(t("add_custom_habit"))
        with st.form("add_habit"):
            name = st.text_input(t("habit_name"))
            c1, c2 = st.columns(2)
            cat  = c1.selectbox(t("category"), ["Mental","Health","Coding"])
            slot = c2.selectbox("Slot",     ["Morning","Work","Fitness","Learning","Night"])
            if st.form_submit_button(t("add_habit_btn"), use_container_width=True):
                if not name:
                    st.error(t("name_required"))
                else:
                    with conn() as db:
                        db.execute("INSERT INTO habits (user_id,name,category,slot) VALUES (?,?,?,?)",
                                   (uid, name, cat, slot))
                    st.success(t("habit_added"))
                    st.rerun()

        section(t("manage_habits"))
        for h in habits:
            hc1, hc2 = st.columns([9, 2])
            hc1.markdown(f'{SLOT_ICONS.get(h["slot"],"")} {h["name"]} '
                         f'<span class="pill pill-slate">{h["slot"]}</span>',
                         unsafe_allow_html=True)
            if hc2.button(t("remove"), key=f"rm_{h['id']}"):
                with conn() as db:
                    db.execute("DELETE FROM habits WHERE id=? AND user_id=?", (h["id"], uid))
                    db.execute("DELETE FROM habit_logs WHERE habit_id=? AND user_id=?", (h["id"], uid))
                st.rerun()


# ──────────────────────────────────────────────────────────────
#   PAGE: REVIEWS
# ──────────────────────────────────────────────────────────────
def page_reviews():
    uid = st.session_state.user_id
    st.markdown(t("progress_reviews"))
    t1, t2, t3 = st.tabs([t("weekly_tab"), t("monthly_tab"), t("yearly_tab")])

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
        c1.markdown(mbox(f"{wr}%",       f"{label} {t('habit_rate')}",  "#34d399"), unsafe_allow_html=True)
        c2.markdown(mbox(f"{adw:.1f}h",  t("avg_deep_work"),             "#38bdf8"), unsafe_allow_html=True)
        c3.markdown(mbox(f"{aex:.0f}m",  t("avg_exercise"),              "#34d399"), unsafe_allow_html=True)
        c4.markdown(mbox(f"{asl:.1f}h",  t("avg_sleep"),                 "#a78bfa"), unsafe_allow_html=True)

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
            if st.form_submit_button(t("save_skill_ratings"), use_container_width=True):
                for sk, r in ratings.items():
                    save_skill(uid, sk, r, nm, ny)
                st.success(t("skill_ratings_saved"))
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
    st.markdown(t("skills_title"))

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
    st.markdown(t("finance_title"))

    qt, qa, qc = random_quote_by_cat("Finance")
    st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

    t1, t2 = st.tabs([t("rules_income"), t("finance_goals_tab")])

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
            st.info(t("no_finance_goals"))
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
    st.markdown(t("profile_settings"))

    with conn() as db:
        u = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

    if u:
        st.markdown(f"""<div class="dv-card dv-card-blue">
            <h3 style="margin:0;color:#38bdf8">@{u['username']}</h3>
            <p style="margin:5px 0;color:#475569">{u['role']}</p>
            <p style="margin:3px 0">
                <span class="pill pill-teal">Stack: {u['stack']}</span>
            </p>
            <p style="margin:5px 0;color:#475569;font-size:.8rem">{t('member_since')} {u['created_at']}</p>
        </div>""", unsafe_allow_html=True)

    habits_count = len(get_habits(uid))
    comp_goals   = get_goals(uid, status="completed")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(mbox(habits_count,               t("active_habits_kpi"), "#34d399"), unsafe_allow_html=True)
    c2.markdown(mbox(len(comp_goals),            t("goals_done"),        "#fbbf24"), unsafe_allow_html=True)
    c3.markdown(mbox(f"{comp_rate(uid,7)}%",     t("7_day_rate"),        "#38bdf8"), unsafe_allow_html=True)
    c4.markdown(mbox(f"{comp_rate(uid,30)}%",    t("30_day_rate"),       "#a78bfa"), unsafe_allow_html=True)

    section(t("update_profile"))
    with st.form("profile_form"):
        role_opts = ["Junior Developer","Mid-level Developer","Senior Developer",
                     "Full-stack Developer","Student"]
        cur_role  = u["role"] if u and u["role"] in role_opts else role_opts[0]
        new_role  = st.selectbox(t("role_lbl"), role_opts, index=role_opts.index(cur_role))
        new_stack = st.text_input(t("stack_lbl"), value=u["stack"] if u else "")
        if st.form_submit_button(t("save_changes"), use_container_width=True):
            with conn() as db:
                db.execute("UPDATE users SET role=?,stack=? WHERE id=?", (new_role, new_stack, uid))
            st.session_state.role  = new_role
            st.session_state.stack = new_stack
            st.success(t("profile_updated"))

    section(t("quotes_library"))
    st.markdown("*Every quote in DevLife OS — rotating daily on your dashboard.*")
    cat_filter = st.selectbox(t("filter_by_cat"),
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
#  PAGE: ADMIN PANEL
# ──────────────────────────────────────────────────────────────
def page_admin():
    if not st.session_state.get("is_admin"):
        st.error("⛔ Access denied. Admins only.")
        return

    # ── Admin re-authentication gate ──
    if not st.session_state.get("admin_authenticated"):
        st.markdown("""
        <div class="admin-gate">
            <div class="admin-gate-icon">🛡️</div>
            <div class="admin-gate-title">Admin Authentication</div>
            <div class="admin-gate-sub">
                Re-enter your password to access the Admin Panel.
            </div>
        </div>
        """, unsafe_allow_html=True)

        _, mid, _ = st.columns([1, 1.4, 1])
        with mid:
            with st.form("admin_auth_form"):
                admin_pw = st.text_input(
                    "Admin Password",
                    type="password",
                    placeholder="Enter your password…",
                )
                submitted = st.form_submit_button("🔓 Unlock Admin Panel", use_container_width=True)
                if submitted:
                    # Verify against stored hash
                    with conn() as db:
                        row = db.execute(
                            "SELECT id FROM users WHERE id=? AND password_hash=?",
                            (st.session_state.user_id, make_hash(admin_pw)),
                        ).fetchone()
                    if row:
                        st.session_state.admin_authenticated = True
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password. Access denied.")
        return  # Don't render the panel until authenticated

    # ── Authenticated — show full admin panel ──
    st.markdown("## 🛡️ Admin Panel")

    # Lock button to end admin session
    col_title, col_lock = st.columns([8, 2])
    with col_lock:
        if st.button("🔒 Lock Panel", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.rerun()

    st.markdown("""<div class="admin-card">
        <b style="color:#f87171;font-size:1.05rem">⚠️ Administrator Zone</b><br>
        <span style="color:#94a3b8;font-size:.85rem">
            Manage users carefully. Deleted users and all their data are permanently removed.
        </span>
    </div>""", unsafe_allow_html=True)

    # ── Load all users ──
    with conn() as db:
        users = db.execute(
            "SELECT id, username, role, stack, created_at, is_admin FROM users ORDER BY created_at DESC"
        ).fetchall()

    if not users:
        st.info("No users found.")
        return

    current_uid = st.session_state.user_id

    # ── Stats ──
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div style="background:#0d1627;border:1px solid #1e2d48;border-radius:12px;
        padding:18px 16px;text-align:center">
        <div style="font-size:2rem;font-weight:800;color:#38bdf8">{len(users)}</div>
        <div style="font-size:.72rem;color:#475569;text-transform:uppercase;letter-spacing:.8px;margin-top:4px">Total Users</div>
    </div>""", unsafe_allow_html=True)
    admin_count = sum(1 for u in users if u["is_admin"])
    c2.markdown(f"""<div style="background:#0d1627;border:1px solid #1e2d48;border-radius:12px;
        padding:18px 16px;text-align:center">
        <div style="font-size:2rem;font-weight:800;color:#f87171">{admin_count}</div>
        <div style="font-size:.72rem;color:#475569;text-transform:uppercase;letter-spacing:.8px;margin-top:4px">Admins</div>
    </div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div style="background:#0d1627;border:1px solid #1e2d48;border-radius:12px;
        padding:18px 16px;text-align:center">
        <div style="font-size:2rem;font-weight:800;color:#34d399">{len(users) - admin_count}</div>
        <div style="font-size:.72rem;color:#475569;text-transform:uppercase;letter-spacing:.8px;margin-top:4px">Regular Users</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──
    tab_users, tab_delete = st.tabs(["👥  All Users", "🗑️  Delete Users"])

    with tab_users:
        st.markdown('<div class="sec-header">Registered Users</div>', unsafe_allow_html=True)
        for u in users:
            badge = '<span class="admin-badge">ADMIN</span>' if u["is_admin"] else ""
            you   = " <span style='color:#34d399;font-size:.7rem'>(you)</span>" if u["id"] == current_uid else ""
            st.markdown(f"""
            <div style="background:#0d1627;border:1px solid #1e2d48;border-radius:10px;
                        padding:12px 16px;margin:5px 0;display:flex;align-items:center;gap:10px">
                <div style="font-size:1.4rem">👤</div>
                <div style="flex:1">
                    <div style="font-weight:700;color:#dce7f3">
                        @{u['username']}{badge}{you}
                    </div>
                    <div style="font-size:.75rem;color:#475569;margin-top:2px">
                        {u['role']} &nbsp;·&nbsp; Stack: {(u['stack'] or '')[:40]}
                        &nbsp;·&nbsp; Joined: {u['created_at']}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    with tab_delete:
        st.markdown('<div class="sec-header">Delete Users</div>', unsafe_allow_html=True)
        st.warning("⚠️ Deleting a user permanently removes their account, habits, goals, journal entries, and all data.", icon="⚠️")

        # Filter out self and other admins for safety
        deletable = [u for u in users if u["id"] != current_uid and not u["is_admin"]]
        admin_only = [u for u in users if u["id"] != current_uid and u["is_admin"]]

        if not deletable:
            st.info("No regular users available to delete.")
        else:
            user_options = {f"@{u['username']}  ({u['role']}) — joined {u['created_at']}": u["id"] for u in deletable}

            selected_labels = st.multiselect(
                "Select users to delete",
                options=list(user_options.keys()),
                placeholder="Choose one or more users…",
            )

            if selected_labels:
                st.markdown(f"""<div style="background:#1a0d0d;border:1px solid #f87171;border-radius:9px;
                    padding:10px 14px;margin:10px 0">
                    <b style="color:#f87171">⚠️ You are about to delete {len(selected_labels)} user(s):</b><br>
                    <span style="color:#94a3b8;font-size:.85rem">{', '.join(selected_labels)}</span>
                </div>""", unsafe_allow_html=True)

                confirm = st.checkbox(f"I confirm I want to permanently delete {len(selected_labels)} user(s)")
                if confirm:
                    if st.button("🗑️ Delete Selected Users", type="primary", use_container_width=True):
                        ids_to_delete = [user_options[lbl] for lbl in selected_labels]
                        with conn() as db:
                            for uid_del in ids_to_delete:
                                db.execute("DELETE FROM habit_logs WHERE user_id=?", (uid_del,))
                                db.execute("DELETE FROM habits WHERE user_id=?", (uid_del,))
                                db.execute("DELETE FROM goals WHERE user_id=?", (uid_del,))
                                db.execute("DELETE FROM journal_entries WHERE user_id=?", (uid_del,))
                                db.execute("DELETE FROM daily_metrics WHERE user_id=?", (uid_del,))
                                db.execute("DELETE FROM skill_ratings WHERE user_id=?", (uid_del,))
                                db.execute("DELETE FROM users WHERE id=?", (uid_del,))
                        st.success(f"✅ Deleted {len(ids_to_delete)} user(s) successfully.")
                        st.rerun()

        if admin_only:
            st.markdown('<div class="sec-header" style="margin-top:20px">Admin Users (Protected)</div>', unsafe_allow_html=True)
            st.info("Admin accounts cannot be deleted through this panel for safety reasons.")
            for u in admin_only:
                st.markdown(f"""<div style="background:#0d1627;border:1px solid #1e2d48;border-radius:9px;
                    padding:10px 14px;margin:4px 0;opacity:.7">
                    🛡️ <b style="color:#f87171">@{u['username']}</b>
                    <span style="color:#475569;font-size:.75rem"> — Admin · {u['created_at']}</span>
                </div>""", unsafe_allow_html=True)

        # ── Promote / demote admin ──
        st.markdown('<div class="sec-header" style="margin-top:20px">Grant / Revoke Admin Access</div>', unsafe_allow_html=True)
        regular_users = [u for u in users if u["id"] != current_uid and not u["is_admin"]]
        admin_users   = [u for u in users if u["id"] != current_uid and u["is_admin"]]

        col_promote, col_demote = st.columns(2)
        with col_promote:
            if regular_users:
                promote_opts = {f"@{u['username']}": u["id"] for u in regular_users}
                to_promote = st.selectbox("Promote to Admin", ["— select —"] + list(promote_opts.keys()), key="promote_sel")
                if to_promote != "— select —" and st.button("⬆️ Grant Admin", use_container_width=True):
                    with conn() as db:
                        db.execute("UPDATE users SET is_admin=1 WHERE id=?", (promote_opts[to_promote],))
                    st.success(f"{to_promote} is now an admin.")
                    st.rerun()
            else:
                st.info("No regular users to promote.")

        with col_demote:
            if admin_users:
                demote_opts = {f"@{u['username']}": u["id"] for u in admin_users}
                to_demote = st.selectbox("Revoke Admin", ["— select —"] + list(demote_opts.keys()), key="demote_sel")
                if to_demote != "— select —" and st.button("⬇️ Revoke Admin", use_container_width=True):
                    with conn() as db:
                        db.execute("UPDATE users SET is_admin=0 WHERE id=?", (demote_opts[to_demote],))
                    st.success(f"{to_demote} is no longer an admin.")
                    st.rerun()
            else:
                st.info("No other admins to demote.")


# ──────────────────────────────────────────────────────────────
#  PAGE: JOURNAL  (dedicated full-page daily journal)
# ──────────────────────────────────────────────────────────────
def page_journal():
    uid = st.session_state.user_id
    st.markdown("## 📝 Daily Journal")

    sel     = st.date_input("Date", value=datetime.date.today(), max_value=datetime.date.today())
    sel_str = sel.isoformat()
    ex      = get_journal(uid, sel_str)

    qt, qa, qc = random_quote_by_cat("Mindset")
    st.markdown(quote_card(qt, qa, qc), unsafe_allow_html=True)

    with st.form("journal_page_form"):
        # ── Nightly Review ──
        st.markdown('<div class="oc-section oc-section-fire"><div style="font-size:.7rem;font-weight:700;'
                    'letter-spacing:1.4px;text-transform:uppercase;color:#f43127;margin-bottom:10px">'
                    '🌙 Nightly Review — দিন শেষের হিসাব</div>', unsafe_allow_html=True)
        nightly_review = st.text_area(
            t("j_accomplished"),
            value=ex["nightly_review"] if ex and ex["nightly_review"] else "",
            height=100, placeholder="I shipped the auth module, fixed 2 bugs…")
        q3 = st.text_area(
            t("j_improve"),
            value=ex["q3"] if ex and ex["q3"] else "",
            height=80, placeholder="Tomorrow I need to focus more on deep work…")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Tomorrow's Plan ──
        st.markdown('<div class="oc-section oc-section-gold"><div style="font-size:.7rem;font-weight:700;'
                    'letter-spacing:1.4px;text-transform:uppercase;color:#fcb302;margin-bottom:10px">'
                    "🎯 Tomorrow's Plan — আগের রাতের পরিকল্পনা</div>", unsafe_allow_html=True)
        tomorrow_plan = st.text_area(
            t("j_tomorrow_plan"),
            value=ex["tomorrow_plan"] if ex and ex["tomorrow_plan"] else "",
            height=100, placeholder="1. Complete the payment API\n2. Write unit tests\n3. Review PRs")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Information Capture ──
        st.markdown('<div class="oc-section oc-section-teal"><div style="font-size:.7rem;font-weight:700;'
                    'letter-spacing:1.4px;text-transform:uppercase;color:#2dd4bf;margin-bottom:10px">'
                    '🔗 Information Capture</div>', unsafe_allow_html=True)
        info_capture = st.text_area(
            t("j_capture"),
            value=ex["info_capture"] if ex and ex["info_capture"] else "",
            height=80, placeholder="https://… | Learned: async generators | Task: update README")
        bd = st.text_area(
            t("brain_dump"),
            value=ex["brain_dump"] if ex and ex["brain_dump"] else "",
            height=80, placeholder="Any ideas, random thoughts…")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Mindset + Vitals ──
        st.markdown('<div class="oc-section oc-section-blue"><div style="font-size:.7rem;font-weight:700;'
                    'letter-spacing:1.4px;text-transform:uppercase;color:#38bdf8;margin-bottom:10px">'
                    '🧠 Mindset Check + Vitals</div>', unsafe_allow_html=True)
        mc, ec = st.columns(2)
        mood   = mc.slider(t("mood"),   1, 10, int(ex["mood"])   if ex else 7)
        energy = ec.slider(t("energy"), 1, 10, int(ex["energy"]) if ex else 7)
        gc, fc = st.columns(2)
        q1 = gc.text_area(t("q1"), value=ex["q1"] if ex and ex["q1"] else "",
                          height=70, placeholder="I am grateful for…")
        q2 = fc.text_area(t("q2"), value=ex["q2"] if ex and ex["q2"] else "",
                          height=70, placeholder="The one technical problem I must solve…")
        mindset_risk    = st.checkbox(t("j_risk"),    value=bool(ex["mindset_risk"])    if ex else False)
        mindset_compare = st.checkbox(t("j_compare"), value=bool(ex["mindset_compare"]) if ex else False)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="btn-fire">', unsafe_allow_html=True)
        submitted = st.form_submit_button(t("j_save"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if submitted:
            save_journal(uid, sel_str, q1, q2, q3, bd, mood, energy,
                         nightly_review=nightly_review, tomorrow_plan=tomorrow_plan,
                         info_capture=info_capture,
                         mindset_risk=mindset_risk, mindset_compare=mindset_compare)
            st.success(t("journal_saved"))

    # ── Past entries ──
    section("📅 Past Journal Entries — last 14 days")
    jdf = get_journal_df(uid, 14)
    if jdf.empty:
        st.info("No journal entries yet. Start writing above.")
    else:
        for _, row in jdf.sort_values("date", ascending=False).iterrows():
            mood_v   = row.get("mood", "?")
            energy_v = row.get("energy", "?")
            with st.expander(f"📝 {row['date']}  —  Mood {mood_v}/10  ·  Energy {energy_v}/10"):
                if row.get("nightly_review"):
                    st.markdown(f"**✅ Accomplished:** {row['nightly_review']}")
                if row.get("tomorrow_plan"):
                    st.markdown(f"**🎯 Tomorrow's plan:** {row['tomorrow_plan']}")
                if row.get("q1"):
                    st.markdown(f"**🙏 Grateful:** {row['q1']}")
                if row.get("q2"):
                    st.markdown(f"**🎯 Focus problem:** {row['q2']}")
                if row.get("brain_dump"):
                    st.markdown(f"**🧠 Brain dump:** {row['brain_dump']}")
                if row.get("info_capture"):
                    st.markdown(f"**🔗 Captured:** {row['info_capture']}")


# ──────────────────────────────────────────────────────────────
#  ROUTER
# ──────────────────────────────────────────────────────────────
PAGES = {
    "dashboard":    page_dashboard,
    "daily":        page_daily,
    "goals":        page_goals,
    "habits":       page_habits,
    "reviews":      page_reviews,
    "skills":       page_skills,
    "finance":      page_finance,
    "journal":      page_journal,
    "profile":      page_profile,
    "admin":        page_admin,
}

def main():
    # Init session state defaults
    defaults = [
        ("logged_in", False), ("user_id", None), ("username", ""),
        ("role", "Developer"), ("stack", "React/PHP/Python"), ("lang", "en"),
        ("is_admin", False),
        ("last_page", "🏠  Dashboard"),
        ("admin_authenticated", False),
    ]
    for k, v in defaults:
        if k not in st.session_state:
            st.session_state[k] = v

    if not st.session_state.logged_in:
        page_auth()
        return

    selected = render_sidebar()

    # Route to the correct page — selected is now a simple key like "dashboard"
    page_fn = PAGES.get(selected, page_dashboard)
    page_fn()


if __name__ == "__main__":
    main()
