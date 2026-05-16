import streamlit as st
from google import genai
import time
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import pandas as pd
from gtts import gTTS
import base64
import os

# --- Config ---
st.set_page_config(page_title="CricketArena", page_icon="🏏", layout="wide")
GEMINI_KEY = "AIzaSyASXQpZ8jQFBGp7ALNW5ARdh3WLggnICpA"
client = genai.Client(api_key=GEMINI_KEY)

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;900&family=DM+Mono:wght@400;500&family=Playfair+Display:ital,wght@1,700;1,900&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background: #FAFAF8; color: #1A1814; }
h1,h2,h3 { font-family: 'Playfair Display', serif; }
.hero { background: linear-gradient(135deg, #1A1814 60%, #7F1D1D); border-radius: 16px; padding: 2rem; color: white; margin-bottom: 1.5rem; }
.hero h1 { font-size: 2.5rem; margin: 0 0 0.5rem 0; font-style: italic; }
.hero .tag { color: #EF4444; font-family: 'DM Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.2em; }
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem; }
.stat-item p { margin: 0; color: rgba(255,255,255,0.4); font-size: 0.65rem; font-family: 'DM Mono', monospace; text-transform: uppercase; }
.stat-item h3 { margin: 0; color: white; font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 800; }
.card { background: #F5F3EE; border-radius: 12px; border: 1px solid rgba(26,24,20,0.08); padding: 1.2rem; margin-bottom: 1rem; }
.badge { display: inline-block; background: #FDE68A; color: #451A03; border-radius: 999px; padding: 4px 14px; font-size: 0.75rem; font-weight: 700; margin: 4px; }
.rank-card { background: #F5F3EE; border-radius: 12px; border: 1px solid rgba(26,24,20,0.08); padding: 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; }
.xp-bar-bg { background: #EDE9E0; border-radius: 999px; height: 8px; width: 100%; }
.xp-bar { background: #D97706; border-radius: 999px; height: 8px; box-shadow: 0 0 10px rgba(217,119,6,0.4); }
.gemini-alert { background: #FEF2F2; border: 1px solid rgba(252,165,165,0.3); border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.stButton > button { background: #DC2626 !important; color: white !important; border-radius: 999px !important; border: none !important; font-weight: 700 !important; padding: 0.6rem 2rem !important; }
.stButton > button:hover { background: #B91C1C !important; transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "xp" not in st.session_state:
    st.session_state.xp = 2450
if "streak" not in st.session_state:
    st.session_state.streak = 4
if "locked" not in st.session_state:
    st.session_state.locked = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "fantasy_team" not in st.session_state:
    st.session_state.fantasy_team = []
if "credits_used" not in st.session_state:
    st.session_state.credits_used = 0

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🏏 CricketArena")
    st.markdown("""
    **How to Play:**
    1. **Predict:** Lock in your match predictions to earn XP.
    2. **Fantasy:** Pick your 11-player dream team within a 100-credit budget.
    3. **AI Coach:** Chat with Gemini for deep match insights.
    4. **Level Up:** Earn XP, climb the leaderboard, and unlock rare badges!
    """)
    st.markdown("---")
    
    selected_tab = option_menu(
        menu_title=None,
        options=["Dashboard", "What-If Simulator", "Predict", "Fantasy", "Leaderboard", "XP & Badges", "AI Coach", "Admin Hub"],
        icons=["house", "controller", "bullseye", "lightning", "trophy", "star", "robot", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "border": "none"},
            "icon": {"color": "#DC2626", "font-size": "14px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "font-family": "Outfit", "color": "#1A1814"},
            "nav-link-selected": {"background-color": "#FEF2F2", "color": "#7F1D1D", "font-weight": "bold"},
        }
    )
    
    st.markdown("---")
    st.metric("XP", f"{st.session_state.xp:,}")
    st.metric("Level", "12 — Elite Scout")
    st.metric("Streak", f"🔥 {st.session_state.streak} days")
    st.markdown("---")
    st.markdown("<p style='font-size:0.7rem;color:#888;font-family:DM Mono,monospace;text-transform:uppercase;'>Powered by Google Gemini</p>", unsafe_allow_html=True)

# ============================================================
# TAB 1 — DASHBOARD
# ============================================================
if selected_tab == "Dashboard":
    st.markdown("""
    <div class="hero">
      <p class="tag">🔴 Live Match • T20 World Cup</p>
      <h1>IND <span style="opacity:0.3">vs</span> AUS</h1>
      <div class="stat-grid">
        <div class="stat-item"><p>Current Score</p><h3>184/4 <span style="font-size:0.8rem;opacity:0.5">(18.2)</span></h3></div>
        <div class="stat-item"><p>Target</p><h3>201</h3></div>
        <div class="stat-item"><p>Required Rate</p><h3>9.27</h3></div>
        <div class="stat-item"><p>Win Probability</p><h3 style="color:#EF4444">64%</h3></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Level 12 — Elite Scout**")
        pct = (st.session_state.xp / 3000) * 100
        st.markdown(f"""
        <div class="xp-bar-bg"><div class="xp-bar" style="width:{min(pct,100):.0f}%"></div></div>
        <p style="font-size:0.75rem;color:#888;margin-top:6px;font-family:DM Mono,monospace">{st.session_state.xp:,} / 3,000 XP</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Weekly Streak**")
        days = ["M","T","W","T","F","S","S"]
        cols = st.columns(7)
        for i, (c, d) in enumerate(zip(cols, days)):
            bg = "#DC2626" if i < st.session_state.streak else "#EDE9E0"
            tc = "white" if i < st.session_state.streak else "#1A1814"
            c.markdown(f'<div style="width:36px;height:36px;border-radius:50%;background:{bg};color:{tc};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.75rem">{d}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:0.8rem;color:#888;margin-top:8px">{st.session_state.streak} day streak! Complete today\'s prediction.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="gemini-alert">
      <b>✨ Gemini Strategist Insight</b><br>
      <span style="font-size:0.85rem;color:#7F1D1D">Bumrah's economy in death overs is at an all-time low (5.2). Consider Australian batsmen for "Top Scorer" but avoid their middle order for "Top Bowler" predictions.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Live Match Momentum")
    df = pd.DataFrame({'Over': [15,16,17,18], 'IND Win %': [40, 45, 30, 64], 'Pressure Index': [80, 70, 90, 50]})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Over'], y=df['IND Win %'], fill='tozeroy', mode='lines', line=dict(color='#DC2626', width=3), name='IND Win %', fillcolor='rgba(220, 38, 38, 0.1)'))
    fig.add_trace(go.Scatter(x=df['Over'], y=df['Pressure Index'], mode='lines', line=dict(color='#D97706', width=2, dash='dash'), name='Pressure Index'))
    fig.update_layout(height=200, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=30,b=0), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Earned Badges")
    st.markdown('<span class="badge">🏆 Rookie</span><span class="badge">🧠 Strategist</span><span class="badge">💎 Loyalist</span>', unsafe_allow_html=True)

# ============================================================
# TAB 2 — WHAT-IF SIMULATOR
# ============================================================
elif selected_tab == "What-If Simulator":
    st.markdown("# *What-If Simulator*")
    st.caption("Powered by Gemini • Predict cascading match effects")
    
    scenario = st.text_input("Enter a scenario (e.g. 'What if Rohit hits 3 sixes in the next over?')")
    if st.button("Simulate Scenario", use_container_width=True):
        if scenario:
            with st.spinner("Gemini is simulating the timeline..."):
                try:
                    sys_prompt = "You are a cricket simulation engine. Analyze this scenario for an IND vs AUS T20 match where IND is currently 184/4 (18.2 overs) chasing 201. Give a 3-sentence dramatic breakdown of how this changes Win Probability and impacts Fantasy Points for the player mentioned."
                    res = client.models.generate_content(model='gemini-1.5-flash', contents=f"{sys_prompt}\nScenario: {scenario}")
                    st.success(res.text)
                    
                    st.markdown("### 📈 Projected Momentum Shift")
                    df = pd.DataFrame({'Over': [18.2, 18.5, 19.0, 19.5, 20.0], 'IND Win %': [64, 75, 82, 90, 99]})
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df['Over'], y=df['IND Win %'], mode='lines+markers', line=dict(color='#DC2626', width=4), name='IND Win Probability'))
                    fig.update_layout(height=250, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=30,b=0), xaxis=dict(title='Overs', showgrid=False), yaxis=dict(title='Probability %', showgrid=False))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Simulation failed: {str(e)}")

# ============================================================
# TAB 3 — PREDICT
# ============================================================
elif selected_tab == "Predict":
    st.markdown("# *Lock In Your Predictions*")
    st.caption("Match: IND vs AUS • Pot: 1,500 XP Total")

    if st.session_state.locked:
        st.success("✅ Predictions locked! +500 XP earned.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**🏆 Match Winner** `+100 XP`")
        winner = st.radio("Pick the winner:", ["🇮🇳 India (Odds: 1.85)", "🇦🇺 Australia (Odds: 2.10)"], horizontal=True, key="winner")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**🏅 Top Scorer** `+250 XP`")
        scorer = st.selectbox("Select player:", ["Virat Kohli", "Rohit Sharma", "Travis Head", "Glenn Maxwell", "Steve Smith"])
        target_runs = st.number_input("Target runs:", min_value=0, max_value=200, value=75)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**🎯 Innings Score Range** `+150 XP`")
        score_est = st.slider("Estimated total score:", 140, 250, 190)
        st.markdown(f'Prediction: **{score_est-5} – {score_est+5}**')
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔒 Lock In Predictions — +500 XP Guaranteed", use_container_width=True):
            st.session_state.locked = True
            st.session_state.xp += 500
            st.session_state.streak = min(st.session_state.streak + 1, 7)
            st.rerun()

# ============================================================
# TAB 4 — FANTASY
# ============================================================
elif selected_tab == "Fantasy":
    st.markdown("# *Build Your Fantasy XI*")
    st.caption("100 credit budget • Pick exactly 11 players")

    PLAYERS = [
        # India Squad (11)
        {"name":"Virat Kohli","role":"BAT","credits":10.0,"team":"IND"},
        {"name":"Rohit Sharma","role":"BAT","credits":9.5,"team":"IND"},
        {"name":"Shubman Gill","role":"BAT","credits":9.0,"team":"IND"},
        {"name":"Suryakumar Yadav","role":"BAT","credits":9.0,"team":"IND"},
        {"name":"Shreyas Iyer","role":"BAT","credits":8.5,"team":"IND"},
        {"name":"KL Rahul","role":"WK","credits":8.5,"team":"IND"},
        {"name":"Rishabh Pant","role":"WK","credits":8.0,"team":"IND"},
        {"name":"Hardik Pandya","role":"ALL","credits":9.0,"team":"IND"},
        {"name":"Ravindra Jadeja","role":"ALL","credits":8.5,"team":"IND"},
        {"name":"Axar Patel","role":"ALL","credits":7.5,"team":"IND"},
        {"name":"Jasprit Bumrah","role":"BOWL","credits":9.5,"team":"IND"},
        {"name":"Mohammed Siraj","role":"BOWL","credits":8.0,"team":"IND"},
        {"name":"Kuldeep Yadav","role":"BOWL","credits":7.5,"team":"IND"},
        {"name":"Arshdeep Singh","role":"BOWL","credits":7.0,"team":"IND"},
        {"name":"Yuzvendra Chahal","role":"BOWL","credits":7.0,"team":"IND"},
        # Australia Squad (11)
        {"name":"Travis Head","role":"BAT","credits":9.5,"team":"AUS"},
        {"name":"David Warner","role":"BAT","credits":9.0,"team":"AUS"},
        {"name":"Steve Smith","role":"BAT","credits":9.0,"team":"AUS"},
        {"name":"Marnus Labuschagne","role":"BAT","credits":8.5,"team":"AUS"},
        {"name":"Matthew Wade","role":"WK","credits":7.5,"team":"AUS"},
        {"name":"Josh Inglis","role":"WK","credits":7.0,"team":"AUS"},
        {"name":"Glenn Maxwell","role":"ALL","credits":9.0,"team":"AUS"},
        {"name":"Cameron Green","role":"ALL","credits":8.0,"team":"AUS"},
        {"name":"Pat Cummins","role":"BOWL","credits":9.0,"team":"AUS"},
        {"name":"Mitchell Starc","role":"BOWL","credits":8.5,"team":"AUS"},
        {"name":"Josh Hazlewood","role":"BOWL","credits":8.0,"team":"AUS"},
        {"name":"Adam Zampa","role":"BOWL","credits":8.0,"team":"AUS"},
        {"name":"Nathan Lyon","role":"BOWL","credits":7.5,"team":"AUS"},
    ]

    credits_used = sum(p["credits"] for p in PLAYERS if p["name"] in st.session_state.fantasy_team)
    remaining = 100 - credits_used

    col1, col2, col3 = st.columns(3)
    col1.metric("Players Selected", f"{len(st.session_state.fantasy_team)}/11")
    col2.metric("Credits Used", f"{credits_used:.1f}/100")
    col3.metric("Credits Left", f"{remaining:.1f}")

    st.markdown("### 🤖 AI Fantasy Optimizer")
    risk_profile = st.selectbox("Select Risk Profile", ["Balanced (Safe)", "Aggressive (High Risk, High Reward)", "Contrarian (Differential Picks)"])
    if st.button("✨ Auto-Generate Best XI", use_container_width=True):
        with st.spinner("Gemini is analyzing player forms and pitch conditions..."):
            try:
                sys_prompt = "You are a Fantasy Cricket AI. Return a comma-separated list of EXACTLY 11 player names from this list that fit the risk profile, strictly staying under 100 total credits. Players: Virat Kohli, Rohit Sharma, Shubman Gill, Suryakumar Yadav, Shreyas Iyer, KL Rahul, Rishabh Pant, Hardik Pandya, Ravindra Jadeja, Axar Patel, Jasprit Bumrah, Mohammed Siraj, Kuldeep Yadav, Arshdeep Singh, Yuzvendra Chahal, Travis Head, David Warner, Steve Smith, Marnus Labuschagne, Matthew Wade, Josh Inglis, Glenn Maxwell, Cameron Green, Pat Cummins, Mitchell Starc, Josh Hazlewood, Adam Zampa, Nathan Lyon. ONLY RETURN COMMA SEPARATED NAMES."
                res = client.models.generate_content(model='gemini-1.5-flash', contents=f"{sys_prompt}\nProfile: {risk_profile}")
                names = [n.strip() for n in res.text.split(',')]
                valid_names = [n for n in names if any(p['name'] == n for p in PLAYERS)][:11]
                if valid_names:
                    st.session_state.fantasy_team = valid_names
                    st.rerun()
            except Exception as e:
                st.error(f"Optimization failed: {str(e)}")

    st.markdown("---")
    for p in PLAYERS:
        col_a, col_b, col_c, col_d = st.columns([3,1,1,1])
        col_a.markdown(f"**{p['name']}** `{p['role']}` — {p['team']}")
        col_b.markdown(f"💰 {p['credits']}")
        if p["name"] in st.session_state.fantasy_team:
            if col_c.button("✅ Remove", key=f"rem_{p['name']}"):
                st.session_state.fantasy_team.remove(p["name"])
                st.rerun()
        else:
            if col_c.button("➕ Add", key=f"add_{p['name']}"):
                if len(st.session_state.fantasy_team) < 11 and credits_used + p["credits"] <= 100:
                    st.session_state.fantasy_team.append(p["name"])
                    st.rerun()

# ============================================================
# TAB 5 — LEADERBOARD
# ============================================================
elif selected_tab == "Leaderboard":
    st.markdown("""
    <div class="hero" style="text-align:center">
      <h1>THE ARENA <span style="color:#D97706">ELITE</span></h1>
      <p style="color:rgba(255,255,255,0.4);font-family:DM Mono,monospace;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.2em">Global Rankings • Updated 2m ago</p>
    </div>
    """, unsafe_allow_html=True)

    LEADERS = [
        (1,"CricketGod99",45200,52,"🔥14"),
        (2,"BumrahFanatic",42150,48,"🔥8"),
        (3,"KohliKing",39800,45,"🔥21"),
        (4,"SpinWizard",35400,41,"5"),
        (5,"PowerHitter",31000,38,"2"),
    ]
    for rank, name, xp, level, streak in LEADERS:
        is_top = rank == 1
        border = "2px solid #FCD34D" if is_top else "1px solid rgba(26,24,20,0.08)"
        bg = "#FFFBEB" if is_top else "#F5F3EE"
        rank_color = "#D97706" if is_top else "rgba(26,24,20,0.2)"
        st.markdown(f"""
        <div style="background:{bg};border:{border};border-radius:12px;padding:1rem;margin-bottom:0.5rem;display:flex;align-items:center;justify-content:space-between">
          <div style="display:flex;align-items:center;gap:16px">
            <span style="font-weight:900;font-style:italic;font-size:1.2rem;color:{rank_color}">#{rank}</span>
            <div style="width:40px;height:40px;border-radius:50%;background:#EDE9E0;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.7rem">{name[:2].upper()}</div>
            <div><b>{name}</b> <span style="font-size:0.65rem;background:#FEF2F2;color:#7F1D1D;padding:2px 6px;border-radius:4px;font-family:DM Mono">{streak}</span><br>
            <span style="font-size:0.65rem;color:#888;font-family:DM Mono">Level {level}</span></div>
          </div>
          <b>{xp:,} XP</b>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#1A1814;color:white;border-radius:12px;padding:1rem;display:flex;align-items:center;justify-content:space-between;margin-top:1rem">
      <div style="display:flex;align-items:center;gap:16px">
        <span style="font-weight:900;font-style:italic;color:rgba(255,255,255,0.4)">#1,204</span>
        <div style="width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.7rem">YOU</div>
        <div><b>Your Ranking</b><br><span style="font-size:0.65rem;color:rgba(255,255,255,0.4);font-family:DM Mono">Level 12</span></div>
      </div>
      <b>{st.session_state.xp:,} XP</b>
    </div>""", unsafe_allow_html=True)

# ============================================================
# TAB 6 — XP & BADGES
# ============================================================
elif selected_tab == "XP & Badges":
    st.markdown("# *XP & Progression*")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total XP", f"{st.session_state.xp:,}")
    col2.metric("Level", "12 — Elite Scout")
    col3.metric("Top %", "Top 5% Global")

    pct = (st.session_state.xp / 3000) * 100
    st.markdown(f"""
    <div style="margin:1.5rem 0">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:0.75rem;font-family:DM Mono;color:#888">LEVEL 12 — ELITE SCOUT</span>
        <span style="font-size:0.75rem;font-family:DM Mono;color:#888">{st.session_state.xp:,} / 3,000 XP</span>
      </div>
      <div class="xp-bar-bg"><div class="xp-bar" style="width:{min(pct,100):.0f}%"></div></div>
      <p style="font-size:0.8rem;color:#888;margin-top:6px">550 XP until Level 13 — Master Tactician</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Streak Calendar")
    week_cols = st.columns(21)
    for i, c in enumerate(week_cols):
        bg = "#DC2626" if i < 14 else "#EDE9E0"
        c.markdown(f'<div style="height:28px;border-radius:4px;background:{bg}"></div>', unsafe_allow_html=True)
    st.caption("🔴 14-day streak  ·  Personal best: 21 days")

    st.markdown("#### Badges Earned")
    badges = [("🏆","Rookie","First correct prediction"),("🧠","Strategist","5 correct in a row"),("💎","Loyalist","7-day streak"),("🔒","Oracle","Locked — 10 consecutive wins")]
    bcols = st.columns(4)
    for i, (icon, name, desc) in enumerate(badges):
        locked = name == "Oracle"
        bg = "#F5F3EE" if not locked else "#FAFAF8"
        opacity = "1" if not locked else "0.4"
        bcols[i].markdown(f'<div style="background:{bg};border-radius:12px;padding:1rem;text-align:center;opacity:{opacity};border:1px solid rgba(26,24,20,0.08)"><div style="font-size:2rem">{icon}</div><b style="font-size:0.85rem">{name}</b><br><span style="font-size:0.7rem;color:#888">{desc}</span></div>', unsafe_allow_html=True)

    st.markdown("#### Recent XP Earnings")
    history = [("Match Winner — IND vs AUS","+100 XP","Today"),("Daily Trivia Challenge","+20 XP","Today"),("Weekly Summary Review","+50 XP","Yesterday"),("Locked In Predictions","+500 XP","2 days ago")]
    for label, xp_val, date in history:
        c1, c2, c3 = st.columns([4,1,1])
        c1.markdown(f"**{label}**")
        c2.markdown(f'<span style="color:#D97706;font-family:DM Mono;font-weight:700">{xp_val}</span>', unsafe_allow_html=True)
        c3.markdown(f'<span style="font-size:0.75rem;color:#888">{date}</span>', unsafe_allow_html=True)

# ============================================================
# TAB 7 — AI COACH
# ============================================================
elif selected_tab == "AI Coach":
    st.markdown("# *AI Cricket Coach*")
    st.caption("Powered by Google Gemini 1.5 Flash")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask about player form, strategy, predictions...")
    if prompt:
        st.session_state.chat_history.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    system = "You are an expert cricket analyst and coach for CricketArena. Give concise, data-driven advice about IPL, T20 matches, player form, fantasy team selection, and match predictions. Keep responses under 150 words."
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=f"{system}\n\nUser: {prompt}"
                    )
                    reply = response.text
                    
                    st.write(reply)
                    st.session_state.chat_history.append({"role":"assistant","content":reply})
                    
                    # Generate Voice Commentary
                    tts = gTTS(text=reply, lang='en', tld='co.in')
                    tts.save("response.mp3")
                    with open("response.mp3", "rb") as f:
                        data = f.read()
                        b64 = base64.b64encode(data).decode()
                        md = f"""
                            <audio controls autoplay="true" style="height:30px;">
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                            </audio>
                            """
                        st.markdown(md, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"⚠️ AI Coach temporarily unavailable. Error: {str(e)}")

# ============================================================
# TAB 8 — ADMIN HUB
# ============================================================
elif selected_tab == "Admin Hub":
    st.markdown("# *Admin Analytics*")
    st.caption("Global Platform Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Predictions", "142,504", "+12% today")
    col2.metric("Active Users", "12,400", "Live")
    col3.metric("Prediction Accuracy", "48.2%", "-2.1%")
    col4.metric("Total XP Awarded", "4.2M")
    
    st.markdown("### 🏏 Global Fantasy Picks")
    df = pd.DataFrame({'Player': ['Virat Kohli', 'Travis Head', 'Jasprit Bumrah', 'Mitchell Starc'], 'Selected %': [82, 76, 71, 64]})
    fig = go.Figure(data=[go.Bar(x=df['Player'], y=df['Selected %'], marker_color='#DC2626')])
    fig.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
