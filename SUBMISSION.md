# Hackathon & Challenge Submission: AI Ghost Story Generator 👻

### Project Details
- **Project Name:** AI Ghost Story Generator
- **Repository Name:** `ai-ghost-story-generator`
- **GitHub Repository URL:** `https://github.com/anubhav9236/ai-ghost-story-generator`
- **Demo / Hosted URL:** *[Local demonstration on http://127.0.0.1:5000 - Public deployment pending self-hosted GPU/Ollama instance]*
- **Challenge / Hackathon Submission URL:** *[Challenge Submission URL Placeholder]*

---

### Project Description

AI Ghost Story Generator is an open-source AI web application that transforms user-provided ideas into original ghost stories. Built with Flask and Ollama, it combines real open-weight AI generation with a spooky animated user interface featuring floating ghosts, walking ghosts, haunted backgrounds, and interactive storytelling.

---

### AI Technology & Runtime

The application uses the Ollama runtime with the `llama3.2:3b` model to generate stories based on user prompts, selected horror categories, and story-length preferences. 

The backend employs tailored prompt engineering to instruct the model with genre-specific atmospheric tones (from gothic dread in Haunted House to poignant sorrow in Emotional Ghost Story) and length guidelines, returning structured output parsed cleanly into story titles and narrative chapters.

---

### Open-Source Benefits

The project demonstrates how developers can customize prompts, inspect the application code, and experiment with locally executed open-weight AI models without requiring a paid AI API.

By running the open-weight model through Ollama:
- Developers avoid recurring third-party token fees.
- User story ideas remain private on the user's local device.
- Developers can swap models (`mistral`, `qwen2.5`, `phi3`) or modify prompt templates without altering the core frontend architecture.

---

### Key Visual & Audio Features
- **Horror Voice Narration (Web Speech API):** Reads generated stories aloud in natural English and Hindi (Devanagari) pronunciation with customizable speed (slow/normal/fast) and ominous low pitch. Includes Listen, Pause, Resume, Stop, and Replay controls, plus an optional Auto-Play setting.
- **Procedural Haunted Atmosphere (Web Audio API):** Synthesizes subtle howling wind and a 55Hz sub-bass drone entirely in the browser without external audio downloads or copyright concerns. Includes an independent volume slider and toggle.
- **Walking Ghost across bottom:** Smooth horizontal travel animation (`walkingGhostJourney`) paired with a separate vertical bobbing step animation simulating walking strides without scrollbar overflow.
- **Hero Floating Ghost:** Cute-spooky large SVG ghost with a glowing violet halo, gentle swaying, and blinking pupils.
- **Interactive Story Assistant:** Near the story generator, a ghost that bounces on hover and populates the prompt input with a random spooky idea on click.
- **Haunted Scenery:** Glowing full moon with radial aura, detailed gothic mansion silhouette with flickering candlelight windows, multi-layered drifting fog, and subtle, accessible lightning flashes.
- **Magical Loading State:** Animated arcane rune rings rotating in opposite directions around a summoning ghost while the model generates the story.

---

### Screenshots

*(Add your screenshots here before final submission)*

- **Hero Screen:** `![Hero Screen](static/images/screenshot-hero.png)` *(Placeholder)*
- **Story Generator & Result Card:** `![Story Result](static/images/screenshot-result.png)` *(Placeholder)*

---

### How to Run Locally

```bash
# 1. Pull the open-weight model in Ollama
ollama pull llama3.2:3b

# 2. Set up Python environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # On Windows PowerShell
pip install -r requirements.txt

# 3. Launch Flask server
python app.py

# 4. Open in browser
http://127.0.0.1:5000
```
