"""
AI Ghost Story Generator - Flask Backend
Connects to local open-weight LLMs via Ollama to generate spine-chilling ghost stories.
"""

import os
import sys
import re
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)

# Configuration
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", 180))

LENGTH_TOKEN_LIMITS = {
    "Short": 260,
    "Medium": 500,
    "Long": 850,
}

ALLOWED_LANGUAGES = {"English", "Hindi"}

ALLOWED_CATEGORIES = {
    "Haunted House",
    "Ghost Mystery",
    "Ancient Folklore",
    "Supernatural Horror",
    "Halloween Adventure",
    "Emotional Ghost Story",
}

ALLOWED_LENGTHS = {
    "Short": "Write a concise, vivid ghost story of approximately 180-250 words across 2 to 3 atmospheric paragraphs.",
    "Medium": "Write a gripping, suspenseful ghost story of approximately 350-500 words across 4 to 5 well-developed paragraphs.",
    "Long": "Write an immersive, detailed ghost story of approximately 650-850 words across 6 to 8 narrative paragraphs with deep dread and atmosphere.",
}

CATEGORY_TONES = {
    "Haunted House": "Focus on gothic dread, creaking floorboards, sinister architecture, shadowy corridors, and trapped souls bound to the structure.",
    "Ghost Mystery": "Focus on investigative intrigue, eerie clues, a forgotten tragedy, and the terrifying unraveling of an ancient secret.",
    "Ancient Folklore": "Focus on generational curses, mythical woodland spirits, cautionary tales, village legends, and timeless supernatural dread.",
    "Supernatural Horror": "Focus on raw paranormal terror, inexplicable cold spots, uncanny phenomena, relentless tension, and heart-stopping encounters.",
    "Halloween Adventure": "Focus on crisp autumn nights, flickering jack-o'-lanterns, misty graveyard paths, mischievous spirits, and eerie seasonal thrill.",
    "Emotional Ghost Story": "Focus on poignant sorrow, unresolved longing, bittersweet apparitions, lingering memories, and touching the boundary between love and death.",
}


def construct_prompt(idea: str, category: str, length: str, custom_title: str = None, language: str = "English") -> str:
    """Build a structured prompt for Ollama to generate an engaging ghost story in English or Hindi."""
    tone_guide = CATEGORY_TONES.get(category, "Evoke rich supernatural dread and atmosphere.")
    length_guide = ALLOWED_LENGTHS.get(length, ALLOWED_LENGTHS["Medium"])

    if language == "Hindi":
        title_instruction = (
            f"उपयोगकर्ता ने शीर्षक दिया है: '{custom_title}'। आपको यही सटीक शीर्षक इस्तेमाल करना होगा।"
            if custom_title
            else "कहानी के लिए एक भयानक, रहस्यमयी और उपयुक्त हिंदी शीर्षक बनाएँ।"
        )
        prompt = f"""आप अलौकिक भूतिया और डरावनी कहानियों के विशेषज्ञ लेखक हैं।

कहानी का विचार / बीज:
"{idea}"

कहानी की श्रेणी:
{category} - {tone_guide}

लंबाई आवश्यकता:
{length_guide}

शीर्षक आवश्यकता:
{title_instruction}

महत्वपूर्ण निर्देश:
1. पूरी कहानी और शीर्षक शुद्ध और स्वाभाविक हिंदी (देवनागरी लिपि) में लिखें।
2. पहली ही पंक्ति से गहरा खौफनाक और रहस्यमयी माहौल तैयार करें।
3. कहानी में रहस्य, अलौकिक घटनाएं और रोंगटे खड़े कर देने वाला अंत शामिल करें।
4. कोई अतिरिक्त बातचीत या प्रस्तावना न लिखें।
5. अपना आउटपुट केवल इसी प्रारूप में दें:

Title: <शीर्षक यहाँ>
Story:
<पूरी हिंदी कहानी यहाँ>"""
    else:
        title_instruction = (
            f"The user has specified the title: '{custom_title}'. You MUST use this exact title."
            if custom_title
            else "Create an original, spine-chilling, atmospheric title for the story."
        )
        prompt = f"""You are a master horror author specializing in supernatural ghost stories.

User's Story Seed:
"{idea}"

Story Category:
{category} - {tone_guide}

Length Requirement:
{length_guide}

Title Requirement:
{title_instruction}

Instructions:
1. Write a completely original ghost story based on the user's seed.
2. Establish a spooky, immersive atmosphere right from the opening sentence.
3. Build suspense through sensory details (cold chills, uncanny sounds, flickering shadows).
4. Deliver a satisfying, chilling, or haunting conclusion appropriate to the {category} category.
5. Avoid meta-commentary, conversational filler, or introductory pleasantries.
6. Format your output EXACTLY as follows:

Title: <Title Here>
Story:
<The full story text here>"""

    return prompt


def parse_ai_response(raw_text: str, custom_title: str = None, fallback_category: str = "Ghost Story") -> tuple[str, str]:
    """Parse the raw Ollama response into a clean title and story body (supports English and Hindi markers)."""
    raw_text = raw_text.strip()

    title = custom_title.strip() if custom_title else ""
    story = ""

    # Look for Title: / शीर्षक: and Story: / कहानी: markers (case-insensitive, handling markdown asterisks)
    title_pattern = re.compile(r"^(?:#+\s*|\*{0,2})(?:Title|शीर्षक)(?:\*{0,2}):\s*(.+)$", re.IGNORECASE | re.MULTILINE)
    story_pattern = re.compile(r"(?:#+\s*|\*{0,2})(?:Story|कहानी)(?:\*{0,2}):\s*\n*(.+)", re.IGNORECASE | re.DOTALL)

    story_match = story_pattern.search(raw_text)

    if not title:
        title_match = title_pattern.search(raw_text)
        if title_match:
            title = title_match.group(1).strip().strip('"*#')
        else:
            # Fallback: take the first non-empty line if short, or create a category-based title
            lines = [line.strip().strip('"*#') for line in raw_text.splitlines() if line.strip()]
            if lines and len(lines[0]) <= 80 and not lines[0].lower().startswith("once upon") and not lines[0].startswith("एक बार"):
                title = lines[0]
                if not story_match and len(lines) > 1:
                    story = "\n\n".join(lines[1:])
            else:
                title = f"The Haunting of {fallback_category}"

    if story_match:
        story = story_match.group(1).strip()
    elif not story:
        # If no explicit "Story:" marker, strip out any "Title: ..." line from the beginning
        remaining = re.sub(r"^(?:#+\s*|\*{0,2})(?:Title|शीर्षक)(?:\*{0,2}):\s*.+\n+", "", raw_text, flags=re.IGNORECASE).strip()
        story = remaining if remaining else raw_text

    # Clean any lingering markdown bold headers inside the title
    title = re.sub(r"^\*+|\*+$", "", title).strip()

    return title, story


@app.route("/")
def index():
    """Render the main horror-themed UI."""
    return render_template("index.html", default_model=OLLAMA_MODEL)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint reporting Flask and Ollama status."""
    ollama_connected = False
    model_available = False

    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=4)
        if resp.status_code == 200:
            ollama_connected = True
            models = resp.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            # Match model name or prefix (e.g. llama3.2:3b or llama3.2:latest)
            model_available = any(
                OLLAMA_MODEL == name or name.startswith(f"{OLLAMA_MODEL}:") or OLLAMA_MODEL.startswith(name.split(":")[0])
                for name in model_names
            )
    except Exception:
        ollama_connected = False
        model_available = False

    return jsonify({
        "status": "ok",
        "flask": "healthy",
        "ollama": {
            "connected": ollama_connected,
            "url": OLLAMA_URL,
            "configured_model": OLLAMA_MODEL,
            "model_available": model_available
        }
    }), 200


@app.route("/generate", methods=["POST"])
def generate():
    """Generate a ghost story using local Ollama model."""
    if not request.is_json:
        return jsonify({"success": False, "error": "Request body must be JSON."}), 400

    data = request.get_json() or {}

    idea = str(data.get("idea", "")).strip()
    category = str(data.get("category", "")).strip()
    length = str(data.get("length", "Medium")).strip()
    custom_title = str(data.get("title", "")).strip()

    language = str(data.get("language", "English")).strip()
    if language not in ALLOWED_LANGUAGES:
        language = "English"

    # Input validation
    if not idea or len(idea) < 3:
        return jsonify({"success": False, "error": "Please provide a story idea (at least 3 characters)."}), 400

    if len(idea) > 2000:
        return jsonify({"success": False, "error": "Story idea exceeds maximum allowed length of 2000 characters."}), 400

    if category not in ALLOWED_CATEGORIES:
        return jsonify({
            "success": False,
            "error": f"Invalid category. Allowed categories: {', '.join(sorted(ALLOWED_CATEGORIES))}"
        }), 400

    if length not in ALLOWED_LENGTHS:
        return jsonify({
            "success": False,
            "error": f"Invalid length. Allowed lengths: {', '.join(sorted(ALLOWED_LENGTHS))}"
        }), 400

    if custom_title and len(custom_title) > 120:
        return jsonify({"success": False, "error": "Custom title cannot exceed 120 characters."}), 400

    prompt = construct_prompt(
        idea=idea,
        category=category,
        length=length,
        custom_title=custom_title if custom_title else None,
        language=language
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.8,
            "top_p": 0.9,
            "num_predict": LENGTH_TOKEN_LIMITS.get(length, 500),
        }
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        resp_json = response.json()
        raw_output = resp_json.get("response", "")

        if not raw_output or not raw_output.strip():
            return jsonify({
                "success": False,
                "error": "The spirits returned an empty response. Please try again with a different prompt."
            }), 502

        title, story = parse_ai_response(
            raw_text=raw_output,
            custom_title=custom_title,
            fallback_category=category
        )

        return jsonify({
            "success": True,
            "title": title,
            "story": story,
            "category": category,
            "length": length,
            "language": language,
            "model": OLLAMA_MODEL
        }), 200

    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "error": "The ghost realm is currently unreachable. Please start Ollama and make sure the AI model is installed.",
            "troubleshooting": [
                "1. Make sure Ollama is installed from https://ollama.com",
                f"2. Start Ollama and pull the model: `ollama pull {OLLAMA_MODEL}`",
                f"3. Verify Ollama is running at {OLLAMA_URL}"
            ]
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "error": f"The spirits took too long to answer (timed out after {REQUEST_TIMEOUT}s). Try a shorter length option."
        }), 504

    except requests.exceptions.HTTPError as err:
        return jsonify({
            "success": False,
            "error": f"Ollama returned HTTP error: {err.response.status_code if err.response else 'Unknown'}"
        }), 502

    except Exception as exc:
        # Keep internal stack trace hidden from user
        return jsonify({
            "success": False,
            "error": "An unexpected darkness enveloped the generator. Please try again later."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    print(f"👻 AI Ghost Story Generator starting on http://127.0.0.1:{port}")
    print(f"🔮 Ollama target: {OLLAMA_URL} (Model: {OLLAMA_MODEL})")
    app.run(host="0.0.0.0", port=port, debug=debug)
