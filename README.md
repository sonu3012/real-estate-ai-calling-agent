# 🏠 Real Estate AI Calling Agent

An AI-powered voice calling agent designed for the real estate industry.

The agent can communicate with customers in **Hindi, Hinglish, and basic English**, understand their property requirements, search matching properties, answer basic project-related questions, collect lead information, and generate a structured lead record after the call.

---

## 📌 Project Overview

This project was developed as part of a technical interview assignment:

> **Build a Live Real Estate AI Calling Agent**

The objective was to create a functional AI voice agent that behaves like a real estate sales executive and can have a natural conversation with prospective customers.

The system connects a voice calling platform with an AI model, property-search API, webhook, database, and Streamlit dashboard.

---

# 🎯 Key Features

- 🎙️ AI voice calling agent
- 🇮🇳 Hindi conversation support
- 🗣️ Hinglish conversation support
- 🇬🇧 Basic English support
- 🏠 Real estate requirement qualification
- 📍 Location understanding
- 🏢 Property type identification
- 🛏️ Configuration detection such as 2 BHK, 3 BHK and 4 BHK
- 💰 Budget understanding
- 👨‍👩‍👧 Self-use / investment identification
- 📅 Purchase timeline collection
- 🔎 Property search based on customer requirements
- 💬 Basic property/project information
- 📞 Customer contact information collection
- 🧠 AI-based conversation processing
- 📝 Automatic lead extraction
- 💾 SQLite lead storage
- 📊 Streamlit lead dashboard
- 🌐 Cloudflare Tunnel for public webhook access
- 🔗 Vapi integration for voice interaction

---

# 🏗️ System Architecture

```text
                    CUSTOMER
                       │
                       ▼
                ┌──────────────┐
                │     Vapi     │
                │ Voice Agent  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Google Gemini│
                │  AI Model    │
                └──────┬───────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
 ┌─────────────────┐       ┌─────────────────┐
 │ Property Search │       │  Vapi Webhook   │
 │      API        │       │                 │
 └────────┬────────┘       └────────┬────────┘
          │                         │
          ▼                         ▼
 ┌─────────────────┐       ┌─────────────────┐
 │ properties.json │       │ Gemini Lead     │
 │ Property Data   │       │ Extraction      │
 └─────────────────┘       └────────┬────────┘
                                    │
                                    ▼
                            ┌─────────────────┐
                            │ SQLite Database │
                            │     Leads       │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │    Streamlit    │
                            │    Dashboard    │
                            └─────────────────┘


                            