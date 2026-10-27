# AI Ghost Story Generator: Bringing Spooky Lore to Life with Open-Weight LLMs & Horror Voice Narration 👻

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)*

---

## What I Built

**AI Ghost Story Generator** is an open-source, full-sensory storytelling application that transforms your darkest ideas, nightmares, and urban legends into spine-chilling ghost stories in both **English and Hindi**.

For the *"Ghost in the Machine"* theme, I wanted to interpret the prompt both literally and poetically: rather than treating AI as a sterile text-completion box, we breathed an eerie, theatrical spirit into the machine itself. 

When you enter a premise—such as a forgotten railway station in Shimla or an abandoned Victorian asylum—the application doesn't just print text:
1. **Open-Weight AI Generation:** Uses local open-weight LLMs (`llama3.2:3b` via Ollama) to craft rich atmospheric horror tailored across 7 distinct categories (Haunted House, Ancient Curse, Urban Legend, Psychological Horror, Folk Ghost Story, Haunted Forest, Emotional Tale).
2. **Horror Voice Narration:** Automatically reads the generated story aloud in an ominous, lowered pitch with sentence-level playback controls (Play, Pause, Resume, Stop, Replay) and bilingual Devanagari Hindi support.
3. **Haunted Atmosphere Soundscape:** Procedurally generates eerie howling wind and a 55Hz sub-bass drone directly in the browser via the Web Audio API—with 0 external audio assets.
4. **Living Haunted Scenery:** A fully animated gothic world featuring floating spirits, a walking ghost pacing across the screen with synchronized footsteps, a glowing full moon, drifting fog, and arcane summoner runes.

---

## Demo

- 🌐 **Live Web App:** [https://ai-ghost-story-generator.vercel.app/](https://ai-ghost-story-generator.vercel.app/)
- 💻 **Local Full-Fidelity Experience:** Run locally with Ollama for 100% offline, private AI generation.

---

## Code

{% github anubhav9236/ai-ghost-story-generator %}

- **GitHub Repository:** [https://github.com/anubhav9236/ai-ghost-story-generator](https://github.com/anubhav9236/ai-ghost-story-generator)
- **License:** MIT Open Source

---

## How I Built It

The project was architected from the ground up around open-source AI and browser-native multimedia standards:

### 1. Open-Source AI Engine (Ollama & Llama 3.2 3B)
- **Local Open-Weight Model:** Powered by Meta's open-weight `llama3.2:3b` running through **Ollama** via its local REST API (`http://127.0.0.1:11434/api/generate`).
- **Bilingual Horror Prompt Engineering:** The Flask backend provides fine-tuned system instructions tailored to horror tropes in both English and Hindi. The Hindi prompt enforces authentic cultural vernacular and Devanagari script without transliteration artifacts.
- **Dynamic Token Budgeting:** Token targets (`num_predict`) dynamically scale between Short (~200 words), Medium (~400 words), and Long (~700 words) to guarantee responsive generation times even on CPU inference.

### 2. Horror Voice Narration Engine (Web Speech API)
- Built on the browser's native `window.speechSynthesis` API.
- **Sentence-Level Chunking Queue:** Chrome and WebKit browsers have a known bug that silently cuts off synthesis on utterances exceeding ~250 characters. We implemented a custom queue that splits stories at sentence boundaries (`[.!?।\n]`), maintaining continuous playback with instant Pause/Resume/Replay support.
- **Atmospheric Modulation:** Narration pitch is lowered (`pitch: 0.72`) and rate moderated (`rate: 0.85`) to evoke the cadence of an old-school campfire storyteller.

### 3. Procedural Haunted Atmosphere (Web Audio API)
- To avoid heavy copyrighted sound files, the eerie audio is generated 100% procedurally:
  - **Howling Wind:** Pink noise synthesized into an `AudioBufferSourceNode`, filtered through a dynamic `BiquadFilterNode` modulated by an LFO (Low-Frequency Oscillator) to create the rise and fall of winter gales.
  - **Sub-Bass Horror Drone:** A pure 55Hz sine-wave oscillator combined with a 110Hz warm undertone that introduces subtle infrasonic tension into headphones.

### 4. Spooky Visual & CSS Animation System
- **Walking Ghost:** A dual-animation keyframe system (`walkingGhostJourney` + `walkingGhostStep`) that traverses the viewport horizontally while bobbing vertically with authentic stride physics.
- **Floating Spirits & Scenery:** Pure SVG ghosts with glowing halos, blinking pupils, a moonlit horizon, drifting multi-layered mist, and rotating arcane summoning rings.

---

## Why Does Open Innovation Matter?

Open innovation is what made this project possible, and it represents the future of creative artificial intelligence:

1. **No Token Tolls or API Paywalls:** Proprietary LLM APIs charge per token and impose rate limits. Running open-weight models locally democratizes immersive digital storytelling for students, writers, and independent creators without a credit card.
2. **Uncensored Creative Horror Fiction:** Closed commercial APIs frequently trigger overzealous safety filters when handling horror themes, supernatural death, curses, or psychological tension. Open-weight models like Llama 3.2 allow authentic, evocative gothic fiction while respecting artistic nuance.
3. **Absolute Privacy:** Your nightmare ideas, folklore prompts, and creative drafts never leave your device. There is no telemetry, no tracking, and no data harvesting.
4. **Interchangeability & Longevity:** Because the backend communicates with Ollama's standardized interface, developers can freely swap `llama3.2:3b` for `mistral`, `qwen2.5`, or custom fine-tuned horror models with zero code rewrites.

---

## My Agent Session

This project was developed through an agentic pair-programming workflow:
- Architected the full-stack Flask and vanilla CSS/JS pipeline.
- Solved Windows UTF-8 console output challenges for Hindi Devanagari text.
- Overcame the Web Speech API 250-character cutoff limitation through a custom queue worker.
- Synthesized browser-native Web Audio procedural atmospheric effects to achieve 0 KB audio bundle overhead.

---

## The Spirit of It

> *"उस रात हवेली की खिड़कियों से कोई रोशनी नहीं आ रही थी, फिर भी अंदर से कदमों की आवाज़ सुनाई दे रही थी..."*

The moment this project truly landed was testing the Hindi horror generation late at night. Hearing the machine narrate an eerie folklore story in Hindi, accompanied by the gentle 55Hz sub-bass drone and the howling wind whistling in the background while little ghosts floated across the screen, felt genuinely magical. It proved that open-source AI isn't just about spreadsheets and code completion—it can evoke genuine wonder, nostalgia, and a good old-fashioned spine shiver.

---

## Prize Categories

- **Ghost in the Machine (Primary Track)**
- **Best Use of Open-Source Models / Local AI (Ollama + Llama 3.2)**
- **Most Creative / Atmospheric User Experience**
