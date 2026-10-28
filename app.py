"""
AI Ghost Story Generator - Flask Backend
Production-ready serverless backend powered by Google Gemini API.
Generates spine-chilling horror stories in English and Hindi with custom tones,
length controls, title parsing, and in-memory rate limiting.
"""

import os
import sys
import re
import time
from collections import defaultdict
from threading import Lock
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Load environment variables from .env if present (local development)
load_dotenv()

app = Flask(__name__)

# Configuration
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

LENGTH_TOKEN_LIMITS = {
    "Short": 350,
    "Medium": 650,
    "Long": 1100,
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

# In-Memory Rate Limiting: 10 requests per minute per IP address
# Note: In a serverless environment (such as Vercel Functions), in-memory rate limiting
# enforces limits per container instance. For globally persistent distributed rate limiting,
# an external low-latency store such as Upstash Redis or Vercel KV would be required.
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 10
_rate_limit_records = defaultdict(list)
_rate_limit_lock = Lock()


def is_rate_limited(client_ip: str) -> bool:
    """Check if the client IP has exceeded the allowed request limit within the sliding window."""
    now = time.time()
    with _rate_limit_lock:
        timestamps = _rate_limit_records[client_ip]
        # Purge timestamps outside the active window
        valid_timestamps = [ts for ts in timestamps if now - ts < RATE_LIMIT_WINDOW_SECONDS]
        if len(valid_timestamps) >= RATE_LIMIT_MAX_REQUESTS:
            _rate_limit_records[client_ip] = valid_timestamps
            return True
        valid_timestamps.append(now)
        _rate_limit_records[client_ip] = valid_timestamps
        return False


def get_client_ip() -> str:
    """Extract client IP securely from request headers (handling proxies/Vercel edge)."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "127.0.0.1"


def construct_prompt(idea: str, category: str, length: str, custom_title: str = None, language: str = "English") -> str:
    """Build a structured prompt for Google Gemini to generate an engaging ghost story in English or Hindi."""
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
    """Parse the raw AI response into a clean title and story body (supports English and Hindi markers)."""
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
    return render_template("index.html", default_model=GEMINI_MODEL)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint reporting Flask status and Gemini API configuration."""
    api_key_configured = bool(os.environ.get("GEMINI_API_KEY", "").strip())
    return jsonify({
        "status": "ok",
        "flask": "healthy",
        "provider": "google-gemini",
        "configured_model": GEMINI_MODEL,
        "api_key_configured": api_key_configured
    }), 200


@app.route("/generate", methods=["POST"])
def generate():
    """Generate a ghost story using Google Gemini API."""
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON.",
            "code": "INVALID_JSON"
        }), 400

    data = request.get_json() or {}

    idea = str(data.get("idea", "")).strip()
    category = str(data.get("category", "")).strip()
    length = str(data.get("length", "Medium")).strip()
    custom_title = str(data.get("title", "")).strip()

    language = str(data.get("language", "English")).strip()
    if language not in ALLOWED_LANGUAGES:
        language = "English"

    # Input validation and size limits
    if not idea or len(idea) < 3:
        return jsonify({
            "success": False,
            "error": "Please provide a story idea (at least 3 characters).",
            "code": "INPUT_TOO_SHORT"
        }), 400

    if len(idea) > 2000:
        return jsonify({
            "success": False,
            "error": "Story idea exceeds maximum allowed length of 2000 characters.",
            "code": "INPUT_TOO_LONG"
        }), 400

    if category not in ALLOWED_CATEGORIES:
        return jsonify({
            "success": False,
            "error": f"Invalid category. Allowed categories: {', '.join(sorted(ALLOWED_CATEGORIES))}",
            "code": "INVALID_CATEGORY"
        }), 400

    if length not in ALLOWED_LENGTHS:
        return jsonify({
            "success": False,
            "error": f"Invalid length. Allowed lengths: {', '.join(sorted(ALLOWED_LENGTHS))}",
            "code": "INVALID_LENGTH"
        }), 400

    if custom_title and len(custom_title) > 120:
        return jsonify({
            "success": False,
            "error": "Custom title cannot exceed 120 characters.",
            "code": "TITLE_TOO_LONG"
        }), 400

    # Rate limiting abuse prevention
    client_ip = get_client_ip()
    if is_rate_limited(client_ip):
        return jsonify({
            "success": False,
            "error": "Too many summoning rituals in a short time. Please wait a moment before trying again.",
            "code": "RATE_LIMITED"
        }), 429

    # Verify server-side API key configuration
    api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"\'')
    if not api_key:
        return jsonify({
            "success": False,
            "error": "The ghost realm is unconfigured. GEMINI_API_KEY is not set on the server. Please configure it in your Vercel Environment Variables.",
            "code": "MISSING_API_KEY"
        }), 500

    prompt = construct_prompt(
        idea=idea,
        category=category,
        length=length,
        custom_title=custom_title if custom_title else None,
        language=language
    )

    max_tokens = LENGTH_TOKEN_LIMITS.get(length, 650)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        # Dynamic model discovery: Query Google for models supported by this specific API key
        discovered_models = []
        list_error_msg = None
        try:
            for m in client.models.list():
                name = getattr(m, "name", "") or ""
                clean_name = name.replace("models/", "").strip()
                methods = getattr(m, "supported_generation_methods", None) or getattr(m, "supported_actions", None) or []
                if not methods or "generateContent" in methods:
                    if clean_name not in discovered_models:
                        discovered_models.append(clean_name)
        except Exception as l_err:
            list_error_msg = str(l_err)
            sys.stderr.write(f"[WARN] client.models.list() failed: {l_err}\n")

        # Preferred models ordered by latency and capability
        priority_models = [
            GEMINI_MODEL,
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro",
            "gemini-1.5-pro-latest",
            "gemini-pro"
        ]

        candidate_models = []
        for p in priority_models:
            if p not in candidate_models:
                candidate_models.append(p)
        for d in discovered_models:
            if d not in candidate_models:
                candidate_models.append(d)

        response = None
        last_exc = None
        actual_model_used = GEMINI_MODEL

        for model_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        top_p=0.9,
                        max_output_tokens=max_tokens,
                    )
                )
                if response and hasattr(response, "text") and response.text:
                    actual_model_used = model_name
                    break
            except Exception as model_err:
                last_exc = model_err
                err_lower = str(model_err).lower()
                # Stop fallback immediately if the key itself is invalid or quota is exhausted
                if "api key" in err_lower or "api_key" in err_lower or "401" in err_lower or "403" in err_lower or "quota" in err_lower or "429" in err_lower:
                    raise model_err
                continue

        if not response:
            if last_exc:
                if list_error_msg:
                    raise Exception(f"{last_exc} (ListModels note: {list_error_msg})")
                raise last_exc
            elif discovered_models:
                raise Exception(f"No generation models responded. Available: {discovered_models[:5]}")
            else:
                raise Exception("No generation models found for this API key.")

        raw_output = response.text if response and hasattr(response, "text") and response.text else ""

        if not raw_output or not raw_output.strip():
            return jsonify({
                "success": False,
                "error": "The spirits returned an empty response. Please try again with a different premise.",
                "code": "EMPTY_RESPONSE"
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
            "model": actual_model_used
        }), 200

    except Exception as exc:
        exc_str = str(exc).lower()
        safe_diagnostic = re.sub(r"AIza[A-Za-z0-9_-]+", "[REDACTED]", str(exc))
        sys.stderr.write(f"[ERROR] Gemini Generation Failed: {safe_diagnostic}\n")

        # Specific handling for Rate Limits
        if "429" in exc_str or "resource_exhausted" in exc_str or "quota" in exc_str:
            return jsonify({
                "success": False,
                "error": "The spirits are overwhelmed by too many summoners. The ghost realm is rate limited; please wait a moment and try again.",
                "details": safe_diagnostic[:300],
                "code": "RATE_LIMITED"
            }), 429

        # Specific handling for Authentication / Invalid Key
        if "401" in exc_str or "403" in exc_str or "unauthenticated" in exc_str or "api key not valid" in exc_str or "api_key_invalid" in exc_str:
            return jsonify({
                "success": False,
                "error": "Authentication failed with the ghost realm. Please verify that GEMINI_API_KEY in your Vercel settings is a valid key from Google AI Studio.",
                "details": safe_diagnostic[:300],
                "code": "AUTH_ERROR"
            }), 502

        # Specific handling for Timeouts / Deadline Exceeded
        if "deadline" in exc_str or "timeout" in exc_str or "timed out" in exc_str:
            return jsonify({
                "success": False,
                "error": "The spirits took too long to answer from the void. Please try again with a shorter length option.",
                "details": safe_diagnostic[:300],
                "code": "TIMEOUT"
            }), 504

        # Model not found or unavailable
        if "not found" in exc_str or "not supported" in exc_str:
            return jsonify({
                "success": False,
                "error": "The selected AI model is currently unavailable for this API key. Please check your Google AI Studio project settings.",
                "details": safe_diagnostic[:300],
                "code": "MODEL_UNAVAILABLE"
            }), 502

        # General server error (protect internal secrets and stack trace)
        return jsonify({
            "success": False,
            "error": "The ghost realm is temporarily unavailable. Please try again shortly.",
            "details": safe_diagnostic[:300],
            "code": "PROVIDER_ERROR"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    print(f"👻 AI Ghost Story Generator starting on http://127.0.0.1:{port}")
    print(f"🔮 AI Provider: Google Gemini ({GEMINI_MODEL})")
    print(f"🔑 GEMINI_API_KEY Configured: {'Yes' if os.environ.get('GEMINI_API_KEY') else 'No (set GEMINI_API_KEY in .env)'}")
    app.run(host="0.0.0.0", port=port, debug=debug)
