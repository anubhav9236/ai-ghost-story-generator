
/**
 * AI Ghost Story Generator - Frontend Application Logic
 * Upgraded with Horror Voice Narration (Web Speech API) and 
 * Procedural Haunted Ambience (Web Audio API).
 * Supports English & Hindi narration, dynamic voices, chunking, and full audio controls.
 */

document.addEventListener('DOMContentLoaded', () => {
    // =========================================================================
    // 1. DOM ELEMENT REFERENCES
    // =========================================================================
    const storyForm = document.getElementById('story-form');
    const ideaInput = document.getElementById('story-idea');
    const ideaCharCount = document.getElementById('idea-char-count');
    const ideaError = document.getElementById('idea-error');
    const surpriseBtn = document.getElementById('surprise-btn');
    const generateBtn = document.getElementById('generate-btn');
    const customTitleInput = document.getElementById('custom-title');
    const interactiveGhost = document.getElementById('interactive-ghost');
    const ghostSpeechBubble = document.getElementById('ghost-speech-bubble');

    // Language, Engine, Category, & Length Selectors
    const languagePills = document.querySelectorAll('.language-pill:not(.engine-pill)');
    const enginePills = document.querySelectorAll('.engine-pill');
    const categoryPills = document.querySelectorAll('.category-pill');
    const lengthOptions = document.querySelectorAll('.length-option');

    // Panels & Feedback
    const loadingPanel = document.getElementById('loading-panel');
    const errorBanner = document.getElementById('error-banner');
    const errorTitle = document.getElementById('error-title');
    const errorMessage = document.getElementById('error-message');
    const errorTroubleshooting = document.getElementById('error-troubleshooting');
    const troubleshootingSteps = document.getElementById('troubleshooting-steps');
    const closeErrorBtn = document.getElementById('close-error-btn');

    // Story Result Elements
    const resultCard = document.getElementById('result-card');
    const resultTitle = document.getElementById('result-title');
    const resultCategory = document.getElementById('result-category');
    const resultLength = document.getElementById('result-length');
    const resultModel = document.getElementById('result-model');
    const resultStory = document.getElementById('result-story');
    const copyStoryBtn = document.getElementById('copy-story-btn');
    const copyToast = document.getElementById('copy-toast');
    const downloadStoryBtn = document.getElementById('download-story-btn');
    const generateAnotherBtn = document.getElementById('generate-another-btn');

    // Voice Narration & Audio Elements
    const voicePlayer = document.getElementById('voice-narration-player');
    const narrationStatus = document.getElementById('narration-status');
    const narrationProgressFill = document.getElementById('narration-progress-fill');
    const voicePlayBtn = document.getElementById('voice-play-btn');
    const voicePauseBtn = document.getElementById('voice-pause-btn');
    const voiceResumeBtn = document.getElementById('voice-resume-btn');
    const voiceStopBtn = document.getElementById('voice-stop-btn');
    const voiceReplayBtn = document.getElementById('voice-replay-btn');
    const autoplayCheckbox = document.getElementById('autoplay-narration-checkbox');
    const toggleVoiceSettingsBtn = document.getElementById('toggle-voice-settings-btn');
    const voiceSettingsPanel = document.getElementById('voice-settings-panel');
    const voiceLanguageSelect = document.getElementById('voice-language-select');
    const voiceSelect = document.getElementById('voice-select');
    const voiceAvailabilityNote = document.getElementById('voice-availability-note');
    const atmosphereToggleBtn = document.getElementById('atmosphere-toggle-btn');
    const atmosphereBtnText = document.getElementById('atmosphere-btn-text');
    const atmosphereVolumeSlider = document.getElementById('atmosphere-volume-slider');
    const atmosphereVolumeLabel = document.getElementById('atmosphere-volume-label');
    const speedPills = document.querySelectorAll('input[name="narration-speed"]');
    const pitchPills = document.querySelectorAll('input[name="voice-pitch"]');

    // Navigation & Layout
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');
    const currentYearSpan = document.getElementById('current-year');

    // Global State
    let currentStoryData = null;
    let isSubmitting = false;

    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

    // =========================================================================
    // 2. SPOOKY STORY IDEAS COLLECTION (English & Hindi)
    // =========================================================================
    const SPOOKY_IDEAS_EN = [
        "A senior developer reviews a pull request merged at 3:33 AM from an anonymous committer whose code compiles into ancient Sumerian incantations.",
        "An IDE plugin that auto-completes code predicting how and when the programmer will die.",
        "A rogue AI script in an abandoned GitHub repo that executes an undocumented bytecode instruction summoning an apparition on screen.",
        "An abandoned Victorian mansion on a coastal cliff where a ghost appears at midnight, searching for a music box buried in the floorboards.",
        "A late-night subway train that stops at an abandoned underground station not on any official transit map.",
        "An antique wooden radio bought at an estate sale that broadcasts whisperings from a family that vanished in 1942.",
        "A lonely lighthouse keeper who notices that the warning beam of light reveals silhouettes of drowned sailors walking across the waves.",
        "An old Polaroid camera that captures a tall, faceless figure standing slightly closer behind the subject in every photo.",
        "A forgotten mountain cemetery where grave markers swap positions whenever a blizzard strikes.",
        "A grandfather clock that only rings the thirteenth hour, unlocking a door in the hallway that does not exist during daylight.",
        "A rainy highway diner where a silent hitchhiker leaves behind soggy matches and a name written on a fogged napkin.",
        "A dollhouse found in the attic that mysteriously mirrors whatever happens in the real house, seconds before it occurs.",
        "A nocturnal librarian who discovers a leather-bound book in the restricted archives that writes itself in real-time.",
        "An old mirror in an antique store that reflects the room empty, even when crowded with shoppers.",
        "A child's imaginary friend who leaves cold, muddy footprints across the ceiling every Halloween night.",
        "A secluded campsite in the ancient pine woods where someone, or something, taps rhythmically on the tent canvas at 3:00 AM.",
        "A forgotten chapel bell in an overgrown forest that chimes without a rope every time a villager falls ill.",
        "A music student who inherits a violin that plays a haunting waltz on its own whenever midnight strikes."
    ];

    const SPOOKY_IDEAS_HI = [
        "एक पुरानी प्रोग्रामिंग फाइल जिसमें आधी रात को खुद-ब-खुद अजीब कोड लिखा जाने लगता है और स्क्रीन से धुआं निकलने लगता है...",
        "एक ऐसा सॉफ्टवेयर बग जो सिर्फ अमावस की रात को एक्टिव होता है और कमरे की बत्तियां बुझा देता है...",
        "एक सुनसान पुरानी हवेली जहाँ हर अमावस्या की रात घुंघरू की रहस्यमयी आवाज गूंजती है।",
        "जंगल के बीचों-बीच स्थित एक सूखा कुआँ जिससे रात के सन्नाटे में कोई पुकारता सुनाई देता है।",
        "एक पुराना आईना जो इंसान के पीछे खड़े उस साए को दिखाता है जो आँखों से नहीं दिखता।",
        "पहाड़ी रास्ते पर स्थित एक पुराना ढाबा जहाँ एक अजनबी मुसाफिर चाय की चुस्की लेते ही गायब हो गया।",
        "गाँव का वो पुराना बरगद का पेड़ जिसके नीचे रात को लाल लालटेन लिए एक बूढ़ा चौकीदार खड़ा मिलता है।",
        "एक बंद रेलवे स्टेशन जहाँ आधी रात को एक ऐसी ट्रेन रुकती है जो किसी समय-सारणी में दर्ज नहीं है।"
    ];

    function getRandomIdea(lang = "English") {
        const pool = (lang === "Hindi") ? SPOOKY_IDEAS_HI : SPOOKY_IDEAS_EN;
        const index = Math.floor(Math.random() * pool.length);
        return pool[index];
    }

    function populateIdea(ideaText, source = "button") {
        if (!ideaInput) return;
        ideaInput.value = ideaText;
        updateCharCount();
        clearError();

        ideaInput.classList.remove('glow-flash');
        void ideaInput.offsetWidth;
        ideaInput.classList.add('glow-flash');

        if (source === "ghost" && ghostSpeechBubble) {
            ghostSpeechBubble.querySelector('span').textContent = "Ooh, that gives me chills! Summon it!";
            setTimeout(() => {
                ghostSpeechBubble.querySelector('span').textContent = "Boo! Ready for a scary story? Click me!";
            }, 4000);
        }
    }

    if (surpriseBtn) {
        surpriseBtn.addEventListener('click', () => {
            const langInput = document.querySelector('input[name="language"]:checked');
            const lang = langInput ? langInput.value : "English";
            populateIdea(getRandomIdea(lang), "button");
        });
    }

    if (interactiveGhost) {
        interactiveGhost.addEventListener('click', () => {
            const langInput = document.querySelector('input[name="language"]:checked');
            const lang = langInput ? langInput.value : "English";
            populateIdea(getRandomIdea(lang), "ghost");
        });

        interactiveGhost.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const langInput = document.querySelector('input[name="language"]:checked');
                const lang = langInput ? langInput.value : "English";
                populateIdea(getRandomIdea(lang), "ghost");
            }
        });
    }

    // =========================================================================
    // 3. INPUT COUNTER & SELECTION PILLS SYNCHRONIZATION
    // =========================================================================
    function updateCharCount() {
        if (!ideaInput || !ideaCharCount) return;
        const count = ideaInput.value.length;
        ideaCharCount.textContent = `${count} / 2000`;
    }

    if (ideaInput) {
        ideaInput.addEventListener('input', () => {
            updateCharCount();
            if (ideaInput.value.trim().length >= 3) {
                clearError();
            }
        });
    }

    // Language selector pills
    languagePills.forEach(pill => {
        pill.addEventListener('click', () => {
            languagePills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const radio = pill.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                // Switch placeholder language subtly
                if (radio.value === "Hindi") {
                    ideaInput.placeholder = "उदाहरण: एक पुरानी हवेली जहाँ आधी रात को सीढ़ियों पर कदमों की आहट सुनाई देती है...";
                } else {
                    ideaInput.placeholder = "Example: An abandoned mansion on the cliff edge where a ghost appears every night at midnight...";
                }
            }
        });
    });

    // Engine selector pills
    enginePills.forEach(pill => {
        pill.addEventListener('click', () => {
            enginePills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const radio = pill.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });

    // Category pills
    categoryPills.forEach(pill => {
        pill.addEventListener('click', () => {
            categoryPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const radio = pill.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });

    // Length options
    lengthOptions.forEach(opt => {
        opt.addEventListener('click', () => {
            lengthOptions.forEach(o => o.classList.remove('active'));
            opt.classList.add('active');
            const radio = opt.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });

    // =========================================================================
    // 4. ERROR AND NOTICE MANAGEMENT
    // =========================================================================
    const errorActions = document.getElementById('error-actions');
    const errorActionKeyBtn = document.getElementById('error-action-key-btn');
    const errorActionLoreBtn = document.getElementById('error-action-lore-btn');

    function showError(message, troubleshooting = null, canFallback = false) {
        if (!errorBanner) return;
        if (errorMessage) errorMessage.textContent = message;

        if (troubleshooting && Array.isArray(troubleshooting) && troubleshooting.length > 0) {
            troubleshootingSteps.innerHTML = '';
            troubleshooting.forEach(step => {
                const li = document.createElement('li');
                li.textContent = step;
                troubleshootingSteps.appendChild(li);
            });
            errorTroubleshooting.classList.remove('hidden');
        } else {
            errorTroubleshooting.classList.add('hidden');
        }

        if (errorActions) {
            if (canFallback) {
                errorActions.classList.remove('hidden');
            } else {
                errorActions.classList.add('hidden');
            }
        }

        errorBanner.classList.remove('hidden');
        errorBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function clearError() {
        if (errorBanner) errorBanner.classList.add('hidden');
        if (errorActions) errorActions.classList.add('hidden');
        if (ideaError) ideaError.textContent = '';
    }

    if (errorActionKeyBtn) {
        errorActionKeyBtn.addEventListener('click', () => {
            const keyModalBtn = document.getElementById('open-key-modal-btn');
            if (keyModalBtn) keyModalBtn.click();
        });
    }

    if (errorActionLoreBtn) {
        errorActionLoreBtn.addEventListener('click', () => {
            const lorePill = document.getElementById('engine-pill-lore');
            if (lorePill) lorePill.click();
            clearError();
            if (storyForm) {
                storyForm.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        });
    }

    if (closeErrorBtn) {
        closeErrorBtn.addEventListener('click', clearError);
    }

    // =========================================================================
    // 5. PROCEDURAL HAUNTED ATMOSPHERE ENGINE (Web Audio API)
    // Generates soft eerie wind and low sub-bass drone with zero external files
    // =========================================================================
    class HauntedAtmosphereEngine {
        constructor() {
            this.ctx = null;
            this.masterGain = null;
            this.windNode = null;
            this.windFilter = null;
            this.drone1 = null;
            this.drone2 = null;
            this.lfo = null;
            this.isPlaying = false;
            this.isEnabled = false;
            this.volume = 0.20;
        }

        initContext() {
            if (!this.ctx) {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (!AudioCtx) return false;
                this.ctx = new AudioCtx();
            }
            if (this.ctx.state === 'suspended') {
                this.ctx.resume();
            }
            return true;
        }

        createWindBuffer() {
            // Generate 4 seconds of subtle pink/brown noise
            const bufferSize = this.ctx.sampleRate * 4;
            const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            const data = buffer.getChannelData(0);
            let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;

            for (let i = 0; i < bufferSize; i++) {
                const white = Math.random() * 2 - 1;
                b0 = 0.99886 * b0 + white * 0.0555179;
                b1 = 0.99332 * b1 + white * 0.0750759;
                b2 = 0.96900 * b2 + white * 0.1538520;
                b3 = 0.86650 * b3 + white * 0.3104856;
                b4 = 0.55000 * b4 + white * 0.5329522;
                b5 = -0.7616 * b5 - white * 0.0168980;
                data[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.04;
                b6 = white * 0.115926;
            }
            return buffer;
        }

        start() {
            if (!this.isEnabled) return;
            if (this.isPlaying) return;
            if (!this.initContext()) return;

            try {
                // Master ambience gain with smooth ramp
                this.masterGain = this.ctx.createGain();
                this.masterGain.gain.setValueAtTime(0.001, this.ctx.currentTime);
                this.masterGain.gain.exponentialRampToValueAtTime(Math.max(0.001, this.volume), this.ctx.currentTime + 0.8);
                this.masterGain.connect(this.ctx.destination);

                // 1. Wind noise generator with bandpass filter sweep
                const windBuffer = this.createWindBuffer();
                this.windNode = this.ctx.createBufferSource();
                this.windNode.buffer = windBuffer;
                this.windNode.loop = true;

                this.windFilter = this.ctx.createBiquadFilter();
                this.windFilter.type = 'bandpass';
                this.windFilter.frequency.setValueAtTime(280, this.ctx.currentTime);
                this.windFilter.Q.setValueAtTime(2.2, this.ctx.currentTime);

                // LFO to slowly sweep wind filter frequency (simulating howling gusts)
                this.lfo = this.ctx.createOscillator();
                this.lfo.frequency.setValueAtTime(0.12, this.ctx.currentTime);
                const lfoGain = this.ctx.createGain();
                lfoGain.gain.setValueAtTime(140, this.ctx.currentTime);
                this.lfo.connect(lfoGain);
                lfoGain.connect(this.windFilter.frequency);

                this.windNode.connect(this.windFilter);
                this.windFilter.connect(this.masterGain);

                // 2. Sub-bass supernatural harmonic drone (55Hz and 110.5Hz for eerie slow beating)
                this.drone1 = this.ctx.createOscillator();
                this.drone1.type = 'sine';
                this.drone1.frequency.setValueAtTime(55, this.ctx.currentTime);

                this.drone2 = this.ctx.createOscillator();
                this.drone2.type = 'sine';
                this.drone2.frequency.setValueAtTime(110.5, this.ctx.currentTime);

                const droneGain = this.ctx.createGain();
                droneGain.gain.setValueAtTime(0.28, this.ctx.currentTime);

                this.drone1.connect(droneGain);
                this.drone2.connect(droneGain);
                droneGain.connect(this.masterGain);

                this.windNode.start();
                this.lfo.start();
                this.drone1.start();
                this.drone2.start();

                this.isPlaying = true;
            } catch (err) {
                console.warn("Web Audio ambience failed to initialize:", err);
            }
        }

        pause() {
            if (!this.isPlaying || !this.ctx || !this.masterGain) return;
            try {
                this.masterGain.gain.setValueAtTime(this.masterGain.gain.value, this.ctx.currentTime);
                this.masterGain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 0.3);
                setTimeout(() => {
                    this.stopNodes();
                    this.isPlaying = false;
                }, 350);
            } catch (e) {
                this.stopNodes();
                this.isPlaying = false;
            }
        }

        resume() {
            if (this.isEnabled && !this.isPlaying) {
                this.start();
            }
        }

        stop() {
            if (!this.isPlaying) return;
            if (this.ctx && this.masterGain) {
                try {
                    this.masterGain.gain.setValueAtTime(this.masterGain.gain.value, this.ctx.currentTime);
                    this.masterGain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 0.4);
                } catch (e) { }
            }
            setTimeout(() => {
                this.stopNodes();
                this.isPlaying = false;
            }, 450);
        }

        stopNodes() {
            try { if (this.windNode) { this.windNode.stop(); this.windNode.disconnect(); } } catch (e) { }
            try { if (this.lfo) { this.lfo.stop(); this.lfo.disconnect(); } } catch (e) { }
            try { if (this.drone1) { this.drone1.stop(); this.drone1.disconnect(); } } catch (e) { }
            try { if (this.drone2) { this.drone2.stop(); this.drone2.disconnect(); } } catch (e) { }
            try { if (this.masterGain) { this.masterGain.disconnect(); } } catch (e) { }
            this.windNode = null;
            this.lfo = null;
            this.drone1 = null;
            this.drone2 = null;
            this.masterGain = null;
        }

        setVolume(val) {
            this.volume = Math.max(0.001, Math.min(1.0, val));
            if (this.masterGain && this.ctx && this.isPlaying) {
                try {
                    this.masterGain.gain.setValueAtTime(this.masterGain.gain.value, this.ctx.currentTime);
                    this.masterGain.gain.linearRampToValueAtTime(this.volume, this.ctx.currentTime + 0.1);
                } catch (e) { }
            }
        }
    }

    const atmosphereEngine = new HauntedAtmosphereEngine();

    // Atmosphere toggle button interaction
    if (atmosphereToggleBtn) {
        atmosphereToggleBtn.addEventListener('click', () => {
            atmosphereEngine.isEnabled = !atmosphereEngine.isEnabled;
            atmosphereToggleBtn.setAttribute('aria-pressed', atmosphereEngine.isEnabled);

            if (atmosphereEngine.isEnabled) {
                atmosphereToggleBtn.classList.add('active');
                if (atmosphereBtnText) atmosphereBtnText.textContent = "Haunted Atmosphere: ON";
                // If story is currently being narrated, start atmosphere right away
                if (voiceNarrator.state === 'playing') {
                    atmosphereEngine.start();
                }
            } else {
                atmosphereToggleBtn.classList.remove('active');
                if (atmosphereBtnText) atmosphereBtnText.textContent = "Haunted Atmosphere: OFF";
                atmosphereEngine.stop();
            }
        });
    }

    // Atmosphere volume slider
    if (atmosphereVolumeSlider && atmosphereVolumeLabel) {
        atmosphereVolumeSlider.addEventListener('input', (e) => {
            const val = parseInt(e.target.value, 10);
            atmosphereVolumeLabel.textContent = `${val}%`;
            atmosphereEngine.setVolume(val / 100);
        });
    }

    // =========================================================================
    // 6. SCARY HORROR VOICE NARRATION ENGINE (Web Speech API)
    // Supports English & Hindi voices, sentence chunking, pitch/rate controls,
    // and full synchronization with sound-wave visualizers.
    // =========================================================================
    class HorrorVoiceNarrator {
        constructor() {
            this.synth = window.speechSynthesis;
            this.availableVoices = [];
            this.chunks = [];
            this.currentChunkIndex = 0;
            this.state = 'idle'; // 'idle' | 'playing' | 'paused' | 'stopped'
            this.storyLanguage = 'English';
            this.selectedVoice = null;
            this.rate = 0.82;   // Slow, suspenseful pace default
            this.pitch = 0.80;  // Deep, ominous pitch default
            this.currentUtterance = null;

            this.initVoices();
        }

        initVoices() {
            if (!this.synth) {
                if (narrationStatus) {
                    narrationStatus.textContent = "Speech synthesis not supported on this browser.";
                }
                return;
            }

            const loadHandler = () => {
                this.availableVoices = this.synth.getVoices();
                this.populateVoiceDropdown();
            };

            loadHandler();
            if (typeof this.synth.onvoiceschanged !== 'undefined') {
                this.synth.onvoiceschanged = loadHandler;
            }
        }

        populateVoiceDropdown() {
            if (!voiceSelect) return;
            voiceSelect.innerHTML = '';

            const defaultOpt = document.createElement('option');
            defaultOpt.value = 'auto';
            defaultOpt.textContent = '✨ Automatic Best Match for Story Language';
            voiceSelect.appendChild(defaultOpt);

            if (!this.availableVoices || this.availableVoices.length === 0) {
                const opt = document.createElement('option');
                opt.value = '';
                opt.textContent = 'Default System Voice (Browser controlled)';
                voiceSelect.appendChild(opt);
                return;
            }

            let hindiVoiceCount = 0;
            this.availableVoices.forEach((voice, index) => {
                const opt = document.createElement('option');
                opt.value = voice.name;
                const langTag = voice.lang || 'unknown';
                opt.textContent = `${voice.name} (${langTag})${voice.default ? ' [Default]' : ''}`;

                if (langTag.startsWith('hi')) {
                    hindiVoiceCount++;
                }
                voiceSelect.appendChild(opt);
            });

            if (voiceAvailabilityNote) {
                if (hindiVoiceCount > 0) {
                    voiceAvailabilityNote.textContent = `Found ${this.availableVoices.length} voices (${hindiVoiceCount} Hindi native voices available on your device).`;
                } else {
                    voiceAvailabilityNote.textContent = `Found ${this.availableVoices.length} voices (Hindi pronunciation supported via multilingual system voices).`;
                }
            }
        }

        selectBestVoice(requestedLang) {
            // Check if user manually selected a specific voice from dropdown
            const manualChoice = voiceSelect ? voiceSelect.value : 'auto';
            if (manualChoice && manualChoice !== 'auto') {
                const found = this.availableVoices.find(v => v.name === manualChoice);
                if (found) return found;
            }

            if (!this.availableVoices || this.availableVoices.length === 0) {
                return null;
            }

            const isHindi = (requestedLang === 'Hindi' || requestedLang === 'hi');

            if (isHindi) {
                // Priority 1: Direct Hindi language tag
                const hiVoice = this.availableVoices.find(v =>
                    (v.lang && (v.lang.toLowerCase() === 'hi-in' || v.lang.toLowerCase().startsWith('hi'))) ||
                    (v.name && (v.name.toLowerCase().includes('hindi') || v.name.includes('हिन्दी') || v.name.includes('Kalpana') || v.name.includes('Hemant')))
                );
                if (hiVoice) return hiVoice;
            } else {
                // English: Prefer deeper, natural English voices (Google, Microsoft David, Mark, etc.)
                const deepEnVoice = this.availableVoices.find(v =>
                    v.lang && v.lang.toLowerCase().startsWith('en') &&
                    (v.name.toLowerCase().includes('david') ||
                        v.name.toLowerCase().includes('mark') ||
                        v.name.toLowerCase().includes('google us') ||
                        v.name.toLowerCase().includes('guy') ||
                        v.name.toLowerCase().includes('natural'))
                );
                if (deepEnVoice) return deepEnVoice;

                const anyEnVoice = this.availableVoices.find(v => v.lang && v.lang.toLowerCase().startsWith('en'));
                if (anyEnVoice) return anyEnVoice;
            }

            // Fallback to first available or default voice
            return this.availableVoices.find(v => v.default) || this.availableVoices[0];
        }

        prepareStoryChunks(title, storyText, language) {
            this.chunks = [];
            this.currentChunkIndex = 0;
            this.storyLanguage = language || 'English';

            // 1. Spooky opening announcement with title
            if (title && title.trim()) {
                if (this.storyLanguage === 'Hindi') {
                    this.chunks.push(`शीर्षक: ${title.trim()}।`);
                } else {
                    this.chunks.push(`Story Title: ${title.trim()}.`);
                }
            }

            // 2. Split story text into complete sentence chunks (~120-180 chars max)
            // Splitting on full stops, exclamation, question mark, and Devanagari danda (।)
            const rawSentences = storyText.split(/(?<=[.!?।\n])\s+/);

            let buffer = "";
            rawSentences.forEach(sentence => {
                const clean = sentence.trim();
                if (!clean) return;

                if ((buffer + " " + clean).length <= 180) {
                    buffer = buffer ? `${buffer} ${clean}` : clean;
                } else {
                    if (buffer) this.chunks.push(buffer);
                    buffer = clean;
                }
            });

            if (buffer) {
                this.chunks.push(buffer);
            }
        }

        start(title, storyText, language) {
            if (!this.synth) return;

            // Stop any ongoing speech
            this.synth.cancel();

            if (title && storyText) {
                this.prepareStoryChunks(title, storyText, language);
            }

            if (this.chunks.length === 0) {
                if (narrationStatus) narrationStatus.textContent = "No story text to narrate.";
                return;
            }

            this.currentChunkIndex = 0;
            this.state = 'playing';

            // Read user settings
            this.updateVoiceSettings();

            // Start ambient audio if enabled
            atmosphereEngine.start();

            // Update UI to active
            this.updatePlayerUI('playing');

            // Speak first chunk
            this.speakNextChunk();
        }

        updateVoiceSettings() {
            // Speed (Rate)
            const speedRadio = document.querySelector('input[name="narration-speed"]:checked');
            this.rate = speedRadio ? parseFloat(speedRadio.value) : 0.82;

            // Pitch
            const pitchRadio = document.querySelector('input[name="voice-pitch"]:checked');
            this.pitch = pitchRadio ? parseFloat(pitchRadio.value) : 0.80;

            // Language check
            const langSelect = voiceLanguageSelect ? voiceLanguageSelect.value : 'auto';
            let targetLang = this.storyLanguage;
            if (langSelect === 'en') targetLang = 'English';
            if (langSelect === 'hi') targetLang = 'Hindi';

            this.selectedVoice = this.selectBestVoice(targetLang);
        }

        speakNextChunk() {
            if (this.state !== 'playing') return;

            if (this.currentChunkIndex >= this.chunks.length) {
                // Completed narration
                this.onNarrationComplete();
                return;
            }

            const chunkText = this.chunks[this.currentChunkIndex];
            const utterance = new SpeechSynthesisUtterance(chunkText);

            if (this.selectedVoice) {
                utterance.voice = this.selectedVoice;
                utterance.lang = this.selectedVoice.lang;
            } else {
                utterance.lang = (this.storyLanguage === 'Hindi') ? 'hi-IN' : 'en-US';
            }

            utterance.rate = this.rate;
            utterance.pitch = this.pitch;

            // Progress tracking
            const progressPercent = Math.round(((this.currentChunkIndex + 1) / this.chunks.length) * 100);
            if (narrationProgressFill) {
                narrationProgressFill.style.width = `${progressPercent}%`;
            }
            if (narrationStatus) {
                const voiceName = this.selectedVoice ? this.selectedVoice.name.split(' ')[0] : 'Spirits';
                narrationStatus.textContent = `Whispering story... (${this.currentChunkIndex + 1}/${this.chunks.length}) • Voice: ${voiceName}`;
            }

            utterance.onend = () => {
                if (this.state === 'playing') {
                    this.currentChunkIndex++;
                    // Slight dramatic breathing pause between sentences (220ms)
                    setTimeout(() => {
                        this.speakNextChunk();
                    }, 220);
                }
            };

            utterance.onerror = (e) => {
                // If speech wasn't interrupted intentionally by stop()
                if (e.error !== 'interrupted' && e.error !== 'canceled') {
                    console.warn("Speech synthesis chunk warning:", e);
                    this.currentChunkIndex++;
                    if (this.state === 'playing') {
                        this.speakNextChunk();
                    }
                }
            };

            this.currentUtterance = utterance;
            this.synth.speak(utterance);
        }

        pause() {
            if (this.state !== 'playing') return;
            this.state = 'paused';
            this.synth.pause();
            atmosphereEngine.pause();
            this.updatePlayerUI('paused');
            if (narrationStatus) narrationStatus.textContent = "Narration paused. Press Resume to continue.";
        }

        resume() {
            if (this.state !== 'paused') return;
            this.state = 'playing';
            this.updatePlayerUI('playing');
            atmosphereEngine.resume();

            // Workaround for browser bug where synth.resume() stays suspended:
            // If resume does not resume speech within 300ms, re-speak current chunk
            this.synth.resume();
            if (!this.synth.speaking) {
                this.speakNextChunk();
            }
        }

        stop() {
            this.state = 'stopped';
            if (this.synth) this.synth.cancel();
            atmosphereEngine.stop();
            this.currentChunkIndex = 0;
            if (narrationProgressFill) narrationProgressFill.style.width = '0%';
            if (narrationStatus) narrationStatus.textContent = "Narration stopped.";
            this.updatePlayerUI('stopped');
        }

        replay() {
            if (!currentStoryData) return;
            this.start(currentStoryData.title, currentStoryData.story, currentStoryData.language || 'English');
        }

        onNarrationComplete() {
            this.state = 'idle';
            atmosphereEngine.stop();
            if (narrationProgressFill) narrationProgressFill.style.width = '100%';
            if (narrationStatus) narrationStatus.textContent = "✨ Story narration complete. Listen again or summon a new nightmare!";
            this.updatePlayerUI('complete');
        }

        updatePlayerUI(state) {
            if (!voicePlayer) return;

            // Reset button display classes
            if (voicePlayBtn) voicePlayBtn.classList.add('hidden');
            if (voicePauseBtn) voicePauseBtn.classList.add('hidden');
            if (voiceResumeBtn) voiceResumeBtn.classList.add('hidden');
            if (voiceStopBtn) voiceStopBtn.classList.add('hidden');
            if (voiceReplayBtn) voiceReplayBtn.classList.add('hidden');

            if (state === 'playing') {
                voicePlayer.classList.add('narrating-active');
                voicePlayer.classList.remove('narrating-paused');
                if (voicePauseBtn) voicePauseBtn.classList.remove('hidden');
                if (voiceStopBtn) voiceStopBtn.classList.remove('hidden');
            } else if (state === 'paused') {
                voicePlayer.classList.add('narrating-paused');
                if (voiceResumeBtn) voiceResumeBtn.classList.remove('hidden');
                if (voiceStopBtn) voiceStopBtn.classList.remove('hidden');
            } else if (state === 'stopped') {
                voicePlayer.classList.remove('narrating-active', 'narrating-paused');
                if (voicePlayBtn) voicePlayBtn.classList.remove('hidden');
                if (voiceReplayBtn) voiceReplayBtn.classList.remove('hidden');
            } else if (state === 'complete') {
                voicePlayer.classList.remove('narrating-active', 'narrating-paused');
                if (voiceReplayBtn) voiceReplayBtn.classList.remove('hidden');
                if (voicePlayBtn) voicePlayBtn.classList.remove('hidden');
            } else {
                // Idle
                voicePlayer.classList.remove('narrating-active', 'narrating-paused');
                if (voicePlayBtn) voicePlayBtn.classList.remove('hidden');
            }
        }
    }

    const voiceNarrator = new HorrorVoiceNarrator();

    // Player button event listeners
    if (voicePlayBtn) {
        voicePlayBtn.addEventListener('click', () => {
            if (!currentStoryData) return;
            voiceNarrator.start(currentStoryData.title, currentStoryData.story, currentStoryData.language || 'English');
        });
    }

    if (voicePauseBtn) {
        voicePauseBtn.addEventListener('click', () => voiceNarrator.pause());
    }

    if (voiceResumeBtn) {
        voiceResumeBtn.addEventListener('click', () => voiceNarrator.resume());
    }

    if (voiceStopBtn) {
        voiceStopBtn.addEventListener('click', () => voiceNarrator.stop());
    }

    if (voiceReplayBtn) {
        voiceReplayBtn.addEventListener('click', () => voiceNarrator.replay());
    }

    // Toggle Voice Settings Collapsible Panel
    if (toggleVoiceSettingsBtn && voiceSettingsPanel) {
        toggleVoiceSettingsBtn.addEventListener('click', () => {
            const isExpanded = toggleVoiceSettingsBtn.getAttribute('aria-expanded') === 'true';
            toggleVoiceSettingsBtn.setAttribute('aria-expanded', !isExpanded);
            voiceSettingsPanel.classList.toggle('hidden');
        });
    }

    // Voice Speed & Pitch Pills Interaction
    speedPills.forEach(pill => {
        pill.addEventListener('change', () => {
            document.querySelectorAll('.voice-pills-row input[name="narration-speed"]').forEach(input => {
                input.closest('.voice-pill').classList.toggle('active', input.checked);
            });
            voiceNarrator.updateVoiceSettings();
        });
    });

    pitchPills.forEach(pill => {
        pill.addEventListener('change', () => {
            document.querySelectorAll('.voice-pills-row input[name="voice-pitch"]').forEach(input => {
                input.closest('.voice-pill').classList.toggle('active', input.checked);
            });
            voiceNarrator.updateVoiceSettings();
        });
    });

    if (voiceSelect) {
        voiceSelect.addEventListener('change', () => {
            voiceNarrator.updateVoiceSettings();
        });
    }

    if (voiceLanguageSelect) {
        voiceLanguageSelect.addEventListener('change', () => {
            voiceNarrator.updateVoiceSettings();
        });
    }

    // =========================================================================
    // 7. STORY GENERATION SUBMISSION HANDLER (Google Gemini API Backend)
    // =========================================================================
    function triggerAutoplayIfNeeded(data, lang) {
        if (autoplayCheckbox && autoplayCheckbox.checked) {
            setTimeout(() => {
                try {
                    voiceNarrator.start(data.title, data.story, data.language || lang);
                } catch (audioErr) {
                    console.warn("Autoplay was prevented by browser policy:", audioErr);
                }
            }, 600);
        }
    }

    if (storyForm) {
        storyForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (isSubmitting) return;

            const idea = ideaInput.value.trim();
            const languageInput = document.querySelector('input[name="language"]:checked');
            const engineInput = document.querySelector('input[name="engine"]:checked');
            const categoryInput = document.querySelector('input[name="category"]:checked');
            const lengthInput = document.querySelector('input[name="length"]:checked');
            const customTitle = customTitleInput ? customTitleInput.value.trim() : "";

            // Client-side validation
            if (!idea || idea.length < 3) {
                if (ideaError) {
                    ideaError.textContent = "Please provide an idea for your ghost story (at least 3 characters).";
                }
                ideaInput.focus();
                return;
            }

            clearError();

            const language = languageInput ? languageInput.value : "English";
            const category = categoryInput ? categoryInput.value : "Haunted House";
            const length = lengthInput ? lengthInput.value : "Medium";
            const useLore = engineInput ? (engineInput.value === "lore") : false;

            // Stop any existing narration when generating a new story
            voiceNarrator.stop();

            // Prepare UI state for loading
            setGeneratingState(true);

            const customApiKey = localStorage.getItem('custom_gemini_api_key') || "";
            const headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Allow-Lore-Fallback': 'true'
            };
            if (customApiKey) {
                headers['X-Gemini-API-Key'] = customApiKey;
            }
            if (useLore) {
                headers['X-Use-Lore-Engine'] = 'true';
            }

            const bodyPayload = {
                idea: idea,
                category: category,
                length: length,
                language: language,
                title: customTitle,
                use_lore_engine: useLore,
                allow_lore_fallback: true
            };
            if (customApiKey) {
                bodyPayload.api_key = customApiKey;
            }

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(bodyPayload)
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    // Auto-rescue: Seamlessly switch to Ancestral Lore Engine if API key is unconfigured
                    if (data.code === "MISSING_API_KEY" || data.can_fallback_to_lore) {
                        console.log("No Gemini API key detected. Seamlessly invoking Ancestral Lore Engine...");
                        const lorePill = document.getElementById('engine-pill-lore');
                        if (lorePill) lorePill.click();

                        bodyPayload.use_lore_engine = true;
                        headers['X-Use-Lore-Engine'] = 'true';

                        const retryRes = await fetch('/generate', {
                            method: 'POST',
                            headers: headers,
                            body: JSON.stringify(bodyPayload)
                        });
                        const retryData = await retryRes.json();
                        if (retryRes.ok && retryData.success) {
                            clearError();
                            displayStoryResult(retryData);
                            triggerAutoplayIfNeeded(retryData, language);
                            return;
                        }
                    }

                    const errMsg = data.error || "The ghost realm is temporarily unavailable. Please try again shortly.";
                    const canFallback = Boolean(data.can_fallback_to_lore || data.code === "MISSING_API_KEY");
                    showError(errMsg, null, canFallback);
                    return;
                }

                // Render real story safely
                clearError();
                displayStoryResult(data);
                triggerAutoplayIfNeeded(data, language);

            } catch (networkError) {
                console.error("Network or server connection error:", networkError);
                showError("Network error: Unable to contact the story generator. Please check your internet connection.");
            } finally {
                setGeneratingState(false);
            }
        });
    }

    function setGeneratingState(isGenerating) {
        isSubmitting = isGenerating;
        if (generateBtn) {
            generateBtn.disabled = isGenerating;
            const btnText = generateBtn.querySelector('.btn-text');
            if (btnText) {
                btnText.textContent = isGenerating ? "SUMMONING FROM THE REALM..." : "GENERATE MY GHOST STORY";
            }
        }

        if (loadingPanel) {
            if (isGenerating) {
                loadingPanel.classList.remove('hidden');
                loadingPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                loadingPanel.classList.add('hidden');
            }
        }
    }

    // =========================================================================
    // 8. DISPLAY STORY RESULT (SAFE DOM RENDERING & CODE BLOCKS)
    // =========================================================================
    function displayStoryResult(data) {
        currentStoryData = data;

        if (resultTitle) resultTitle.textContent = data.title || "The Unnamed Apparition";
        if (resultCategory) resultCategory.textContent = data.category || "Ghost Story";
        if (resultLength) resultLength.textContent = data.length || "Medium";
        if (resultModel) {
            const langLabel = data.language ? ` • ${data.language}` : '';
            if (data.is_failsafe) {
                resultModel.innerHTML = `Ancestral Lore Engine <span class="failsafe-badge">Quota Shield 🛡️</span>${langLabel}`;
            } else {
                resultModel.textContent = `Google Gemini (${data.model || "gemini-2.0-flash"}${langLabel})`;
            }
        }

        // Reset voice narration player state for new story
        if (narrationStatus) {
            const langName = data.language === 'Hindi' ? 'Hindi (हिन्दी)' : 'English';
            narrationStatus.textContent = `Ready to narrate in ${langName}. Press Listen to Story!`;
        }
        if (narrationProgressFill) narrationProgressFill.style.width = '0%';
        voiceNarrator.updatePlayerUI('idle');

        // Render story paragraphs and code blocks safely (prevents XSS vulnerabilities)
        if (resultStory) {
            resultStory.innerHTML = '';
            const rawStory = data.story || "";
            const paragraphs = rawStory.split(/\n\s*\n/).filter(p => p.trim().length > 0);

            if (paragraphs.length > 0) {
                paragraphs.forEach(paraText => {
                    paraText = paraText.trim();
                    if (paraText.startsWith('```') && paraText.endsWith('```')) {
                        const pre = document.createElement('pre');
                        const code = document.createElement('code');
                        const lines = paraText.split('\n');
                        code.textContent = lines.slice(1, -1).join('\n');
                        pre.appendChild(code);
                        resultStory.appendChild(pre);
                    } else if (paraText.includes('```')) {
                        const parts = paraText.split(/(```[\s\S]*?```)/g);
                        parts.forEach(part => {
                            if (part.startsWith('```') && part.endsWith('```')) {
                                const pre = document.createElement('pre');
                                const code = document.createElement('code');
                                const lines = part.split('\n');
                                code.textContent = lines.slice(1, -1).join('\n');
                                pre.appendChild(code);
                                resultStory.appendChild(pre);
                            } else if (part.trim()) {
                                const p = document.createElement('p');
                                p.textContent = part.trim();
                                resultStory.appendChild(p);
                            }
                        });
                    } else {
                        const p = document.createElement('p');
                        p.textContent = paraText;
                        resultStory.appendChild(p);
                    }
                });
            } else {
                const p = document.createElement('p');
                p.textContent = rawStory;
                resultStory.appendChild(p);
            }
        }

        if (resultCard) {
            resultCard.classList.remove('hidden');
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // =========================================================================
    // 9. COPY STORY TO CLIPBOARD
    // =========================================================================
    if (copyStoryBtn) {
        copyStoryBtn.addEventListener('click', async () => {
            if (!currentStoryData) return;

            const engineName = `Google Gemini (${currentStoryData.model || "gemini-2.5-flash"})`;
            const textToCopy = `${currentStoryData.title}\n\nCategory: ${currentStoryData.category} | Length: ${currentStoryData.length} | Language: ${currentStoryData.language || 'English'}\nAI Engine: ${engineName}\n\n${currentStoryData.story}`;

            try {
                if (navigator.clipboard && window.isSecureContext) {
                    await navigator.clipboard.writeText(textToCopy);
                } else {
                    const textArea = document.createElement("textarea");
                    textArea.value = textToCopy;
                    textArea.style.position = "fixed";
                    textArea.style.left = "-999999px";
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    document.execCommand('copy');
                    textArea.remove();
                }

                if (copyToast) {
                    copyToast.classList.remove('hidden');
                    setTimeout(() => {
                        copyToast.classList.add('hidden');
                    }, 3000);
                }
            } catch (err) {
                console.error("Failed to copy text:", err);
                alert("Could not automatically copy to clipboard. Please select the story text manually.");
            }
        });
    }

    // =========================================================================
    // 10. DOWNLOAD STORY AS TXT FILE
    // =========================================================================
    if (downloadStoryBtn) {
        downloadStoryBtn.addEventListener('click', () => {
            if (!currentStoryData) return;

            const safeTitle = (currentStoryData.title || "ghost-story")
                .toLowerCase()
                .replace(/[^a-z0-9]/g, '-')
                .replace(/-+/g, '-')
                .replace(/^-|-$/g, '');

            const filename = `${safeTitle || 'ghost-story'}.txt`;
            const engineLabel = `Google Gemini (${currentStoryData.model || "gemini-2.5-flash"})`;

            const fileContent = `=====================================================
${currentStoryData.title.toUpperCase()}
=====================================================
Language: ${currentStoryData.language || 'English'}
Category: ${currentStoryData.category}
Length:   ${currentStoryData.length}
Engine:   ${engineLabel}
Date:     ${new Date().toLocaleDateString()}
=====================================================

${currentStoryData.story}

=====================================================
Generated by AI Ghost Story Generator
"Turn Your Imagination into Terrifying Ghost Stories!"
=====================================================
`;

            const blob = new Blob([fileContent], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }

    // =========================================================================
    // 11. GENERATE ANOTHER STORY
    // =========================================================================
    if (generateAnotherBtn) {
        generateAnotherBtn.addEventListener('click', () => {
            voiceNarrator.stop();
            const generatorSection = document.getElementById('generator');
            if (generatorSection) {
                generatorSection.scrollIntoView({ behavior: 'smooth' });
            }
            if (ideaInput) {
                ideaInput.focus();
                ideaInput.select();
            }
        });
    }

    // =========================================================================
    // 12. RESPONSIVE MOBILE NAVIGATION MENU
    // =========================================================================
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
            mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
            mobileMenuBtn.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                mobileMenuBtn.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }

    // =========================================================================
    // 13. CUSTOM GEMINI API KEY MODAL (BRING YOUR OWN KEY)
    // =========================================================================
    const keyModal = document.getElementById('key-modal');
    const openKeyModalBtn = document.getElementById('open-key-modal-btn');
    const closeKeyModalBtn = document.getElementById('close-key-modal-btn');
    const customKeyInput = document.getElementById('custom-gemini-key');
    const saveKeyBtn = document.getElementById('save-key-btn');
    const clearKeyBtn = document.getElementById('clear-key-btn');
    const toggleKeyVisibilityBtn = document.getElementById('toggle-key-visibility-btn');
    const keyStatusText = document.getElementById('key-status-text');
    const navKeyBtn = document.getElementById('open-key-modal-btn');
    const navKeyText = document.getElementById('nav-key-text');

    function updateKeyModalUI() {
        const savedKey = localStorage.getItem('custom_gemini_api_key') || "";
        if (customKeyInput) customKeyInput.value = savedKey;

        if (savedKey) {
            if (keyStatusText) keyStatusText.textContent = "Active (Using Your Personal Gemini Key)";
            if (navKeyBtn) navKeyBtn.classList.add('has-key');
            if (navKeyText) navKeyText.textContent = "Custom Key (Active)";
        } else {
            if (keyStatusText) keyStatusText.textContent = "Using Shared Server Key & Quota Shield";
            if (navKeyBtn) navKeyBtn.classList.remove('has-key');
            if (navKeyText) navKeyText.textContent = "Gemini Key";
        }
    }

    if (openKeyModalBtn && keyModal) {
        openKeyModalBtn.addEventListener('click', () => {
            updateKeyModalUI();
            keyModal.classList.remove('hidden');
            if (customKeyInput) customKeyInput.focus();
        });
    }

    if (closeKeyModalBtn && keyModal) {
        closeKeyModalBtn.addEventListener('click', () => {
            keyModal.classList.add('hidden');
        });
    }

    if (keyModal) {
        keyModal.addEventListener('click', (e) => {
            if (e.target === keyModal) {
                keyModal.classList.add('hidden');
            }
        });
    }

    if (toggleKeyVisibilityBtn && customKeyInput) {
        toggleKeyVisibilityBtn.addEventListener('click', () => {
            const isPassword = customKeyInput.type === 'password';
            customKeyInput.type = isPassword ? 'text' : 'password';
            toggleKeyVisibilityBtn.textContent = isPassword ? '🔒' : '👁️';
        });
    }

    if (saveKeyBtn && customKeyInput) {
        saveKeyBtn.addEventListener('click', () => {
            const val = customKeyInput.value.trim();
            if (val) {
                localStorage.setItem('custom_gemini_api_key', val);
            } else {
                localStorage.removeItem('custom_gemini_api_key');
            }
            updateKeyModalUI();
            if (keyModal) keyModal.classList.add('hidden');
        });
    }

    if (clearKeyBtn) {
        clearKeyBtn.addEventListener('click', () => {
            localStorage.removeItem('custom_gemini_api_key');
            if (customKeyInput) customKeyInput.value = '';
            updateKeyModalUI();
            if (keyModal) keyModal.classList.add('hidden');
        });
    }

    // Auto-detect server configuration and auto-select Lore Engine if key is unconfigured
    async function checkServerHealthAndConfig() {
        try {
            const res = await fetch('/health');
            if (res.ok) {
                const data = await res.json();
                const customKey = localStorage.getItem('custom_gemini_api_key') || "";
                if (!data.api_key_configured && !customKey) {
                    const lorePill = document.getElementById('engine-pill-lore');
                    if (lorePill) lorePill.click();
                }
            }
        } catch (e) {
            // Ignore background health check errors
        }
    }

    // Initialize UI on load
    updateKeyModalUI();
    checkServerHealthAndConfig();
});

