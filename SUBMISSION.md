# AI Ghost Story Generator: Bringing Gothic Folklore to Life with Local Open-Weight LLMs, Hindi Support & Horror Voice Narration 👻

_This is a submission for the [MLH x DEV Writing Challenge](https://dev.to/mlh-hackathon)_

<!-- Make sure you're signed in to DEV with the MLH account linked to your hackathon registration! -->

---

## What I Built

**AI Ghost Story Generator** is an open-source, full-sensory horror storytelling web application. It transforms simple seeds, late-night thoughts, eerie childhood memories, or urban folklore into chilling, original ghost stories in both **English and Hindi (हिन्दी)**.

Instead of treating AI as a sterile chatbot in a plain white box, I set out to make the machine feel genuinely *haunted*. When you summon a story, you don't just receive text—you enter an immersive, multisensory gothic experience:

1. **Cloud-Native Google Gemini AI Generation:** Powered by Google's flagship `gemini-2.5-flash` model using the modern `google-genai` SDK on a serverless Vercel Python runtime. It supports 6 distinct horror sub-genres (Haunted House, Ghost Mystery, Ancient Folklore, Supernatural Horror, Halloween Adventure, and Emotional Ghost Story) across 3 configurable story lengths, running on any smartphone or browser with zero software downloads.
2. **Scary Horror Voice Narration:** Built on the browser's native **Web Speech API (`speechSynthesis`)**, featuring sentence-level chunking to eliminate browser synthesis cutoffs, pitch and speed modulation for an authentic campfire cadence, and dedicated support for Hindi voices (Google हिन्दी, Microsoft Kalpana/Hemant).
3. **Procedural Haunted Ambience (0 KB External Audio):** Uses the **Web Audio API** to synthesize procedural gusting wind (via pink noise and LFO-modulated biquad filters) and a 55Hz sub-bass supernatural drone directly in the browser—with zero external audio files or copyright concerns.
4. **Living Haunted Visual Canvas:** Pure CSS keyframe animations featuring an animated walking ghost traversing the viewport with synchronized vertical stride physics, floating spirits with glowing halos, a gothic mansion silhouette with flickering candlelight, drifting multi-tier fog, and arcane summoning runes.
5. **Writer-First Utilities:** One-click clipboard copy, client-side `.txt` story file downloads with formatted headers, and a "Surprise Me 👻" inspiration bank containing 21 curated horror seeds.

### What Inspired It?
Growing up, hearing ghost stories around a campfire or listening to grandmother's folklore on dark stormy nights was an unforgettable experience. Today, most generative AI applications feel like corporate spreadsheets or sanitized chatbots. Furthermore, running local models requires beefy laptops with GBs of VRAM, cutting off billions of mobile phone users.

I wanted to bridge this divide: take the immersive gothic design, procedural soundscapes, and bilingual Hindi/English folklore, and connect it to Google's ultra-fast, state-of-the-art **Gemini 2.5 Flash** API on serverless infrastructure. Now, anyone opening the link on an iPhone, Android, or laptop can generate rich horror fiction instantly without installing anything.

### What I Learned Along the Way
- **Migrating to the Unified Google Gen AI SDK:** Upgrading from legacy generative AI packages to the official `google-genai` SDK (`from google import genai`) allowed seamless structured prompt generation, token budgeting, and native safety handling with `gemini-2.5-flash`.
- **Taming Web Speech API Cutoffs:** Chromium and WebKit browsers have a notorious bug where `speechSynthesis` silently crashes or stops speaking after ~250 characters or 15 seconds. I designed a custom sentence-level chunking queue (`[.!?।\n]`) that feeds sentences sequentially, preserving full playback control (Play, Pause, Resume, Replay).
- **Procedural Audio Engineering:** Creating eerie sound effects doesn't require downloading massive `.mp3` files. Synthesizing pink noise through an LFO-modulated bandpass filter recreates whistling winter wind, while dual sine waves at 55Hz and 110Hz generate an infrasonic hum that induces psychological dread.
- **Bilingual LLM Prompt Engineering:** Instructing Gemini to generate literary Hindi in clean Devanagari script (without transliteration or code-switching) required crafting fine-tuned prompt constraints, cultural tone guidelines, and dedicated output tags (`Title:` / `शीर्षक:`, `Story:` / `कहानी:`).
- **Two-Tier CSS Animation Physics:** Animating a character walking across the screen while bobbing up and down usually causes CSS transform collisions. Separating the horizontal screen traverse (`translateX`) into an outer container and the vertical stride bounce (`translateY`) into an inner element eliminated glitches completely.

---

## Demo

- 🌐 **Live Web Application:** [https://ai-ghost-story-generator.vercel.app/](https://ai-ghost-story-generator.vercel.app/)
- 💻 **GitHub Repository:** [https://github.com/anubhav9236/ai-ghost-story-generator](https://github.com/anubhav9236/ai-ghost-story-generator)

### Walkthrough & Features in Action

1. **Summoning Inspiration:** Click the floating assistant ghost or hit **"Surprise Me 👻"** to load a spine-chilling premise in English or Hindi (e.g., *"A late-night subway train that stops at an abandoned underground station not on any transit map"* or *"एक वीरान रेलवे स्टेशन जहाँ रात के ठीक 2 बजे एक पुरानी स्टीम ट्रेन आती है..."*).
2. **Configuring the Ritual:** Select your desired language, choose from 6 horror sub-genres, adjust story length (Short ~200 words, Medium ~400 words, Long ~700 words), or specify a custom story title.
3. **The Arcane Summoning State:** While Google Gemini generates the tale, the screen enters a mystical trance: rotating summoning rune rings spin, spirits float across the altar, and real-time status messages display the ritual's progress.
4. **Immersive Story Presentation & Narration:** The story renders in gothic typography with clean paragraph separation. Hit **"Listen to Story"** to hear the deep voice narrate the tale, accompanied by howling winds and the 55Hz supernatural drone.
5. **One-Click Export:** Copy the story directly to your clipboard or download it as a formatted `.txt` file for your creative writing portfolio.

<!-- Embed your demo video or screenshots here -->
<!-- {% video https://www.youtube.com/watch?v=YOUR_DEMO_VIDEO %} -->

```text
+-----------------------------------------------------------------------+
|  👻 AI GHOST STORY GENERATOR (Powered by Google Gemini 2.5 Flash)    |
|  [ English | हिन्दी ]                                                  |
|                                                                       |
|  Story Seed: "An antique grandfather clock that chimes at 3:00 AM..." |
|  Category: [ Haunted House ]    Length: [ Medium ~400 words ]         |
|  [ 🔮 Summon Ghost Story ]                                            |
|                                                                       |
|  -------------------------------------------------------------------  |
|  📖 The Midnight Chiming of Blackwood Manor                           |
|  "The pendulum swung with an unnatural weight..."                     |
|                                                                       |
|  🔊 Narration: [ ▶ Play ] [ ❚❚ Pause ] [ ⏹ Stop ]                     |
|  🌫️ Haunted Atmosphere: [ ON ] | Volume: [ 50% ]                      |
|  [ 📋 Copy Story ] [ 💾 Download TXT ]                                |
+-----------------------------------------------------------------------+
```

---

## Partner Technologies

To build a reliable, private, and high-performance storytelling engine accessible to any browser worldwide, this project leveraged key partner and cloud technologies:

### 1. Google Gemini API (`gemini-2.5-flash` via `google-genai` SDK)
- **Implementation:** The core narrative engine utilizes Google's state-of-the-art **Gemini 2.5 Flash** model via the official `google-genai` Python SDK (`from google import genai`).
- **Why It Shined:** Gemini 2.5 Flash delivers lightning-fast inference times (often <2 seconds), superior bilingual fluency in literary Devanagari Hindi, and deep understanding of atmospheric horror pacing without over-sanitizing creative gothic fiction.
- **Inference Configuration:** Dynamically configured with token caps (`max_output_tokens`: 350 for Short, 650 for Medium, 1100 for Long) and temperature tuning (0.85) to balance unpredictable literary twists with rapid serverless execution.
- **Security & Privacy:** Server-side execution guarantees the `GEMINI_API_KEY` is never exposed to browser clients, inspect tools, or public git commits.

### 2. Vercel Serverless Architecture (`@vercel/python`)
- **Implementation:** Configured as a serverless microservice using `vercel.json` routing all incoming traffic to `api/index.py` via Vercel's Python runtime.
- **Developer Experience:** Instant global edge distribution with zero server management overhead. The architecture includes in-memory sliding-window IP rate limiting (10 requests/minute) and strict payload validation (3–2000 characters) to prevent abuse and protect API quotas.

### 3. GitHub (Open Source Collaboration & CI/CD)
- **Implementation:** Complete project version control, automated testing workflows, and open-source issue management.
- **Developer Experience:** The repository includes a comprehensive `pytest` suite (`test_app.py`) covering 17 unit and integration test cases (mocking Gemini client responses, verifying rate limits, validating input constraints, and testing error handling).

---

## Hackathon Experience

Participating in this hackathon was an exhilarating creative journey:

### The Atmosphere
Building against the clock brought an electrifying energy. While many AI hackathon projects gravitate toward commercial productivity tools, enterprise dashboards, or data summarizers, I wanted to lean into **art, folklore, and sensory storytelling**. 

Hacking late into the night in a dimly lit room, brainstorming haunted folklore scenarios, and listening to the procedural audio synthesizer come to life set a uniquely atmospheric mood that perfectly matched the project's soul.

### The Defining Moment
The turning point happened around 2:00 AM while testing the bilingual Hindi generation with Gemini 2.5 Flash. I prompted the system with an idea about an abandoned railway junction in the misty hills of Shimla. When the generated Hindi folklore story appeared on screen and the synthesized narration began reciting it in a slow, ominous cadence—underlaid by the gentle 55Hz sub-bass drone and whistling wind—I felt genuine goosebumps. It proved that cutting-edge foundation models and web audio can create a deeply human, culturally resonant storytelling experience.

### Key Takeaways & What's Next
This hackathon proved that **combining modern foundation models with browser-native multimedia standards creates captivating, immersive art accessible on any device worldwide**. 

Moving forward, I plan to expand the AI Ghost Story Generator with:
- Multi-speaker voice dialogues (narrator vs. ghostly entity).
- Dynamic SVG mood lighting that shifts based on the emotional sentiment of each paragraph.
- Fine-tuned community lore packs (Celtic folklore, Japanese Kaidan, and Himalayan folklore).

---

## 🌐 Community Wisdom

When building interactive voice and serverless AI web applications, community patterns and insights from fellow builders on DEV provide invaluable guidance:

- **Migrating to the Unified Google Gen AI SDK:** Transitioning to the modern `google-genai` client standardizes multi-turn prompting and token budgeting across serverless environments. See community discussions on [Building with the Google GenAI SDK and Gemini on DEV](https://dev.to/search?q=google%20genai%20python) for architectural blueprints and best practices.
- **Serverless Python APIs on Vercel:** Structuring WSGI/ASGI Python apps via lightweight `api/index.py` entry points and declarative `vercel.json` rewrites ensures snappy cold starts and zero-config edge deployments. Community walkthroughs on [Deploying Python Microservices to Vercel](https://dev.to/search?q=vercel%20python%20flask) helped optimize the application layout.
- **Overcoming Web Speech API Gotchas:** Managing browser speech synthesis across different operating systems and languages is a known challenge. Insights from DEV articles like [Creating a Speech Synthesizer using Web Speech API](https://dev.to/t/webspeechapi) highlight best practices for handling asynchronous `voiceschanged` events and sentence boundary queue management.

---

## Code & Links

- **GitHub Repository:** [https://github.com/anubhav9236/ai-ghost-story-generator](https://github.com/anubhav9236/ai-ghost-story-generator)
- **Live Demo:** [https://ai-ghost-story-generator.vercel.app/](https://ai-ghost-story-generator.vercel.app/)
- **License:** MIT Open Source
