import requests

# Replace with your Gemini API details
GEMINI_API_URL = "https://api.gemini-model.com/v1/analyze"
API_KEY = "AIzaSyC68e3yceFdgQ_xDUHxHs2PmQ4ItM0pfkc"

def call_gemini_api(description):
    """
    Calls the Gemini API to analyze the cyber incident description
    and returns structured story and checklist.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": description,
        "task": "cyberattack_explanation"  # Example task name for Gemini
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Expected response format:
        # {
        #   "story": "...",
        #   "checklist": ["step1", "step2", ...]
        # }

        return {
            "story": data.get("story", ""),
            "checklist": data.get("checklist", [])
        }

    except Exception as e:
        # Log the error or print it during development
        print(f"Error calling Gemini API: {e}")

        # Fallback generic response
        return {
            "story": "We couldn't analyze this input well. Please be careful online.",
            "checklist": [
                "Be cautious of anything unusual online.",
                "Change passwords if you suspect a problem.",
                "Ask a trusted person for help if unsure."
            ]
        }
