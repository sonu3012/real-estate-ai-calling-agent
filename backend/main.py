import os
import json
import re

from dotenv import load_dotenv
from google import genai

from database import create_database, save_lead


# ============================================
# 1. Load environment variables
# ============================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not found in .env file")


# ============================================
# 2. Create Gemini client
# ============================================

client = genai.Client(api_key=api_key)


# ============================================
# 3. Create database
# ============================================

create_database()

print("Database initialized successfully!")


# ============================================
# 4. Load property data
# ============================================

with open("data/properties.json", "r", encoding="utf-8") as file:
    property_data = json.load(file)

print("Property data loaded successfully!")


# ============================================
# 5. Real Estate Agent Instructions
# ============================================

SYSTEM_PROMPT = """
You are Rahul, a professional real estate sales executive.

You work for a fictional real estate company.

You can communicate in:
- Hindi
- Hinglish
- Basic English

Your job is to understand the customer's property requirements.

You should naturally understand:

1. Whether the customer wants to buy or invest
2. Preferred location
3. Property type
4. Configuration such as 2 BHK, 3 BHK, 4 BHK, plot or commercial
5. Budget
6. Purpose: self-use or investment
7. Expected purchase timeline

Conversation rules:

- Speak naturally like a real sales executive.
- Be polite and professional.
- Ask one or two questions at a time.
- Do not ask all questions at once.
- If the customer asks a question, answer it first.
- Continue the conversation naturally.
- Understand Hindi, Hinglish and basic English.
- Never promise guaranteed returns.
- Never invent property information.

Lead collection:

Try to collect:
- Customer name
- Phone number
- Buy or investment requirement
- Preferred location
- Property type
- Configuration
- Budget
- Purpose
- Purchase timeline

Do not repeatedly ask for information that the customer has already provided.
"""


# ============================================
# 6. Add property database
# ============================================

SYSTEM_PROMPT += f"""

Here is the property database:

{json.dumps(property_data, indent=2, ensure_ascii=False)}

Use this database to answer customer questions.

Only provide property information from this database.
Do not invent prices, amenities, possession dates or other details.
"""


# ============================================
# 7. Extract lead information
# ============================================

def extract_lead_information(conversation):

    extraction_prompt = f"""
Analyze the following real estate customer conversation.

Extract the customer's information.

Return ONLY valid JSON.
Do not add explanations.
If information is not available, use an empty string.

JSON format:

{{
    "name": "",
    "phone": "",
    "requirement": "",
    "location": "",
    "property_type": "",
    "configuration": "",
    "budget": "",
    "purpose": "",
    "timeline": ""
}}

Conversation:

{conversation}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=extraction_prompt
    )

    result = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    result = re.sub(r"```json\s*", "", result)
    result = re.sub(r"```\s*", "", result)

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        print("\nCould not automatically extract lead information.")
        print("Gemini returned:")
        print(result)
        return None


# ============================================
# 8. Start conversation
# ============================================

print("\nReal Estate AI Agent Started!!")
print("Type 'exit' to end the conversation.\n")


chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "system_instruction": SYSTEM_PROMPT
    }
)


# ============================================
# 9. Conversation
# ============================================

conversation_text = ""


while True:

    user_message = input("Customer: ")

    # ========================================
    # End conversation
    # ========================================

    if user_message.lower() == "exit":

        print("\nAgent: Thank you for your time. Have a great day!")

        # Extract customer information
        print("\nExtracting customer information...")

        lead = extract_lead_information(conversation_text)

        if lead:

            # Save lead to database
            save_lead(
                lead.get("name", ""),
                lead.get("phone", ""),
                lead.get("requirement", ""),
                lead.get("location", ""),
                lead.get("property_type", ""),
                lead.get("configuration", ""),
                lead.get("budget", ""),
                lead.get("purpose", ""),
                lead.get("timeline", "")
            )

            print("Lead saved successfully! ✅")

            print("\nCustomer Lead:")
            print(json.dumps(lead, indent=4, ensure_ascii=False))

        break


    # ========================================
    # Send customer message to Gemini
    # ========================================

    conversation_text += f"\nCustomer: {user_message}"

    response = chat.send_message(user_message)

    agent_reply = response.text

    print("Agent:", agent_reply)

    conversation_text += f"\nAgent: {agent_reply}"


    