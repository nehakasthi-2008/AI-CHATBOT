import streamlit as st
import ollama

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    initial_sidebar_state="expanded",
)

# ---------- PASTE YOUR AI IMAGE LINKS HERE (optional) ----------
# Must be direct image links ending in .jpg / .png / .webp
IMAGES = [
    # "https://your-site.com/ai-image-1.jpg",
    # "https://your-site.com/ai-image-2.jpg",
    # "https://your-site.com/ai-image-3.jpg",
]
SECONDS_PER_IMAGE = 6

# ---------- BUILD SLIDESHOW CSS ----------
n = len(IMAGES)
total = max(n, 1) * SECONDS_PER_IMAGE
slot = 100 / max(n, 1)

layer_css = ""
layer_html = ""
for i, url in enumerate(IMAGES):
    layer_css += (
        f".bg{i} {{ background-image: url('{url}'); "
        f"animation-delay: {i * SECONDS_PER_IMAGE}s; }}\n"
    )
    layer_html += f'<div class="bg-layer bg{i}"></div>'

slideshow_css = f"""
.bg-layer {{
    animation: fade {total}s infinite, zoom {total}s infinite;
}}
@keyframes fade {{
    0%   {{ opacity: 0; }}
    {slot * 0.2:.2f}% {{ opacity: 1; }}
    {slot:.2f}% {{ opacity: 1; }}
    {slot * 1.3:.2f}% {{ opacity: 0; }}
    100% {{ opacity: 0; }}
}}
@keyframes zoom {{
    0%   {{ transform: scale(1); }}
    {slot * 1.3:.2f}% {{ transform: scale(1.15); }}
    100% {{ transform: scale(1.15); }}
}}
{layer_css}
"""

# ---------- MAIN CSS ----------
main_css = """
/* Animated moving blue gradient */
.stApp {
    background: linear-gradient(-45deg, #0d47a1, #1976d2, #42a5f5, #0a2472);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
    color: white;
}
@keyframes gradientMove {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Transparent containers so the background shows */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Optional image slideshow layers */
.bg-layer {
    position: fixed;
    inset: 0;
    z-index: -1;
    background-size: cover;
    background-position: center;
    opacity: 0;
    pointer-events: none;
}
.bg-overlay {
    position: fixed;
    inset: 0;
    z-index: -1;
    background: linear-gradient(160deg, rgba(13,71,161,0.55), rgba(25,118,210,0.35));
    pointer-events: none;
}

/* Rising glowing bubbles */
.bubble {
    position: fixed;
    bottom: -120px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.7), rgba(255,255,255,0.08));
    box-shadow: 0 0 20px rgba(255,255,255,0.4);
    pointer-events: none;
    z-index: 0;
    animation: rise linear infinite;
}
.b1 { left: 5%;  width: 40px; height: 40px; animation-duration: 12s; }
.b2 { left: 20%; width: 70px; height: 70px; animation-duration: 18s; animation-delay: 2s; }
.b3 { left: 38%; width: 30px; height: 30px; animation-duration: 10s; animation-delay: 4s; }
.b4 { left: 55%; width: 90px; height: 90px; animation-duration: 22s; animation-delay: 1s; }
.b5 { left: 72%; width: 50px; height: 50px; animation-duration: 14s; animation-delay: 3s; }
.b6 { left: 88%; width: 35px; height: 35px; animation-duration: 11s; animation-delay: 5s; }
@keyframes rise {
    0%   { transform: translateY(0) scale(1); opacity: 0; }
    10%  { opacity: 1; }
    100% { transform: translateY(-115vh) scale(1.3); opacity: 0; }
}

/* White text */
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label {
    color: white !important;
}
h1 {
    text-align: center;
    font-weight: 800;
    letter-spacing: 2px;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
}

/* Sidebar (history panel) */
[data-testid="stSidebar"] {
    background: rgba(8, 30, 90, 0.85) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    z-index: 100;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    text-align: left;
    font-size: 1.3rem;
    letter-spacing: 0;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    justify-content: flex-start;
    background: rgba(255, 255, 255, 0.12);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 0.5rem 0.8rem;
    margin-bottom: 4px;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateX(4px);
}
[data-testid="stSidebar"] input {
    color: white !important;
    background: rgba(255, 255, 255, 0.12) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 10px;
}
[data-testid="stSidebar"] input::placeholder {
    color: #cfe3ff !important;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
}

/* Chat input */
[data-testid="stBottom"] > div {
    background: transparent;
}
[data-testid="stChatInput"] {
    background: #0b3a82;
    border: 2px solid white;
    border-radius: 25px;
}
[data-testid="stChatInput"] textarea {
    color: white !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #cfe3ff !important;
}

/* Floating stickers */
.sticker {
    position: fixed;
    font-size: 45px;
    opacity: 0.9;
    pointer-events: none;
    z-index: 1;
    animation: float 4s ease-in-out infinite;
}
.s1 { top: 12%; left: 3%; }
.s2 { top: 25%; right: 4%; animation-delay: 1s; }
.s3 { top: 55%; left: 2%; animation-delay: 2s; }
.s4 { top: 70%; right: 3%; animation-delay: 0.5s; }
.s5 { top: 88%; left: 8%; animation-delay: 1.5s; }
.s6 { top: 8%; right: 12%; animation-delay: 2.5s; }
@keyframes float {
    0%, 100% { transform: translateY(0) rotate(-5deg); }
    50% { transform: translateY(-15px) rotate(5deg); }
}
"""

# ---------- HTML ELEMENTS (bubbles + stickers) ----------
html_elements = """
<div class="bubble b1"></div>
<div class="bubble b2"></div>
<div class="bubble b3"></div>
<div class="bubble b4"></div>
<div class="bubble b5"></div>
<div class="bubble b6"></div>
<div class="sticker s1">🤖</div>
<div class="sticker s2">⭐</div>
<div class="sticker s3">🚀</div>
<div class="sticker s4">💬</div>
<div class="sticker s5">😎</div>
<div class="sticker s6">✨</div>
"""

full_html = (
    f"<style>{main_css}{slideshow_css}</style>"
    f"{layer_html}<div class='bg-overlay'></div>"
    f"{html_elements}"
)

# Remove indentation and blank lines so Streamlit doesn't treat it as a code block
full_html = "\n".join(line.strip() for line in full_html.splitlines() if line.strip())

st.markdown(full_html, unsafe_allow_html=True)

# ---------- SESSION STATE (chat history) ----------
if "chats" not in st.session_state:
    st.session_state.chats = [{"title": "New chat", "messages": []}]
    st.session_state.current = 0

chats = st.session_state.chats

# ---------- SIDEBAR: SEARCH HISTORY ----------
with st.sidebar:
    st.header("🕘 Chat History")

    if st.button("➕ New chat"):
        # Only create a new chat if the current one is not already empty
        if chats[st.session_state.current]["messages"]:
            chats.append({"title": "New chat", "messages": []})
            st.session_state.current = len(chats) - 1
        st.rerun()

    query = st.text_input("Search history", placeholder="🔍 Search your chats...")

    st.divider()

    shown = 0
    for idx in reversed(range(len(chats))):
        chat = chats[idx]
        if not chat["messages"]:
            continue

        # Search in the title and in every message
        if query:
            text = chat["title"] + " " + " ".join(m["content"] for m in chat["messages"])
            if query.lower() not in text.lower():
                continue

        marker = "▶ " if idx == st.session_state.current else "💬 "
        if st.button(marker + chat["title"], key=f"chat_{idx}"):
            st.session_state.current = idx
            st.rerun()
        shown += 1

    if shown == 0:
        st.caption("No chats found yet ✨")

    st.divider()

    if st.button("🗑️ Delete all history"):
        st.session_state.chats = [{"title": "New chat", "messages": []}]
        st.session_state.current = 0
        st.rerun()

# ---------- CHATBOT ----------
st.title("🤖 AI CHATBOT 💬")
st.caption("Powered by Llama 3.2 ✨")

current_chat = chats[st.session_state.current]
messages = current_chat["messages"]

for message in messages:
    avatar = "😎" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

user_input = st.chat_input("Type your message here... 😊")

if user_input:
    # Use the first message as the chat title
    if not messages:
        current_chat["title"] = user_input[:28] + ("..." if len(user_input) > 28 else "")

    messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="😎"):
        st.write(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking... 🤔"):
            response = ollama.chat(
                model="llama3.2",
                messages=messages,
            )
            ai_message = response["message"]["content"]
            st.write(ai_message)

    messages.append({"role": "assistant", "content": ai_message})
    st.rerun()  # refresh so the new chat appears in the sidebar immediately