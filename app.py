# 📜 Ancient Epics Story Generator with Mystical Vibes
# Full Streamlit App: Generates AI-based stories, illustrations, and PDFs

import streamlit as st
import requests
import os
import base64
import random
from fpdf import FPDF

# === OPENROUTER API KEY ===
OPENROUTER_API_KEY = "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"  # Replace with your actual key

# === PAGE SETUP ===
st.set_page_config(page_title="Ancient Epics AI", page_icon="🪷", layout="wide")

# === CUSTOM STYLING ===
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1a002b, #2e005a, #3f0068);
        color: #f5f5f5 !important;
    }
    .block-container {
        background-color: rgba(0,0,0,0.7);
        padding: 2rem;
        border-radius: 1rem;
        color: #f5f5f5 !important;
    }
    .stSelectbox div[data-baseweb="select"],
    .stRadio div[data-baseweb="radio"],
    .stTextInput > div > input,
    .stRadio label,
    .stTextInput label,
    .stSelectbox label,
    .stRadio > div > label {
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2c2c54;
    }
    .stButton > button {
        background-color: #9b59b6;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# === BACKGROUND IMAGE BASED ON EPIC ===
def set_background(epic):
    image_file = "bg.ramayana.png" if epic == "Ramayana" else "bg.mahabharata.png"
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            bg_data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_data}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)

# === UI ===
st.title("🪷 Ancient Epics: AI Story Generator")
epic = st.radio("Choose Epic", ["Ramayana", "Mahabharata"], horizontal=True)
set_background(epic)

characters = {
    "Ramayana": ["Rama", "Sita", "Hanuman", "Ravana", "Kaikeyi", "Lakshmana", "Vali", "Sugriva"],
    "Mahabharata": ["Karna", "Krishna", "Draupadi", "Bhishma", "Arjuna", "Abhimanyu", "Yudhishthira", "Shakuni"]
}[epic]

what_ifs = {
    "Ramayana": [
        "What if Sita had never been kidnapped?",
        "What if Hanuman forgot his powers?",
        "What if Ravana chose peace?",
        "What if Rama allied with Ravana?",
        "What if Kaikeyi had no boons?",
        "What if Lakshmana ruled Ayodhya?",
        "What if Vali lived longer?",
        "What if Hanuman ruled Lanka?"
    ],
    "Mahabharata": [
        "What if Karna chose Krishna?",
        "What if Draupadi ruled the kingdom?",
        "What if Bhishma broke his vow?",
        "What if Arjuna refused to fight?",
        "What if Duryodhana was kind?",
        "What if Abhimanyu survived?",
        "What if Yudhishthira lost his memory?",
        "What if Shakuni turned good?"
    ]
}[epic]

themes = ["Divine Encounter", "Time Travel", "Secret Love", "Reincarnation", "Battle Strategy"]
styles = ["Poetic", "Serious", "Philosophical", "Humorous", "Action-packed"]

col1, col2 = st.columns(2)
with col1:
    character = st.selectbox("Choose Character", characters)
with col2:
    theme = st.selectbox("Select a Story Theme", themes)

col3, col4 = st.columns([3, 1])
with col3:
    user_prompt = st.text_input("🪄 What-if Prompt", random.choice(what_ifs))
with col4:
    if st.button("🎲 Roll Dice"):
        user_prompt = random.choice(what_ifs)
        st.session_state["user_prompt"] = user_prompt

style = st.radio("Narration Style", styles)

# === GENERATE ===
if st.button("📖 Generate Story"):
    full_prompt = f"""
    You are a master storyteller of Indian epics. Write a {style.lower()} tale featuring {character} from {epic}.
    Theme: {theme}. Scenario: {user_prompt}
    Include emotion, morals, and ancient cultural tone.
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openrouter.ai",
        "X-Title": "Ancient Epics AI"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are an epic Indian mythological storyteller."},
            {"role": "user", "content": full_prompt}
        ]
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if res.status_code == 200:
        story = res.json()["choices"][0]["message"]["content"]

        st.markdown("## 📜 Your Generated Scroll")
        st.markdown(f"""
        <div style='background-color: rgba(0,0,0,0.5); padding: 25px; border-radius: 15px;
                    color: #dddddd; font-family: Georgia; font-size: 18px; line-height: 1.8;'>
        {story}
        </div>
        """, unsafe_allow_html=True)

        # === IMAGE GENERATION ===
        with st.spinner("🖼 Generating sacred art..."):
            img_prompt = f"{character} from {epic} in {style.lower()} epic scene, illustrated ancient Indian art"
            img_data = {
                "model": "stability/stable-diffusion-xl",
                "prompt": img_prompt
            }
            img_res = requests.post("https://openrouter.ai/api/v1/images/generate", headers=headers, json=img_data)
            if img_res.status_code == 200:
                img_url = img_res.json().get("data", [{}])[0].get("url")
                if img_url:
                    st.image(img_url, caption="✨ Divine Visualization", use_column_width=True)

        # === DOWNLOAD PDF ===
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, story)
        pdf_path = "story.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Epic_Story.pdf">📥 Download Scroll (PDF)</a>'
            st.markdown(href, unsafe_allow_html=True)

        # === CONTINUE STORY OPTION ===
        if st.button("🔮 Continue the Tale"):
            continue_prompt = f"Continue the following epic story with the same tone and characters:\n\n{story}"
            data["messages"].append({"role": "user", "content": continue_prompt})
            cont_res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            if cont_res.status_code == 200:
                continuation = cont_res.json()["choices"][0]["message"]["content"]
                st.markdown("### 🔗 Continued Story")
                st.markdown(f"""
                <div style='background-color: rgba(0,0,0,0.3); padding: 20px; border-radius: 12px;
                            color: #eeeeee; font-family: Georgia; font-size: 17px;'>
                {continuation}
                </div>
                """, unsafe_allow_html=True)

    else:
        st.error(f"❌ Could not generate story: {res.status_code} - {res.text}")
