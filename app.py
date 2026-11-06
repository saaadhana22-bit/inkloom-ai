import streamlit as st
import re
import html
from datetime import datetime
from ai_engine import rewrite_content

# ============================================================
# INKLOOM AI — BRAND COMMUNICATION & CONTENT STUDIO
# Main application file. Keep ai_engine.py in the same folder.
# ============================================================

st.set_page_config(
    page_title="Inkloom AI | Your Brand. Your Voice.",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------- DESIGN ----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --ink: #201b35;
    --muted: #77728b;
    --violet: #7657e8;
    --violet-dark: #5134bd;
    --coral: #ff786f;
    --peach: #fff0e9;
    --lavender: #eee9ff;
    --cream: #fbf9f6;
    --line: #e9e5f2;
    --mint: #dff5ed;
}
html { scroll-behavior: smooth; }
/* Make Streamlit's own top header fully transparent and remove its dark divider. */
header[data-testid="stHeader"],
.stAppHeader {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}
header[data-testid="stHeader"]::before,
header[data-testid="stHeader"]::after,
.stAppHeader::before,
.stAppHeader::after {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stDecoration"] {
    display: none !important;
    height: 0 !important;
}
.stApp {
    background: #fbf9ff;
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}
.block-container {
    max-width: 1240px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}
h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--ink);
    letter-spacing: -0.04em;
}
p, li, label, .stMarkdown { font-family: 'DM Sans', sans-serif; }
a { text-decoration: none !important; }
section[data-testid="stSidebar"] { background: #f1edff; }
div[data-testid="stVerticalBlock"] { gap: 0.8rem; }

.topbar {
    display:flex; align-items:center; justify-content:space-between;
    padding: 12px 20px; border:1px solid rgba(118,87,232,.13);
    border-radius:18px; background:rgba(255,255,255,.88);
    box-shadow:0 8px 30px rgba(43,29,89,.05);
    margin-bottom:28px;
}
.logo { font-family:'Space Grotesk'; font-weight:800; font-size:1.25rem; color:#261d45; }
.logo span { color:#7657e8; }
.navlinks { color:#716b82; font-size:.88rem; font-weight:700; }
.eyebrow {
    display:inline-block; padding:7px 12px; border-radius:30px;
    background:#eee9ff; color:#6447d2; font-size:.76rem;
    font-weight:800; letter-spacing:.09em; text-transform:uppercase;
}
.hero {
    position:relative; overflow:hidden; border-radius:30px;
    padding:58px 48px; min-height:410px;
    background: radial-gradient(circle at 82% 18%, #ffd4c8 0, transparent 26%),
                radial-gradient(circle at 68% 90%, #c8baff 0, transparent 35%),
                linear-gradient(120deg,#f0eaff 0%,#fff1eb 55%,#f8eaff 100%);
    border:1px solid #eee5ff;
}
.hero h1 { font-size:clamp(2.6rem,5vw,4.8rem); line-height:1.02; max-width:650px; margin:18px 0; }
.hero p { color:#625b76; font-size:1.08rem; max-width:560px; line-height:1.75; }
.hero-art {
    position:absolute; right:2%; top:9%; width:43%; max-width:500px;
    filter:drop-shadow(0 25px 28px rgba(48,32,91,.2));
    transform:rotate(-5deg);
    animation: floaty 5s ease-in-out infinite;
}
@keyframes floaty { 0%,100%{transform:translateY(0) rotate(-5deg)} 50%{transform:translateY(-12px) rotate(-3deg)} }
@keyframes rise { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
.fade { animation:rise .7s ease both; }
.pill {
    display:inline-block; padding:8px 12px; border-radius:30px;
    background:white; border:1px solid #eee8fa; color:#5d4a9b;
    font-size:.78rem; font-weight:700; margin:4px 4px 0 0;
}
.section { padding:48px 0 16px; }
.section-kicker { color:#7657e8; font-weight:800; text-transform:uppercase; letter-spacing:.13em; font-size:.75rem; }
.section-title { font-size:2.35rem; margin:8px 0 10px; }
.section-desc { color:#77728b; line-height:1.75; max-width:760px; }
.card {
    background:white; border:1px solid var(--line); border-radius:22px;
    padding:23px; height:100%; box-shadow:0 8px 28px rgba(40,28,80,.035);
    transition:transform .22s ease, box-shadow .22s ease;
}
.card:hover { transform:translateY(-5px); box-shadow:0 16px 36px rgba(65,44,130,.09); }
.card-icon {
    width:48px;height:48px;display:flex;align-items:center;justify-content:center;
    border-radius:15px;background:#f0ebff;font-size:1.35rem;margin-bottom:14px;
}
.card h3 { font-size:1.12rem; margin:4px 0 8px; }
.card p { color:#77728b; line-height:1.65; font-size:.92rem; }
.soft-panel {
    border-radius:26px; padding:28px; background:linear-gradient(135deg,#f0ebff,#fff0e9);
    border:1px solid #e9e0ff;
}
.dark-panel {
    border-radius:26px; padding:32px; color:white;
    background:linear-gradient(120deg,#292044,#4d367f 70%,#7657e8);
}
.dark-panel h2,.dark-panel h3,.dark-panel p { color:white; }
.stat {
    border-radius:18px; background:white; border:1px solid var(--line);
    padding:17px; text-align:center;
}
.stat strong { display:block; font-family:'Space Grotesk'; font-size:1.6rem; color:#7657e8; }
.stat span { color:#77728b; font-size:.8rem; }
.score-number {
    font-family:'Space Grotesk'; font-size:3.5rem; font-weight:800;
    color:#7657e8; line-height:1;
}
.score-track { height:9px; border-radius:20px; background:#eeeaf5; overflow:hidden; }
.score-fill { height:9px; border-radius:20px; background:linear-gradient(90deg,#7657e8,#ff8b7d); }
.result-box {
    background:#fff; border:1px solid #e9e5f2; border-radius:18px;
    padding:18px; min-height:150px; white-space:pre-wrap; line-height:1.7;
}
.preview-instagram {
    max-width:440px; margin:auto; background:white; border:1px solid #e8e3ed;
    border-radius:20px; overflow:hidden; box-shadow:0 12px 32px rgba(30,20,55,.08);
}
.preview-head { padding:13px 16px; font-weight:800; font-size:.9rem; }
.preview-image { width:100%; height:150px; object-fit:cover; }
.preview-caption { padding:14px 16px 18px; font-size:.9rem; line-height:1.6; color:#373044; }
.footer {
    margin-top:55px; padding:32px; border-radius:24px;
    background:#211b35; color:#eae5ff;
}
.footer strong { color:white; font-family:'Space Grotesk'; font-size:1.35rem; }
.footer p { color:#c5bddb; font-size:.88rem; line-height:1.7; }
div.stButton > button {
    border:0; border-radius:13px; padding:.72rem 1.2rem;
    font-weight:800; background:linear-gradient(100deg,#7657e8,#9678f3);
    color:white; transition:all .2s ease;
}
div.stButton > button:hover {
    transform:translateY(-2px); box-shadow:0 8px 20px rgba(118,87,232,.25);
    color:white; border:0;
}
div[data-testid="stDownloadButton"] button {
    border-radius:12px; border:1px solid #dcd3f5; color:#5c43b7; font-weight:800;
}
input, textarea, [data-baseweb="select"] > div {
    border-radius:12px !important;
}
/* Keep Streamlit form labels and entered text readable on light surfaces. */
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stDateInput"] label,
div[data-testid="stTimeInput"] label {
    color:#201b35 !important;
    font-weight:700 !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background:#ffffff !important;
    color:#201b35 !important;
    -webkit-text-fill-color:#201b35 !important;
    caret-color:#201b35 !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color:#77728b !important;
    -webkit-text-fill-color:#77728b !important;
    opacity:1 !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background:#ffffff !important;
    color:#201b35 !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"] *,
div[data-testid="stMultiSelect"] [data-baseweb="select"] * {
    color:#201b35 !important;
}
div[data-testid="stTextArea"] textarea { background:#fff !important; }
hr { border-color:#eee9f5; }
.small-note { color:#8b849d; font-size:.78rem; line-height:1.55; }
@media(max-width:850px) {
    .hero { padding:34px 25px 260px; }
    .hero-art { width:75%; right:8%; top:auto; bottom:8px; }
    .hero h1 { font-size:2.8rem; }
    .section-title { font-size:1.9rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------- HELPERS ----------------------------

def section_heading(kicker, title, description=""):
    st.markdown(
        f"""<div class="section">
        <div class="section-kicker">{html.escape(kicker)}</div>
        <div class="section-title">{html.escape(title)}</div>
        <div class="section-desc">{html.escape(description)}</div>
        </div>""",
        unsafe_allow_html=True,
    )

def safe_text(value):
    return html.escape(str(value or ""))

def calculate_content_score(text, platform, content_type):
    """Transparent heuristic score; not an engagement prediction."""
    words = re.findall(r"\b[\w'-]+\b", text)
    word_count = len(words)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    avg_sentence = word_count / max(len(sentences), 1)

    clarity = 20 if word_count >= 8 else max(5, word_count * 2)
    if avg_sentence <= 22:
        clarity += 0
    else:
        clarity -= min(8, int(avg_sentence - 22))
    clarity = max(5, min(20, clarity))

    structure = 8
    if len(sentences) >= 2:
        structure += 5
    if "\n" in text or any(mark in text for mark in ["•", "-", "1."]):
        structure += 4
    if text.strip() and text.strip()[-1] in ".!?":
        structure += 3
    structure = min(20, structure)

    readability = 20
    if avg_sentence > 28:
        readability -= 7
    elif avg_sentence > 20:
        readability -= 3
    if text.count(",") > max(4, word_count / 12):
        readability -= 3
    readability = max(5, readability)

    engagement = 5
    if "?" in text:
        engagement += 5
    if re.search(r"\b(you|your|we|our|join|share|discover|learn)\b", text, re.I):
        engagement += 5
    if re.search(r"\b(try|explore|visit|learn|shop|contact|follow|comment|share)\b", text, re.I):
        engagement += 5
    engagement = min(20, engagement)

    platform_score = 12
    if platform == "Instagram" and word_count <= 150:
        platform_score += 8
    elif platform == "LinkedIn" and 40 <= word_count <= 250:
        platform_score += 8
    elif platform in ["Website", "Blog"] and word_count >= 50:
        platform_score += 8
    elif platform in ["Facebook", "Email"] and word_count >= 25:
        platform_score += 8
    platform_score = min(20, platform_score)

    components = {
        "Clarity": clarity,
        "Structure": structure,
        "Readability": readability,
        "Engagement readiness": engagement,
        "Platform fit": platform_score,
    }
    total = round(sum(components.values()) / 100 * 100)
    total = max(0, min(100, total))

    strengths = []
    improvements = []
    if clarity >= 15: strengths.append("The main message is reasonably easy to understand.")
    else: improvements.append("Make the main message more direct and specific.")
    if structure >= 15: strengths.append("The content has some useful structure.")
    else: improvements.append("Break the message into clearer sentences or short paragraphs.")
    if readability >= 15: strengths.append("The wording is relatively easy to scan.")
    else: improvements.append("Shorten long sentences and simplify dense wording.")
    if engagement >= 15: strengths.append("The content speaks to the reader or invites action.")
    else: improvements.append("Consider adding a relevant question or call to action.")
    if platform_score >= 17: strengths.append(f"The length is a reasonable starting point for {platform}.")
    else: improvements.append(f"Review the length and format for {platform}.")

    if not strengths:
        strengths.append("You have a starting draft to build on.")
    return total, components, strengths, improvements, word_count, len(text)

def make_report(brand_name, platform, score, components, strengths, improvements, original, rewritten):
    lines = [
        "INKLOOM AI — CONTENT REVIEW",
        f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
        f"Brand: {brand_name or 'Not specified'}",
        f"Platform: {platform}",
        f"Heuristic content score: {score}/100",
        "",
        "SCORE BREAKDOWN:",
    ]
    lines += [f"- {name}: {value}/20" for name, value in components.items()]
    lines += ["", "STRENGTHS:"] + [f"- {x}" for x in strengths]
    lines += ["", "SUGGESTIONS:"] + [f"- {x}" for x in improvements]
    lines += ["", "ORIGINAL CONTENT:", original, "", "REWRITTEN CONTENT:", rewritten]
    lines += ["", "Note: Scores are rule-based writing indicators, not predictions of reach, engagement, or business results."]
    return "\n".join(lines)

# ---------------------------- SESSION STATE ----------------------------

if "rewrite_result" not in st.session_state:
    st.session_state.rewrite_result = None
if "history" not in st.session_state:
    st.session_state.history = []
if "last_original" not in st.session_state:
    st.session_state.last_original = ""

# ---------------------------- NAVIGATION ----------------------------

st.markdown("""
<div class="topbar">
  <div class="logo">✦ inkloom<span>AI</span></div>
  <div class="navlinks">HOME　 ·　 ABOUT　 ·　 FEATURES　 ·　 HOW IT WORKS　 ·　 WORKSPACE　 ·　 FAQ</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------- HERO ----------------------------

st.markdown("""
<div class="hero fade">
  <div style="max-width:58%;position:relative;z-index:2">
    <span class="eyebrow">✦ YOUR CREATIVE BRAND STUDIO</span>
    <h1>Your brand.<br>Your voice.<br><span style="color:#7657e8">Every word.</span></h1>
    <p>Turn everyday drafts into thoughtful brand communication. Shape your identity, refine your message and create content that feels unmistakably yours.</p>
    <div style="margin-top:22px">
      <span class="pill">Brand identity</span><span class="pill">Content intelligence</span><span class="pill">Smart rewrite</span>
    </div>
  </div>
  <img class="hero-art" alt="Modern laptop mockup" src="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=1100&q=85">
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="stat"><strong>01</strong><span>Define your brand voice</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat"><strong>02</strong><span>Understand your content</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat"><strong>03</strong><span>Refine your message</span></div>', unsafe_allow_html=True)

# ---------------------------- INTRODUCTION ----------------------------

section_heading(
    "INTRODUCING INKLOOM",
    "Good content deserves a recognisable voice.",
    "Inkloom AI is a brand communication and content enhancement workspace. It brings brand identity, writing checks and content refinement together in one place."
)
intro_left, intro_right = st.columns([1.05, 0.95], gap="large")
with intro_left:
    st.markdown("""
    <div class="card">
      <div class="card-icon">✧</div>
      <h3>Not just another text box.</h3>
      <p>Every brand has its own personality. The words it chooses, the way it speaks and the feeling it leaves with its audience all contribute to its identity.</p>
      <p>Inkloom helps make those choices more intentional by using your brand preferences as the guide for content improvement.</p>
      <p><b>Our idea:</b> make consistent communication easier to plan, review and create.</p>
    </div>
    """, unsafe_allow_html=True)
with intro_right:
    st.image(
        "https://images.unsplash.com/photo-1523726491678-bf852e717f6a?auto=format&fit=crop&w=1000&q=85",
        caption="A creative space for ideas, identity and communication.",
        use_container_width=True,
    )

# ---------------------------- ABOUT ----------------------------

section_heading(
    "ABOUT THE PROJECT",
    "Built around the identity behind the words.",
    "Inkloom AI is designed for creators, small businesses, student founders and teams who want their communication to feel clear and consistent."
)
a1, a2 = st.columns(2, gap="large")
with a1:
    st.markdown("""
    <div class="soft-panel">
      <div class="section-kicker">OUR VISION</div>
      <h2>Make every brand voice matter.</h2>
      <p>We imagine a world where businesses and creators can communicate with clarity and personality, without losing what makes their brand distinct.</p>
    </div>
    """, unsafe_allow_html=True)
with a2:
    st.markdown("""
    <div class="soft-panel">
      <div class="section-kicker">OUR MISSION</div>
      <h2>Make brand-led writing easier.</h2>
      <p>Our mission is to bring brand preferences and practical content-improvement tools into one accessible creative workspace.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
st.image(
    "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1500&q=85",
    caption="Ideas become stronger when a team shares a clear direction.",
    use_container_width=True,
)

# ---------------------------- PROBLEM ----------------------------

section_heading(
    "THE CHALLENGE",
    "A brand is more than a logo.",
    "A recognisable brand voice is built through repeated communication. But keeping that voice consistent can take time and attention."
)
problem_cols = st.columns(3)
problem_cards = [
    ("◉", "Inconsistent tone", "Content can sound different from one post to the next, making a brand feel less recognisable."),
    ("⌁", "Too much rewriting", "Creators and small teams can spend valuable time polishing the same message repeatedly."),
    ("◎", "Platform differences", "A message may need a different structure or length depending on where it will appear."),
]
for col, (icon, title, desc) in zip(problem_cols, problem_cards):
    with col:
        st.markdown(f'<div class="card"><div class="card-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

# ---------------------------- FEATURES ----------------------------

section_heading(
    "THE INKLOOM TOOLKIT",
    "Everything starts with your brand.",
    "Explore the tools that make up the Inkloom workflow. The current prototype includes practical rule-based content checks and rewriting."
)
feature_data = [
    ("✦", "Brand Identity Studio", "Set your brand name, industry, personality, tone, audience and preferred vocabulary."),
    ("✎", "Smart Rewrite", "Generate several wording variations using the selected brand settings and supported rewrite rules."),
    ("◷", "Content Intelligence", "Review clarity, structure, readability, engagement readiness and platform fit."),
    ("✓", "Brand Consistency Check", "Review whether selected brand preferences and avoid-words appear in the draft."),
    ("↗", "Content Suggestions", "Get practical ideas for clearer structure, stronger openings and calls to action."),
    ("▣", "Platform Preview", "View a simple mock-up of how your content could be presented on a selected platform."),
    ("⇄", "Before & After", "Compare the original draft with the selected rewrite."),
    ("▤", "Content History", "Keep a session-based list of recent drafts and rewrites while the app remains open."),
]
for row in range(0, len(feature_data), 4):
    cols = st.columns(4, gap="medium")
    for col, (icon, title, desc) in zip(cols, feature_data[row:row+4]):
        with col:
            st.markdown(f'<div class="card"><div class="card-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

# ---------------------------- HOW IT WORKS ----------------------------

section_heading(
    "A SIMPLE WORKFLOW",
    "From first draft to brand-ready direction.",
    "Four clear steps take you from defining your brand to reviewing an improved version of your content."
)
steps = st.columns(4)
step_data = [
    ("01", "Define", "Tell Inkloom about your brand's personality, audience and preferred tone."),
    ("02", "Add", "Paste your draft and choose its content type, purpose and platform."),
    ("03", "Review", "Check the writing score, suggestions and available rewrite versions."),
    ("04", "Use", "Compare versions, preview the result and copy or download your content."),
]
for col, (number, title, desc) in zip(steps, step_data):
    with col:
        st.markdown(f'<div class="card"><div class="section-kicker">{number}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

# ---------------------------- WORKSPACE ----------------------------

section_heading(
    "YOUR CREATIVE WORKSPACE",
    "Let's make your next message count.",
    "Complete the brand profile, add a draft and explore the content review. You can change your selections and run the rewrite again."
)

with st.container():
    st.markdown("### 01 · Build your brand profile")
    st.caption("These settings guide the prototype's rewrite choices and the explanations shown with your results.")
    b1, b2 = st.columns(2)
    with b1:
        brand_name = st.text_input("Brand name", placeholder="e.g. Bloom Studio")

        industry_choice = st.selectbox(
            "Industry",
            ["Choose an industry", "Fashion & lifestyle", "Technology", "Education", "Food & beverage", "Beauty & wellness", "Retail & e-commerce", "Creative services", "Other"],
        )
        industry_custom = st.text_input("Enter your industry", placeholder="e.g. Healthcare, Sports") if industry_choice == "Other" else ""
        industry = industry_custom.strip() if industry_choice == "Other" and industry_custom.strip() else industry_choice

        personality_options = ["Friendly", "Professional", "Bold", "Minimal", "Playful", "Trustworthy", "Innovative", "Elegant", "Other"]
        personality = st.multiselect("Brand personality", personality_options, default=["Friendly", "Professional"])
        personality_custom = st.text_input("Enter another personality", placeholder="e.g. witty, calm, adventurous") if "Other" in personality else ""
        personality = [item for item in personality if item != "Other"]
        if personality_custom.strip():
            personality.extend([item.strip() for item in personality_custom.split(",") if item.strip()])

        tone_choice = st.selectbox(
            "Preferred communication tone",
            ["Friendly", "Professional", "Creative", "Formal", "Inspirational", "Other"],
            index=0,
        )
        tone_custom = st.text_input("Enter your preferred tone", placeholder="e.g. warm, witty, reassuring") if tone_choice == "Other" else ""
        tone = tone_custom.strip() if tone_choice == "Other" and tone_custom.strip() else tone_choice

    with b2:
        audience = st.text_input("Target audience", placeholder="e.g. young professionals, students")
        brand_description = st.text_area("Describe your brand", placeholder="What do you offer? What makes your brand different?", height=105)
        preferred_words = st.text_input("Words your brand likes (comma-separated)", placeholder="thoughtful, simple, discover")
        avoid_words = st.text_input("Words or phrases to avoid (comma-separated)", placeholder="cheap, guaranteed, hurry up")

    st.markdown("### 02 · Set up your content")
    p1, p2, p3 = st.columns(3)
    with p1:
        platform_choice = st.selectbox("Publishing platform", ["Instagram", "LinkedIn", "Facebook", "Website", "Email", "Blog", "Other"])
        platform_custom = st.text_input("Enter your platform", placeholder="e.g. WhatsApp, Pinterest") if platform_choice == "Other" else ""
        platform = platform_custom.strip() if platform_choice == "Other" and platform_custom.strip() else platform_choice
    with p2:
        content_type_choice = st.selectbox("Content type", ["Social media post", "Advertisement", "Product description", "Announcement", "Email", "Blog introduction", "Other"])
        content_type_custom = st.text_input("Enter your content type", placeholder="e.g. event invitation, press release") if content_type_choice == "Other" else ""
        content_type = content_type_custom.strip() if content_type_choice == "Other" and content_type_custom.strip() else content_type_choice
    with p3:
        purpose_choice = st.selectbox("Content purpose", ["Inform", "Promote", "Educate", "Engage", "Inspire", "Other"])
        purpose_custom = st.text_input("Enter your content purpose", placeholder="e.g. build trust, announce a launch") if purpose_choice == "Other" else ""
        purpose = purpose_custom.strip() if purpose_choice == "Other" and purpose_custom.strip() else purpose_choice

    length_choice_option = st.selectbox(
        "Preferred output length",
        ["Keep close to original", "Short", "Medium", "Detailed", "Other"],
    )
    length_custom = st.text_input("Describe your preferred length", placeholder="e.g. exactly 3 sentences") if length_choice_option == "Other" else ""
    length_choice = length_custom.strip() if length_choice_option == "Other" and length_custom.strip() else length_choice_option
    original_content = st.text_area(
        "Paste your content",
        placeholder="Start with your draft here. It can be a social post, product description, announcement or another short piece of brand communication...",
        height=190,
        key="main_content",
    )
    word_count_live = len(re.findall(r"\b[\w'-]+\b", original_content))
    char_count_live = len(original_content)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Words", word_count_live)
    with m2:
        st.metric("Characters", char_count_live)
    with m3:
        st.metric("Platform", platform)

    st.markdown("<div class='small-note'>Prototype note: the current rewrite engine uses Python-based rules and phrase substitutions. It does not yet understand content like a full generative AI model.</div>", unsafe_allow_html=True)

    run_button = st.button("✦ Analyse & rewrite my content", use_container_width=True, type="primary")

# ---------------------------- ANALYSIS + RESULTS ----------------------------

if run_button:
    if not original_content.strip():
        st.warning("Add some content first, then run the analysis.")
    else:
        try:
            result = rewrite_content(
                original_content,
                personality,
                tone,
                audience or "Not specified",
                platform,
                brand_name=brand_name,
                brand_description=brand_description,
            )
            # Compatibility with the current ai_engine.py return structure.
            if "main" not in result:
                main_text = result.get("rewritten_content", original_content)
                result = {
                    "main": main_text,
                    "friendly": main_text,
                    "professional": main_text,
                    "creative": main_text,
                    "explanations": result.get("explanations", []),
                }

            total, components, strengths, improvements, words, chars = calculate_content_score(
                original_content, platform, content_type
            )

            avoid_list = [x.strip().lower() for x in avoid_words.split(",") if x.strip()]
            preferred_list = [x.strip().lower() for x in preferred_words.split(",") if x.strip()]
            rewritten = result.get("main", original_content)
            avoided_found = [word for word in avoid_list if word in rewritten.lower()]
            preferred_found = [word for word in preferred_list if word in rewritten.lower()]
            consistency_score = max(0, min(100, 100 - len(avoided_found) * 20 + min(10, len(preferred_found) * 5)))
            if not personality:
                consistency_score = max(0, consistency_score - 10)

            suggestions = list(improvements)
            if not re.search(r"\b(try|explore|visit|learn|shop|contact|follow|comment|share|discover)\b", original_content, re.I):
                suggestions.append("Consider a clear call to action that tells the reader what to do next.")
            if original_content.count("!") > 2:
                suggestions.append("Reduce repeated exclamation marks for a more controlled brand voice.")
            if not audience:
                suggestions.append("Define a target audience to make future content decisions more focused.")
            if len(original_content.split()) < 12:
                suggestions.append("Add a little more context so readers understand the value of your message.")

            st.session_state.rewrite_result = {
                "result": result,
                "score": total,
                "components": components,
                "strengths": strengths,
                "improvements": improvements,
                "suggestions": suggestions,
                "consistency": consistency_score,
                "avoided_found": avoided_found,
                "preferred_found": preferred_found,
                "original": original_content,
                "platform": platform,
                "brand": brand_name,
                "content_type": content_type,
                "purpose": purpose,
                "length": length_choice,
                "timestamp": datetime.now().strftime("%H:%M"),
            }
            st.session_state.history.insert(0, {
                "time": datetime.now().strftime("%d %b %H:%M"),
                "brand": brand_name or "Untitled brand",
                "platform": platform,
                "original": original_content,
                "rewritten": rewritten,
                "score": total,
            })
            st.session_state.history = st.session_state.history[:8]
        except Exception as error:
            st.error(f"Something went wrong while running the rewrite: {error}")
            st.info("Check that ai_engine.py is in the same folder and contains rewrite_content().")

if st.session_state.rewrite_result:
    data = st.session_state.rewrite_result
    result = data["result"]
    st.markdown("---")
    section_heading("YOUR CONTENT REPORT", "A clearer view of your draft.", "Review the writing indicators, explore suggestions and choose the version that best fits your message.")

    score_col, detail_col = st.columns([0.8, 1.2], gap="large")
    with score_col:
        st.markdown(f"""
        <div class="dark-panel">
          <div style="color:#d9d0ff;font-weight:800;letter-spacing:.12em;font-size:.75rem">CONTENT INTELLIGENCE</div>
          <div class="score-number" style="color:white;margin-top:14px">{data['score']}<span style="font-size:1.1rem">/100</span></div>
          <p style="margin-top:12px;color:#e1dcf4">A rule-based review of your original draft, not a prediction of likes, reach or conversions.</p>
        </div>
        """, unsafe_allow_html=True)
    with detail_col:
        for name, value in data["components"].items():
            st.markdown(f"**{name}** · {value}/20")
            st.markdown(f"<div class='score-track'><div class='score-fill' style='width:{value*5}%'></div></div>", unsafe_allow_html=True)

    good_col, improve_col = st.columns(2, gap="large")
    with good_col:
        st.markdown("### ✦ What's working")
        for item in data["strengths"]:
            st.success(item)
    with improve_col:
        st.markdown("### ↗ Opportunities")
        for item in data["suggestions"]:
            st.info(item)

    st.markdown("### Brand consistency review")
    bc1, bc2 = st.columns([1, 2])
    with bc1:
        st.metric("Preference alignment", f"{data['consistency']}/100")
    with bc2:
        if data["avoided_found"]:
            st.warning("Avoid-words found in rewrite: " + ", ".join(data["avoided_found"]))
        else:
            st.success("No selected avoid-words were detected in the main rewrite.")
        if data["preferred_found"]:
            st.caption("Preferred words detected: " + ", ".join(data["preferred_found"]))
        else:
            st.caption("No preferred vocabulary was detected. This is a simple word check, not a semantic brand assessment.")

    st.markdown("### ✍️ Choose your rewrite")
    tabs = st.tabs(["Brand aligned", "Friendly", "Professional", "Creative"])
    version_map = [
        ("main", "Brand aligned"),
        ("friendly", "Friendly"),
        ("professional", "Professional"),
        ("creative", "Creative"),
    ]
    selected_rewrite = result.get("main", data["original"])
    for tab, (key, label) in zip(tabs, version_map):
        with tab:
            text_value = result.get(key, result.get("main", data["original"]))
            st.markdown(f"<div class='result-box'>{safe_text(text_value)}</div>", unsafe_allow_html=True)
            st.download_button(
                f"Download {label} version",
                data=text_value,
                file_name=f"inkloom_{key}_rewrite.txt",
                mime="text/plain",
                key=f"download_{key}",
            )
            if key == "main":
                selected_rewrite = text_value

    st.markdown("### ⇄ Before & after")
    before_col, after_col = st.columns(2, gap="large")
    with before_col:
        st.markdown("**Original draft**")
        st.markdown(f"<div class='result-box'>{safe_text(data['original'])}</div>", unsafe_allow_html=True)
    with after_col:
        st.markdown("**Brand-aligned rewrite**")
        st.markdown(f"<div class='result-box'>{safe_text(selected_rewrite)}</div>", unsafe_allow_html=True)

    st.markdown("### Platform preview")
    if data["platform"] == "Instagram":
        st.markdown(f"""
        <div class="preview-instagram">
          <div class="preview-head">✦ {safe_text(data['brand'] or 'Your Brand')}　 ·　 Sponsored / Post</div>
          <img class="preview-image" src="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=900&q=80">
          <div class="preview-caption"><b>{safe_text(data['brand'] or 'yourbrand')}</b><br>{safe_text(selected_rewrite)}</div>
        </div>
        """, unsafe_allow_html=True)
    elif data["platform"] == "LinkedIn":
        st.markdown(f"""
        <div class="card" style="max-width:700px;margin:auto">
          <b>{safe_text(data['brand'] or 'Your Brand')}</b><br><span style="color:#888">Brand update · Preview</span>
          <hr>{safe_text(selected_rewrite)}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card" style="max-width:700px;margin:auto">
          <div class="section-kicker">{safe_text(data['platform'])} PREVIEW</div>
          <h3>{safe_text(data['brand'] or 'Your Brand')}</h3>
          <p>{safe_text(selected_rewrite)}</p>
        </div>
        """, unsafe_allow_html=True)

    report = make_report(
        data["brand"], data["platform"], data["score"], data["components"],
        data["strengths"], data["suggestions"], data["original"], selected_rewrite
    )
    st.download_button(
        "⬇ Download complete content review",
        data=report,
        file_name="inkloom_content_review.txt",
        mime="text/plain",
        use_container_width=True,
    )

# ---------------------------- HISTORY ----------------------------

section_heading(
    "YOUR RECENT WORK",
    "A little trail of your ideas.",
    "Recent rewrites are kept in this browser session while the app remains open. They are not saved to a permanent account or database."
)
if st.session_state.history:
    for item in st.session_state.history:
        with st.expander(f"{item['time']} · {item['brand']} · {item['platform']} · Score {item['score']}/100"):
            st.markdown("**Original**")
            st.write(item["original"])
            st.markdown("**Rewrite**")
            st.write(item["rewritten"])
else:
    st.markdown('<div class="card"><h3>Your recent work will appear here.</h3><p>Run your first content review in the workspace above to start your session history.</p></div>', unsafe_allow_html=True)

# ---------------------------- INSPIRATION ----------------------------

section_heading(
    "THE CREATIVE CORNER",
    "A little inspiration for your next big idea.",
    "A visual moodboard celebrating creative work, thoughtful branding and the people behind great communication."
)
img1, img2, img3 = st.columns(3, gap="medium")
with img1:
    st.image("https://images.unsplash.com/photo-1558655146-9f40138edfeb?auto=format&fit=crop&w=900&q=85", caption="Visual identity & design", use_container_width=True)
with img2:
    st.image("https://images.unsplash.com/photo-1545235617-9465d2a55698?auto=format&fit=crop&w=900&q=85", caption="Creative digital spaces", use_container_width=True)
with img3:
    st.image("https://images.unsplash.com/photo-1559028012-481c04fa702d?auto=format&fit=crop&w=900&q=85", caption="Ideas into experiences", use_container_width=True)

# ---------------------------- FAQ ----------------------------

section_heading(
    "GOOD TO KNOW",
    "Frequently asked questions.",
    "A few quick answers about the current Inkloom AI prototype."
)
faq_items = [
    ("What is Inkloom AI?", "Inkloom AI is a brand communication and content enhancement prototype. It helps users define brand preferences, review drafts and explore rewritten versions."),
    ("Does it use a generative AI model right now?", "The current prototype uses Python-based rules and phrase substitutions. It is not connected to a generative AI model yet."),
    ("Are the content scores engagement predictions?", "No. Scores are transparent, rule-based indicators of writing characteristics. They do not predict views, likes, reach or sales."),
    ("Which platforms can I preview?", "The prototype includes simple preview layouts for Instagram, LinkedIn and a general layout for other selected platforms."),
    ("Is my content permanently saved?", "No. The recent-work list is stored only in the active Streamlit session. It is not a permanent account or database."),
    ("Can I download my results?", "Yes. You can download individual rewrite versions and a plain-text content review report."),
]
for question, answer in faq_items:
    with st.expander(question):
        st.write(answer)

# ---------------------------- ABOUT / FOOTER ----------------------------

st.markdown("""
<div class="dark-panel" style="margin-top:48px">
  <div class="section-kicker" style="color:#d6caff">THE INKLOOM PROMISE</div>
  <h2 style="font-size:2.2rem;margin-top:10px">Make your message feel like you.</h2>
  <p style="max-width:720px">Start with your brand identity. Build a message with intention. Keep your voice recognisable wherever your ideas go.</p>
</div>
<div class="footer">
  <strong>✦ inkloomAI</strong>
  <p>Brand communication and content enhancement studio.</p>
  <p>Home　·　About　·　Features　·　Workspace　·　FAQ</p>
  <hr style="border-color:#51486a">
  <p>© 2026 Inkloom AI · Prototype edition<br>
  Built to explore more consistent, thoughtful brand communication.</p>
</div>
""", unsafe_allow_html=True)

st.caption("Prototype transparency: some features use simple heuristics and formatting rules. Online photographs are loaded from Unsplash and require an internet connection.")
