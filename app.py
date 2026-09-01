import streamlit as st
import os
import base64
from google import genai
from PIL import Image


# =========================================================
# GEMINI SETUP
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found.")
    st.stop()

client = genai.Client(api_key=api_key)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MemoryLens AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "ai_result" not in st.session_state:
    st.session_state.ai_result = ""

if "current_memory" not in st.session_state:
    st.session_state.current_memory = None

if "memories" not in st.session_state:
    st.session_state.memories = []

if "actions" not in st.session_state:
    st.session_state.actions = []


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.hero {
    padding: 28px 32px;
    border-radius: 18px;
    background: linear-gradient(135deg, #eef2ff, #fdf4ff);
    border: 1px solid #e5e7eb;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 17px;
    color: #64748b;
}

.memory-card {
    padding: 20px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.small-label {
    color: #64748b;
    font-size: 13px;
}

.big-number {
    font-size: 28px;
    font-weight: 700;
}

.tag {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    background: #eef2ff;
    font-size: 13px;
    margin-top: 8px;
    margin-right: 5px;
}

.ai-box {
    padding: 22px;
    border-radius: 16px;
    background: #f8f7ff;
    border: 1px solid #ddd6fe;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🧠 MemoryLens")

    st.caption("Your AI-powered memory layer")

    st.divider()

    if st.button("🏠  Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.button("📸  Capture", use_container_width=True):
        st.session_state.page = "Capture"

    if st.button("🔎  Memories", use_container_width=True):
        st.session_state.page = "Memories"

    if st.button("⏰  Actions", use_container_width=True):
        st.session_state.page = "Actions"

    st.divider()

    st.caption("AI Memory System")
    st.caption("Capture → Understand → Remember → Act")


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">Good afternoon 👋</div>
        <div class="hero-subtitle">
            Turn the information you capture into memories you can actually use.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your Memory Overview")

    total_memories = 12 + len(st.session_state.memories)
    total_actions = 5 + len(st.session_state.actions)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="memory-card">
            <div class="small-label">Total Memories</div>
            <div class="big-number">{total_memories}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="memory-card">
            <div class="small-label">Upcoming</div>
            <div class="big-number">{len(st.session_state.actions)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="memory-card">
            <div class="small-label">Actions</div>
            <div class="big-number">{total_actions}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="memory-card">
            <div class="small-label">Organized</div>
            <div class="big-number">92%</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Recent Memories")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="memory-card">
            <h4>📢 Pune City Battle</h4>
            <p>Hackathon registration notice</p>
            <span class="tag">Deadline: Sept 1</span>
            <span class="tag">Intent: Register</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="memory-card">
            <h4>📄 DBMS Project</h4>
            <p>College project submission information</p>
            <span class="tag">Deadline: Sept 5</span>
            <span class="tag">Intent: Prepare</span>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.memories:

        st.subheader("Recently Captured")

        for memory in reversed(st.session_state.memories[-3:]):

            with st.container(border=True):

                st.subheader(f"🧠 {memory['title']}")

                st.write(memory["type"])

                st.write(
                    f"📅 **Important Date:** {memory['date']}"
                )

                st.write(
                    f"🎯 **Intent:** {memory['intent']}"
                )

                st.write(
                    f"⚡ **Priority:** {memory['priority']}"
                )


# =========================================================
# CAPTURE
# =========================================================

elif st.session_state.page == "Capture":

    st.title("📸 Capture a New Memory")

    st.write(
        "Capture anything from the real world that you may need to remember later."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload a photo",
        type=["png", "jpg", "jpeg"],
        help="Upload a notice, document, whiteboard, receipt or other information."
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Captured information",
            width=600
        )

        st.write("")

        if st.button(
            "🤖 Analyze with MemoryLens",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "🧠 MemoryLens is understanding your capture..."
            ):

                try:

                    # Get image data
                    image_bytes = uploaded_file.getvalue()

                    image_base64 = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    mime_type = uploaded_file.type

                    # Prompt for Gemini
                    prompt = """
You are MemoryLens, an AI personal memory assistant.

Analyze the uploaded image and extract useful information.

Return the result in exactly this format:

TITLE:
TYPE:
IMPORTANT DATE:
INTENT:
PRIORITY:
SUGGESTED ACTION:
WHY IT MATTERS:

Keep each answer short and useful.

INTENT should be one of:
Register, Prepare, Review, Buy, Pay, Attend, Submit, Follow-up, Other

PRIORITY should be:
High, Medium, or Low

If a field is not present in the image, write:
Not detected
"""

                    # Gemini Interactions API
                    interaction = client.interactions.create(
                        model="gemini-3.6-flash",
                        input=[
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "data": image_base64,
                                "mime_type": mime_type
                            }
                        ]
                    )

                    result = interaction.output_text

                    # -------------------------------------------------
                    # PARSE GEMINI RESPONSE
                    # -------------------------------------------------

                    data = {
                        "title": "AI Captured Memory",
                        "type": "Captured Information",
                        "date": "Not detected",
                        "intent": "Other",
                        "priority": "Medium",
                        "action": "Review captured information",
                        "why": "Information extracted from uploaded image.",
                        "raw": result
                    }

                    current_field = None

                    for line in result.splitlines():

                        line = line.strip()

                        if line.startswith("TITLE:"):

                            data["title"] = line.replace(
                                "TITLE:", ""
                            ).strip()

                            current_field = "title"

                        elif line.startswith("TYPE:"):

                            data["type"] = line.replace(
                                "TYPE:", ""
                            ).strip()

                            current_field = "type"

                        elif line.startswith("IMPORTANT DATE:"):

                            data["date"] = line.replace(
                                "IMPORTANT DATE:", ""
                            ).strip()

                            current_field = "date"

                        elif line.startswith("INTENT:"):

                            data["intent"] = line.replace(
                                "INTENT:", ""
                            ).strip()

                            current_field = "intent"

                        elif line.startswith("PRIORITY:"):

                            data["priority"] = line.replace(
                                "PRIORITY:", ""
                            ).strip()

                            current_field = "priority"

                        elif line.startswith("SUGGESTED ACTION:"):

                            data["action"] = line.replace(
                                "SUGGESTED ACTION:", ""
                            ).strip()

                            current_field = "action"

                        elif line.startswith("WHY IT MATTERS:"):

                            data["why"] = line.replace(
                                "WHY IT MATTERS:", ""
                            ).strip()

                            current_field = "why"

                        elif line and current_field:

                            data[current_field] += " " + line

                    # Save AI result
                    st.session_state.ai_result = result

                    st.session_state.current_memory = data

                    st.session_state.analyzed = True

                except Exception as e:

                    st.error(
                        "Something went wrong while analyzing the image."
                    )

                    st.code(str(e))


    # =====================================================
    # DISPLAY AI RESULT
    # =====================================================

    if st.session_state.analyzed:

        st.markdown("""
        <div class="ai-box">
            <h3>🧠 MemoryLens understood your capture</h3>
            <p>
            AI extracted important information and identified
            what action may be required.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.subheader("📋 AI Analysis")

        st.text(st.session_state.ai_result)

        st.divider()

        memory = st.session_state.current_memory

        if memory:

            st.subheader("✨ Extracted Information")

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Title:** {memory['title']}"
                )

                st.write(
                    f"**Type:** {memory['type']}"
                )

                st.write(
                    f"**Important Date:** {memory['date']}"
                )

                st.write(
                    f"**Intent:** {memory['intent']}"
                )

            with col2:

                st.write(
                    f"**Priority:** {memory['priority']}"
                )

                st.write(
                    f"**Suggested Action:** {memory['action']}"
                )

                st.write(
                    f"**Why it matters:** {memory['why']}"
                )

            st.divider()

            st.subheader("What should MemoryLens do?")

            b1, b2 = st.columns(2)

            with b1:

                if st.button(
                    "⏰ Create Reminder",
                    type="primary",
                    use_container_width=True
                ):

                    action = {
                        "title": memory["action"],
                        "date": memory["date"],
                        "intent": memory["intent"],
                        "priority": memory["priority"]
                    }

                    if action not in st.session_state.actions:

                        st.session_state.actions.append(action)

                    if memory not in st.session_state.memories:

                        st.session_state.memories.append(memory)

                    st.success(
                        "✅ Reminder created and memory saved!"
                    )

            with b2:

                if st.button(
                    "💾 Save Memory",
                    use_container_width=True
                ):

                    if memory not in st.session_state.memories:

                        st.session_state.memories.append(memory)

                    st.success(
                        "💾 Memory saved successfully!"
                    )


# =========================================================
# MEMORIES
# =========================================================

elif st.session_state.page == "Memories":

    st.title("🔎 Your Memories")

    st.write(
        "Search information captured from the real world."
    )

    search = st.text_input(
        "Search your memories",
        placeholder="Try: hackathon, deadline, project..."
    )

    st.divider()

    if not st.session_state.memories:

        st.info(
            "No new memories saved yet. Capture an image and save it."
        )

    else:

        if search:

            search_lower = search.lower()

            results = [
                memory
                for memory in st.session_state.memories
                if search_lower in str(memory).lower()
            ]

        else:

            results = st.session_state.memories

        if not results:

            st.warning(
                f"No memories found for: {search}"
            )

        else:

            st.success(
                f"Found {len(results)} memory/memories."
            )

            for memory in reversed(results):

                with st.container(border=True):

                    st.subheader(
                        f"🧠 {memory['title']}"
                    )

                    st.write(
                        memory["type"]
                    )

                    st.write(
                        f"📅 **Important Date:** {memory['date']}"
                    )

                    st.write(
                        f"🎯 **Intent:** {memory['intent']}"
                    )

                    st.write(
                        f"⚡ **Priority:** {memory['priority']}"
                    )

                    st.write(
                        f"✅ **Suggested Action:** {memory['action']}"
                    )

                    st.write(
                        f"💡 **Why it matters:** {memory['why']}"
                    )

                    st.caption(
                        "MemoryLens AI"
                    )


# =========================================================
# ACTIONS
# =========================================================

elif st.session_state.page == "Actions":

    st.title("⏰ Upcoming Actions")

    st.write(
        "Things MemoryLens identified as requiring your attention."
    )

    st.divider()

    # -----------------------------------------------------
    # Existing demo actions
    # -----------------------------------------------------

    st.error("""
🔴 **Register for Pune City Battle**

Deadline: September 1, 2026 — 11:59 PM

Intent: Register
""")

    st.warning("""
🟠 **Prepare DBMS Project**

Deadline: September 5, 2026

Intent: Prepare
""")

    st.info("""
🔵 **Review Machine Learning Notes**

Deadline: September 8, 2026

Intent: Review
""")

    # -----------------------------------------------------
    # AI CREATED ACTIONS
    # -----------------------------------------------------

    if st.session_state.actions:

        st.subheader("✨ Actions created by MemoryLens")

        for action in reversed(
            st.session_state.actions
        ):

            priority = action["priority"].lower()

            if priority == "high":

                st.error(
                    f"""
🔴 **{action["title"]}**

Deadline: {action["date"]}

Intent: {action["intent"]}

Priority: {action["priority"]}
"""
                )

            elif priority == "medium":

                st.warning(
                    f"""
🟠 **{action["title"]}**

Deadline: {action["date"]}

Intent: {action["intent"]}

Priority: {action["priority"]}
"""
                )

            else:

                st.info(
                    f"""
🔵 **{action["title"]}**

Deadline: {action["date"]}

Intent: {action["intent"]}

Priority: {action["priority"]}
"""
                )