import streamlit as st
import sqlite3
import hashlib
import datetime
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DevLife OS",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR DARK/DEV THEME ---
st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    .metric-card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True) # <-- Changed here

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
        ("No Phone First 30 Mins", "Mental", "Morning"),
        ("10 Min Stillness/Breathing", "Mental", "Morning"),
        ("Physical Activation (15m)", "Health", "Morning"),
        ("Deep Learning Block (60m)", "Coding", "Morning"),
        ("High-Protein Screenless Breakfast", "Health", "Morning"),
        ("Deep Work Block 1 (Hard Code)", "Coding", "Work"),
        ("Reactive Tasks Window", "Coding", "Work"),
        ("Disconnect & Walk Lunch", "Health", "Work"),
        ("Project / Build Time", "Coding", "Work"),
        ("Shutdown Ritual executed", "Mental", "Work"),
        ("Posterior Chain / Strength Training", "Health", "Fitness"),
        ("Digital Sunset @ 9:00 PM", "Health", "Night"),
        ("Post-Work Decompression Walk", "Health", "Fitness")
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
    st.subheader("Your personal engineering environment for an intentional life.")
    
    auth_mode = st.radio("Choose Mode", ["Login", "Register"], horizontal=True)
    
    with st.form("auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(auth_mode)
        
        if submit:
            if auth_mode == "Register":
                if register_user(username, password):
                    st.success("Account created successfully! Please Switch to Login mode.")
                else:
                    st.error("Username already exists.")
            else:
                user = login_user(username, password)
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user['id']
                    st.session_state['username'] = user['username']
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    st.stop()

# --- MAIN APP ARCHITECTURE (LOGGED IN) ---
user_id = st.session_state['user_id']
today = datetime.date.today().strftime("%Y-%m-%d")

# Sidebar Workspace Navigation
st.sidebar.title(f"🚀 {st.session_state['username']}@devlife_os")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Routine Tracker", "Goal Architecture", "Advanced Reports & Analytics"])

if st.sidebar.button("System Shutdown (Logout)"):
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = ""
    st.rerun()

# --- MODULE 1: DASHBOARD ---
if menu == "Dashboard":
    st.title("🧭 System Dashboard")
    st.write(f"**Current Epoch:** {datetime.date.today().strftime('%A, %B %d, %Y')}")
    
    with get_db_connection() as conn:
        total_habits = conn.execute("SELECT COUNT(*) FROM habits WHERE user_id = ?", (user_id,)).fetchone()[0]
        completed_today = conn.execute("SELECT COUNT(*) FROM habit_logs WHERE user_id = ? AND date = ? AND completed = 1", (user_id, today)).fetchone()[0]
    
    completion_rate = (completed_today / total_habits) * 100 if total_habits > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Today's Compilation Rate", f"{completion_rate:.1f}%", f"{completed_today}/{total_habits} Tasks")
    with col2:
        st.metric("System Up-Time Status", "Optimal" if completion_rate > 50 else "Degraded", "Based on daily runtime")
    with col3:
        st.metric("Cognitive Infrastructure", "Configured", "Prefrontal cortex online")

    st.markdown("---")
    
    st.subheader("🎯 Primary Directives (MIT)")
    with get_db_connection() as conn:
        active_goals = conn.execute("SELECT * FROM goals WHERE user_id = ? AND progress < 100 LIMIT 3", (user_id,)).fetchall()
    
    if active_goals:
        for goal in active_goals:
            st.markdown(f"- **[{goal['category']}]** {goal['title']} — Progress: `{goal['progress']}%`")
    else:
        st.info("No active pipeline execution goals found. Go to 'Goal Architecture' to assign compilation targets.")

# --- MODULE 2: ROUTINE TRACKER ---
elif menu == "Routine Tracker":
    st.title("🌅 System Routine Engine")
    
    with get_db_connection() as conn:
        all_habits = conn.execute("SELECT * FROM habits WHERE user_id = ?", (user_id,)).fetchall()
        for habit in all_habits:
            conn.execute("INSERT OR IGNORE INTO habit_logs (user_id, habit_id, date, completed) VALUES (?, ?, ?, 0)", 
                         (user_id, habit['id'], today))
        conn.commit()

    tab1, tab2, tab3 = st.tabs(["⚡ Checklists", "📝 Deep Journaling", "🧠 Brain Dump"])
    
    with tab1:
        st.subheader("Daily Execution Framework")
        with get_db_connection() as conn:
            logs = conn.execute("""
                SELECT hl.id, h.name, h.slot, hl.completed 
                FROM habit_logs hl 
                JOIN habits h ON hl.habit_id = h.id 
                WHERE hl.user_id = ? AND hl.date = ?
            """, (user_id, today)).fetchall()
            
        slots = ["Morning", "Work", "Fitness", "Night"]
        for slot in slots:
            st.write(f"#### {slot} Routine")
            slot_logs = [log for log in logs if log['slot'] == slot]
            
            for log in slot_logs:
                is_checked = bool(log['completed'])
                cb = st.checkbox(log['name'], value=is_checked, key=f"habit_{log['id']}")
                if cb != is_checked:
                    with get_db_connection() as conn:
                        conn.execute("UPDATE habit_logs SET completed = ? WHERE id = ?", (1 if cb else 0, log['id']))
                        conn.commit()
                    st.rerun()
                    
    with tab2:
        st.subheader("Developer Reflection Node")
        with get_db_connection() as conn:
            existing_j = conn.execute("SELECT * FROM journal_entries WHERE user_id = ? AND date = ?", (user_id, today)).fetchone()
            
        with st.form("journal_form"):
            q1 = st.text_area("1. What technical problems did we solve today?", value=existing_j['q1'] if existing_j else "")
            q2 = st.text_area("2. What architecture patterns did we process?", value=existing_j['q2'] if existing_j else "")
            q3 = st.text_area("3. What are we avoiding in the codebase?", value=existing_j['q3'] if existing_j else "")
            
            col_m, col_e = st.columns(2)
            with col_m:
                mood = st.slider("Mood Tuning (1-10)", 1, 10, int(existing_j['mood']) if existing_j and existing_j['mood'] else 5)
            with col_e:
                energy = st.slider("Energy Configuration (1-10)", 1, 10, int(existing_j['energy']) if existing_j and existing_j['energy'] else 5)
                
            if st.form_submit_button("Commit Reflection Entry"):
                with get_db_connection() as conn:
                    conn.execute("""
                        INSERT INTO journal_entries (user_id, date, q1, q2, q3, mood, energy) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(date) DO UPDATE SET q1=excluded.q1, q2=excluded.q2, q3=excluded.q3, mood=excluded.mood, energy=excluded.energy
                    """, (user_id, today, q1, q2, q3, mood, energy))
                    conn.commit()
                st.success("Reflection array committed.")
                
    with tab3:
        st.subheader("Async Garbage Collection (Brain Dump)")
        with get_db_connection() as conn:
            existing_bd = conn.execute("SELECT brain_dump FROM journal_entries WHERE user_id = ? AND date = ?", (user_id, today)).fetchone()
            
        bd_text = st.text_area("Unload mental processing threads here:", 
                               value=existing_bd['brain_dump'] if (existing_bd and existing_bd['brain_dump']) else "", height=250)
        if st.button("Flush Cache to Storage"):
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO journal_entries (user_id, date, brain_dump) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(date) DO UPDATE SET brain_dump=excluded.brain_dump
                """, (user_id, today, bd_text))
                conn.commit()
            st.success("Thread flushed.")

# --- MODULE 3: GOAL ARCHITECTURE ---
elif menu == "Goal Architecture":
    st.title("🎯 Structural Pipeline Goals")
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        st.subheader("Inject New Goal")
        with st.form("new_goal_form"):
            title = st.text_input("Goal Title")
            category = st.selectbox("Category", ["Coding", "Finance", "Health", "Learning", "Social"])
            timeframe = st.selectbox("Timeframe", ["Daily", "Weekly", "Monthly", "Yearly"])
            deadline = st.date_input("Deadline")
            if st.form_submit_button("Compile Goal") and title:
                with get_db_connection() as conn:
                    conn.execute("INSERT INTO goals (user_id, title, category, timeframe, progress, deadline) VALUES (?, ?, ?, ?, 0, ?)",
                                 (user_id, title, category, timeframe, deadline.strftime("%Y-%m-%d")))
                    conn.commit()
                st.success("Goal stacked.")
                st.rerun()

    with col_g2:
        st.subheader("Active Objectives")
        with get_db_connection() as conn:
            goals = conn.execute("SELECT * FROM goals WHERE user_id = ?", (user_id,)).fetchall()
        if not goals:
            st.info("No active goals.")
        else:
            for g in goals:
                with st.expander(f"[{g['category']}] {g['title']} - {g['timeframe']}"):
                    prog = st.slider("Progress (%)", 0, 100, int(g['progress']), key=f"prog_{g['id']}")
                    if prog != g['progress']:
                        with get_db_connection() as conn:
                            conn.execute("UPDATE goals SET progress = ? WHERE id = ?", (prog, g['id']))
                            conn.commit()
                        st.rerun()
                    if st.button("Delete Goal", key=f"del_{g['id']}"):
                        with get_db_connection() as conn:
                            conn.execute("DELETE FROM goals WHERE id = ?", (g['id'],))
                            conn.commit()
                        st.rerun()

# --- MODULE 4: ADVANCED REPORTS & ANALYTICS ---
elif menu == "Advanced Reports & Analytics":
    st.title("📅 Time-Series Analytics & Reports")
    
    # 1. Fetch raw data from database
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
        st.warning("Not enough data yet. Complete routines to generate analysis reports.")
    else:
        # 2. Setup Timeframe Logic
        st.write("Select how you want to aggregate and view your data:")
        timeframe_option = st.selectbox(
            "Report Frequency", 
            ["Daily", "Weekly", "Monthly", "Quarterly", "Half-Yearly", "Yearly"]
        )
        
        # Mapping timeframe selection to Pandas Frequency Strings
        freq_mapping = {
            "Daily": "D",
            "Weekly": "W-MON", # Week starts on Monday
            "Monthly": "ME",   # Month End
            "Quarterly": "QE", # Quarter End
            "Half-Yearly": "2QE", # 2 Quarters = Half Year
            "Yearly": "YE"     # Year End
        }
        pd_freq = freq_mapping[timeframe_option]

        # Convert date columns to actual pandas DateTime objects
        log_df['date'] = pd.to_datetime(log_df['date'])
        
        # 3. Process Habit Data grouped by the selected timeframe
        # Group by the chosen timeframe to calculate completion rates
        time_grouped = log_df.groupby(pd.Grouper(key='date', freq=pd_freq)).agg(
            total_tasks=('completed', 'count'),
            completed_tasks=('completed', 'sum')
        ).reset_index()
        
        # Calculate completion percentage for that period
        time_grouped['completion_rate'] = (time_grouped['completed_tasks'] / time_grouped['total_tasks']) * 100
        # Format date for clean display
        time_grouped['period'] = time_grouped['date'].dt.strftime('%Y-%m-%d')
        
        st.markdown(f"### 📈 {timeframe_option} Consistency Report")
        
        # Plotly Bar Chart showing completion over time
        fig_time = px.bar(
            time_grouped, x='period', y='completion_rate', 
            text='completion_rate',
            labels={'period': 'Time Period', 'completion_rate': 'Success Rate (%)'},
            title=f"Habit Completion Trends ({timeframe_option})", 
            template="plotly_dark", color='completion_rate', color_continuous_scale="Viridis"
        )
        fig_time.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_time, use_container_width=True)

        # 4. Data Table Report (Exportable)
        st.write(f"**Detailed {timeframe_option} Data Table:**")
        st.dataframe(time_grouped[['period', 'total_tasks', 'completed_tasks', 'completion_rate']].style.format({'completion_rate': "{:.2f}%"}), use_container_width=True)

        st.markdown("---")
        
        # 5. Process Mood & Energy by Timeframe
        if not journal_df.empty and not journal_df['mood'].isna().all():
            st.subheader(f"🧠 {timeframe_option} Mood & Energy Averages")
            journal_df['date'] = pd.to_datetime(journal_df['date'])
            # Convert columns to numeric, forcing errors to NaN
            journal_df['mood'] = pd.to_numeric(journal_df['mood'], errors='coerce')
            journal_df['energy'] = pd.to_numeric(journal_df['energy'], errors='coerce')
            
            # Group by timeframe
            journal_grouped = journal_df.groupby(pd.Grouper(key='date', freq=pd_freq))[['mood', 'energy']].mean().reset_index()
            journal_grouped['period'] = journal_grouped['date'].dt.strftime('%Y-%m-%d')
            
            # Remove empty rows
            journal_grouped = journal_grouped.dropna(subset=['mood', 'energy'])
            
            if not journal_grouped.empty:
                fig_bio = px.line(
                    journal_grouped, x='period', y=['mood', 'energy'], markers=True,
                    labels={'value': 'Average Score (1-10)', 'period': 'Time Period'},
                    title=f"Biometric Trends ({timeframe_option} Average)", template="plotly_dark"
                )
                st.plotly_chart(fig_bio, use_container_width=True)
            else:
                st.info("Fill out your daily mood/energy sliders in the 'Routine Tracker' to see biometric trends here.")
