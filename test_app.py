"""
Unit and integration tests for AI Ghost Story Generator Flask application.
All tests use mocking where necessary so that tests do not require real Ollama service or model.
"""

from unittest.mock import patch, MagicMock
import pytest
import requests

from app import app, ALLOWED_CATEGORIES, ALLOWED_LENGTHS, parse_ai_response, construct_prompt


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage_loads(client):
    """Confirm the homepage renders successfully with HTTP 200 and expected title."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "AI Ghost Story Generator" in html
    assert "Create Your Own Nightmare" in html


def test_health_endpoint_healthy(client):
    """Confirm the health check endpoint returns 200 with structured JSON."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [{"name": "llama3.2:3b"}, {"name": "mistral:latest"}]
        }
        mock_get.return_value = mock_response

        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["flask"] == "healthy"
        assert data["ollama"]["connected"] is True
        assert data["ollama"]["model_available"] is True


def test_health_endpoint_ollama_disconnected(client):
    """Confirm the health check reports disconnected when Ollama is offline without crashing."""
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError("Offline")):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["flask"] == "healthy"
        assert data["ollama"]["connected"] is False
        assert data["ollama"]["model_available"] is False


def test_generate_non_json_request(client):
    """Confirm non-JSON requests are rejected with HTTP 400."""
    response = client.post("/generate", data="plain text data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Request body must be JSON" in data["error"]


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


def test_generate_connection_failure(client):
    """Confirm connection failure to Ollama returns HTTP 503 with helpful user guidance."""
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Refused")):
        response = client.post(
            "/generate",
            json={
                "idea": "A phantom train that only runs when the moon is blood red.",
                "category": "Supernatural Horror",
                "length": "Short"
            }
        )
        assert response.status_code == 503
        data = response.get_json()
        assert data["success"] is False
        assert "The ghost realm is currently unreachable" in data["error"]
        assert "troubleshooting" in data


def test_generate_timeout_failure(client):
    """Confirm Ollama request timeout returns HTTP 504."""
    with patch("requests.post", side_effect=requests.exceptions.Timeout("Timed out")):
        response = client.post(
            "/generate",
            json={
                "idea": "A cursed antique clock that ticks backwards.",
                "category": "Ancient Folklore",
                "length": "Long"
            }
        )
        assert response.status_code == 504
        data = response.get_json()
        assert data["success"] is False
        assert "timed out" in data["error"].lower()


def test_generate_success_mocked_ollama(client):
    """Confirm successful story generation with mocked Ollama response."""
    mock_llm_text = (
        "Title: The Whispering Gallery\n"
        "Story:\n"
        "The dust in the forgotten wing of Ashburn Hall hung motionless until midnight.\n\n"
        "Elena took three hesitant steps onto the cracked marble. That was when she heard her own name "
        "whispered back to her, spoken in a voice she had buried twenty years ago."
    )

    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": mock_llm_text}
        mock_post.return_value = mock_response

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


def test_generate_custom_title_honored(client):
    """Confirm custom title supplied by user is used in the response."""
    mock_llm_text = (
        "Title: Some AI Generated Title\n"
        "Story:\n"
        "The bell in the chapel tower toll without a rope."
    )

    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": mock_llm_text}
        mock_post.return_value = mock_response

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


def test_generate_hindi_success_mocked_ollama(client):
    """Confirm successful Hindi story generation with mocked Ollama response."""
    mock_hindi_text = (
        "शीर्षक: पुरानी हवेली का साया\n"
        "कहानी:\n"
        "रात के बारह बजते ही हवेली के पुराने शीशम के दरवाजे खुद-ब-खुद चरमराने लगे।\n\n"
        "रोहन ने जैसे ही कदम आगे बढ़ाया, उसे महसूस हुआ कि अंधेरे में कोई उसका नाम फुसफुसा रहा था।"
    )

    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": mock_hindi_text}
        mock_post.return_value = mock_response

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


if __name__ == "__main__":
    pytest.main(["-v", __file__])

