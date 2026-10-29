"""
Unit and integration tests for AI Ghost Story Generator Flask application.
All tests use mocking so that tests execute rapidly without requiring live Google Gemini credentials.
"""

import os
from unittest.mock import patch, MagicMock
import pytest

from app import app, ALLOWED_CATEGORIES, ALLOWED_LENGTHS, parse_ai_response, construct_prompt, is_rate_limited, _rate_limit_records


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    _rate_limit_records.clear()
    with app.test_client() as client:
        yield client


def test_homepage_loads(client):
    """Confirm the homepage renders successfully with HTTP 200 and expected title."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "AI Ghost Story Generator" in html
    assert "Create Your Own Nightmare" in html


def test_health_endpoint_configured(client):
    """Confirm the health check endpoint returns 200 when GEMINI_API_KEY is configured."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_test_key_12345"}):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["flask"] == "healthy"
        assert data["provider"] == "google-gemini"
        assert data["api_key_configured"] is True


def test_health_endpoint_unconfigured(client):
    """Confirm the health check endpoint reports unconfigured when GEMINI_API_KEY is missing."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["flask"] == "healthy"
        assert data["api_key_configured"] is False


def test_generate_non_json_request(client):
    """Confirm non-JSON requests are rejected with HTTP 400."""
    response = client.post("/generate", data="plain text data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Request body must be JSON" in data["error"]
    assert data["code"] == "INVALID_JSON"


def test_generate_missing_idea(client):
    """Confirm missing or too short idea is rejected with HTTP 400."""
    response = client.post(
        "/generate",
        json={"idea": "", "category": "Haunted House", "length": "Short"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "at least 3 characters" in data["error"]
    assert data["code"] == "INPUT_TOO_SHORT"


def test_generate_oversized_idea(client):
    """Confirm idea exceeding 2000 characters is rejected with HTTP 400."""
    oversized_idea = "A" * 2001
    response = client.post(
        "/generate",
        json={"idea": oversized_idea, "category": "Haunted House", "length": "Short"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "exceeds maximum allowed length" in data["error"]
    assert data["code"] == "INPUT_TOO_LONG"


def test_generate_invalid_category(client):
    """Confirm invalid category is rejected with HTTP 400."""
    response = client.post(
        "/generate",
        json={"idea": "An abandoned hospital", "category": "Romantic Comedy", "length": "Short"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Invalid category" in data["error"]
    assert data["code"] == "INVALID_CATEGORY"


def test_generate_invalid_length(client):
    """Confirm invalid length is rejected with HTTP 400."""
    response = client.post(
        "/generate",
        json={"idea": "An abandoned lighthouse", "category": "Ghost Mystery", "length": "Gigantic"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Invalid length" in data["error"]
    assert data["code"] == "INVALID_LENGTH"


def test_generate_missing_api_key(client):
    """Confirm missing GEMINI_API_KEY returns HTTP 500 with configuration guidance."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
        response = client.post(
            "/generate",
            json={
                "idea": "A phantom train on abandoned tracks.",
                "category": "Supernatural Horror",
                "length": "Short"
            }
        )
        assert response.status_code == 500
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "MISSING_API_KEY"
        assert "GEMINI_API_KEY is not set" in data["error"]


def test_generate_gemini_api_error(client):
    """Confirm general Gemini API error returns HTTP 500 with safe error message."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.models.generate_content.side_effect = Exception("Internal RPC failure")
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/generate",
                json={
                    "idea": "An antique mirror reflecting an empty room.",
                    "category": "Haunted House",
                    "length": "Short"
                }
            )
            assert response.status_code == 500
            data = response.get_json()
            assert data["success"] is False
            assert data["code"] == "PROVIDER_ERROR"
            assert "temporarily unavailable" in data["error"]


def test_generate_gemini_rate_limit_rescued_by_lore_engine(client):
    """Confirm Gemini rate limit error (429 / resource exhausted) is rescued by Lore Engine returning HTTP 200."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.models.generate_content.side_effect = Exception("429 ResourceExhausted: Quota exceeded")
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/generate",
                json={
                    "idea": "A whispering well in the deep woods.",
                    "category": "Ancient Folklore",
                    "length": "Short"
                }
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data.get("is_failsafe") is True
            assert "Ancient Folklore" == data["category"]
            assert len(data["story"]) > 50


def test_generate_cursed_code_category(client):
    """Confirm Cursed Code horror category generates successfully."""
    mock_llm_text = (
        "Title: Segmentation Fault in the Soul\n"
        "Story:\n"
        "The terminal flickered at 3:33 AM.\n\n"
        "```c\nvoid* daemon = allocate_shadow();\n```\n\n"
        "The cursor moved without a hand on the mouse."
    )
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.text = mock_llm_text
            mock_client.models.generate_content.return_value = mock_response
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/generate",
                json={
                    "idea": "A Python script that auto-completes names of people who will die tonight.",
                    "category": "Cursed Code",
                    "length": "Short"
                }
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["category"] == "Cursed Code"
            assert "Segmentation Fault" in data["title"]


def test_generate_gemini_timeout(client):
    """Confirm Gemini timeout returns HTTP 504."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.models.generate_content.side_effect = Exception("Deadline exceeded / timed out waiting for response")
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/generate",
                json={
                    "idea": "A ticking clock in an empty room.",
                    "category": "Ghost Mystery",
                    "length": "Long"
                }
            )
            assert response.status_code == 504
            data = response.get_json()
            assert data["success"] is False
            assert data["code"] == "TIMEOUT"


def test_generate_success_mocked_gemini(client):
    """Confirm successful English story generation with mocked Gemini response."""
    mock_llm_text = (
        "Title: The Whispering Gallery\n"
        "Story:\n"
        "The dust in the forgotten wing of Ashburn Hall hung motionless until midnight.\n\n"
        "Elena took three hesitant steps onto the cracked marble. That was when she heard her own name "
        "whispered back to her, spoken in a voice she had buried twenty years ago."
    )

    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.text = mock_llm_text
            mock_client.models.generate_content.return_value = mock_response
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/generate",
                json={
                    "idea": "An old mirror that reflects someone standing right behind you.",
                    "category": "Haunted House",
                    "length": "Short"
                }
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["title"] == "The Whispering Gallery"
            assert "Ashburn Hall" in data["story"]
            assert data["category"] == "Haunted House"
            assert data["length"] == "Short"
            assert "gemini" in data["model"].lower()


def test_generate_hindi_success_mocked_gemini(client):
    """Confirm successful Hindi story generation with mocked Gemini response."""
    mock_hindi_text = (
        "शीर्षक: पुरानी हवेली का साया\n"
        "कहानी:\n"
        "रात के बारह बजते ही हवेली के पुराने शीशम के दरवाजे खुद-ब-खुद चरमराने लगे।\n\n"
        "रोहन ने जैसे ही कदम आगे बढ़ाया, उसे महसूस हुआ कि अंधेरे में कोई उसका नाम फुसफुसा रहा था।"
    )

    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.text = mock_hindi_text
            mock_client.models.generate_content.return_value = mock_response
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/generate",
                json={
                    "idea": "एक पुरानी हवेली जहाँ आधी रात को घुंघरू की आवाज आती है।",
                    "category": "Haunted House",
                    "length": "Short",
                    "language": "Hindi"
                }
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert "पुरानी हवेली" in data["title"]
            assert "रोहन" in data["story"]
            assert data["language"] == "Hindi"


def test_generate_custom_title_honored(client):
    """Confirm custom title supplied by user is used in the response."""
    mock_llm_text = (
        "Title: Some Gemini Title\n"
        "Story:\n"
        "The bell in the chapel tower tolled without a rope."
    )

    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.text = mock_llm_text
            mock_client.models.generate_content.return_value = mock_response
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/generate",
                json={
                    "idea": "The church bell that rings on stormy nights.",
                    "category": "Ghost Mystery",
                    "length": "Short",
                    "title": "Midnight Toll of Sorrow"
                }
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data["success"] is True
            assert data["title"] == "Midnight Toll of Sorrow"


def test_parse_ai_response_edge_cases():
    """Verify response parsing handles varied markdown formatting gracefully in English and Hindi."""
    # Case 1: Markdown headers
    text1 = "### Title: The Crimson Lantern\n\n**Story:**\nIn the deep woods, the red glow lingered."
    t1, s1 = parse_ai_response(text1)
    assert t1 == "The Crimson Lantern"
    assert "In the deep woods" in s1

    # Case 2: No explicit story marker
    text2 = "Title: Shadows in the Fog\nOnce upon a dark road, the lantern flickered out."
    t2, s2 = parse_ai_response(text2)
    assert t2 == "Shadows in the Fog"
    assert "Once upon a dark road" in s2

    # Case 3: Custom title overrides
    t3, s3 = parse_ai_response("Just raw story text without markers.", custom_title="Custom Dread")
    assert t3 == "Custom Dread"
    assert "Just raw story text" in s3

    # Case 4: Devanagari Hindi markers (शीर्षक / कहानी)
    text4 = "शीर्षक: खामोश कब्रिस्तान\nकहानी:\nकब्रिस्तान के सन्नाटे में एक सफेद परछाईं तैर रही थी।"
    t4, s4 = parse_ai_response(text4)
    assert t4 == "खामोश कब्रिस्तान"
    assert "कब्रिस्तान के सन्नाटे" in s4


def test_rate_limiter_exceeded(client):
    """Verify client IP rate limiter triggers HTTP 429 when threshold is reached."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_123"}):
        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Title: Quick Tale\nStory:\nA quick ghost story."
            mock_client.models.generate_content.return_value = mock_response
            mock_client_cls.return_value = mock_client

            payload = {
                "idea": "A recurring shadow in the hallway.",
                "category": "Supernatural Horror",
                "length": "Short"
            }

            # Send 10 requests (the allowed max per minute)
            for _ in range(10):
                res = client.post("/generate", json=payload)
                assert res.status_code == 200

            # The 11th request must be rate limited
            res_limited = client.post("/generate", json=payload)
            assert res_limited.status_code == 429
            data = res_limited.get_json()
            assert data["code"] == "RATE_LIMITED"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
