# AI Ghost Story Generator 👻

> **"Turn Your Imagination into Terrifying Ghost Stories!"**

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask: 3.x](https://img.shields.io/badge/Flask-3.x-black.svg)](https://flask.palletsprojects.com/)
[![Ollama: llama3.2:3b](https://img.shields.io/badge/AI-Ollama%20%7C%20llama3.2%3A3b-orange.svg)](https://ollama.com)
[![Tests: Passing](https://img.shields.io/badge/Tests-12%20Passed-brightgreen.svg)](test_app.py)

AI Ghost Story Generator is a complete, full-stack open-source web application designed for creative storytelling and AI hackathons. It transforms simple seeds, eerie locations, nightmares, or strange childhood memories into rich, original ghost stories using open-weight AI models executed locally through **Ollama** (`llama3.2:3b`), framed inside a cinematic gothic user interface with visible, animated ghost characters.

---

## 📖 Table of Contents

1. [Project Overview & Problem Statement](#-project-overview--problem-statement)
2. [Key Features](#-key-features)
3. [Haunted Design & Ghost Animations](#-haunted-design--ghost-animations)
4. [Technology Stack](#-technology-stack)
5. [How AI Generation Works](#-how-ai-generation-works)
6. [Why Open-Weight AI Matters & Privacy](#-why-open-weight-ai-matters--privacy)
7. [Screenshots & Visuals](#-screenshots--visuals)
8. [Prerequisites](#-prerequisites)
9. [Installation & Setup](#-installation--setup)
   - [Windows (PowerShell)](#windows-powershell)
   - [macOS / Linux](#macos--linux)
10. [Running the Application](#-running-the-application)
11. [Running Automated Tests](#-running-automated-tests)
12. [Troubleshooting Guide](#-troubleshooting-guide)
13. [Project Structure](#-project-structure)
14. [Deployment Considerations](#-deployment-considerations)
15. [Contributing & Future Enhancements](#-contributing--future-enhancements)
16. [License](#-license)

---

## 🌌 Project Overview & Problem Statement

### The Problem
Most AI writing applications either rely on expensive, proprietary cloud APIs with recurring subscription fees, store private prompts on remote third-party servers, or present bland, static user interfaces that lack atmosphere and emotional immersion.

### The Solution
**AI Ghost Story Generator** brings creative horror writing directly to the user's local machine:
- **100% Free & Open-Weight**: Uses Meta's `llama3.2:3b` model executed locally via **Ollama**. No credit cards, token billing, or paid API keys required.
- **Device-Level Privacy**: In its default local configuration, all story ideas and generated narratives remain on your own machine.
- **Cinematic Atmosphere**: Features an animated haunted mansion, a glowing full moon, drifting fog waves, and multiple distinct CSS and SVG ghost characters that visibly float and walk across the screen.

---

## ⚡ Key Features

- **Real Open-Weight AI Generation**: Connects to the local Ollama REST API (`/api/generate`) with temperature-tuned prompt engineering.
- **🇬🇧 English & 🇮🇳 Hindi Bilingual Storytelling**: Native generation in English and natural Devanagari Hindi (हिन्दी) with language-specific prompts and formatting markers.
- **🔊 Scary Voice Narration (Web Speech API)**:
  - Reads generated stories aloud in natural pronunciation matching the selected language.
  - Automatically selects native Hindi voices (like Google हिन्दी, Microsoft Kalpana/Hemant) or deep suspenseful English voices (David, Mark, Guy).
  - Sentence chunking queue prevents browser TTS timeouts on long stories.
  - Controls: **Listen to Story**, **Pause**, **Resume**, **Stop**, and **Replay**.
  - Animated sound-wave visualizer and glowing active player state.
  - Pitch (Low/Normal/High) and Speed (Slow/Normal/Fast) controls tailored for horror pacing.
- **👻 Haunted Atmosphere Ambience (Web Audio API)**:
  - Zero external sound files or copyright issues! Synthesizes eerie gusting wind and a deep 55Hz sub-bass supernatural drone procedurally.
  - Independent volume slider and toggle switch.
  - Synchronizes with narration play, pause, and stop states.
- **Optional Auto-Play Narration**: Automatically begins reading aloud upon generation when enabled (OFF by default).
- **6 Horror Sub-Genres**:
  - 🏚️ *Haunted House* (Gothic dread, creaking floorboards, cursed architecture)
  - 🔍 *Ghost Mystery* (Investigative intrigue, eerie clues, forgotten tragedies)
  - 🌲 *Ancient Folklore* (Generational curses, woodland spirits, timeless legends)
  - 👁️ *Supernatural Horror* (Cold chills, uncanny phenomena, unrelenting suspense)
  - 🎃 *Halloween Adventure* (Autumn nights, flickering jack-o'-lanterns, mischievous spirits)
  - 💔 *Emotional Ghost Story* (Bittersweet apparitions, lingering memories, poignant sorrow)
- **Flexible Story Lengths**:
  - *Short*: ~180–250 words (2–3 punchy paragraphs)
  - *Medium*: ~350–500 words (4–5 suspenseful paragraphs)
  - *Long*: ~650–850 words (6–8 narrative paragraphs)
- **Custom or AI-Crafted Titles**: Provide your own story title or let the AI generate an evocative, chilling name.
- **"Surprise Me 👻" Generator**: Instant inspiration with 21 curated spine-chilling story ideas in English and Hindi.
- **Magical Summoning Loading State**: Displays rotating arcane rune rings, a summoning spirit, and glowing progress indicators while the AI creates the story.
- **One-Click Export**:
  - 📋 **Copy Story**: Formats title and story for clipboard with instant visual confirmation.
  - 💾 **Download as TXT**: Clean client-side `.txt` file export with metadata header.
- **Safe DOM Rendering**: Stories are injected securely using `textContent` and paragraph nodes to prevent XSS vulnerabilities.
- **Mobile Responsive & Accessible**: Full support for screen readers, keyboard navigation, and `prefers-reduced-motion` accommodations.

---

## 👻 Haunted Design & Ghost Animations

The application features multiple independent CSS keyframe-animated ghost characters rendered as inline vector SVGs:

1. **Walking Ghost (Essential - Screen Journey)**:
   - Fixed along the bottom of the viewport (`bottom: 24px; z-index: 15`).
   - Uses a two-layer animation hierarchy:
     - Outer track translates horizontally across the entire screen from `translateX(-160px)` (outside left edge) to `translateX(calc(100vw + 160px))` (outside right edge) over a 20-second loop.
     - Inner nested bobber executes an independent vertical walking bob (`translateY(-18px)` every 0.65s) with a swaying tail and expanding ground shadow, ensuring horizontal and vertical movements never conflict.
   - Guarded with `overflow-x: hidden` and `pointer-events: none` so it never creates horizontal scrollbars or blocks clicks.
2. **Hero Floating Ghost**:
   - A large, cute-but-spooky white ghost in the hero section with a soft violet glowing aura (`drop-shadow`).
   - Floats up and down (`translateY(-36px)`), sways gently side-to-side, subtly tilts (`rotate(-4deg)` to `rotate(4deg)`), and blinks its glowing purple pupils.
3. **Flying Ghost**:
   - Glides diagonally across the hero sky (`flyingGhostDiagonal`) with subtle scale and opacity breathing.
4. **Interactive Assistant Ghost**:
   - Stationed beside the story generator card.
   - Bounces excitedly on hover and updates its speech bubble (*"Boo! Ready for a scary story?"*).
   - Clicking it populates the story idea textarea with a random spooky prompt accompanied by a ghostly glowing ripple effect.
5. **Background Drifting Ghosts**:
   - Three translucent spectral figures floating across the How It Works, Open-Source AI, and About sections with staggered durations (8s, 12s, 10s).
6. **Footer Ghost**:
   - A playful spirit drifting peacefully across the site footer.
7. **Haunted Scenery**:
   - Detailed gothic mansion SVG silhouette with flickering amber candlelight in the arched windows.
   - Glowing full moon with radial aura and crater depth.
   - Three layers of semi-transparent drifting fog moving at different speeds.
   - Floating supernatural spirit particles rising towards the sky.
   - Infrequent, subtle background lightning glow designed to be non-intense and accessible.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JS | Zero external framework overhead; pure semantic HTML and modular CSS. |
| **Typography** | Google Fonts | `Cinzel Decorative` for gothic titles; `Plus Jakarta Sans` for clean body readability. |
| **Backend** | Python 3.10+, Flask 3.x | Lightweight REST API with validation, prompt construction, and error handling. |
| **AI Runtime** | Ollama | Local inference server (`http://127.0.0.1:11434/api/generate`). |
| **Default Model** | `llama3.2:3b` | Open-weight 3-billion parameter model by Meta; fast and creative on consumer hardware. |
| **HTTP Client** | `requests` | Handles REST calls to Ollama with timeout protection. |
| **Testing** | `pytest` | 12 automated unit and integration tests with mocked Ollama responses. |

---

## 🧠 How AI Generation Works

1. **User Input**: The user selects a story idea, horror category, and desired length.
2. **Prompt Engineering (`app.py`)**: The backend builds a specialized prompt injecting:
   - The user's story seed.
   - Specific stylistic tone guidelines tailored to the chosen sub-genre.
   - Paragraph and word-count targets based on the requested length.
   - Title generation instructions or user custom title preservation.
   - Output delimiter tags: `Title: <title>\nStory:\n<story>`.
3. **Local Inference**: Flask posts the request to `http://127.0.0.1:11434/api/generate` with `stream: False`, `temperature: 0.8`, and `top_p: 0.9`.
4. **Robust Parsing (`parse_ai_response`)**: Handles variations in model responses (markdown headers, missing tags, or raw text) and cleans up formatting safely.
5. **Safe Display (`script.js`)**: The frontend receives structured JSON and inserts text into DOM nodes using `textContent` and paragraph elements, completely avoiding `innerHTML` risks.

---

## 🔒 Why Open-Weight AI Matters & Privacy

- **Data Privacy**: When using the default local setup (`OLLAMA_URL=http://127.0.0.1:11434`), your prompts and generated stories never leave your local device.
- **Cost Independence**: Run thousands of creative prompts without per-token charges or monthly subscription tiers.
- **Customizability**: You can modify system prompts, change model temperatures, or swap models (e.g., `qwen2.5:3b`, `mistral:7b`, `phi3:mini`) with a single environment variable change.
- **Offline Capable**: Once Ollama and the model weights are downloaded, the entire generation process can run completely offline without an internet connection.

---

## 📸 Screenshots & Visuals

*(Screenshots can be captured and placed into `static/images/`)*

| Desktop Hero View | Story Generator & Magical Summoning |
| :---: | :---: |
| *Full moon, floating ghost, gothic mansion* | *Arcane loading runes, interactive ghost* |

---

## 📋 Prerequisites

Before running the application, make sure you have:
1. **Python 3.10 or higher** installed.
2. **Ollama** installed from [ollama.com](https://ollama.com).
3. The default model downloaded:
   ```bash
   ollama pull llama3.2:3b
   ```

---

## 🚀 Installation & Setup

### Windows (PowerShell)

1. Clone or navigate to the project directory:
   ```powershell
   cd "ai-ghost-story-generator"
   ```

2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install required Python packages:
   ```powershell
   pip install -r requirements.txt
   ```

4. Verify Ollama is running and download the model:
   ```powershell
   ollama pull llama3.2:3b
   ```

5. (Optional) Create your custom environment file:
   ```powershell
   Copy-Item .env.example .env
   ```

---

### macOS / Linux

1. Navigate to the project directory:
   ```bash
   cd ai-ghost-story-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Pull the model:
   ```bash
   ollama pull llama3.2:3b
   ```

---

## 🎮 Running the Application

Start the Flask server:
```bash
python app.py
```

You should see output similar to:
```text
👻 AI Ghost Story Generator starting on http://127.0.0.1:5000
🔮 Ollama target: http://127.0.0.1:11434 (Model: llama3.2:3b)
 * Running on http://127.0.0.1:5000
```

Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

The project includes automated tests for endpoint validation, connection error handling, timeouts, and mocked AI responses. The tests do not require the Ollama server to be running.

Run the test suite with `pytest`:
```bash
pytest -v test_app.py
```

Or run directly with Python:
```bash
python test_app.py
```

Expected output:
```text
test_app.py::test_homepage_loads PASSED                                  [  8%]
test_app.py::test_health_endpoint_healthy PASSED                         [ 16%]
test_app.py::test_health_endpoint_ollama_disconnected PASSED             [ 25%]
test_app.py::test_generate_non_json_request PASSED                       [ 33%]
test_app.py::test_generate_missing_idea PASSED                           [ 41%]
test_app.py::test_generate_invalid_category PASSED                       [ 50%]
test_app.py::test_generate_invalid_length PASSED                         [ 58%]
test_app.py::test_generate_connection_failure PASSED                     [ 66%]
test_app.py::test_generate_timeout_failure PASSED                        [ 75%]
test_app.py::test_generate_success_mocked_ollama PASSED                  [ 83%]
test_app.py::test_generate_custom_title_honored PASSED                   [ 91%]
test_app.py::test_parse_ai_response_edge_cases PASSED                    [100%]

============================= 12 passed in 0.12s ==============================
```

---

## 🩺 Troubleshooting Guide

### 1. "The ghost realm is currently unreachable..." (HTTP 503)
- **Cause**: Ollama is not running on your machine or is bound to a different port.
- **Solution**:
  1. Open a new terminal and run `ollama serve`.
  2. Verify Ollama responds by opening `http://127.0.0.1:11434` in your browser (it should display *"Ollama is running"*).
  3. Check the health check endpoint: `http://127.0.0.1:5000/health`.

### 2. "The spirits took too long to answer..." (HTTP 504)
- **Cause**: Generating longer stories on a CPU can take between 45–90 seconds depending on system specs.
- **Solution**:
  - Choose the **Short** story length option.
  - Increase the timeout in your `.env` file:
    ```env
    REQUEST_TIMEOUT=120
    ```

### 3. Model Not Found Error
- **Cause**: The model `llama3.2:3b` has not been downloaded yet.
- **Solution**:
  ```bash
  ollama pull llama3.2:3b
  ```

### 4. Port 5000 Already in Use
- **Cause**: Another service is using port 5000.
- **Solution**: Set a different port in `.env`:
  ```env
  PORT=5050
  ```

---

## 📂 Project Structure

```text
ai-ghost-story-generator/
│
├── app.py                  # Main Flask application and Ollama integration
├── test_app.py             # Automated unit & integration test suite (12 tests)
├── requirements.txt        # Python package dependencies
├── .env.example            # Documented environment configuration template
├── .gitignore              # Git ignore rules for Python, virtualenvs, & caches
├── LICENSE                 # MIT Open-Source License
├── README.md               # Comprehensive project documentation
├── SUBMISSION.md           # Hackathon / Challenge submission template
│
├── templates/
│   └── index.html          # Semantic HTML5 template with SVG ghost characters
│
├── static/
│   ├── css/
│   │   └── style.css       # Complete haunted design tokens & ghost keyframe animations
│   ├── js/
│   │   └── script.js       # Client-side validation, interactive ghost, API fetch, export
│   └── images/             # Static screenshots and graphics directory
│
└── tests/
    └── __init__.py         # Test package initializer
```

---

## 🌐 Deployment Considerations

- **Architecture Distinction**: The Flask frontend/backend and the Ollama AI model are separate decoupled components. Standard serverless Flask hosts (e.g. Vercel, Render free tier) do not provide local GPUs or Ollama runtimes.
- **Production Deployment Options**:
  1. **Self-Hosted VPS**: Deploy Flask and Ollama on a GPU/CPU VPS (such as DigitalOcean, AWS EC2, or Hetzner).
  2. **Remote Ollama Service**: Set `OLLAMA_URL=https://your-secured-ollama-instance.com` in environment variables.
  3. **Security**: Never expose an unauthenticated Ollama API endpoint publicly without a reverse proxy (Nginx/Caddy) with HTTPS and authentication.

---

## 🤝 Contributing & Future Enhancements

Contributions are welcome! Potential future improvements include:
- [ ] Integration of local open-source Text-to-Speech (TTS) for eerie story audio narration.
- [ ] Additional horror sub-genres (Cosmic Horror, Cyberpunk Spirits, Urban Legends).
- [ ] Atmospheric audio toggle (subtle rain and wind soundscapes).
- [ ] Story history saved to local storage (`localStorage`).

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for complete details.
