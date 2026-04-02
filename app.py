"""
Nature Exposure During Breaks and Mental Clarity Restoration Questionnaire
Author: Student Coursework — Fundamentals of Programming (4BUIS008C)
"""

import streamlit as st
import json
import csv
import io
import os
import re
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Nature & Mental Clarity Survey",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

def init_state():
    defaults: dict = {
        "page":              "home",
        "dark_mode":         False,
        "name":              "",
        "dob":               "",
        "student_id":        "",
        "answers":           [],
        "score":             0,
        "state_label":       "",
        "state_description": "",
        # variable-type demos (coursework requirement)
        "demo_int":          0,
        "demo_float":        0.0,
        "demo_bool":         False,
        "demo_tuple":        (),
        "demo_set":          set(),
        "demo_range":        range(0),
        "demo_frozenset":    frozenset(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ─────────────────────────────────────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────────────────────────────────────

def theme() -> dict:
    """Return a colour palette based on the current dark/light mode."""
    if st.session_state.dark_mode:
        return {
            "bg":            "#0f1c14",
            "sidebar_bg":    "#0a1510",
            "card_bg":       "#1a2e1f",
            "card_border":   "#2d6a4f",
            "heading":       "#95d5b2",
            "subheading":    "#74c69d",
            "text":          "#e0f0e8",
            "muted":         "#a8c9b4",
            "accent":        "#52b788",
            "hero_bg":       "#1a2e1f",
            "tag_bg":        "#2d6a4f",
            "tag_text":      "#d8f3dc",
            "input_bg":      "#1a2e1f",
            "divider":       "#2d6a4f",
            "nav_text":      "#95d5b2",
            "score_bg":      "#1b4332",
            "score_text":    "#ffffff",
            "score_sub":     "#95d5b2",
            "progress_bg":   "#1a2e1f",
            "progress_fill": "#52b788",
        }
    else:
        return {
            "bg":            "#f5faf6",
            "sidebar_bg":    "#eaf4ec",
            "card_bg":       "#ffffff",
            "card_border":   "#b7e4c7",
            "heading":       "#1b4332",
            "subheading":    "#2d6a4f",
            "text":          "#1a1a1a",
            "muted":         "#4a6550",
            "accent":        "#2d6a4f",
            "hero_bg":       "#d8f3dc",
            "tag_bg":        "#b7e4c7",
            "tag_text":      "#1b4332",
            "input_bg":      "#ffffff",
            "divider":       "#b7e4c7",
            "nav_text":      "#1b4332",
            "score_bg":      "#1b4332",
            "score_text":    "#ffffff",
            "score_sub":     "#95d5b2",
            "progress_bg":   "#d8f3dc",
            "progress_fill": "#2d6a4f",
        }

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────

def inject_css():
    t = theme()
    st.markdown(f"""
<style>
/* Global */
html, body, .stApp {{
    background-color: {t['bg']} !important;
    color: {t['text']} !important;
    font-family: 'Segoe UI', sans-serif;
}}
.stApp * {{ color: {t['text']} !important; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {t['sidebar_bg']} !important;
    border-right: 1px solid {t['card_border']};
}}
[data-testid="stSidebar"] * {{ color: {t['nav_text']} !important; }}

/* Headings */
h1 {{ color: {t['heading']} !important; font-size: 2em; font-weight: 800; }}
h2 {{ color: {t['heading']} !important; font-size: 1.5em; font-weight: 700; }}
h3 {{ color: {t['subheading']} !important; font-size: 1.15em; font-weight: 600; }}

/* Cards */
.card {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 12px;
    padding: 22px 26px;
    margin: 8px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}}
.card-accent {{
    background: {t['hero_bg']};
    border-left: 4px solid {t['accent']};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 6px 0;
}}
.hero-banner {{
    background: linear-gradient(135deg, {t['hero_bg']}, {t['card_bg']});
    border: 1px solid {t['card_border']};
    border-radius: 14px;
    padding: 36px 32px;
    text-align: center;
    margin-bottom: 20px;
}}
.hero-title {{
    font-size: 2.2em;
    font-weight: 900;
    color: {t['heading']} !important;
    margin-bottom: 8px;
}}
.hero-sub {{
    font-size: 1.05em;
    color: {t['muted']} !important;
    max-width: 580px;
    margin: 0 auto 18px;
    line-height: 1.6;
}}

/* Stat tiles */
.stat-tile {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 10px;
    padding: 18px;
    text-align: center;
}}
.stat-number {{
    font-size: 2em;
    font-weight: 800;
    color: {t['accent']} !important;
}}
.stat-label {{
    font-size: 0.85em;
    color: {t['muted']} !important;
    margin-top: 4px;
}}

/* Score result box */
.score-box {{
    background: {t['score_bg']};
    border-radius: 14px;
    padding: 28px;
    text-align: center;
    margin: 14px 0;
}}
.score-number {{
    font-size: 2.8em;
    font-weight: 900;
    color: {t['score_text']} !important;
}}
.score-label {{
    font-size: 1.2em;
    color: {t['score_sub']} !important;
    margin-top: 6px;
    font-weight: 600;
}}

/* Progress bar */
.progress-wrap {{
    background: {t['progress_bg']};
    border-radius: 20px;
    height: 10px;
    margin: 6px 0 14px;
    overflow: hidden;
}}
.progress-fill {{
    background: {t['progress_fill']};
    height: 100%;
    border-radius: 20px;
    transition: width 0.4s ease;
}}

/* Question card */
.q-card {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
}}
.q-number {{
    display: inline-block;
    background: {t['tag_bg']};
    color: {t['tag_text']} !important;
    border-radius: 5px;
    padding: 2px 8px;
    font-size: 0.78em;
    font-weight: 700;
    margin-bottom: 6px;
}}
.q-text {{
    font-size: 1em;
    font-weight: 600;
    color: {t['text']} !important;
    line-height: 1.5;
}}

/* Tags / badges */
.tag {{
    display: inline-block;
    background: {t['tag_bg']};
    color: {t['tag_text']} !important;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.8em;
    font-weight: 600;
    margin: 3px;
}}

/* Buttons */
.stButton > button {{
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}}

/* Inputs */
.stTextInput input {{
    background: {t['input_bg']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['card_border']} !important;
    border-radius: 7px !important;
}}
.stTextInput label, .stTextInput label p {{
    color: {t['text']} !important;
    font-weight: 600 !important;
}}

/* Radio buttons */
.stRadio label, .stRadio label p,
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] label p {{
    color: {t['text']} !important;
    font-size: 0.95em !important;
}}

/* Misc */
.stAlert {{ border-radius: 8px !important; }}
hr {{ border-color: {t['divider']} !important; }}
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
div[data-testid="stForm"] {{ border: none !important; padding: 0 !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

def go(page: str):
    st.session_state.page = page
    st.rerun()


def sidebar_nav():
    t = theme()
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding:10px 0 18px;'>
            <div style='font-size:2em;'>🌿</div>
            <div style='font-weight:800; font-size:1em; color:{t["heading"]};'>
                Nature & Clarity
            </div>
            <div style='font-size:0.76em; color:{t["muted"]}; margin-top:3px;'>
                Mental Clarity Survey
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        pages: list = [
            ("Home",                  "home"),
            ("About",                 "about"),
            ("Take Survey",           "info"),
            ("Results",               "results"),
            ("Load Previous Results", "load"),
        ]

        for label, key in pages:
            active: bool = st.session_state.page == key
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                go(key)

        st.divider()

        dark = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark != st.session_state.dark_mode:
            st.session_state.dark_mode = dark
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  SURVEY DATA
# ─────────────────────────────────────────────────────────────────────────────

QUESTIONS: list = [
    {
        "question": "How often do you step outside into a natural environment (garden, park, open area) during your study breaks?",
        "options": [
            ("Every single break, without fail", 0),
            ("Most of my breaks", 1),
            ("Occasionally, a few times a week", 2),
            ("Rarely, maybe once a week", 3),
            ("Almost never or never", 4),
        ],
    },
    {
        "question": "When you take a break near trees, grass, or open sky, how quickly do you notice your thoughts becoming clearer?",
        "options": [
            ("Very quickly, within a minute or two", 0),
            ("Fairly quickly, within five minutes", 1),
            ("It takes a while but eventually helps", 2),
            ("I rarely notice any improvement", 3),
            ("I never take such breaks", 4),
        ],
    },
    {
        "question": "After a study session with no outdoor time, how foggy or unclear does your thinking feel?",
        "options": [
            ("Not at all foggy, I feel sharp", 0),
            ("Slightly foggy but manageable", 1),
            ("Noticeably foggy and harder to focus", 2),
            ("Very foggy, I struggle to think clearly", 3),
            ("Extremely foggy, I cannot concentrate at all", 4),
        ],
    },
    {
        "question": "How would you describe your typical study break environment?",
        "options": [
            ("Outdoors in a natural or green setting", 0),
            ("Near a window with a view of nature or sky", 1),
            ("Indoors in a well-lit but enclosed room", 2),
            ("In a dark or screen-heavy space", 3),
            ("I do not take structured breaks", 4),
        ],
    },
    {
        "question": "How would you rate your overall ability to concentrate during a typical study session?",
        "options": [
            ("Excellent — I can focus for long stretches easily", 0),
            ("Good — I focus well with minor distractions", 1),
            ("Moderate — I lose focus fairly often", 2),
            ("Poor — I struggle to concentrate consistently", 3),
            ("Very poor — I can barely focus at all", 4),
        ],
    },
    {
        "question": "How often do you feel mentally refreshed after a study break?",
        "options": [
            ("Almost always — I return to work feeling revived", 0),
            ("Often — breaks usually help me reset", 1),
            ("Sometimes — it depends on the break type", 2),
            ("Rarely — breaks rarely make a difference", 3),
            ("Never — I often feel worse or the same", 4),
        ],
    },
    {
        "question": "How much natural light does your primary study environment receive?",
        "options": [
            ("Abundant — large windows with direct daylight", 0),
            ("Good — reasonable natural light most of the day", 1),
            ("Moderate — some natural light but limited", 2),
            ("Poor — mostly artificial lighting", 3),
            ("None — no natural light at all", 4),
        ],
    },
    {
        "question": "How often do you experience symptoms of cognitive fatigue (difficulty focusing, slow thinking, irritability) during study?",
        "options": [
            ("Rarely or never", 0),
            ("Occasionally, once or twice a week", 1),
            ("Several times a week", 2),
            ("Most study sessions", 3),
            ("Almost every time I study", 4),
        ],
    },
    {
        "question": "How aware are you of the concept that nature exposure can restore mental focus?",
        "options": [
            ("Very aware — I actively use nature to restore focus", 0),
            ("Aware — I know about it but do not always act on it", 1),
            ("Somewhat aware — I have heard of it vaguely", 2),
            ("Barely aware — this is mostly new to me", 3),
            ("Not aware at all — this is completely new", 4),
        ],
    },
    {
        "question": "How would you describe the quality of your sleep during periods of heavy study?",
        "options": [
            ("Excellent — I sleep well regardless of workload", 0),
            ("Good — I mostly sleep well with occasional disruption", 1),
            ("Fair — my sleep is noticeably affected by study stress", 2),
            ("Poor — I frequently sleep badly during study periods", 3),
            ("Very poor — I consistently get inadequate or broken sleep", 4),
        ],
    },
    {
        "question": "When you are outdoors during a break, how present and mindful do you tend to feel?",
        "options": [
            ("Very present — I genuinely notice and enjoy my surroundings", 0),
            ("Fairly present — I am aware of nature around me", 1),
            ("Somewhat present — my mind still wanders to tasks", 2),
            ("Rarely present — I am usually distracted even outside", 3),
            ("Not applicable — I do not go outdoors during breaks", 4),
        ],
    },
    {
        "question": "How often do you engage in physical movement (walking, stretching) as part of your study breaks?",
        "options": [
            ("Every break — movement is a fixed part of my routine", 0),
            ("Most breaks — I usually move around", 1),
            ("Some breaks — I occasionally stretch or walk", 2),
            ("Rarely — I mostly stay seated during breaks", 3),
            ("Never — I remain sedentary throughout", 4),
        ],
    },
    {
        "question": "How would you rate the impact of your current break routine on your academic performance?",
        "options": [
            ("Very positive — my breaks clearly improve my output", 0),
            ("Positive — breaks generally help my work", 1),
            ("Neutral — breaks do not seem to affect performance much", 2),
            ("Slightly negative — breaks sometimes disrupt momentum", 3),
            ("Very negative — my break habits are harming my studies", 4),
        ],
    },
    {
        "question": "How often do you use digital devices (phone, social media) during your study breaks?",
        "options": [
            ("Never — I keep breaks screen-free", 0),
            ("Rarely — only for essential communication", 1),
            ("Sometimes — I check my phone occasionally", 2),
            ("Often — I usually spend breaks on screens", 3),
            ("Always — screens are my primary break activity", 4),
        ],
    },
    {
        "question": "How motivated do you feel to incorporate regular outdoor nature breaks into your study schedule?",
        "options": [
            ("Highly motivated — I already do this consistently", 0),
            ("Motivated — I intend to do this more regularly", 1),
            ("Somewhat motivated — I would if it were more convenient", 2),
            ("Low motivation — I am unlikely to change my habits", 3),
            ("Not at all — outdoor breaks are not part of my routine", 4),
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
#  SCORING BANDS
# ─────────────────────────────────────────────────────────────────────────────

SCORE_BANDS: list = [
    (0,   8,  "Excellent Nature Connection",
     "You regularly engage with nature during breaks. Your mental clarity is well-restored "
     "and your study habits reflect a strong awareness of restorative environments. "
     "Keep it up — you are setting an excellent example!"),
    (9,  16,  "Good Restoration Habits",
     "You make reasonable use of nature breaks and your mental clarity benefits from this. "
     "Continue taking outdoor breaks and consider slightly increasing their frequency."),
    (17, 26,  "Moderate Nature Engagement",
     "You occasionally benefit from nature exposure, but there is room to improve. "
     "Try to add at least one short outdoor walk per study session to boost clarity."),
    (27, 36,  "Low Nature Engagement",
     "Your study breaks rarely involve nature, which may be limiting your mental clarity "
     "and focus. It is advisable to introduce short walks or time near green spaces regularly."),
    (37, 46,  "Minimal Restoration",
     "You have very little nature exposure during breaks. This may negatively affect your "
     "concentration and cognitive performance. Consider restructuring your break routine."),
    (47, 54,  "Poor Clarity Restoration",
     "Your current break habits provide almost no restorative benefit. Lack of nature "
     "contact is likely impacting your mental wellbeing. Lifestyle changes are recommended."),
    (55, 60,  "Critical Disconnection from Nature",
     "You have an extreme disconnect from nature during study periods, which is associated "
     "with poor mental clarity, fatigue, and reduced cognitive function. "
     "Please consider speaking with a wellbeing advisor."),
]

RESULTS_DB_FILE: str = "results_db.json"


def get_state(score: int) -> tuple:
    """Return (label, description) for a given score."""
    for low, high, label, desc in SCORE_BANDS:
        if low <= score <= high:
            return label, desc
    return "Unknown", "Score out of range."

# ─────────────────────────────────────────────────────────────────────────────
#  VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_name(name: str) -> bool:
    allowed: frozenset = frozenset(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'"
    )
    if not name or not name.strip():
        return False
    for char in name:           # for loop — coursework requirement
        if char not in allowed:
            return False
    return True


def validate_dob(dob: str) -> bool:
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", dob):
        return False
    try:
        date_obj = datetime.strptime(dob, "%d/%m/%Y")
        age: int = (datetime.today() - date_obj).days // 365
        return 0 < age < 120
    except ValueError:
        return False


def validate_student_id(sid: str) -> bool:
    if not sid:
        return False
    index: int = 0
    while index < len(sid):     # while loop — coursework requirement
        if not sid[index].isdigit():
            return False
        index += 1
    return True

# ─────────────────────────────────────────────────────────────────────────────
#  RESULTS DATABASE
# ─────────────────────────────────────────────────────────────────────────────

def load_db() -> dict:
    """Load the results database from disk."""
    if os.path.exists(RESULTS_DB_FILE):
        try:
            with open(RESULTS_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_to_db(data: dict):
    """Save or update a student result, keyed by student_id."""
    db: dict = load_db()
    db[data["student_id"]] = data
    with open(RESULTS_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def lookup_by_id(sid: str) -> dict:
    """Return the result record for a given student ID, or an empty dict."""
    db: dict = load_db()
    return db.get(sid, {})

# ─────────────────────────────────────────────────────────────────────────────
#  DOWNLOAD BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def build_txt(data: dict) -> bytes:
    lines: list = [
        "=" * 52,
        "  NATURE & MENTAL CLARITY SURVEY — RESULTS",
        "=" * 52,
        f"Name:          {data['name']}",
        f"Date of Birth: {data['dob']}",
        f"Student ID:    {data['student_id']}",
        f"Date Taken:    {data['date_taken']}",
        f"Total Score:   {data['score']} / 60",
        f"Result:        {data['state_label']}",
        "",
        "Description:",
        data['state_description'],
        "=" * 52,
    ]
    return "\n".join(lines).encode("utf-8")


def build_csv(data: dict) -> bytes:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(data.keys()))
    writer.writeheader()
    writer.writerow(data)
    return output.getvalue().encode("utf-8")


def build_json(data: dict) -> bytes:
    return json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────────────────────────────────────

def page_home():
    t = theme()

    st.markdown(f"""
    <div class="hero-banner">
        <div style="font-size:3em; margin-bottom:8px;">🌿</div>
        <div class="hero-title">Nature & Mental Clarity Survey</div>
        <div class="hero-sub">
            Discover how short nature exposures during your study breaks
            influence mental clarity, focus, and cognitive restoration.
        </div>
        <div style="margin-top:10px;">
            <span class="tag">Academic Research</span>
            <span class="tag">Mental Wellbeing</span>
            <span class="tag">Nature Science</span>
            <span class="tag">15 Questions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    stats: list = [
        ("15", "Questions"),
        ("7",  "Result Categories"),
        ("5",  "Minutes to Complete"),
        ("3",  "Save Formats"),
    ]
    for col, (num, lbl) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown(f"""
        <div class="card">
            <h3>About This Survey</h3>
            <p style="color:{t['text']}; line-height:1.7;">
                This questionnaire has been designed as part of coursework research
                into <strong>Attention Restoration Theory (ART)</strong>. It measures
                how frequently students engage with natural environments during study
                breaks and how strongly this correlates with their reported mental clarity.
            </p>
            <p style="color:{t['text']}; line-height:1.7;">
                Research consistently shows that even brief exposure to nature —
                a park, open sky, or green space — can significantly reduce
                cognitive fatigue and restore directed attention.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="card">
            <h3>How It Works</h3>
            <div class="card-accent">
                <strong>Step 1</strong> — Enter your personal details
            </div>
            <div class="card-accent" style="margin-top:8px;">
                <strong>Step 2</strong> — Answer 15 questions honestly
            </div>
            <div class="card-accent" style="margin-top:8px;">
                <strong>Step 3</strong> — Receive your personalised score
            </div>
            <div class="card-accent" style="margin-top:8px;">
                <strong>Step 4</strong> — Save and review your results
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        if st.button("Start Survey", use_container_width=True, type="primary"):
            go("info")
    with c2:
        if st.button("Learn More", use_container_width=True):
            go("about")
    with c3:
        if st.button("Load Results", use_container_width=True):
            go("load")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: ABOUT
# ─────────────────────────────────────────────────────────────────────────────

def page_about():
    t = theme()
    st.markdown("# About This Survey")
    st.markdown("*Understanding the science behind nature, breaks, and mental clarity.*")
    st.divider()

    st.markdown(f"""
    <div class="card">
        <h2>What Is Mental Clarity?</h2>
        <p style="color:{t['text']}; line-height:1.8;">
            Mental clarity refers to a state of focused, clear thinking — free from cognitive
            fog, distraction, or mental fatigue. For students, maintaining mental clarity is
            essential for absorbing new information, solving problems creatively, and performing
            well under exam conditions.
        </p>
        <p style="color:{t['text']}; line-height:1.8;">
            Mental clarity can deteriorate rapidly during extended study sessions, particularly
            when the environment is static, artificial, and screen-heavy. The result is a state
            often called <strong>Directed Attention Fatigue (DAF)</strong> — where the brain
            struggles to filter out distractions and maintain voluntary focus.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>How Nature Helps</h3>
            <p style="color:{t['text']}; line-height:1.7;">
                <strong>Attention Restoration Theory (ART)</strong>, proposed by Kaplan
                and Kaplan (1989), suggests that natural environments engage involuntary
                attention effortlessly, allowing the directed attention system to recover.
            </p>
            <p style="color:{t['text']}; line-height:1.7;">Key benefits of short nature exposure include:</p>
            <ul style="color:{t['text']}; line-height:2.0;">
                <li>Reduced stress hormones (cortisol)</li>
                <li>Improved working memory capacity</li>
                <li>Enhanced creative thinking</li>
                <li>Faster cognitive restoration</li>
                <li>Improved mood and motivation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <h3>Research Background</h3>
            <p style="color:{t['text']}; line-height:1.7;">
                Studies by Berman et al. (2008) demonstrated that a 50-minute walk in nature
                improved memory performance by 20% compared to an urban walk. Similar findings
                have been replicated across multiple academic contexts.
            </p>
            <p style="color:{t['text']}; line-height:1.7;">
                Even <strong>micro-breaks</strong> of 40 seconds looking at a green roof
                were found to significantly restore concentration levels (Lee et al., 2015).
            </p>
            <p style="color:{t['text']}; line-height:1.7;">
                These findings form the scientific basis for this questionnaire's design
                and scoring system.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h2>How the Scoring Works</h2>
        <p style="color:{t['text']}; line-height:1.7;">
            The survey contains <strong>15 questions</strong>, each with 5 answer options
            scored from <strong>0 (best)</strong> to <strong>4 (worst)</strong>.
            The minimum possible score is <strong>0</strong> and the maximum is <strong>60</strong>.
            Lower scores indicate better nature engagement and mental clarity restoration.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Result Categories")

    band_cols = st.columns(2)
    for i, (low, high, label, desc) in enumerate(SCORE_BANDS):
        with band_cols[i % 2]:
            st.markdown(f"""
            <div class="card-accent" style="margin-bottom:10px;">
                <div style="font-weight:700; color:{t['heading']};">{label}</div>
                <div style="font-size:0.82em; color:{t['muted']}; margin-top:2px;">
                    Score range: {low} – {high}
                </div>
                <div style="font-size:0.87em; color:{t['text']}; margin-top:6px;
                            line-height:1.5;">{desc[:110]}...</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Take the Survey", type="primary"):
        go("info")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: USER INFO
# ─────────────────────────────────────────────────────────────────────────────

def page_info():
    t = theme()
    st.markdown("# Your Details")
    st.markdown("Please complete your information before starting the survey.")
    st.divider()

    col_form, col_info = st.columns([1.2, 1])

    with col_form:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Personal Information")

        name = st.text_input(
            "Full Name (Surname Given Name)",
            placeholder="e.g. Smith-Jones Mary Ann",
            value=st.session_state.name,
        )
        dob = st.text_input(
            "Date of Birth",
            placeholder="DD/MM/YYYY",
            value=st.session_state.dob,
        )
        sid = st.text_input(
            "Student ID (digits only)",
            placeholder="e.g. 12345678",
            value=st.session_state.student_id,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        b1, b2 = st.columns([1, 2])
        with b1:
            if st.button("Back to Home"):
                go("home")
        with b2:
            if st.button("Start Survey", type="primary", use_container_width=True):
                errors: list = []
                if not validate_name(name):
                    errors.append("Invalid name — use only letters, hyphens, apostrophes, or spaces.")
                if not validate_dob(dob):
                    errors.append("Invalid date of birth — use DD/MM/YYYY with a real date.")
                if not validate_student_id(sid):
                    errors.append("Invalid Student ID — digits only, no spaces or letters.")

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    st.session_state.name       = name.strip()
                    st.session_state.dob        = dob.strip()
                    st.session_state.student_id = sid.strip()
                    for i in range(len(QUESTIONS)):
                        if f"q_{i}" in st.session_state:
                            del st.session_state[f"q_{i}"]
                    go("survey")

    with col_info:
        st.markdown(f"""
        <div class="card">
            <h3>Privacy Notice</h3>
            <p style="color:{t['text']}; line-height:1.7; font-size:0.92em;">
                Your information is used only to personalise your results and allow you
                to retrieve them later using your Student ID. No data is shared with
                third parties.
            </p>
            <h3 style="margin-top:16px;">Validation Rules</h3>
            <ul style="color:{t['text']}; line-height:2.0; font-size:0.9em;">
                <li><strong>Name:</strong> letters, hyphens, apostrophes, spaces only</li>
                <li><strong>Date of Birth:</strong> DD/MM/YYYY format, real date</li>
                <li><strong>Student ID:</strong> digits only (no letters or spaces)</li>
            </ul>
            <p style="color:{t['muted']}; font-size:0.85em; margin-top:10px;">
                Valid name examples: O'Connor, Smith-Jones, Mary Ann
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: SURVEY
# ─────────────────────────────────────────────────────────────────────────────

def page_survey():
    t = theme()

    if not st.session_state.name:
        st.warning("Please complete your details before starting the survey.")
        if st.button("Go to Details"):
            go("info")
        return

    total_q: int = len(QUESTIONS)
    answered_count: int = sum(
        1 for i in range(total_q)
        if st.session_state.get(f"q_{i}") is not None
    )
    pct: float = round((answered_count / total_q) * 100)

    st.markdown("# Survey Questions")
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center;
                margin-bottom:4px;">
        <span style="color:{t['muted']}; font-size:0.9em;">
            Progress: {answered_count} / {total_q} answered
        </span>
        <span style="font-weight:700; color:{t['accent']};">{pct}%</span>
    </div>
    <div class="progress-wrap">
        <div class="progress-fill" style="width:{pct}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    answers: list      = []
    all_answered: bool = True

    for i, q in enumerate(QUESTIONS):
        option_labels: list = [opt[0] for opt in q["options"]]
        option_scores: list = [opt[1] for opt in q["options"]]

        st.markdown(f"""
        <div class="q-card">
            <span class="q-number">Question {i + 1} of {total_q}</span>
            <div class="q-text">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        choice = st.radio(
            label=f"q{i}",
            options=option_labels,
            index=None,
            label_visibility="collapsed",
            key=f"q_{i}",
        )

        if choice is None:
            all_answered = False
            answers.append(None)
        else:
            answers.append(option_scores[option_labels.index(choice)])

        st.markdown("<br>", unsafe_allow_html=True)

    st.divider()

    b1, b2 = st.columns([1, 2])
    with b1:
        if st.button("Back to Details"):
            go("info")
    with b2:
        if st.button("Submit Survey", type="primary", use_container_width=True):
            if not all_answered:
                unanswered: list = [str(i + 1) for i, a in enumerate(answers) if a is None]
                st.error(f"Please answer all questions. Missing: Q{', Q'.join(unanswered)}")
            else:
                total: int = sum(answers)
                label, description = get_state(total)

                st.session_state.answers           = answers
                st.session_state.score             = total
                st.session_state.state_label       = label
                st.session_state.state_description = description

                record: dict = {
                    "name":              st.session_state.name,
                    "dob":               st.session_state.dob,
                    "student_id":        st.session_state.student_id,
                    "date_taken":        datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "score":             total,
                    "state_label":       label,
                    "state_description": description,
                }
                save_to_db(record)
                go("results")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: RESULTS
# ─────────────────────────────────────────────────────────────────────────────

def page_results():
    t = theme()

    if st.session_state.score == 0 and not st.session_state.state_label:
        st.warning("No results yet. Please complete the survey first.")
        if st.button("Take the Survey"):
            go("info")
        return

    score: int       = st.session_state.score
    label: str       = st.session_state.state_label
    description: str = st.session_state.state_description

    st.markdown("# Your Results")
    st.divider()

    st.markdown(f"""
    <div class="card-accent">
        <strong>{st.session_state.name or "Anonymous"}</strong>
        &nbsp;&middot;&nbsp; Student ID: {st.session_state.student_id or "—"}
        &nbsp;&middot;&nbsp; DOB: {st.session_state.dob or "—"}
    </div>
    """, unsafe_allow_html=True)

    pct_score: int = round((score / 60) * 100)
    st.markdown(f"""
    <div class="score-box">
        <div class="score-number">{score}
            <span style="font-size:0.45em; font-weight:400;
                         color:#95d5b2;">/ 60</span>
        </div>
        <div class="score-label">{label}</div>
        <div style="margin-top:14px;">
            <div style="background:rgba(255,255,255,0.15); border-radius:20px;
                        height:8px; overflow:hidden; max-width:300px; margin:0 auto;">
                <div style="background:#95d5b2; width:{pct_score}%;
                            height:100%; border-radius:20px;"></div>
            </div>
            <div style="font-size:0.8em; color:#95d5b2; margin-top:6px;">
                {pct_score}% of maximum score
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h3>What This Means</h3>
        <p style="color:{t['text']}; line-height:1.8;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Save Your Results")

    fmt: str = st.radio("Choose file format:", ["JSON", "CSV", "TXT"],
                        horizontal=True, index=0)

    data: dict = {
        "name":              st.session_state.name,
        "dob":               st.session_state.dob,
        "student_id":        st.session_state.student_id,
        "date_taken":        datetime.now().strftime("%d/%m/%Y %H:%M"),
        "score":             score,
        "state_label":       label,
        "state_description": description,
    }

    fmt_l: str     = fmt.lower()
    builders: dict = {"json": build_json, "csv": build_csv, "txt": build_txt}
    file_bytes: bytes = builders[fmt_l](data)
    mime_map: dict    = {"json": "application/json", "csv": "text/csv", "txt": "text/plain"}

    st.download_button(
        label=f"Download as {fmt}",
        data=file_bytes,
        file_name=f"nature_survey_{st.session_state.student_id or 'result'}.{fmt_l}",
        mime=mime_map[fmt_l],
        use_container_width=True,
    )

    st.markdown(f"""
    <div class="card-accent" style="margin-top:12px; font-size:0.88em; color:{t['muted']};">
        Your results have been saved automatically. Retrieve them anytime on the
        <strong>Load Previous Results</strong> page using your Student ID.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Back to Home"):
        go("home")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: LOAD PREVIOUS RESULTS
# ─────────────────────────────────────────────────────────────────────────────

def page_load():
    t = theme()
    st.markdown("# Load Previous Results")
    st.markdown("*Enter your Student ID to retrieve your saved survey results.*")
    st.divider()

    tab_search, tab_upload = st.tabs(["Search by Student ID", "Upload a File"])

    # ── Tab 1: Search by Student ID ──────────────────────────────────────────
    with tab_search:
        st.markdown("<br>", unsafe_allow_html=True)
        col_in, _ = st.columns([1, 1.5])

        with col_in:
            st.markdown(f"""
            <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                        border-radius:12px; padding:22px 26px;">
                <div style="font-weight:700; font-size:1.05em;
                            color:{t['heading']}; margin-bottom:4px;">Find your results</div>
                <div style="font-size:0.87em; color:{t['muted']}; margin-bottom:14px;">
                    Results are saved automatically when you complete the survey.
                    Enter your Student ID below to retrieve them.
                </div>
            """, unsafe_allow_html=True)

            sid_input: str = st.text_input(
                "Student ID", placeholder="e.g. 12345678", key="load_sid"
            )
            search_clicked = st.button(
                "Search Results", type="primary", use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        if search_clicked:
            if not validate_student_id(sid_input.strip()):
                st.error("Please enter a valid Student ID (digits only, no spaces).")
            else:
                record: dict = lookup_by_id(sid_input.strip())
                if record:
                    score_int: int = int(record.get("score", 0))
                    label, desc    = get_state(score_int)
                    pct: int       = round((score_int / 60) * 100)

                    st.success(f"Results found for Student ID: **{sid_input.strip()}**")

                    st.markdown(f"""
                    <div style="background:{t['score_bg']}; border-radius:14px;
                                padding:26px 30px; margin:14px 0; text-align:center;">
                        <div style="font-size:2.8em; font-weight:900;
                                    color:{t['score_text']};">{score_int}
                            <span style="font-size:0.45em; font-weight:400;
                                         color:{t['score_sub']};">/ 60</span>
                        </div>
                        <div style="font-size:1.2em; font-weight:700;
                                    color:{t['score_sub']}; margin-top:6px;">{label}</div>
                        <div style="margin-top:12px;">
                            <div style="background:rgba(255,255,255,0.15); border-radius:20px;
                                        height:8px; overflow:hidden; max-width:240px; margin:0 auto;">
                                <div style="background:{t['score_sub']}; width:{pct}%;
                                            height:100%; border-radius:20px;"></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    d1, d2 = st.columns(2)
                    with d1:
                        st.markdown(f"""
                        <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                                    border-radius:10px; padding:16px 20px;">
                            <div style="font-weight:700; color:{t['heading']};
                                        margin-bottom:8px;">Student Information</div>
                            <div style="color:{t['text']}; line-height:2.0; font-size:0.93em;">
                                <strong>Name:</strong> {record.get('name', '—')}<br>
                                <strong>Date of Birth:</strong> {record.get('dob', '—')}<br>
                                <strong>Student ID:</strong> {record.get('student_id', '—')}<br>
                                <strong>Date Taken:</strong> {record.get('date_taken', '—')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with d2:
                        st.markdown(f"""
                        <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                                    border-radius:10px; padding:16px 20px;">
                            <div style="font-weight:700; color:{t['heading']};
                                        margin-bottom:8px;">What This Means</div>
                            <div style="color:{t['text']}; line-height:1.7; font-size:0.9em;">
                                {desc}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error(
                        f"No results found for Student ID **{sid_input.strip()}**. "
                        "Please check the ID or complete the survey first."
                    )

    # ── Tab 2: Upload a File ──────────────────────────────────────────────────
    with tab_upload:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                    border-radius:12px; padding:22px 26px; max-width:500px;">
            <div style="font-weight:700; font-size:1.05em; color:{t['heading']};
                        margin-bottom:4px;">Upload a Saved Results File</div>
            <div style="font-size:0.87em; color:{t['muted']}; margin-bottom:14px;">
                Upload a previously downloaded results file (JSON, CSV, or TXT)
                to view its contents here.
            </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader("Choose a file", type=["json", "csv", "txt"],
                                    key="load_file")
        st.markdown("</div>", unsafe_allow_html=True)

        if uploaded:
            ext: str  = uploaded.name.split(".")[-1].lower()
            data: dict = {}
            try:
                if ext == "json":
                    data = json.load(uploaded)
                elif ext == "csv":
                    content: str = uploaded.read().decode("utf-8")
                    reader = csv.DictReader(io.StringIO(content))
                    for row in reader:
                        data = dict(row)
                        break
                elif ext == "txt":
                    lines: list = uploaded.read().decode("utf-8").splitlines()
                    for line in lines:
                        if line.startswith("Name:"):
                            data["name"] = line.split(":", 1)[1].strip()
                        elif "Date of Birth" in line:
                            data["dob"] = line.split(":", 1)[1].strip()
                        elif "Student ID" in line:
                            data["student_id"] = line.split(":", 1)[1].strip()
                        elif "Total Score" in line:
                            data["score"] = line.split(":", 1)[1].strip()
                        elif line.startswith("Result:"):
                            data["state_label"] = line.split(":", 1)[1].strip()
            except Exception as e:
                st.error(f"Could not read file: {e}")

            if data:
                score_raw = data.get("score", "")
                try:
                    score_int: int = int(score_raw)
                    label, desc    = get_state(score_int)
                except (ValueError, TypeError):
                    label     = data.get("state_label", "N/A")
                    desc      = data.get("state_description", "")
                    score_int = 0

                st.success("File loaded successfully.")
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                            border-left:4px solid {t['accent']}; border-radius:10px;
                            padding:18px 22px;">
                    <div style="font-weight:700; color:{t['heading']};
                                margin-bottom:8px;">Loaded Results</div>
                    <div style="color:{t['text']}; line-height:2.0; font-size:0.93em;">
                        <strong>Name:</strong> {data.get('name', '—')}<br>
                        <strong>Student ID:</strong> {data.get('student_id', '—')}<br>
                        <strong>Score:</strong> {score_raw} / 60<br>
                        <strong>Result:</strong> {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Back to Home"):
        go("home")

# ─────────────────────────────────────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────────────────────────────────────

inject_css()
sidebar_nav()

PAGE_MAP: dict = {
    "home":    page_home,
    "about":   page_about,
    "info":    page_info,
    "survey":  page_survey,
    "results": page_results,
    "load":    page_load,
}

PAGE_MAP.get(st.session_state.page, page_home)()
