# 🧠 Academic Research Assistant

An AI-powered research assistant that helps you explore the latest academic papers from **arXiv** using a conversational interface.

Built with **LangChain**, **OpenRouter**, **Streamlit**, and **FastAPI**, this app provides a seamless way to access scientific literature through natural language queries.

---

## 🚀 Features

- 🔍 **Search academic papers** using a simple question or topic
- 🤖 Powered by **LangChain** agents and **OpenRouter GPT**
- ⚡ Backend with **FastAPI** that interfaces with the arXiv API
- 🧩 Modular design with custom tool integration
- 🌐 Beautiful and responsive **Streamlit** UI
- 🔐 Environment-variable-based API key management

---

## 📸 UI Preview

![App UI Screenshot]() <!-- Add your own screenshot image in the repo -->

---

## 🧰 Tech Stack

| Layer        | Tool/Library          |
|--------------|------------------------|
| LLM          | [OpenRouter](https://openrouter.ai/) via GPT-3.5 |
| Agent System | [LangChain](https://www.langchain.com/) |
| UI           | [Streamlit](https://streamlit.io/) |
| Backend API  | [FastAPI](https://fastapi.tiangolo.com/) |
| Data Source  | [arXiv API](https://arxiv.org/help/api/index) |

---

## 📂 Project Structure
corp8/
├── langchain_ui_app.py # Streamlit UI app
├── fastapi_server.py # FastAPI arXiv API server
├── .env # API keys
├── requirements.txt # Dependencies
└── README.md # You're reading it!
