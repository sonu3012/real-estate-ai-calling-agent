from flask import Flask, request, jsonify
import json
import os
import re

from dotenv import load_dotenv
from google import genai

from database import save_lead


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# GEMINI SETUP
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


# =========================================================
# PROPERTY FILE
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROPERTY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "properties.json"
)


# =========================================================
# LOAD PROPERTIES
# =========================================================

def load_properties():

    with open(
        PROPERTY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data.get("properties", [])


# =========================================================
# EXTRACT BUDGET
# =========================================================

def extract_budget(budget_text):

    if not budget_text:
        return None

    text = budget_text.lower()

    text = (
        text
        .replace("₹", "")
        .replace(",", "")
        .strip()
    )

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(lakh|lakhs|lac|crore|cr)",
        text
    )

    if not match:
        return None

    value = float(match.group(1))

    unit = match.group(2)

    if unit in ["crore", "cr"]:
        return value * 100

    return value


# =========================================================
# GET PROPERTY PRICE RANGE
# =========================================================

def get_price_range(price_text):

    if not price_text:
        return None, None

    text = price_text.lower()

    numbers = re.findall(
        r"(\d+(?:\.\d+)?)\s*(lakh|lakhs|crore|cr)",
        text
    )

    if len(numbers) < 2:
        return None, None

    prices = []

    for value, unit in numbers:

        value = float(value)

        if unit in ["crore", "cr"]:
            value = value * 100

        prices.append(value)

    return min(prices), max(prices)


# =========================================================
# PROPERTY MATCHING
# =========================================================

def property_matches(
    property_data,
    location="",
    property_type="",
    configuration="",
    budget=""
):

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    if location:

        customer_location = location.lower().strip()

        property_location = (
            property_data
            .get("location", "")
            .lower()
        )

        location_match = (
            customer_location in property_location
            or
            (
                customer_location in [
                    "gurgaon",
                    "gurugram"
                ]
                and
                (
                    "gurgaon" in property_location
                    or
                    "gurugram" in property_location
                )
            )
        )

        if not location_match:
            return False


    # -----------------------------------------------------
    # PROPERTY TYPE
    # -----------------------------------------------------

    if property_type:

        customer_type = (
            property_type
            .lower()
            .strip()
        )

        actual_type = (
            property_data
            .get("property_type", "")
            .lower()
        )

        if customer_type in [
            "apartment",
            "flat"
        ]:

            if "apartment" not in actual_type:
                return False

        elif customer_type not in actual_type:

            return False


    # -----------------------------------------------------
    # CONFIGURATION
    # -----------------------------------------------------

    if configuration:

        customer_configuration = (
            configuration
            .lower()
            .strip()
        )

        configurations = [
            config.lower()
            for config in
            property_data.get(
                "configurations",
                []
            )
        ]

        configuration_found = False

        for config in configurations:

            if customer_configuration == config:

                configuration_found = True
                break

            if customer_configuration in config:

                configuration_found = True
                break

        if not configuration_found:

            return False


    # -----------------------------------------------------
    # BUDGET
    # -----------------------------------------------------

    if budget:

        customer_budget = extract_budget(budget)

        if customer_budget is not None:

            minimum_price, maximum_price = get_price_range(
                property_data.get(
                    "price_range",
                    ""
                )
            )

            if minimum_price is not None:

                if customer_budget < minimum_price:

                    return False


    return True


# =========================================================
# NORMAL PROPERTY SEARCH API
# =========================================================

@app.route(
    "/api/search-properties",
    methods=["POST"]
)
def search_properties():

    data = request.get_json() or {}

    location = data.get(
        "location",
        ""
    )

    property_type = data.get(
        "property_type",
        ""
    )

    configuration = data.get(
        "configuration",
        ""
    )

    budget = data.get(
        "budget",
        ""
    )

    properties = load_properties()

    matches = []

    for property_data in properties:

        if property_matches(
            property_data,
            location,
            property_type,
            configuration,
            budget
        ):

            matches.append(property_data)


    return jsonify({

        "success": True,

        "count": len(matches),

        "properties": matches[:5]

    })


# =========================================================
# VAPI PROPERTY SEARCH TOOL
# =========================================================

@app.route(
    "/api/vapi-search-properties",
    methods=["POST"]
)
def vapi_search_properties():

    data = request.get_json() or {}


    # -----------------------------------------------------
    # VAPI FUNCTION TOOL REQUEST
    # -----------------------------------------------------

    if (
        "message" in data
        and
        "toolCallList" in data["message"]
    ):

        tool_calls = data["message"]["toolCallList"]

        results = []


        for tool_call in tool_calls:

            arguments = (
                tool_call
                .get("function", {})
                .get("arguments", {})
            )


            location = arguments.get(
                "location",
                ""
            )

            property_type = arguments.get(
                "property_type",
                ""
            )

            configuration = arguments.get(
                "configuration",
                ""
            )

            budget = arguments.get(
                "budget",
                ""
            )


            properties = load_properties()

            matches = []


            for property_data in properties:

                if property_matches(
                    property_data,
                    location,
                    property_type,
                    configuration,
                    budget
                ):

                    matches.append(property_data)


            results.append({

                "toolCallId": tool_call.get(
                    "id"
                ),

                "result": json.dumps({

                    "success": True,

                    "count": len(matches),

                    "properties": matches[:5]

                })

            })


        return jsonify({

            "results": results

        })


    # -----------------------------------------------------
    # NORMAL REQUEST
    # -----------------------------------------------------

    location = data.get(
        "location",
        ""
    )

    property_type = data.get(
        "property_type",
        ""
    )

    configuration = data.get(
        "configuration",
        ""
    )

    budget = data.get(
        "budget",
        ""
    )


    properties = load_properties()

    matches = []


    for property_data in properties:

        if property_matches(
            property_data,
            location,
            property_type,
            configuration,
            budget
        ):

            matches.append(property_data)


    return jsonify({

        "success": True,

        "count": len(matches),

        "properties": matches[:5]

    })


# =========================================================
# GEMINI LEAD EXTRACTION
# =========================================================

def extract_lead_information(conversation):

    extraction_prompt = f"""
Analyze the following real estate customer conversation.

Extract the customer's information.

Return ONLY valid JSON.
Do not add explanations.

If information is not available,
use an empty string.

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


    # Remove markdown code fences
    result = re.sub(
        r"```json\s*",
        "",
        result
    )

    result = re.sub(
        r"```\s*",
        "",
        result
    )


    try:

        return json.loads(result)


    except json.JSONDecodeError:

        print(
            "\nCould not automatically "
            "extract lead information."
        )

        print(
            "\nGemini returned:"
        )

        print(result)

        return None


# =========================================================
# VAPI END-OF-CALL WEBHOOK
# =========================================================

@app.route(
    "/api/vapi-webhook",
    methods=["POST"]
)
def vapi_webhook():

    data = request.get_json() or {}


    print(
        "\n========== VAPI WEBHOOK =========="
    )


    message = data.get(
        "message",
        {}
    )


    event_type = message.get(
        "type",
        ""
    )


    print(
        "Event Type:",
        event_type
    )


    # -----------------------------------------------------
    # GET TRANSCRIPT
    # -----------------------------------------------------

    transcript = message.get(
        "transcript",
        ""
    )


    # -----------------------------------------------------
    # TRY ARTIFACT
    # -----------------------------------------------------

    if not transcript:

        artifact = message.get(
            "artifact",
            {}
        )


        if isinstance(
            artifact,
            dict
        ):

            transcript = artifact.get(
                "transcript",
                ""
            )


    # -----------------------------------------------------
    # TRY ARTIFACT MESSAGES
    # -----------------------------------------------------

    if not transcript:

        artifact = message.get(
            "artifact",
            {}
        )


        if isinstance(
            artifact,
            dict
        ):

            messages = artifact.get(
                "messages",
                []
            )


            conversation_parts = []


            if isinstance(
                messages,
                list
            ):

                for item in messages:

                    if not isinstance(
                        item,
                        dict
                    ):

                        continue


                    role = item.get(
                        "role",
                        ""
                    )


                    text = item.get(
                        "message",
                        ""
                    )


                    if role and text:

                        conversation_parts.append(

                            f"{role}: {text}"

                        )


            transcript = "\n".join(
                conversation_parts
            )


    print(
        "\nTranscript:"
    )

    print(transcript)


    # =====================================================
    # PROCESS COMPLETED CALL
    # =====================================================

    if (
        event_type == "end-of-call-report"
        and
        transcript
    ):


        print(
            "\nExtracting lead information using Gemini..."
        )


        lead = extract_lead_information(
            transcript
        )


        if lead:


            print(
                "\n========== EXTRACTED LEAD =========="
            )


            print(

                json.dumps(
                    lead,
                    indent=2,
                    ensure_ascii=False
                )

            )


            # -------------------------------------------------
            # SAVE LEAD TO SQLITE
            # -------------------------------------------------

            save_lead(

                lead.get(
                    "name",
                    ""
                ),

                lead.get(
                    "phone",
                    ""
                ),

                lead.get(
                    "requirement",
                    ""
                ),

                lead.get(
                    "location",
                    ""
                ),

                lead.get(
                    "property_type",
                    ""
                ),

                lead.get(
                    "configuration",
                    ""
                ),

                lead.get(
                    "budget",
                    ""
                ),

                lead.get(
                    "purpose",
                    ""
                ),

                lead.get(
                    "timeline",
                    ""
                )

            )


            print(
                "\nLead successfully saved to SQLite database."
            )


    print(
        "\n========== END WEBHOOK ==========\n"
    )


    return jsonify({

        "success": True,

        "message": "Webhook received"

    })


# =========================================================
# HOME / HEALTH CHECK
# =========================================================

@app.route("/")
def home():

    return jsonify({

        "message":
        "Real Estate AI Backend is running!"

    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )

    