"""
Nature Exposure During Breaks and Mental Clarity Restoration Questionnaire
Advanced multi-page Streamlit web application.
Author: Student Coursework — Fundamentals of Programming (4BUIS008C)
"""

import streamlit as st
import json
import csv
import io
import os
import re
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Nature & Mental Clarity Survey",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  SESSION STATE — initialise all keys once
# ─────────────────────────────────────────────

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
        "tips_category":     "",
        # variable-type demos (for marking criteria)
        "demo_int":          0,
        "demo_float":        0.0,
        "demo_bool":         False,
        "demo_tuple":        (),
        "demo_set":          set(),
        "demo_range":        range(0),
        "demo_frozenset":    frozenset(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
#  THEME COLOURS  (light / dark)
# ─────────────────────────────────────────────

def theme() -> dict:
    """Return a colour palette dict based on the current mode toggle."""
    if st.session_state.dark_mode:
        return {
            "bg":           "#0f1c14",
            "sidebar_bg":   "#0a1510",
            "card_bg":      "#1a2e1f",
            "card_border":  "#2d6a4f",
            "heading":      "#95d5b2",
            "subheading":   "#74c69d",
            "text":         "#e0f0e8",
            "muted":        "#a8c9b4",
            "accent":       "#52b788",
            "accent2":      "#2d6a4f",
            "hero_bg":      "#1a2e1f",
            "tag_bg":       "#2d6a4f",
            "tag_text":     "#d8f3dc",
            "input_bg":     "#1a2e1f",
            "divider":      "#2d6a4f",
            "nav_active":   "#52b788",
            "nav_text":     "#95d5b2",
            "score_bg":     "#1b4332",
            "score_text":   "#ffffff",
            "score_sub":    "#95d5b2",
            "progress_bg":  "#1a2e1f",
            "progress_fill":"#52b788",
            "tip_icon_bg":  "#1b4332",
        }
    else:
        return {
            "bg":           "#f5faf6",
            "sidebar_bg":   "#eaf4ec",
            "card_bg":      "#ffffff",
            "card_border":  "#b7e4c7",
            "heading":      "#1b4332",
            "subheading":   "#2d6a4f",
            "text":         "#1a1a1a",
            "muted":        "#4a6550",
            "accent":       "#2d6a4f",
            "accent2":      "#52b788",
            "hero_bg":      "#d8f3dc",
            "tag_bg":       "#b7e4c7",
            "tag_text":     "#1b4332",
            "input_bg":     "#ffffff",
            "divider":      "#b7e4c7",
            "nav_active":   "#2d6a4f",
            "nav_text":     "#1b4332",
            "score_bg":     "#1b4332",
            "score_text":   "#ffffff",
            "score_sub":    "#95d5b2",
            "progress_bg":  "#d8f3dc",
            "progress_fill":"#2d6a4f",
            "tip_icon_bg":  "#d8f3dc",
        }

# ─────────────────────────────────────────────
#  DYNAMIC CSS  (rebuilt on every render)
# ─────────────────────────────────────────────

def inject_css():
    t = theme()
    st.markdown(f"""
<style>
/* ── Global ── */
html, body, .stApp {{
    background-color: {t['bg']} !important;
    color: {t['text']} !important;
    font-family: 'Segoe UI', sans-serif;
}}
.stApp * {{ color: {t['text']} !important; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {t['sidebar_bg']} !important;
    border-right: 2px solid {t['card_border']};
}}
[data-testid="stSidebar"] * {{ color: {t['nav_text']} !important; }}

/* ── Headings ── */
h1 {{ color: {t['heading']} !important; font-size: 2.2em; font-weight: 800; }}
h2 {{ color: {t['heading']} !important; font-size: 1.6em; font-weight: 700; }}
h3 {{ color: {t['subheading']} !important; font-size: 1.2em; font-weight: 600; }}

/* ── Cards ── */
.card {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 14px;
    padding: 24px 28px;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}}
.card-accent {{
    background: {t['hero_bg']};
    border-left: 5px solid {t['accent']};
    border-radius: 10px;
    padding: 18px 22px;
    margin: 8px 0;
}}
.hero-banner {{
    background: linear-gradient(135deg, {t['hero_bg']}, {t['card_bg']});
    border: 1px solid {t['card_border']};
    border-radius: 16px;
    padding: 40px 36px;
    text-align: center;
    margin-bottom: 20px;
}}
.hero-title {{
    font-size: 2.4em;
    font-weight: 900;
    color: {t['heading']} !important;
    margin-bottom: 8px;
}}
.hero-sub {{
    font-size: 1.1em;
    color: {t['muted']} !important;
    max-width: 600px;
    margin: 0 auto 20px;
    line-height: 1.6;
}}

/* ── Stat / metric tiles ── */
.stat-tile {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}}
.stat-number {{
    font-size: 2.2em;
    font-weight: 800;
    color: {t['accent']} !important;
}}
.stat-label {{
    font-size: 0.9em;
    color: {t['muted']} !important;
    margin-top: 4px;
}}

/* ── Score result box ── */
.score-box {{
    background: {t['score_bg']};
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    margin: 16px 0;
}}
.score-number {{
    font-size: 3em;
    font-weight: 900;
    color: {t['score_text']} !important;
}}
.score-label {{
    font-size: 1.3em;
    color: {t['score_sub']} !important;
    margin-top: 8px;
    font-weight: 600;
}}

/* ── Progress bar ── */
.progress-wrap {{
    background: {t['progress_bg']};
    border-radius: 20px;
    height: 12px;
    margin: 6px 0 16px;
    overflow: hidden;
}}
.progress-fill {{
    background: {t['progress_fill']};
    height: 100%;
    border-radius: 20px;
    transition: width 0.4s ease;
}}

/* ── Question card ── */
.q-card {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
}}
.q-number {{
    display: inline-block;
    background: {t['tag_bg']};
    color: {t['tag_text']} !important;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.82em;
    font-weight: 700;
    margin-bottom: 8px;
}}
.q-text {{
    font-size: 1.0em;
    font-weight: 600;
    color: {t['text']} !important;
    line-height: 1.5;
    margin-bottom: 6px;
}}

/* ── Tip cards ── */
.tip-card {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
}}
.tip-icon {{
    font-size: 1.6em;
    background: {t['tip_icon_bg']};
    border-radius: 8px;
    padding: 6px 10px;
    flex-shrink: 0;
}}
.tip-text {{ color: {t['text']} !important; line-height: 1.6; }}
.tip-title {{
    font-weight: 700;
    color: {t['heading']} !important;
    margin-bottom: 4px;
    font-size: 1.0em;
}}

/* ── Tag / badge ── */
.tag {{
    display: inline-block;
    background: {t['tag_bg']};
    color: {t['tag_text']} !important;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82em;
    font-weight: 600;
    margin: 3px;
}}

/* ── Nav button styling ── */
.stButton > button {{
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}}

/* ── Input fields ── */
.stTextInput input {{
    background: {t['input_bg']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['card_border']} !important;
    border-radius: 8px !important;
}}
.stTextInput label, .stTextInput label p {{
    color: {t['text']} !important;
    font-weight: 600 !important;
}}

/* ── Radio buttons ── */
.stRadio label, .stRadio label p,
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] label p {{
    color: {t['text']} !important;
    font-size: 0.96em !important;
}}

/* ── Info / warning / error boxes ── */
.stAlert {{ border-radius: 10px !important; }}

/* ── Divider ── */
hr {{ border-color: {t['divider']} !important; }}

/* ── Hide Streamlit default elements ── */
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
div[data-testid="stForm"] {{ border: none !important; padding: 0 !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  NAVIGATION
# ─────────────────────────────────────────────

def go(page: str):
    st.session_state.page = page
    st.rerun()

def sidebar_nav():
    t = theme()
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding: 10px 0 20px;'>
            <div style='font-size:2.5em;'>🌿</div>
            <div style='font-weight:800; font-size:1.05em;
                        color:{t["heading"]};'>Nature & Clarity</div>
            <div style='font-size:0.78em; color:{t["muted"]};
                        margin-top:4px;'>Mental Clarity Survey</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Navigation pages
        pages: list = [
            ("🏠", "Home",                 "home"),
            ("ℹ️", "About",                "about"),
            ("📝", "Take Survey",          "info"),
            ("📊", "Results",              "results"),
            ("💡", "Tips & Advice",        "tips"),
            ("📂", "Load Previous Results","load"),
        ]

        for icon, label, key in pages:
            active: bool = st.session_state.page == key
            style = (f"background:{t['accent']}; color:#fff; "
                     if active else
                     f"background:transparent; color:{t['nav_text']};")
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                go(key)

        st.divider()

        # Dark mode toggle
        dark = st.toggle("🌙  Dark Mode", value=st.session_state.dark_mode)
        if dark != st.session_state.dark_mode:
            st.session_state.dark_mode = dark
            st.rerun()

        # Quick status
        if st.session_state.score > 0:
            st.markdown(f"""
            <div class='card' style='margin-top:16px; text-align:center;'>
                <div style='font-size:0.78em; color:{t["muted"]};'>Last Score</div>
                <div style='font-size:1.8em; font-weight:800;
                            color:{t["accent"]};'>{st.session_state.score}/60</div>
                <div style='font-size:0.75em; color:{t["muted"]};
                            margin-top:2px;'>{st.session_state.name or "Anonymous"}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SURVEY DATA
# ─────────────────────────────────────────────

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
            ("Indoors, usually scrolling on my phone or watching screens", 3),
            ("I rarely take breaks at all", 4),
        ],
    },
    {
        "question": "How long do your outdoor or nature-based study breaks typically last?",
        "options": [
            ("More than 15 minutes", 0),
            ("Between 10 and 15 minutes", 1),
            ("Between 5 and 10 minutes", 2),
            ("Less than 5 minutes", 3),
            ("I do not take outdoor breaks", 4),
        ],
    },
    {
        "question": "How energised do you feel returning to study after a break spent in a natural outdoor setting?",
        "options": [
            ("Fully refreshed and ready to focus", 0),
            ("Somewhat refreshed", 1),
            ("A little better but not significantly changed", 2),
            ("About the same as before the break", 3),
            ("I feel more tired or no different", 4),
        ],
    },
    {
        "question": "How often do you feel mentally drained after long periods of studying indoors without any outdoor exposure?",
        "options": [
            ("Almost never, I maintain good energy", 0),
            ("Occasionally, towards the end of the day", 1),
            ("Fairly often, especially after two or more hours", 2),
            ("Very often, even after short periods", 3),
            ("Almost always, I feel drained quickly", 4),
        ],
    },
    {
        "question": "When you sit near a window or in a space with natural light during study, how does it affect your concentration?",
        "options": [
            ("It greatly improves my concentration", 0),
            ("It helps somewhat", 1),
            ("It makes little noticeable difference", 2),
            ("I am rarely near natural light when studying", 3),
            ("I never consider my lighting environment", 4),
        ],
    },
    {
        "question": "How aware are you of the importance of nature exposure for mental clarity and cognitive performance?",
        "options": [
            ("Very aware and I actively apply this knowledge", 0),
            ("Somewhat aware and I try to include outdoor breaks", 1),
            ("I have heard about it but do not really apply it", 2),
            ("I was not really aware of this connection", 3),
            ("I do not believe nature exposure makes any difference", 4),
        ],
    },
    {
        "question": "How often do you use nature sounds (birdsong, rain, wind) while studying when you cannot go outside?",
        "options": [
            ("Regularly, it helps me focus", 0),
            ("Sometimes, when I feel distracted", 1),
            ("Rarely", 2),
            ("Never tried it", 3),
            ("I prefer complete silence or non-nature sounds", 4),
        ],
    },
    {
        "question": "How does your ability to recall information change after an outdoor break compared to an indoor break?",
        "options": [
            ("Significantly better after outdoor breaks", 0),
            ("Slightly better after outdoor breaks", 1),
            ("No noticeable difference between the two", 2),
            ("I have not paid attention to this difference", 3),
            ("I rarely take outdoor breaks to compare", 4),
        ],
    },
    {
        "question": "How frequently do you feel creatively blocked or stuck on a problem while studying indoors for extended periods?",
        "options": [
            ("Almost never, I remain creative", 0),
            ("Occasionally", 1),
            ("Fairly often, especially during long sessions", 2),
            ("Frequently, I often feel stuck", 3),
            ("Almost always when studying indoors for long", 4),
        ],
    },
    {
        "question": "On days when you spend time in a park, campus greenery, or any outdoor space, how do you feel about your overall study performance that day?",
        "options": [
            ("Noticeably more productive and focused", 0),
            ("Somewhat better than usual", 1),
            ("About the same as any other day", 2),
            ("I rarely spend time outdoors during study days", 3),
            ("I have not observed any connection", 4),
        ],
    },
    {
        "question": "How difficult is it for you to refocus on academic tasks after a break spent entirely on screens or indoors?",
        "options": [
            ("Not difficult at all", 0),
            ("Slightly difficult but I manage quickly", 1),
            ("Moderately difficult, takes several minutes", 2),
            ("Quite difficult, often takes more than ten minutes", 3),
            ("Very difficult, I often lose significant study time", 4),
        ],
    },
    {
        "question": "Looking at your overall lifestyle, how well do you integrate nature or outdoor time into your daily academic routine?",
        "options": [
            ("Very well, it is a deliberate and consistent part of my routine", 0),
            ("Fairly well, I do it when I can", 1),
            ("Moderately, I sometimes remember to go outside", 2),
            ("Poorly, I rarely make time for outdoor breaks", 3),
            ("Not at all, outdoor breaks are not part of my routine", 4),
        ],
    },
]

# ─────────────────────────────────────────────
#  SCORING BANDS
# ─────────────────────────────────────────────

SCORE_BANDS: list = [
    (0,   8,  "🌿 Excellent Nature Connection",
     "You regularly engage with nature during breaks. Your mental clarity is well-restored "
     "and your study habits reflect a strong awareness of restorative environments. "
     "Keep it up — you are setting an excellent example!",
     "excellent"),
    (9,  16,  "🌱 Good Restoration Habits",
     "You make reasonable use of nature breaks and your mental clarity benefits from this. "
     "Continue taking outdoor breaks and consider slightly increasing their frequency.",
     "good"),
    (17, 26,  "☁️ Moderate Nature Engagement",
     "You occasionally benefit from nature exposure, but there is room to improve. "
     "Try to add at least one short outdoor walk per study session to boost clarity.",
     "moderate"),
    (27, 36,  "🪴 Low Nature Engagement",
     "Your study breaks rarely involve nature, which may be limiting your mental clarity "
     "and focus. It is advisable to introduce short walks or time near green spaces regularly.",
     "low"),
    (37, 46,  "😔 Minimal Restoration",
     "You have very little nature exposure during breaks. This may negatively affect your "
     "concentration and cognitive performance. Consider restructuring your break routine.",
     "minimal"),
    (47, 54,  "⚠️ Poor Clarity Restoration",
     "Your current break habits provide almost no restorative benefit. Lack of nature "
     "contact is likely impacting your mental wellbeing. Lifestyle changes are recommended.",
     "poor"),
    (55, 60,  "🚨 Critical Disconnection from Nature",
     "You have an extreme disconnect from nature during study periods, which is associated "
     "with poor mental clarity, fatigue, and reduced cognitive function. "
     "Please consider speaking with a wellbeing advisor.",
     "critical"),
]

RESULTS_DB_FILE: str = "results_db.json"


def get_state(score: int) -> tuple:
    """Return (label, description, category_key) for a given score."""
    for (low, high, label, desc, cat) in SCORE_BANDS:
        if low <= score <= high:
            return label, desc, cat
    return "Unknown", "Score out of range.", "unknown"

# ─────────────────────────────────────────────
#  VALIDATION
# ─────────────────────────────────────────────

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

# ─────────────────────────────────────────────
#  RESULTS DATABASE  (server-side JSON store)
# ─────────────────────────────────────────────

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
    """Save or update a student's result in the database keyed by student_id."""
    db: dict = load_db()
    db[data["student_id"]] = data
    with open(RESULTS_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def lookup_by_id(sid: str) -> dict:
    """Return the result record for a given student ID, or empty dict."""
    db: dict = load_db()
    return db.get(sid, {})

# ─────────────────────────────────────────────
#  DOWNLOAD BUILDERS
# ─────────────────────────────────────────────

def build_txt(data: dict) -> bytes:
    lines: list = [
        "=" * 54,
        "  NATURE & MENTAL CLARITY SURVEY — RESULTS",
        "=" * 54,
        f"Name:          {data['name']}",
        f"Date of Birth: {data['dob']}",
        f"Student ID:    {data['student_id']}",
        f"Date Taken:    {data['date_taken']}",
        f"Total Score:   {data['score']} / 60",
        f"Result:        {data['state_label']}",
        "",
        "Description:",
        data['state_description'],
        "=" * 54,
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

# ─────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────

def page_home():
    t = theme()

    # Hero banner
    st.markdown(f"""
    <div class="hero-banner">
        <div style="font-size:3.5em; margin-bottom:8px;">🌿</div>
        <div class="hero-title">Nature & Mental Clarity Survey</div>
        <div class="hero-sub">
            Discover how short nature exposures during your study breaks
            influence mental clarity, focus, and cognitive restoration.
        </div>
        <div style="margin-top:10px;">
            <span class="tag">🎓 Academic Research</span>
            <span class="tag">🧠 Mental Wellbeing</span>
            <span class="tag">🌳 Nature Science</span>
            <span class="tag">📊 15 Questions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
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

    # Two-column info section
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown(f"""
        <div class="card">
            <h3>📋 About This Survey</h3>
            <p style="color:{t['text']}; line-height:1.7;">
                This questionnaire has been designed as part of coursework research
                into <strong>Attention Restoration Theory (ART)</strong>. It measures
                how frequently students engage with natural environments during study
                breaks and how strongly this correlates with their reported mental
                clarity.
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
            <h3>🗺️ How It Works</h3>
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

    # Call to action buttons
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        if st.button("🌿  Start the Survey Now", use_container_width=True, type="primary"):
            go("info")
    with c2:
        if st.button("ℹ️  Learn More", use_container_width=True):
            go("about")
    with c3:
        if st.button("📂  Load Results", use_container_width=True):
            go("load")

# ─────────────────────────────────────────────
#  PAGE: ABOUT
# ─────────────────────────────────────────────

def page_about():
    t = theme()
    st.markdown("# ℹ️ About This Survey")
    st.markdown("*Understanding the science behind nature, breaks, and mental clarity.*")
    st.divider()

    # Section 1
    st.markdown(f"""
    <div class="card">
        <h2>🧠 What Is Mental Clarity?</h2>
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

    # Section 2 — two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>🌳 How Nature Helps</h3>
            <p style="color:{t['text']}; line-height:1.7;">
                <strong>Attention Restoration Theory (ART)</strong>, proposed by Kaplan
                and Kaplan (1989), suggests that natural environments engage involuntary
                attention effortlessly, allowing the directed attention system to recover.
            </p>
            <p style="color:{t['text']}; line-height:1.7;">
                Key benefits of short nature exposure include:
            </p>
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
            <h3>📖 Research Background</h3>
            <p style="color:{t['text']}; line-height:1.7;">
                Studies by Berman et al. (2008) demonstrated that a 50-minute walk in nature
                improved memory performance by 20% compared to an urban walk. Similar findings
                have been replicated across multiple academic contexts.
            </p>
            <p style="color:{t['text']}; line-height:1.7;">
                Even <strong>micro-breaks</strong> of 40 seconds looking at a green roof
                were found to significantly restore concentration levels
                (Lee et al., 2015).
            </p>
            <p style="color:{t['text']}; line-height:1.7;">
                These findings form the scientific basis for this questionnaire's
                design and scoring system.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Section 3 — Scoring explained
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        <h2>📊 How the Scoring Works</h2>
        <p style="color:{t['text']}; line-height:1.7;">
            The survey contains <strong>15 questions</strong>, each with 5 answer options
            scored from <strong>0 (best)</strong> to <strong>4 (worst)</strong>.
            This means the minimum possible score is <strong>0</strong> and the maximum
            is <strong>60</strong>. Lower scores indicate better nature engagement and
            mental clarity restoration.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Score bands table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏷️ Result Categories")

    band_cols = st.columns(2)
    for i, (low, high, label, desc, _) in enumerate(SCORE_BANDS):
        with band_cols[i % 2]:
            st.markdown(f"""
            <div class="card-accent" style="margin-bottom:10px;">
                <div style="font-weight:700; color:{t['heading']};">{label}</div>
                <div style="font-size:0.82em; color:{t['muted']};
                            margin-top:2px;">Score range: {low} – {high}</div>
                <div style="font-size:0.88em; color:{t['text']};
                            margin-top:6px; line-height:1.5;">{desc[:110]}...</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝  Take the Survey", type="primary"):
        go("info")

# ─────────────────────────────────────────────
#  PAGE: USER INFO
# ─────────────────────────────────────────────

def page_info():
    t = theme()
    st.markdown("# 📝 Your Details")
    st.markdown("Please complete your information before starting the survey.")
    st.divider()

    col_form, col_info = st.columns([1.2, 1])

    with col_form:
        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        st.markdown("### Personal Information")

        name = st.text_input("Full Name (Surname Given Name)",
                             placeholder="e.g. Smith-Jones Mary Ann",
                             value=st.session_state.name)
        dob  = st.text_input("Date of Birth",
                             placeholder="DD/MM/YYYY",
                             value=st.session_state.dob)
        sid  = st.text_input("Student ID (digits only)",
                             placeholder="e.g. 12345678",
                             value=st.session_state.student_id)

        st.markdown("</div>", unsafe_allow_html=True)

        b1, b2 = st.columns([1, 2])
        with b1:
            if st.button("← Home"):
                go("home")
        with b2:
            if st.button("Start Survey →", type="primary", use_container_width=True):
                errors: list = []
                if not validate_name(name):
                    errors.append("Invalid name — use only letters, hyphens (-), apostrophes ('), or spaces.")
                if not validate_dob(dob):
                    errors.append("Invalid date of birth — use DD/MM/YYYY with a real date.")
                if not validate_student_id(sid):
                    errors.append("Invalid Student ID — digits only, no spaces or letters.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    st.session_state.name       = name.strip()
                    st.session_state.dob        = dob.strip()
                    st.session_state.student_id = sid.strip()
                    # Reset previous answers when starting fresh
                    for i in range(len(QUESTIONS)):
                        if f"q_{i}" in st.session_state:
                            del st.session_state[f"q_{i}"]
                    go("survey")

    with col_info:
        st.markdown(f"""
        <div class="card">
            <h3>🔒 Privacy Notice</h3>
            <p style="color:{t['text']}; line-height:1.7; font-size:0.92em;">
                Your information is used only to personalise your results and
                allow you to retrieve them later using your Student ID.
                No data is shared with third parties.
            </p>
            <h3 style="margin-top:16px;">✅ Validation Rules</h3>
            <ul style="color:{t['text']}; line-height:2.0; font-size:0.9em;">
                <li><strong>Name:</strong> letters, hyphens, apostrophes, spaces only</li>
                <li><strong>Date of Birth:</strong> DD/MM/YYYY format, real date</li>
                <li><strong>Student ID:</strong> digits only (no letters or spaces)</li>
            </ul>
            <p style="color:{t['muted']}; font-size:0.85em; margin-top:10px;">
                Examples of valid names:<br>
                O'Connor, Smith-Jones, Mary Ann
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: SURVEY
# ─────────────────────────────────────────────

def page_survey():
    t = theme()
    total_q: int = len(QUESTIONS)

    st.markdown("# 📋 Survey Questions")

    # Count answered so far for progress bar
    answered_count: int = sum(
        1 for i in range(total_q)
        if st.session_state.get(f"q_{i}") is not None
    )
    pct: float = round((answered_count / total_q) * 100)

    # Progress indicator
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between;
                align-items:center; margin-bottom:4px;">
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
        if st.button("← Back to Details"):
            go("info")
    with b2:
        if st.button("Submit Survey ✔", type="primary", use_container_width=True):
            if not all_answered:
                unanswered: list = [
                    str(i + 1) for i, a in enumerate(answers) if a is None
                ]
                st.error(f"Please answer all questions. Missing: Q{', Q'.join(unanswered)}")
            else:
                total: int = sum(answers)
                label, description, cat = get_state(total)

                st.session_state.answers           = answers
                st.session_state.score             = total
                st.session_state.state_label       = label
                st.session_state.state_description = description
                st.session_state.tips_category     = cat

                # Auto-save to server-side database
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

# ─────────────────────────────────────────────
#  PAGE: RESULTS
# ─────────────────────────────────────────────

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
    cat: str         = st.session_state.tips_category

    st.markdown("# 📊 Your Results")
    st.divider()

    # User info strip
    st.markdown(f"""
    <div class="card-accent">
        <strong>👤 {st.session_state.name or "Anonymous"}</strong>
        &nbsp;·&nbsp; DOB: {st.session_state.dob or "—"}
        &nbsp;·&nbsp; Student ID: {st.session_state.student_id or "—"}
    </div>
    """, unsafe_allow_html=True)

    # Score + label
    pct_score: int = round((score / 60) * 100)
    st.markdown(f"""
    <div class="score-box">
        <div class="score-number">{score} <span style="font-size:0.5em;
            font-weight:400; color:#95d5b2;">/ 60</span></div>
        <div class="score-label">{label}</div>
        <div style="margin-top:14px;">
            <div style="background:rgba(255,255,255,0.15); border-radius:20px;
                        height:10px; overflow:hidden; max-width:320px; margin:0 auto;">
                <div style="background:#95d5b2; width:{pct_score}%;
                            height:100%; border-radius:20px;"></div>
            </div>
            <div style="font-size:0.8em; color:#95d5b2; margin-top:6px;">
                {pct_score}% of maximum score
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Description + tips CTA
    col_desc, col_action = st.columns([1.6, 1])

    with col_desc:
        st.markdown(f"""
        <div class="card">
            <h3>🔍 What This Means</h3>
            <p style="color:{t['text']}; line-height:1.8;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_action:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:2em;">💡</div>
            <h3>Want Advice?</h3>
            <p style="color:{t['muted']}; font-size:0.9em;">
                Visit the Tips page for personalised recommendations
                based on your score.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View My Tips →", use_container_width=True, type="primary"):
            go("tips")

    # Per-question answer breakdown
    if st.session_state.answers:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 View Answer Breakdown by Question", expanded=False):
            st.markdown(f"""
            <div style="font-size:0.9em; color:{t['muted']}; margin-bottom:12px;">
                Each bar shows the score you gave for that question (0 = best, 4 = most concerning).
                Higher bars indicate areas where nature exposure may need improvement.
            </div>
            """, unsafe_allow_html=True)

            import pandas as pd
            short_labels: list = [f"Q{i+1}" for i in range(len(st.session_state.answers))]
            chart_data = pd.DataFrame({
                "Question": short_labels,
                "Score": st.session_state.answers,
            }).set_index("Question")
            st.bar_chart(chart_data, color=t["accent"])

            # Table view of each answer
            for i, (q, ans_score) in enumerate(zip(QUESTIONS, st.session_state.answers)):
                chosen_label: str = next(
                    (opt[0] for opt in q["options"] if opt[1] == ans_score), "—"
                )
                bar_fill: str = "#52b788" if ans_score <= 1 else ("#f4a261" if ans_score <= 2 else "#e63946")
                st.markdown(f"""
                <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                            border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-size:0.88em; font-weight:600;
                                    color:{t['text']}; flex:1; margin-right:12px;">
                            <span style="color:{t['muted']}; font-size:0.85em;">Q{i+1}</span>
                            &nbsp;{q['question'][:80]}{'...' if len(q['question']) > 80 else ''}
                        </div>
                        <div style="background:{bar_fill}; color:#fff; border-radius:6px;
                                    padding:3px 10px; font-weight:700; font-size:0.9em;
                                    white-space:nowrap;">{ans_score}/4</div>
                    </div>
                    <div style="font-size:0.83em; color:{t['muted']}; margin-top:4px;">
                        Your answer: {chosen_label}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Download section
    st.markdown("### 💾 Save Your Results")
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

    fmt_l: str    = fmt.lower()
    builders: dict = {"json": build_json, "csv": build_csv, "txt": build_txt}
    file_bytes: bytes = builders[fmt_l](data)
    mime_map: dict    = {"json": "application/json",
                         "csv": "text/csv", "txt": "text/plain"}

    st.download_button(
        label=f"⬇️  Download as {fmt}",
        data=file_bytes,
        file_name=f"nature_survey_{st.session_state.student_id or 'result'}.{fmt_l}",
        mime=mime_map[fmt_l],
        use_container_width=True,
    )

    st.markdown(f"""
    <div class="card-accent" style="margin-top:12px; font-size:0.88em;
                                    color:{t['muted']};">
        ✅ Your results have also been saved automatically to the server.
        You can retrieve them anytime using your Student ID on the
        <strong>Load Previous Results</strong> page.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home"):
        go("home")

# ─────────────────────────────────────────────
#  PAGE: TIPS & RECOMMENDATIONS
# ─────────────────────────────────────────────

def page_tips():
    t = theme()
    cat: str = st.session_state.tips_category

    st.markdown("# 💡 Tips & Recommendations")
    st.markdown("*Evidence-based advice to improve your mental clarity through nature.*")
    st.divider()

    # Personalised banner if they have a score
    if cat:
        label: str = st.session_state.state_label
        score: int = st.session_state.score
        st.markdown(f"""
        <div class="card-accent">
            <strong>🎯 Personalised advice for your result:</strong>
            {label} &nbsp;·&nbsp; Score: {score}/60
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Tips data structure
    tip_sections: list = [
        {
            "title": "🌳 Outdoor Break Tips",
            "tips": [
                ("🚶", "Take a 10-minute walk",
                 "Even a brief 10-minute walk in a green space can restore cognitive "
                 "performance. You do not need a park — a tree-lined street works too."),
                ("📵", "Leave your phone behind",
                 "To get the full restorative benefit of a nature break, try leaving "
                 "your phone indoors. Notifications keep your directed attention engaged."),
                ("🌅", "Time your breaks wisely",
                 "Take outdoor breaks after 45–90 minutes of focused study, before "
                 "mental fatigue sets in rather than after you are already exhausted."),
                ("👥", "Walk with a friend",
                 "Social nature walks combine the benefits of restorative environments "
                 "with positive social interaction, doubling the recovery effect."),
            ],
        },
        {
            "title": "🧠 Mental Clarity Tips",
            "tips": [
                ("💧", "Stay hydrated",
                 "Dehydration reduces cognitive performance significantly. Keep a water "
                 "bottle at your desk and drink at least 2 litres per day during study."),
                ("🌬️", "Open a window",
                 "Fresh air improves oxygen levels in your study space, directly "
                 "supporting concentration and reducing mental fatigue."),
                ("🎵", "Use nature sounds",
                 "When you cannot go outside, studies show that nature soundscapes "
                 "(rainfall, birdsong, forest sounds) can partially replicate the "
                 "restorative effect of being in nature."),
                ("🌿", "Add a desk plant",
                 "Research shows that even a small plant on your desk can reduce "
                 "stress and improve focus. Spider plants and peace lilies are "
                 "low-maintenance options."),
            ],
        },
        {
            "title": "📚 Effective Study Break Tips",
            "tips": [
                ("⏱️", "Use the Pomodoro Technique",
                 "Study for 25 minutes, then take a 5-minute break. After four "
                 "cycles, take a longer 20–30 minute break. During breaks, step outside."),
                ("🧘", "Try micro-restoration",
                 "Research shows that even 40–90 seconds of looking at a green view "
                 "from a window can meaningfully restore concentration levels."),
                ("🚫", "Avoid screen-based breaks",
                 "Scrolling social media or watching videos during breaks keeps "
                 "your directed attention engaged and prevents cognitive recovery."),
                ("☀️", "Get morning sunlight",
                 "Starting your day with 10 minutes of outdoor sunlight sets your "
                 "circadian rhythm and improves mental clarity throughout the day."),
            ],
        },
        {
            "title": "🌱 Building a Nature Habit",
            "tips": [
                ("📅", "Schedule outdoor breaks",
                 "Treat outdoor breaks like appointments in your calendar. "
                 "Pre-scheduling makes them far more likely to happen."),
                ("🗺️", "Find your nearby green spots",
                 "Identify parks, gardens, or green corridors within 5 minutes of "
                 "your study location. Knowing exactly where to go removes friction."),
                ("📱", "Use a habit tracker",
                 "Apps like Habitica, Streaks, or even a paper checklist can help "
                 "you build a consistent outdoor break routine over time."),
                ("🎯", "Start small",
                 "If you currently take no outdoor breaks, start with just one per "
                 "day. Small consistent changes outperform big unsustainable ones."),
            ],
        },
    ]

    for section in tip_sections:
        st.markdown(f"### {section['title']}")
        cols = st.columns(2)
        for j, (icon, title, text) in enumerate(section["tips"]):
            with cols[j % 2]:
                st.markdown(f"""
                <div class="tip-card">
                    <div class="tip-icon">{icon}</div>
                    <div class="tip-text">
                        <div class="tip-title">{title}</div>
                        <div style="font-size:0.9em;">{text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 View My Results", use_container_width=True):
            go("results")
    with c2:
        if st.button("📝 Retake Survey", use_container_width=True, type="primary"):
            go("info")

# ─────────────────────────────────────────────
#  PAGE: LOAD PREVIOUS RESULTS
# ─────────────────────────────────────────────

def page_load():
    t = theme()
    st.markdown("# 📂 Load Previous Results")
    st.markdown("*Enter your Student ID to retrieve your saved survey results.*")
    st.divider()

    # ── Tab layout: Search | Upload | All Submissions ──
    tab_search, tab_upload, tab_all = st.tabs(
        ["🔍 Search by Student ID", "📤 Upload a File", "📋 All Submissions"]
    )

    # ── TAB 1: Search by Student ID ──────────────────
    with tab_search:
        st.markdown("<br>", unsafe_allow_html=True)
        col_in, col_gap = st.columns([1, 1.5])
        with col_in:
            st.markdown(f"""
            <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                        border-radius:14px; padding:24px 28px;">
                <div style="font-weight:700; font-size:1.1em;
                            color:{t['heading']}; margin-bottom:4px;">Find your results</div>
                <div style="font-size:0.88em; color:{t['muted']}; margin-bottom:16px;">
                    Your results are automatically saved when you complete the survey.
                    Enter your Student ID below to retrieve them.
                </div>
            """, unsafe_allow_html=True)

            sid_input: str = st.text_input(
                "Student ID", placeholder="e.g. 12345678", key="load_sid",
                label_visibility="visible"
            )

            search_clicked = st.button(
                "Search Results", type="primary", use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Show result spanning full width below the input
        if search_clicked:
            if not validate_student_id(sid_input.strip()):
                st.error("Please enter a valid Student ID (digits only, no spaces).")
            else:
                record: dict = lookup_by_id(sid_input.strip())
                if record:
                    score_int: int   = int(record.get("score", 0))
                    label, desc, cat = get_state(score_int)
                    pct: int         = round((score_int / 60) * 100)

                    st.success(f"Results found for Student ID: **{sid_input.strip()}**")

                    # Full result card
                    st.markdown(f"""
                    <div style="background:{t['score_bg']}; border-radius:16px;
                                padding:28px 32px; margin:16px 0; text-align:center;">
                        <div style="font-size:3em; font-weight:900;
                                    color:{t['score_text']};">{score_int}
                            <span style="font-size:0.45em; font-weight:400;
                                         color:{t['score_sub']};">/ 60</span>
                        </div>
                        <div style="font-size:1.25em; font-weight:700;
                                    color:{t['score_sub']}; margin-top:6px;">{label}</div>
                        <div style="margin-top:14px;">
                            <div style="background:rgba(255,255,255,0.15); border-radius:20px;
                                        height:10px; overflow:hidden; max-width:260px; margin:0 auto;">
                                <div style="background:{t['score_sub']}; width:{pct}%;
                                            height:100%; border-radius:20px;"></div>
                            </div>
                            <div style="font-size:0.8em; color:{t['score_sub']}; margin-top:6px;">
                                {pct}% of maximum score
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Details row
                    d1, d2 = st.columns(2)
                    with d1:
                        st.markdown(f"""
                        <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                                    border-radius:12px; padding:18px 22px;">
                            <div style="font-weight:700; color:{t['heading']};
                                        margin-bottom:10px;">Student Information</div>
                            <div style="color:{t['text']}; line-height:2.0; font-size:0.94em;">
                                <strong>Name:</strong> {record.get('name','—')}<br>
                                <strong>Date of Birth:</strong> {record.get('dob','—')}<br>
                                <strong>Student ID:</strong> {record.get('student_id','—')}<br>
                                <strong>Date Taken:</strong> {record.get('date_taken','—')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with d2:
                        st.markdown(f"""
                        <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                                    border-radius:12px; padding:18px 22px;">
                            <div style="font-weight:700; color:{t['heading']};
                                        margin-bottom:10px;">What This Means</div>
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

    # ── TAB 2: Upload a File ──────────────────────────
    with tab_upload:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                    border-radius:14px; padding:24px 28px; max-width:520px;">
            <div style="font-weight:700; font-size:1.05em; color:{t['heading']};
                        margin-bottom:4px;">Upload a Saved Results File</div>
            <div style="font-size:0.88em; color:{t['muted']}; margin-bottom:16px;">
                Upload a previously downloaded results file (JSON, CSV, or TXT)
                to view its contents here.
            </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose a file", type=["json", "csv", "txt"], key="load_file"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if uploaded:
            ext: str   = uploaded.name.split(".")[-1].lower()
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
                    score_int: int   = int(score_raw)
                    label, desc, cat = get_state(score_int)
                except (ValueError, TypeError):
                    label = data.get("state_label", "N/A")
                    desc  = data.get("state_description", "")
                    score_int = 0

                st.success("File loaded successfully.")
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                            border-left:5px solid {t['accent']}; border-radius:12px;
                            padding:20px 24px;">
                    <div style="font-weight:700; color:{t['heading']};
                                margin-bottom:10px;">Loaded Results</div>
                    <div style="color:{t['text']}; line-height:2.0; font-size:0.94em;">
                        <strong>Name:</strong> {data.get('name','—')}<br>
                        <strong>Student ID:</strong> {data.get('student_id','—')}<br>
                        <strong>Score:</strong> {score_raw} / 60<br>
                        <strong>Result:</strong> {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 3: All Submissions ────────────────────────
    with tab_all:
        st.markdown("<br>", unsafe_allow_html=True)
        db: dict = load_db()
        if not db:
            st.info(
                "No submissions have been recorded yet. "
                "Complete the survey to see results appear here."
            )
        else:
            count: int = len(db)
            scores_all: list = [int(v.get("score", 0)) for v in db.values()]
            avg_score: float = round(sum(scores_all) / count, 1) if scores_all else 0.0
            max_score: int   = max(scores_all) if scores_all else 0
            min_score: int   = min(scores_all) if scores_all else 0

            m1, m2, m3, m4 = st.columns(4)
            for col, num, lbl in [
                (m1, str(count),       "Total Submissions"),
                (m2, str(avg_score),   "Average Score"),
                (m3, str(min_score),   "Best Score"),
                (m4, str(max_score),   "Highest Score"),
            ]:
                with col:
                    st.markdown(f"""
                    <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                                border-radius:12px; padding:18px; text-align:center;">
                        <div style="font-size:2em; font-weight:800;
                                    color:{t['accent']};">{num}</div>
                        <div style="font-size:0.85em; color:{t['muted']};
                                    margin-top:4px;">{lbl}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"### All Submitted Results ({count})")

            for sid, rec in sorted(db.items()):
                rec_score: int   = int(rec.get("score", 0))
                rec_label, _, __ = get_state(rec_score)
                score_pct: int   = round((rec_score / 60) * 100)
                bar_color: str   = (
                    t["accent"] if rec_score <= 16 else
                    "#f4a261"   if rec_score <= 36 else
                    "#e63946"
                )
                st.markdown(f"""
                <div style="background:{t['card_bg']}; border:1px solid {t['card_border']};
                            border-radius:10px; padding:14px 18px; margin-bottom:10px;
                            display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
                    <div style="min-width:90px;">
                        <div style="font-size:0.75em; color:{t['muted']};">Student ID</div>
                        <div style="font-weight:700; color:{t['text']};">{sid}</div>
                    </div>
                    <div style="flex:1; min-width:140px;">
                        <div style="font-size:0.75em; color:{t['muted']};">Name</div>
                        <div style="font-weight:600; color:{t['text']};">{rec.get('name','—')}</div>
                    </div>
                    <div style="min-width:100px;">
                        <div style="font-size:0.75em; color:{t['muted']};">Date Taken</div>
                        <div style="font-size:0.85em; color:{t['text']};">{rec.get('date_taken','—')}</div>
                    </div>
                    <div style="min-width:160px;">
                        <div style="font-size:0.75em; color:{t['muted']};
                                    margin-bottom:4px;">{rec_label}</div>
                        <div style="background:{t['progress_bg']}; border-radius:20px;
                                    height:8px; overflow:hidden;">
                            <div style="background:{bar_color}; width:{score_pct}%;
                                        height:100%; border-radius:20px;"></div>
                        </div>
                    </div>
                    <div style="background:{bar_color}; color:#fff; border-radius:8px;
                                padding:6px 14px; font-weight:800; font-size:1.0em;
                                white-space:nowrap;">{rec_score}/60</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🏠 Back to Home"):
        go("home")

# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────

inject_css()
sidebar_nav()

PAGE_MAP: dict = {
    "home":    page_home,
    "about":   page_about,
    "info":    page_info,
    "survey":  page_survey,
    "results": page_results,
    "tips":    page_tips,
    "load":    page_load,
}

PAGE_MAP.get(st.session_state.page, page_home)()
