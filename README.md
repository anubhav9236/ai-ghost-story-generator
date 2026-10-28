# AI Ghost Story Generator 👻

> **"Turn Your Imagination into Terrifying Ghost Stories!"**

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask: 3.x](https://img.shields.io/badge/Flask-3.x-black.svg)](https://flask.palletsprojects.com/)
[![Google Gemini API: gemini-2.5-flash](https://img.shields.io/badge/AI-Google%20Gemini%20%7C%20gemini--2.5--flash-blue.svg)](https://ai.google.dev)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black.svg)](https://vercel.com)
[![Tests: Passing](https://img.shields.io/badge/Tests-17%20Passed-brightgreen.svg)](test_app.py)

**AI Ghost Story Generator** is an open-source, production-ready web application designed for creative gothic storytelling. It transforms simple seeds, eerie locations, nightmares, or strange childhood memories into rich, original ghost stories in both **English and Hindi (हिन्दी)** using the **Google Gemini API** (`gemini-2.5-flash`).

Built with a responsive cinematic gothic user interface, it features animated ghost characters, scary horror voice narration (Web Speech API), and procedurally synthesized haunted atmospheric wind and sub-bass drones (Web Audio API)—accessible from any mobile phone, tablet, or desktop with **zero software installation required for visitors**.

---

## 📖 Table of Contents

1. [Key Features](#-key-features)
2. [Architecture & Vercel Serverless](#-architecture--vercel-serverless)
3. [Technology Stack](#-technology-stack)
4. [Google Gemini API Integration](#-google-gemini-api-integration)
5. [API Key Security & Environment Variables](#-api-key-security--environment-variables)
6. [Abuse Prevention & Rate Limiting](#-abuse-prevention--rate-limiting)
7. [Installation & Local Setup](#-installation--local-setup)
8. [Vercel Deployment Guide](#-vercel-deployment-guide)
9. [Running Automated Tests](#-running-automated-tests)
10. [Troubleshooting Guide](#-troubleshooting-guide)
11. [License](#-license)

---

## ⚡ Key Features

- **Production Cloud AI Generation**: Powered by the official Google GenAI SDK (`gemini-2.5-flash`) for responsive, high-fidelity gothic horror generation.
- **🇬🇧 English & 🇮🇳 Hindi Bilingual Storytelling**: Native generation in English and natural Devanagari Hindi (हिन्दी) with culturally authentic folklore prompts.
- **🔊 Scary Voice Narration (Web Speech API)**:
  - Reads stories aloud in an ominous cadence with sentence chunking queue to prevent browser TTS cutoffs.
  - Controls: **Listen to Story**, **Pause**, **Resume**, **Stop**, and **Replay**.
  - Animated sound-wave visualizer and custom pitch/speed horror modulation.
- **👻 Procedural Haunted Ambience (Web Audio API)**:
  - 0 KB audio bundle overhead! Procedurally generates whistling winter wind (pink noise + LFO bandpass filter) and a deep 55Hz supernatural sub-bass drone directly in the browser.
- **Living Haunted Visuals**:
  - Dual-axis walking ghost pacing the viewport with realistic stride physics.
  - Floating spirits with glowing violet halos, full moon, drifting fog waves, and rotating arcane summoning runes.
- **One-Click Export**:
  - 📋 **Copy Story**: Formats title, story body, and metadata for clipboard.
  - 💾 **Download as TXT**: Clean client-side `.txt` export with header.
- **Mobile & Touchscreen Optimized**: Fully responsive layout tested on iOS, Android, macOS, and Windows.

---

## 🏗️ Architecture & Vercel Serverless

The application is architected for zero-configuration serverless deployment on Vercel:

```text
[ Browser / Mobile Client ]
         │
         ▼  HTTPS Request (Same-Origin)
[ Vercel Edge / CDN ]
         │
         ▼  Rewrite (/(.*) -> api/index.py)
[ Python Serverless Function (Flask WSGI) ]
         │
         ├── Rate Limiter (10 req/min per IP)
         ├── Input Validation (Size & Tones)
         │
         ▼  Official google-genai SDK
[ Google Gemini API (gemini-2.5-flash) ]
```

- **`api/index.py`**: Serverless function entrypoint exposing the Flask WSGI instance to Vercel's Python runtime.
- **`app.py`**: Core backend logic handling input validation, prompt engineering, rate limiting, and response parsing.
- **`vercel.json`**: Directs all incoming traffic to `api/index.py`.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JS | Lightweight, semantic, zero-framework overhead. |
| **Backend** | Python 3.10+, Flask 3.x | Lightweight WSGI serverless application. |
| **AI Engine** | Google Gemini API | `gemini-2.5-flash` via official `google-genai` SDK. |
| **Speech** | Web Speech API | Browser-native `window.speechSynthesis` with sentence queue. |
| **Audio** | Web Audio API | In-browser procedural pink noise and sine oscillators. |
| **Deployment** | Vercel Serverless | Python runtime with automated Git CI/CD. |
| **Testing** | `pytest` | 17 unit and integration tests with mocked API clients. |

---

## 🔑 Google Gemini API Integration

The backend interacts with Gemini using the official Google GenAI Python SDK (`google-genai`):

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0.8,
        top_p=0.9,
        max_output_tokens=max_tokens,
    )
)
```

### Supported Story Categories:
1. 🏚️ **Haunted House** (Gothic dread, creaking floorboards, cursed architecture)
2. 🔍 **Ghost Mystery** (Investigative intrigue, forgotten tragedies)
3. 🌲 **Ancient Folklore** (Generational curses, mythical woodland spirits)
4. 👁️ **Supernatural Horror** (Cold spots, uncanny phenomena, relentless suspense)
5. 🎃 **Halloween Adventure** (Crisp autumn nights, pumpkin lanterns, playful thrills)
6. 💔 **Emotional Ghost Story** (Bittersweet apparitions, lingering memories)

---

## 🔒 API Key Security & Environment Variables

### Critical Security Rules:
- **`GEMINI_API_KEY` is strictly server-side.** It is never exposed in client HTML, CSS, JavaScript, API responses, or source maps.
- **`.gitignore`** protects all `.env` files from being committed to version control.
- If the server API key is unconfigured, the API returns a safe HTTP 500 error:
  `"The ghost realm is unconfigured. GEMINI_API_KEY is not set on the server."`

### Obtaining an API Key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click **"Create API Key"** and copy the generated key.

---

## 🛡️ Abuse Prevention & Rate Limiting

To prevent API abuse on public URLs:
- **Input Limits**: Story seeds are restricted to between 3 and 2,000 characters; titles to 120 characters.
- **In-Memory Rate Limiting**: Enforces a maximum of 10 requests per minute per IP address. Exceeded requests receive an HTTP 429 response.
- *Note on Distributed Scaling*: In-memory rate limiting applies per serverless container instance. For enterprise cross-region persistent rate limiting across all concurrent instances, a managed store like Upstash Redis can be integrated.

---

## 💻 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/anubhav9236/ai-ghost-story-generator.git
cd ai-ghost-story-generator
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=5000
```

### 5. Run the Local Server
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🚀 Vercel Deployment Guide

Deploying to Vercel takes less than two minutes:

### Option A: Via GitHub (Recommended)
1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: migrate to Google Gemini API for public Vercel access"
   git push origin main
   ```
2. Go to your [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New Project"**.
3. Import your `ai-ghost-story-generator` repository.
4. In the **Environment Variables** section, add:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** `your_google_gemini_api_key`
   - *(Optional)* **Name:** `GEMINI_MODEL`, **Value:** `gemini-2.5-flash`
5. Click **"Deploy"**. Vercel will build and assign your production HTTPS URL (e.g., `https://ai-ghost-story-generator.vercel.app/`).

---

## 🧪 Running Automated Tests

The test suite validates input parsing, rate limiting, error codes, and mocked Gemini API responses:

```bash
pytest
```

Output:
```text
============================= test session starts =============================
collected 17 items

test_app.py .................                                            [100%]

======================== 17 passed in 3.58s ========================
```

---

## 🔧 Troubleshooting Guide

| Issue | Cause | Resolution |
| :--- | :--- | :--- |
| **HTTP 500: Missing API Key** | `GEMINI_API_KEY` is not set. | Add `GEMINI_API_KEY` in Vercel Project Settings -> Environment Variables and redeploy. |
| **HTTP 429: Rate Limited** | Free-tier Gemini quota or local IP limit reached. | Wait 30-60 seconds before making additional requests. |
| **HTTP 502: Auth Error** | The provided API key is invalid. | Verify your key in [Google AI Studio](https://aistudio.google.com/app/apikey) and re-enter it. |
| **No Audio on Mobile** | Browser audio autoplay policy. | Tap anywhere on the screen or press the **"Listen to Story"** button directly to grant audio permission. |

---

## 📜 License

Released under the **MIT License**. Feel free to use, modify, and distribute for personal and educational projects.
