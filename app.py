import streamlit as st
from nlp_engine import CollegeFAQEngine

# Page configuration
st.set_page_config(
    page_title="College FAQ Chatbot - NLP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .badge-cat {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-conf {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .suggestion-btn {
        margin: 4px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    return CollegeFAQEngine()

engine = load_engine()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 I am your **College FAQ Chatbot**. You can ask me questions about Examinations, Fees, Timetables, Placements, Hostels, Events, or Student Services.",
            "category": "General",
            "confidence": None,
            "suggestions": []
        }
    ]

# Sidebar
st.sidebar.image("https://img.icons8.com/illustrations/100/graduation-cap.png", width=70)
st.sidebar.title("Campus FAQ Hub")
st.sidebar.markdown("---")

# Topic Filter
selected_category = st.sidebar.selectbox(
    "📌 Filter FAQ Category",
    options=engine.categories,
    index=0
)

# Sample Questions
st.sidebar.markdown("### 💡 Sample Questions")
sample_questions = [
    "What are the library timings?",
    "How can I apply for a bonafide certificate?",
    "When are the semester exams?",
    "How to pay tuition fees online?",
    "What is the hostel fee structure?",
    "When do campus placements start?",
    "What is the minimum attendance required?"
]

selected_sample = None
for q in sample_questions:
    if st.sidebar.button(q, key=f"btn_{q}"):
        selected_sample = q

# Controls
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat Conversation", use_container_width=True):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Chat history cleared! How can I assist you today?",
            "category": "General",
            "confidence": None,
            "suggestions": []
        }
    ]
    st.rerun()

# Main Container
tab_chat, tab_kb = st.tabs(["💬 Interactive Chatbot", "📚 FAQ Knowledge Base"])

with tab_chat:
    st.markdown("<div class='main-title'>🎓 College FAQ Chatbot</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Powered by Natural Language Processing (TF-IDF & Cosine Similarity)</div>", unsafe_allow_html=True)

    # Render Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("category") and message.get("confidence") is not None:
                st.markdown(
                    f"<span class='badge-cat'>📁 {message['category']}</span> "
                    f"<span class='badge-conf'>🎯 Confidence: {message['confidence']}%</span>",
                    unsafe_allow_html=True
                )
            if message.get("suggestions"):
                st.markdown("**Suggested Related Questions:**")
                cols = st.columns(len(message["suggestions"]))
                for idx, sug in enumerate(message["suggestions"]):
                    if cols[idx].button(f"🔍 {sug}", key=f"sug_{hash(sug)}_{idx}"):
                        st.session_state["pending_input"] = sug
                        st.rerun()

    # Process user input from text box or sidebar button
    user_input = st.chat_input("Ask a question (e.g. 'What are the library timings?')...")
    
    if "pending_input" in st.session_state:
        user_input = st.session_state.pop("pending_input")
    elif selected_sample:
        user_input = selected_sample

    if user_input:
        # Append User Message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # Process with NLP Engine
        res = engine.get_answer(user_input, category_filter=selected_category)

        # Append Assistant Response
        st.session_state.messages.append({
            "role": "assistant",
            "content": res["answer"],
            "category": res["category"],
            "confidence": res["confidence"],
            "suggestions": res.get("suggestions", [])
        })

        st.rerun()

with tab_kb:
    st.header("📚 Complete College FAQ Knowledge Base")
    st.markdown("Browse frequently asked questions categorized across college departments.")
    
    filter_kb = st.selectbox("Select Department / Topic", options=engine.categories, key="kb_filter")
    
    search_term = st.text_input("🔍 Search Knowledge Base", "")

    count = 0
    for item in engine.faq_list:
        if filter_kb != "All Categories" and item["category"] != filter_kb:
            continue
        
        if search_term:
            in_q = search_term.lower() in item["question"].lower()
            in_a = search_term.lower() in item["answer"].lower()
            if not (in_q or in_a):
                continue

        count += 1
        with st.expander(f"**Q{item['id']}. {item['question']}** [{item['category']}]"):
            st.markdown(f"**Answer:** {item['answer']}")
            if item.get("variations"):
                st.markdown(f"*Alternative Question Phrases:* {', '.join(item['variations'])}")
    
    if count == 0:
        st.info("No FAQ entries match your search filter.")
