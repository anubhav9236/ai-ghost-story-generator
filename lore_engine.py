"""
Ancestral Lore Engine - High-Fidelity Procedural & Quota-Resilient Horror Story Synthesizer
Provides atmospheric, context-aware horror story and cursed code generation when cloud LLM quotas are exhausted.
Supports English and Hindi across all 7 horror categories and configurable lengths.
"""

import re
import random

CATEGORY_PRESETS_EN = {
    "Cursed Code": {
        "titles": [
            "The 3:33 AM Pull Request",
            "Stack Trace from the Void",
            "Segmentation Fault in the Astral Plane",
            "The Dead Process That Wouldn't Terminate",
            "Binary Incantations of Repository 13",
            "The Infinite Loop of Blackwood Server",
            "The Uncommitted Memory Leak"
        ],
        "code_snippets": [
'''```c
// [CRITICAL ERROR: Corrupted Stack Frame at 0x00000333]
// WARNING: Do NOT execute on machines with microphone or camera enabled.
void* summon_daemon_thread(void *soul_ptr) {
    while (!process_terminated) {
        detect_pulse_through_keyboard();
        if (room_temperature_drops()) {
            mirror_user_reflection_in_screen();
            open_socket_to_void(0xDEAD);
        }
    }
    return (void*)0x666; // Loop is perpetual; memory is eternal
}
```''',
'''```python
# WARNING: Auto-generated subroutine discovered in legacy backup
import os, sys, paranormal

class LivingRepository:
    def __init__(self, target_host):
        self.host = target_host
        self.heartbeat = True
        self.specter_id = 0xDEADBEEF

    def listen_in_darkness(self):
        while self.heartbeat:
            unseen = paranormal.scan_shadow_behind_chair()
            if unseen.is_breathing:
                sys.stdout.write("WE ARE ALREADY INSIDE YOUR MEMORY\\n")
                sys.stdout.flush()
```''',
'''```rust
// Compile-time assertion failed: Thread bound to mortal observer
fn execute_cursed_instruction() -> Result<(), SpectralAnomaly> {
    let mut shadow_stream = AstralStream::bind("127.0.0.1:6666")?;
    loop {
        if shadow_stream.detect_gaze_upon_monitor() {
            shadow_stream.send_signal(b"DO NOT LOOK BEHIND YOU")?;
            panic!("Mortal process terminated by external presence.");
        }
    }
}
```'''
        ]
    },
    "Haunted House": {
        "titles": [
            "The Whispering Floorboards of Blackwood Manor",
            "Shadows in the Master Bedroom",
            "The Locked Cellar of Crowhurst Hall",
            "Echoes of the Gilded Parlor",
            "The Attic That Never Was",
            "The Portrait with Unblinking Eyes"
        ]
    },
    "Ghost Mystery": {
        "titles": [
            "The Unsolved Secret of Room 217",
            "The Vanishing of Abigail Crane",
            "Clues Left in Cold Ash",
            "The Silent Telegram of 1928",
            "The Lantern on Widow\'s Walk",
            "The Ledger of the Drowned"
        ]
    },
    "Ancient Folklore": {
        "titles": [
            "The Curse of the Witch\'s Hollow",
            "The Blood Oak of Elderfield",
            "The Howl Across the Mist Valley",
            "Offerings to the Bog Mother",
            "The Stone Ring of the Forgotten",
            "The Midnight Chime of the Forest Bell"
        ]
    },
    "Supernatural Horror": {
        "titles": [
            "The Presence in the Mirror",
            "Cold Hands in the Pitch Dark",
            "The Figure at the Foot of the Bed",
            "The Knocking Inside the Walls",
            "The Faceless Guest of Autumn",
            "The Shadow That Cast No Light"
        ]
    },
    "Halloween Adventure": {
        "titles": [
            "The Night the Jack-o\'-Lanterns Spoke",
            "The Phantom Carnival on Elm Ridge",
            "The Trick That Never Ended",
            "The Midnight Hayride into Oblivion",
            "The Mask That Wouldn\'t Come Off",
            "The Graveyard Shortcut at All Hallows"
        ]
    },
    "Emotional Ghost Story": {
        "titles": [
            "The Letter Left Upon the Piano",
            "A Waltz for the Unforgotten",
            "The Ghost Who Waited by the Sea",
            "Sorrow Lingering in the Rain",
            "A Lullaby Sung from the Beyond",
            "The Memory of Her Gentle Hand"
        ]
    }
}

CATEGORY_PRESETS_HI = {
    "Cursed Code": {
        "titles": [
            "शापित कोड का काला सच",
            "रात 3:33 का खतरनाक कमिट",
            "अंधेरी दुनिया का टर्मिनल",
            "स्क्रीन में कैद रूह",
            "कयामत की प्रोग्रामिंग"
        ],
        "code_snippets": [
'''```c
// [चेतावनी: 0x00000333 पर अलौकिक गड़बड़ी पाई गई]
void* aatma_loop() {
    while (1) {
        kamre_ka_taapman_kam_karo();
        screen_par_saya_dikhaye();
        darwaja_khud_band_karo();
    }
}
```'''
        ]
    },
    "Haunted House": {
        "titles": [
            "काली हवेली का पुराना राज़",
            "सुनसान कोठी की खौफनाक रात",
            "हवेली की सीढ़ियों पर कदमों की आहट",
            "भूतिया महल का आखिरी चिराग",
            "अमावस्या की रात का साया"
        ]
    },
    "Ghost Mystery": {
        "titles": [
            "कमरा नंबर 13 का रहस्य",
            "पुरानी डायरी का खौफनाक पन्ना",
            "खोई हुई चीख का राज़",
            "तस्वीर जो सब देखती थी",
            "आधी रात की आखिरी गवाही"
        ]
    },
    "Ancient Folklore": {
        "titles": [
            "शापित बरगद और लाल लालटेन",
            "जंगल के पुराने कुएँ का खौफ",
            "गाँव का वो पुराना श्राप",
            "डरावनी चुड़ैल की घाटी",
            "सदी पुरानी रूहानी चेतावनी"
        ]
    },
    "Supernatural Horror": {
        "titles": [
            "आईने में छुपा भयानक चेहरा",
            "अंधेरे में छूने वाले ठंडे हाथ",
            "दीवार के पीछे से आती खटखटाहट",
            "साया जो कभी नहीं छूटता",
            "बिस्तर के नीचे जागती आंखें"
        ]
    },
    "Halloween Adventure": {
        "titles": [
            "कब्रिस्तान का वो वीरान रास्ता",
            "जलती आंखों वाला कद्दू",
            "अक्टूबर की वो डरावनी रात",
            "मुखौटा जो चेहरे से चिपक गया",
            "आधी रात का भूतों का मेला"
        ]
    },
    "Emotional Ghost Story": {
        "titles": [
            "एक रूह का अधूरा इंतजार",
            "पियानो पर गूंजती पुरानी धुन",
            "बारिश में भीगती खामोश याद",
            "मौत के बाद भी कायम मोहब्बत",
            "आखिरी खत जो कभी न पहुंचा"
        ]
    }
}


def clean_premise(raw_idea: str) -> str:
    """Extract and sanitize a clean narrative clause from user prompt."""
    cleaned = raw_idea.strip().rstrip(".!?:")
    if len(cleaned) > 200:
        cleaned = cleaned[:197] + "..."
    return cleaned


def generate_failsafe_story(idea: str, category: str = "Haunted House", length: str = "Medium", language: str = "English", custom_title: str = None) -> tuple[str, str]:
    """
    Generate a richly detailed, atmospheric horror story tailored to the user's premise.
    Guarantees instant, zero-latency delivery without relying on external cloud APIs.
    """
    cleaned_idea = clean_premise(idea)
    cat_key = category if category in CATEGORY_PRESETS_EN else "Haunted House"

    if language == "Hindi":
        return _generate_hindi_story(cleaned_idea, cat_key, length, custom_title)
    else:
        return _generate_english_story(cleaned_idea, cat_key, length, custom_title)


def _generate_english_story(idea: str, category: str, length: str, custom_title: str = None) -> tuple[str, str]:
    """Synthesize high-atmosphere English horror fiction."""
    presets = CATEGORY_PRESETS_EN.get(category, CATEGORY_PRESETS_EN["Haunted House"])
    
    # Title selection
    if custom_title and custom_title.strip():
        title = custom_title.strip()
    else:
        title = random.choice(presets["titles"])

    code_snippet = ""
    if category == "Cursed Code":
        code_snippet = random.choice(presets["code_snippets"])

    # Atmospheric sentence pools tailored to horror categories
    openers = [
        f"The night was draped in suffocating silence when it began—born from the uncanny reality of {idea.lower()}.",
        f"No living soul in the county dared speak of what occurred, yet everyone recognized the dread that started with {idea.lower()}.",
        f"It was exactly 3:17 AM when the air turned frigid, carrying the faint scent of damp earth and ozone, all tracing back to {idea.lower()}."
    ]

    anomalies = [
        "At first, the signs were deceptive in their subtlety: a clock ticking slightly out of cadence, shadows lingering a split second too long after the candle flickered, and an inexplicable cold spot that settled heavy in the room.",
        "The temperature dropped so sharply that breath crystallized in white plumes. The floorboards let out a slow, deliberate groan—not the settling of old timber, but the rhythmic, measured tread of barefoot steps approaching.",
        "A low, vibrating resonance hummed through the walls. Every electronic screen in the room pulsed with an eerie static, refracting pale violet light across the ceiling like submerged water ripples."
    ]

    climaxes = {
        "Cursed Code": (
            f"The terminal window began executing commands on its own, spawning subroutines that bypassed every firewall and hardware interrupt:\n\n"
            f"{code_snippet}\n\n"
            f"As the glowing green text burned into the phosphor display, the reflection on the glass didn't mirror the room. It revealed a gaunt, hollow-eyed figure leaning over the developer's shoulder, watching each line compile with eternal patience."
        ),
        "Haunted House": (
            "From the dark alcove, the air thickened into a solid mass. The wallpaper peeled in long curls as long, pale fingers gripped the doorframe. What stepped into the moonlight had no face, only hollow sockets burning with mournful blue luminescence that froze the blood."
        ),
        "Ghost Mystery": (
            "The final missing piece clicked into place with horrifying clarity. The old newspaper clippings, the scratched floorboards, and the cold draft were all directing attention to the space behind the hearth. There, etched into the blackened brick, was a fresh inscription wet with ink that had dried eighty years ago."
        ),
        "Ancient Folklore": (
            "The trees outside ceased their swaying, freezing in complete stillness. From the mist-drenched treeline came the rhythmic chant of the ancients—a guttural verse in a dialect that predated civilization. The boundary between the living soil and the hollow realm dissolved like smoke."
        ),
        "Supernatural Horror": (
            "The reflection in the glass failed to follow the movement. When the hand pulled away, the reflection stayed pressed against the pane, its jaw unhinging in a soundless scream that shattered every lightbulb in the corridor simultaneously."
        ),
        "Halloween Adventure": (
            "The flickering jack-o'-lanterns all extinguished at once, replaced by pale ghastly embers. Out from the autumn fog came a carriage drawn by phantom horses, their hooves silent against the dead leaves, stopping right at the garden gate."
        ),
        "Emotional Ghost Story": (
            "A tender, sorrowful chill brushed against the cheek, like a hand longing to bridge the abyss between this world and the next. In that fragile instant, a familiar whisper echoed through the stillness: 'I never truly left you. I was only waiting for the lights to dim.'"
        )
    }

    twists = [
        "When morning finally fractured the horizon with pale grey light, the room appeared untouched. But on the dusty surface lay two fresh footprints, pointing directly toward the closet door that had been locked from the inside for decades.",
        "The silence that followed was louder than any scream. And as the dawn arrived, one horrifying realization took root: whatever had crossed the threshold had not returned to the void—it was now standing quietly behind the door, listening.",
        "The clocks never ticked again in that house. And those who pass by at night swear they can still see a pale silhouette standing motionless in the second-floor window, watching the road with unwavering eyes."
    ]

    opener_text = random.choice(openers)
    anomaly_text = random.choice(anomalies)
    climax_text = climaxes.get(category, climaxes["Haunted House"])
    twist_text = random.choice(twists)

    paragraphs = []
    if length == "Short":
        # ~200 words
        p1 = f"{opener_text} {anomaly_text}"
        p2 = f"{climax_text}\n\n{twist_text}"
        paragraphs = [p1, p2]
    elif length == "Long":
        # ~650 words
        p1 = opener_text
        p2 = (
            f"Those who knew the history of the place had warned against tampering with such things. "
            f"Generations had whispered of the spectral entity that lingered here, tethered to the tragic remnants of a forgotten ritual. "
            f"Yet curiosity has always been the swiftest path into the jaws of the paranormal."
        )
        p3 = anomaly_text
        p4 = (
            f"Dread coiled tightly in the chest as the boundary between reality and nightmare frayed. "
            f"Every instinct screamed to turn back, to flee into the rain-slicked night, but the legs refused to move—paralyzed by an ancient, predatory stillness."
        )
        p5 = climax_text
        p6 = (
            f"The supernatural manifestation lingered for what felt like an eternity, defying every known law of physics and mortality. "
            f"The air hummed with a vibration so deep it rattled the teeth, smelling faintly of ancient cedar, burnt tallow, and forgotten tombs."
        )
        p7 = twist_text
        paragraphs = [p1, p2, p3, p4, p5, p6, p7]
    else:
        # Medium (~400 words)
        p1 = opener_text
        p2 = anomaly_text
        p3 = (
            f"A pervasive sense of malevolence filled every corner. It became undeniable that the boundary between the living and the spectral realm had been completely breached, invited by the very nature of {idea.lower()}."
        )
        p4 = climax_text
        p5 = twist_text
        paragraphs = [p1, p2, p3, p4, p5]

    story = "\n\n".join(paragraphs)
    return title, story


def _generate_hindi_story(idea: str, category: str, length: str, custom_title: str = None) -> tuple[str, str]:
    """Synthesize high-atmosphere Hindi horror fiction in pure Devanagari script."""
    presets = CATEGORY_PRESETS_HI.get(category, CATEGORY_PRESETS_HI["Haunted House"])

    if custom_title and custom_title.strip():
        title = custom_title.strip()
    else:
        title = random.choice(presets["titles"])

    code_snippet = ""
    if category == "Cursed Code":
        code_snippet = (
            "अचानक स्क्रीन पर खून जैसे लाल अक्षरों में यह शापित कोड चलने लगा:\n\n"
            + random.choice(presets.get("code_snippets", ["```c\n// AATMA LOOP DETECTED\nwhile(1) { darwaja_khatkhatao(); }\n```"]))
            + "\n\n"
        )

    openers = [
        f"रात के सन्नाटे में जब हवाएं भी थम चुकी थीं, तभी उस भयानक घटना की शुरुआत हुई—जिसकी जड़ें '{idea}' से जुड़ी हुई थीं।",
        f"गाँव का कोई भी इंसान उस रास्ते पर जाने की हिम्मत नहीं करता था। सब जानते थे कि जब भी '{idea}' का ज़िक्र होता, मौत का साया करीब आ जाता था।",
        f"रात के ठीक 2:45 बज रहे थे। पुराने शीशम के दरवाजे खुद-ब-खुद चरमराने लगे, और हवा में एक अजीब सी ठंडी सिहरन तैरने लगी, जिसका कारण '{idea}' था।"
    ]

    anomalies = [
        "शुरुआत में सब कुछ बहुत सामान्य लगा, लेकिन फिर अचानक कमरे का तापमान तेजी से गिरने लगा। सांसों से भाप निकलने लगी और कोनों में गहरी परछाइयां हिलने लगीं।",
        "दीवार पर टंगी पुरानी घड़ी की सुइयां उल्टी दिशा में घूमने लगीं। फर्श के नीचे से ऐसी आवाजें आ रही थीं जैसे कोई भारी जंजीरों को खींचता हुआ दरवाजे की ओर बढ़ रहा हो।",
        "अंधेरे में अचानक घुंघरुओं की हल्की झंकार गूंजी। कमरे का हर आईना धुंधला पड़ गया और उस धुंध में कोई बिना पलक झपकाए घूरता हुआ महसूस हुआ।"
    ]

    climaxes = {
        "Cursed Code": (
            f"{code_snippet}कीबोर्ड के बटन अपने-आप दबने लगे। मॉनिटर की नीली रोशनी में एक कंकाल जैसा हाथ कीबोर्ड पर रेंगता हुआ साफ दिखाई दिया।"
        ),
        "Haunted House": (
            "दरवाजे की ओट से एक लंबा, सफेद साया बाहर निकला। उसकी आंखें खाली गड्ढों की तरह थीं, जिनमें नीली खौफनाक आग जल रही थी। उसने एक कंपकपाती उंगली से सामने की ओर इशारा किया।"
        ),
        "Ghost Mystery": (
            "सालों से दफन वो पुराना राज़ आखिरकार सामने आ चुका था। पुरानी संदूक के नीचे मिले उस कंकाल की उंगलियों में वही लाल अंगूठी थी, जो पचास साल पहले गायब हुई दुल्हन की थी।"
        ),
        "Ancient Folklore": (
            "जंगल के उस प्राचीन बरगद के पत्तों से खून की बूंदें टपकने लगीं। हवा में किसी बूढ़ी औरत की दर्दनाक चीख गूंज उठी, जिसने सदियों पुराने उस श्राप को फिर से जीवित कर दिया था।"
        ),
        "Supernatural Horror": (
            "जब आईने में देखा, तो सामने खड़ा अक्स अपनी जगह से हिला ही नहीं। उसका जबड़ा भयानक तरीके से खुला और एक ऐसी आवाज निकली जिसने हड्डियों तक को कंपकपा दिया।"
        ),
        "Halloween Adventure": (
            "सड़क पर रखे सभी कद्दू एक साथ बुझ गए। घने कोहरे में से एक काली बग्गी निकलकर आई, जिसके घोड़े बिना पैरों के हवा में दौड़ रहे थे।"
        ),
        "Emotional Ghost Story": (
            "हवा में एक जानी-पहचानी खुशबू फैली। एक नम, ठंडी छुअन ने माथे को छुआ और कानों में एक धीमी फुसफुसाहट गूंजी: 'डरो मत, मैं हमेशा तुम्हारे साथ हूँ...'"
        )
    }

    twists = [
        "सुबह जब सूरज की पहली किरण कमरे में आई, तो सब कुछ शांत था। लेकिन फर्श पर धूल में दो ताजे पैरों के निशान थे—जो बंद अलमारी की तरफ जाकर अचानक गायब हो गए थे।",
        "सूरज निकलने के बाद भी वो सन्नाटा टूटा नहीं। और एक भयानक सच सबके सामने आ गया: वो साया कहीं गया नहीं था, बल्कि अब भी उसी कमरे में खामोशी से सांस ले रहा था।",
        "गाँव के लोग कहते हैं कि आज भी अमावस की रात उस खिड़की पर एक दिया खुद-ब-खुद जल उठता है, और कोई अंदर से सड़क को निहारता रहता है।"
    ]

    opener_text = random.choice(openers)
    anomaly_text = random.choice(anomalies)
    climax_text = climaxes.get(category, climaxes["Haunted House"])
    twist_text = random.choice(twists)

    if length == "Short":
        p1 = f"{opener_text} {anomaly_text}"
        p2 = f"{climax_text}\n\n{twist_text}"
        paragraphs = [p1, p2]
    elif length == "Long":
        p1 = opener_text
        p2 = "बुजुर्गों ने हमेशा कहा था कि बीती हुई बातों को दोबारा कुरेदना मौत को दावत देने जैसा है। उस हवेली के कमरों में जो कुछ भी कैद था, वो इंसानी दुनिया से परे था।"
        p3 = anomaly_text
        p4 = "दिल की धड़कनें इतनी तेज हो गईं कि अपनी ही सांसों की आवाज कानों में हथौड़ों की तरह बजने लगी। भागने का हर रास्ता बंद हो चुका था।"
        p5 = climax_text
        p6 = "उस भयानक रूहानी साए ने कमरे की पूरी हवा को जहरीला बना दिया था। ऐसा लग रहा था मानो वक्त खुद खौफ के मारे वहीं थम गया हो।"
        p7 = twist_text
        paragraphs = [p1, p2, p3, p4, p5, p6, p7]
    else:
        p1 = opener_text
        p2 = anomaly_text
        p3 = "सन्नाटा इतना गहरा था कि रूह तक कांप उठी। यह साफ हो गया था कि जो साया वहां मौजूद था, वो किसी भी हाल में जिंदा इंसानों को बख्शने के मूड में नहीं था।"
        p4 = climax_text
        p5 = twist_text
        paragraphs = [p1, p2, p3, p4, p5]

    story = "\n\n".join(paragraphs)
    return title, story
