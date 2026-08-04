import streamlit as st
import os
import sys
import requests
import re
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="Digital Munshi AI - Pakistan Legal Tech",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Append services paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

# Import Local Services (with safety checks)
@st.cache_resource
def load_ml_services():
    classifier = None
    retriever = None
    
    try:
        from classifier import QueryClassifier
        classifier = QueryClassifier()
    except Exception as e:
        st.sidebar.warning(f"⚠️ Classifier could not be loaded: {str(e)[:50]}")
        
    try:
        from retriever import DocumentRetriever
        retriever = DocumentRetriever()
    except Exception as e:
        st.sidebar.warning(f"⚠️ Retriever/FAISS could not be loaded: {str(e)[:50]}")
        
    return classifier, retriever

classifier, retriever = load_ml_services()

# Config Groq API
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')

# Custom CSS for Premium Design
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1A2530;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px;
        color: #B89047;
        text-align: center;
        margin-bottom: 25px;
        font-style: italic;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        color: #1A2530;
    }
    .chat-box {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
    }
    .bot-message {
        background-color: #F9F9F9;
        border-left: 5px solid #B89047;
    }
</style>
""", unsafe_allow_html=True)

# App Layout
st.markdown("<div class='main-title'>⚖️ Digital Munshi AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Bilingual Legal Assistant for the Citizens of Pakistan</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<div class='sidebar-title'>Navigation</div>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Choose a module:",
    ["💬 AI Legal Chat", "✍️ Legal Draft Generator", "📄 Document Analysis & OCR"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ System Status")
st.sidebar.text(f"Groq API: {'🟢 Connected' if GROQ_API_KEY else '🔴 Missing Key'}")
st.sidebar.text(f"Local Classifier: {'🟢 Ready' if classifier else '🔴 Offline'}")
st.sidebar.text(f"Local FAISS Index: {'🟢 Loaded' if retriever else '🔴 Offline'}")

# =========================================================
# Groq Helper Function
# =========================================================
def call_groq(prompt, system_instruction="You are a legal assistant."):
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY is missing from the environment config."
        
    try:
        resp = requests.post(
            GROQ_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.3
            },
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: API returned status code {resp.status_code} - {resp.text}"
    except Exception as e:
        return f"Error connecting to API: {str(e)}"

# =========================================================
# MODULE 1: AI Legal Chat
# =========================================================
if page == "💬 AI Legal Chat":
    st.header("💬 AI Legal Chat Q&A")
    st.write("Type your legal question in Urdu, Roman Urdu, or English to receive plain-language explanations with Pakistani statutory references.")
    
    # Session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    # Input area
    user_question = st.text_input("Enter your question:", key="question_input", placeholder="e.g., How can I get bail in a cheque bounce case?")
    
    if st.button("Submit Question", type="primary") and user_question.strip():
        with st.spinner("Analyzing query and searching Pakistani statutes..."):
            # 1. Classify Category
            category = "General Law"
            confidence = 0.5
            if classifier:
                try:
                    res = classifier.classify(user_question)
                    category = res.get('category', 'General')
                    confidence = res.get('confidence', 0.5)
                except:
                    pass
            
            # 2. Retrieve FAISS context
            doc_context = "No direct document links found."
            if retriever:
                try:
                    docs = retriever.retrieve(user_question, top_k=3)
                    if docs:
                        doc_context = "\n\n".join([
                            f"Title: {d.get('title','N/A')}\nSection: {d.get('section','N/A')}\nContent: {d.get('content', d.get('body',''))}"
                            for d in docs
                        ])
                except:
                    pass
            
            # 3. Call Groq
            system_prompt = (
                "You are DigitalMunshi, an expert AI legal assistant specializing in Pakistani law.\n"
                "Rules:\n"
                "- Answer the question clearly, utilizing any provided legal context where relevant.\n"
                "- Provide statutory references (e.g., Pakistan Penal Code Section 302, Family Courts Act 1964).\n"
                "- Respond in clear, helpful language (Roman Urdu or English as requested by the user).\n"
                "- Give brief next steps/action items for the user."
            )
            
            prompt = f"""
            Category: {category}
            Relevant Statutes Context:
            {doc_context}
            
            Question:
            {user_question}
            """
            
            answer = call_groq(prompt, system_prompt)
            
            # Add to history
            st.session_state.chat_history.append((user_question, answer, category, confidence))
            
    # Display Chat History
    for q, a, cat, conf in reversed(st.session_state.chat_history):
        st.markdown(f"**🧑 User:** {q}")
        st.info(f"🏷️ **Category:** {cat} (Confidence: {conf*100:.1f}%)")
        st.markdown(f"🤖 **Digital Munshi:** {a}")
        st.markdown("---")

# =========================================================
# MODULE 2: Legal Draft Generator
# =========================================================
elif page == "✍️ Legal Draft Generator":
    st.header("✍️ Legal Draft Generator")
    st.write("Generate formal legal documents customized to the laws of Pakistan. Select a document type and fill in the details.")
    
    col1, col2 = st.columns(2)
    with col1:
        doc_type = st.selectbox(
            "Select Document Type:",
            ["First Information Report (FIR)", "Legal Notice (Tenancy/Eviction)", "Complaint to Consumer Court", "Affidavit / Declaration"]
        )
        parties = st.text_input("Parties Involved:", placeholder="e.g., Muhammad Ali (Complainant) vs. John Doe (Accused)")
        incident_date = st.date_input("Date of Incident / Notice:")
        location = st.text_input("Location / Address:", placeholder="e.g., Gulberg III, Lahore")
        
    with col2:
        details = st.text_area(
            "Detailed Description of Situation:",
            height=180,
            placeholder="Describe exactly what happened. Be clear about monetary claims, damage, or criminal behavior."
        )
        
    if st.button("Generate Draft", type="primary"):
        if not parties or not details:
            st.warning("Please fill in both the Parties Involved and the Description details.")
        else:
            with st.spinner("Drafting formal legal document..."):
                system_prompt = (
                    "You are an expert legal draftsman in Pakistan. Generate formal, professional drafts. "
                    "Use precise legal terminology, leaving placeholders (like [Complainant CNIC]) where specific details are needed. "
                    "Make sure the draft is structured professionally with headings, subject lines, statement of facts, and prayer/relief clauses."
                )
                
                prompt = f"""
                Document Type: {doc_type}
                Date: {incident_date}
                Location: {location}
                Parties: {parties}
                Facts of the situation: {details}
                
                Compile a complete, legally sound, and formal draft.
                """
                
                draft = call_groq(prompt, system_prompt)
                
                st.subheader("📄 Generated Legal Draft")
                st.text_area("Copy/Edit Draft:", value=draft, height=450)
                st.success("Draft created successfully! You can copy and edit this text.")

# =========================================================
# MODULE 3: Document Analysis & OCR
# =========================================================
elif page == "📄 Document Analysis & OCR":
    st.header("📄 Document Analysis & Summary")
    st.write("Extract text, summarize legal contracts, and locate key binding clauses.")
    
    uploaded_text = st.text_area("Paste Legal Document Text here:", height=200, placeholder="Paste the text of a contract, lease, or complaint application here...")
    
    if st.button("Analyze Document", type="primary"):
        if not uploaded_text.strip():
            st.warning("Please paste document text to analyze.")
        else:
            with st.spinner("Analyzing document structure..."):
                system_prompt = (
                    "You are a legal document analyst. Analyze the provided legal text, extract the key clauses, "
                    "identify potential liabilities, flag missing critical items (like signatures or dates), and write a 3-sentence plain language summary."
                )
                
                analysis = call_groq(uploaded_text, system_prompt)
                
                st.subheader("📊 Analysis Output")
                st.markdown(analysis)
