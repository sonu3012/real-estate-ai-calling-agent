# 🏠 Real Estate AI Calling Agent

An AI-powered voice calling agent designed for the real estate industry.

The agent behaves like a real estate sales executive and can communicate with customers in **Hindi, Hinglish, and basic English**. It understands customer property requirements, searches matching properties, answers basic project-related questions, collects lead information, and stores structured lead data after the call.

---

## 📌 Project Overview

This project was developed as part of a technical interview assignment:

> **Build a Live Real Estate AI Calling Agent**

The objective was to build a functional AI voice agent that can have a natural conversation with prospective real estate customers.

The system integrates:

- Voice AI calling
- Google Gemini
- Vapi
- Flask backend
- Property search API
- Vapi webhook
- SQLite database
- Streamlit dashboard
- Cloudflare Tunnel

The project uses **dummy/sample property data** for demonstration purposes.

---

# 🎯 Key Features

- 🎙️ AI voice calling agent
- 🇮🇳 Hindi conversation support
- 🗣️ Hinglish conversation support
- 🇬🇧 Basic English support
- 🏠 Real estate requirement qualification
- 📍 Location understanding
- 🏢 Property type identification
- 🛏️ 2 BHK / 3 BHK / 4 BHK configuration understanding
- 💰 Customer budget understanding
- 👨‍👩‍👧 Self-use / investment identification
- 📅 Purchase timeline collection
- 🔎 Property search based on customer requirements
- 💬 Basic property/project information
- 📞 Customer contact information collection
- 🧠 AI-based conversation processing
- 📝 Automatic lead extraction
- 💾 SQLite lead storage
- 📊 Streamlit lead dashboard
- 🌐 Cloudflare Tunnel for public backend access
- 🔗 Vapi voice integration

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google Gemini | AI conversation and lead extraction |
| Vapi | Voice calling and voice assistant |
| Flask | Backend REST API |
| SQLite | Lead database |
| Streamlit | Lead management dashboard |
| Cloudflare Tunnel | Public access to local backend |
| JSON | Sample property data |
| Git | Version control |
| GitHub | Source code repository |

---

# 🤖 AI Model

The project uses **Google Gemini** for AI-powered processing.

Gemini is used for:

1. Understanding customer conversation
2. Processing natural-language requirements
3. Extracting structured lead information
4. Generating conversational responses
5. Processing the final conversation after the call

The AI agent is designed to communicate naturally rather than behave like a fixed IVR system.

---

# 🎙️ Voice / Calling Platform

The project uses **Vapi** as the voice interaction platform.

Vapi handles:

- Voice conversation
- Speech interaction
- AI assistant configuration
- Tool calling
- Property-search requests
- End-of-call webhook events

The Vapi assistant communicates with the Flask backend through publicly accessible HTTPS endpoints.

---

# 🏗️ System Architecture

```text
                         CUSTOMER
                            │
                            ▼
                    ┌───────────────┐
                    │     Vapi      │
                    │  Voice Agent  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Google Gemini │
                    │   AI Model    │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
     ┌─────────────────┐         ┌─────────────────┐
     │ Property Search │         │  Vapi Webhook   │
     │      API        │         │                 │
     └────────┬────────┘         └────────┬────────┘
              │                           │
              ▼                           ▼
     ┌─────────────────┐         ┌─────────────────┐
     │ properties.json │         │ Gemini Lead     │
     │ Property Data   │         │ Extraction      │
     └─────────────────┘         └────────┬────────┘
                                          │
                                          ▼
                                  ┌─────────────────┐
                                  │ SQLite Database │
                                  │      Leads      │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │    Streamlit    │
                                  │    Dashboard    │
                                  └─────────────────┘
🔄 Conversation Flow

The AI agent follows a real estate sales qualification flow.

Step 1 — Greeting

The agent introduces itself as a real estate representative.

Example:

"Namaste! Main aapki real estate property requirements mein help karne ke liye available hoon."

Step 2 — Customer Intent

The agent asks whether the customer wants to:

Buy a property
Invest in property
Step 3 — Requirement Collection

The agent collects information such as:

Preferred location
Property type
Configuration
Budget
Purpose
Purchase timeline

Example:

Location: Gurgaon
Property Type: Apartment
Configuration: 3 BHK
Budget: 90 Lakh
Purpose: Self Use
Timeline: 6 Months
Step 4 — Property Search

The agent can search the sample property database according to customer requirements.

For example:

Customer:
"Mujhe Gurgaon mein 90 lakh ke budget mein 3 BHK chahiye."

Agent:
Searches the property API and provides matching properties.
Step 5 — Property Information

The agent can answer basic questions about sample properties, including:

Project name
Location
Configuration
Price range
Amenities
Possession timeline
Location advantages
Step 6 — Lead Information

The agent collects customer information such as:

Name
Phone number
Property requirement
Location
Property type
Configuration
Budget
Purpose
Purchase timeline
Step 7 — Call Summary

After the conversation ends, the system processes the call and creates structured lead information.

🔎 Property Search

Sample property information is stored in:

data/properties.json

The property search API receives customer requirements and returns matching properties.

Example request:

{
    "location": "Gurgaon",
    "property_type": "Apartment",
    "configuration": "3 BHK",
    "budget": "90 lakh"
}

The API searches the sample property data and returns suitable matches.

🧠 Lead Extraction

At the end of the call, Vapi sends the call information to the backend webhook.

The backend processes the conversation using Google Gemini.

Gemini extracts important customer information and converts the conversation into structured lead data.

Example:

Name: Sonu Kumar
Phone: 6205346480
Intent: Buy property
Location: Gurgaon
Property Type: Flat
Configuration: 3 BHK
Budget: 90 Lakh
Purpose: Self Use
Timeline: 6 Months
💾 Lead Storage

Lead information is stored in a local SQLite database.

Database file:

real_estate_leads.db

The database is intentionally excluded from GitHub using .gitignore.

The database can be viewed through the Streamlit dashboard.

📊 Streamlit Dashboard

The project includes a Streamlit dashboard for viewing captured leads.

The dashboard displays information such as:

Total leads
Customer name
Phone number
Requirement
Location
Property type
Configuration
Budget
Purpose
Purchase timeline

The dashboard provides a simple interface for reviewing leads generated from AI voice calls.

🌐 Cloudflare Tunnel

The Flask backend runs locally during development.

Example:

http://127.0.0.1:5000

Cloudflare Tunnel is used to expose the local backend through a temporary HTTPS URL so that Vapi can communicate with the backend.

Example:

https://your-random-name.trycloudflare.com

The Cloudflare Quick Tunnel URL may change when the tunnel is restarted.

When the URL changes, the corresponding Vapi server/webhook URLs need to be updated.

📂 Project Structure
Real Estate AI Agent/
│
├── backend/
│   ├── api.py
│   ├── database.py
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── properties.json
│
├── .gitignore
├── README.md
└── requirements.txt
⚙️ Installation
1. Clone the repository
git clone https://github.com/sonu3012/real-estate-ai-calling-agent.git

Move into the project directory:

cd real-estate-ai-calling-agent
2. Create a virtual environment
python -m venv venv

Activate it on Windows PowerShell:

.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file in the project root.

Example:

GEMINI_API_KEY=your_gemini_api_key

Do not upload the .env file to GitHub.

The project .gitignore contains:

.env
venv/
__pycache__/
*.pyc
real_estate_leads.db
cloudflared.exe
▶️ Running the Backend

Start the Flask backend:

python backend/api.py

The backend runs locally on:

http://127.0.0.1:5000
▶️ Running the Streamlit Dashboard

Open another terminal and run:

streamlit run dashboard/app.py

The Streamlit dashboard will open in the browser.

🌐 Running Cloudflare Tunnel

Open another terminal:

.\cloudflared.exe tunnel --url http://127.0.0.1:5000

Cloudflare will generate a temporary public HTTPS URL.

Example:

https://example.trycloudflare.com

This URL is used by Vapi to communicate with the backend.

🧪 Demo Test

A typical demo conversation can be:

Customer:
Namaste, mujhe Gurgaon mein property leni hai.

AI:
Aap property buy karna chahte hain ya investment ke liye?

Customer:
Buy karna hai, family ke liye.

AI:
Aapko kis type ki property chahiye?

Customer:
3 BHK flat.

AI:
Aapka budget approximately kitna hai?

Customer:
Around 90 lakh.

AI:
Aap Gurgaon mein kis area ko prefer karte hain?

Customer:
Sector 70 ke around.

AI:
Aap self-use ke liye property dekh rahe hain ya investment?

Customer:
Self-use.

AI:
Aap approximately kab tak purchase karna chahte hain?

Customer:
6 months mein.

The AI can then search the property database and provide matching sample properties.

📞 End-to-End Lead Flow
Customer starts voice call
            ↓
Vapi Voice Agent
            ↓
Customer requirement collection
            ↓
Property search
            ↓
AI property response
            ↓
Customer contact details
            ↓
Call ends
            ↓
Vapi Webhook
            ↓
Google Gemini
            ↓
Structured lead extraction
            ↓
SQLite Database
            ↓
Streamlit Dashboard
⚠️ Known Limitations

This project is a functional technical-interview prototype and is not a production real estate platform.

Current limitations include:

Property data is sample/dummy data.
Cloudflare Quick Tunnel provides a temporary public URL.
The public tunnel URL can change after restarting Cloudflare.
The system does not connect to a live real estate property inventory.
Property prices and availability are not real-time.
The application is not deployed on a permanent production server.
Voice quality and response time can depend on external services.
The project does not include production-grade authentication or authorization.
🚧 Challenges Faced

During development, some of the main challenges included:

1. Voice AI Integration

Connecting the voice assistant with the backend and making the conversation natural required configuration and testing.

2. Backend Connectivity

The local Flask API needed to be accessible from Vapi.

Cloudflare Tunnel was used to provide public HTTPS access.

3. Property Search

The system needed to understand customer requirements and convert them into property search parameters.

4. Lead Extraction

The final conversation needed to be converted from natural language into structured lead information.

Google Gemini was used for this processing.

5. Database Integration

The extracted information needed to be stored reliably and displayed in the Streamlit dashboard.

🚀 Future Improvements

Possible improvements for the next version include:

Deploy the backend to a permanent cloud server.
Use a permanent Cloudflare named tunnel.
Connect to a real property database/API.
Add real-time property availability.
Add CRM integration.
Add automated follow-up calls.
Add WhatsApp integration.
Add email notifications for new leads.
Add lead scoring.
Add authentication for the dashboard.
Add analytics and conversion tracking.
Improve multilingual voice quality.
Add conversation history.
Add appointment/site-visit scheduling.
🔐 Security

The project does not store API keys in the source code.

Sensitive files are excluded through .gitignore.

The following files are not intended to be uploaded to GitHub:

.env
venv/
real_estate_leads.db
cloudflared.exe

The sample property information used in this project is for demonstration purposes.

📦 Functional Components
Component	Status
Voice Agent	✅ Functional
Vapi Integration	✅ Functional
Gemini Integration	✅ Functional
Property Search API	✅ Functional
Sample Property Data	✅ Functional
Lead Extraction	✅ Functional
SQLite Storage	✅ Functional
Streamlit Dashboard	✅ Functional
Cloudflare Tunnel	✅ Functional
GitHub Repository	✅ Functional
🎥 Demonstration

The final demonstration shows:

Starting a live voice conversation
Hindi/Hinglish customer interaction
Collecting property requirements
Searching matching properties
Answering property questions
Collecting customer information
Ending the call
Extracting lead information
Saving the lead in SQLite
Viewing the lead in the Streamlit dashboard
👨‍💻 Developer

Sonu Kumar Roy

B.Tech — Artificial Intelligence & Data Science

📌 Project Purpose

This project was created as a technical interview assignment to demonstrate practical skills in:

Artificial Intelligence
Generative AI
Voice AI
API development
Backend development
Database integration
Natural Language Processing
Automation
Data extraction
Dashboard development
Third-party API integration

The primary objective was to build and demonstrate a working end-to-end AI voice solution rather than a production-ready commercial platform.