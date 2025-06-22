import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY not found in .env file")
    st.stop()

# Tool to call FastAPI server
def search_arxiv(query: str) -> str:
    try:
        res = requests.get(
            "http://127.0.0.1:8000/search_arxiv",
            params={"query": query},
            timeout=10
        )
        res.raise_for_status()
        data = res.json()

        if "papers" not in data or not data["papers"]:
            return "\n🔍 No papers found for this topic."

        top_papers = data["papers"][:2]
        return "\n\n".join([
            f"📄 <b>{p['title']}</b><br>👤 <i>{p['author']}</i><br>🔗 <a href='{p['link']}' target='_blank'>{p['link']}</a><br>📝 {p['summary'][:300]}..."
            for p in top_papers
        ])
    except Exception as e:
        return f"❌ Error while querying arXiv API: {str(e)}"

# Register tool
tools = [
    Tool(
        name="arXiv Search",
        func=search_arxiv,
        description="Find academic papers from arXiv by topic (e.g., 'quantum computing')."
    )
]

# Initialize LLM with OpenRouter API
llm = ChatOpenAI(
    temperature=0,
    model="openai/gpt-3.5-turbo",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api_key
)

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Streamlit UI
st.set_page_config(page_title="🔬 AI-Powered Research Assistant", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .title-style {
        text-align: center;
        font-size: 3em;
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 0.2em;
    }
    .desc-style {
        text-align: center;
        font-size: 1.3em;
        color: #444;
        margin-bottom: 2.5em;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: black;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-size: 1.1em;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #125a94;
    }
    .stTextInput > div > input {
        border-radius: 10px;
        font-size: 1.1em;
        padding: 0.6em;
        border: 1px solid #ccc;
    }
    .result-card {
        background: #f9f9f9;
        padding: 1.2em;
        border-radius: 12px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
        margin-bottom: 1.5em;
        color: black;
        font-size: 1.05em;
        line-height: 1.6em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-style'>🧠 LangChain Research Agent</div>", unsafe_allow_html=True)
st.markdown("""
<div class='desc-style'>
Use AI to explore the latest <b>academic research</b> from arXiv.<br>
Powered by <i>LangChain</i>, <i>OpenRouter</i>, <i>Streamlit</i>, and <i>FastAPI</i>.
</div>
""", unsafe_allow_html=True)

query = st.text_input("🔍 Enter your research topic/question:", "")

if st.button("🚀 Search Academic Papers") and query:
    with st.spinner("🤖 Searching arXiv..."):
        try:
            response = agent.run(query)
            st.success("✅ Results fetched successfully!")
            st.markdown("### 📄 Top Papers")
            for block in response.split("\n\n"):
                st.markdown(f"<div class='result-card'>{block}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"⚠️ Error occurred: {str(e)}")

st.markdown("---")
st.caption("Made  by Amritanshu using LangChain, Streamlit & OpenRouter")
