"""Video prompt categories and format definitions."""

from common.prompt_styles import SHARED_STYLES

VIDEO_CATEGORIES = {
    "cinematic": {
        "name": "Cinematic Movie Scene",
        "format": [
            "Genre/setting",
            "Main character/subject",
            "Action",
            "Environment details",
            "Mood",
            "Camera techniques",
            "Lighting style"
        ],
        "keywords": [
            "movie", "film", "epic", "battle", "scene", "dramatic", "knight",
            "hero", "villain", "noir", "thriller", "action", "war", "fight"
        ],
        "examples": [
            "An epic fantasy battle scene at dusk on a misty plain. A lone knight rises from the ground and draws a glowing sword as armies charge behind him. Slow-motion highlights dust and embers in the air, with dramatic backlighting casting a heroic silhouette, and the camera pulls back in a wide, sweeping shot to reveal the scale of the conflict.",
            "A film noir detective scene in a 1940s city. A trench-coated detective walks down a dim alley under flickering streetlamps in pouring rain. Low-key lighting and deep shadows create mystery. The camera follows in a tracking shot from behind, then cuts to a close-up of water dripping off his hat as jazzy music plays in the background."
        ]
    },
    "animation": {
        "name": "Animation/Cartoon Sequence",
        "format": [
            "Animation style",
            "Characters/creatures",
            "Action/story",
            "Visual style",
            "Stylistic influences",
            "Camera movements",
            "Lighting conditions"
        ],
        "keywords": [
            "cartoon", "anime", "animated", "pixar", "2d", "3d", "character",
            "cute", "funny", "disney", "ghibli", "toon"
        ],
        "examples": [
            "A Pixar-style 3D animated scene of two talking cats on a rooftop at sunset. One cat strums a guitar while the other sings. The style is cute and cartoonish with vibrant colors and exaggerated expressions. Soft, warm lighting from the setting sun creates long shadows, and the camera does a slow zoom as they perform, capturing a heartwarming mood.",
            "A 2D anime action sequence in a futuristic city. A cyberpunk hero with a neon visor leaps between hovering cars, chasing a villain. The visual aesthetic is high-energy anime, with dynamic motion lines and glowing neon lights against a dark skyline. The scene uses quick cuts and a dramatic angle from below to intensify the action."
        ]
    },
    "fashion": {
        "name": "Fashion Show Runway",
        "format": [
            "Venue/theme",
            "Model(s) and attire",
            "Actions/poses",
            "Atmosphere",
            "Camera work",
            "Lighting descriptors",
            "Overall vibe"
        ],
        "keywords": [
            "fashion", "runway", "model", "dress", "outfit", "couture",
            "designer", "catwalk", "style", "clothing", "gown"
        ],
        "examples": [
            "A high-fashion runway scene in Paris, inside a grand hall with a reflective black floor. A model in an avant-garde red gown glides down the catwalk. Bright white spotlights follow her every move, and camera flashes sparkle from the audience. The camera shoots in slow motion as the gown's train billows, capturing an elegant and dramatic vibe with each step.",
            "A summer beachwear fashion show at an outdoor seaside venue. Models in light, tropical outfits walk barefoot on a sand-covered runway. The atmosphere is casual and upbeat – natural golden-hour lighting and tiki torches provide a warm glow. A drone camera gives an aerial shot of the runway by the waves, then cuts to a close-up of a model's flowing cover-up as music pumps."
        ]
    },
    "product": {
        "name": "Product Showcase/Advertisement",
        "format": [
            "Product",
            "Setting/backdrop",
            "Demonstration",
            "Visual style",
            "Text/graphics overlays",
            "Camera movements",
            "Brand style"
        ],
        "keywords": [
            "product", "commercial", "advertisement", "demo", "showcase",
            "brand", "marketing", "promo", "ad", "sell", "launch"
        ],
        "examples": [
            "A commercial showcasing the latest smartphone. The phone rotates slowly against a clean white background while soft studio lighting highlights its glossy finish. Close-up shots show the camera lens and edge-to-edge screen. Then, the scene cuts to the phone in use: a person snapping a photo at night, and the image is crystal clear – demonstrating the low-light camera feature with a text overlay. The style is sleek, high-tech, and cinematic, with a smooth tracking shot following the phone's movement.",
            "A product demo video for a blender in a kitchen setting. A presenter blends a variety of fruits; the prompt details the blender's stainless steel design and bright digital display. Natural morning light fills the kitchen, giving a fresh feel. Shots alternate between wide shots of the whole counter and close-ups of the blender's blades in action, even a slow-motion segment of fruit swirling. The prompt ends with the blender pouring a smoothie, emphasizing a vibrant, healthy-lifestyle vibe."
        ]
    },
    "nature": {
        "name": "Nature Documentary Segment",
        "format": [
            "Location and time",
            "Subject",
            "Action/behavior",
            "Sensory details",
            "Camera style",
            "Lighting conditions",
            "Narrative tone"
        ],
        "keywords": [
            "nature", "wildlife", "animal", "documentary", "ocean", "forest",
            "safari", "bird", "fish", "landscape", "mountain", "river", "sea"
        ],
        "examples": [
            "A nature documentary scene at dawn on the African savannah. A herd of elephants gathers around a watering hole, mist rising as the first light of day paints the sky in pastel hues. The camera begins with an aerial wide shot showing the vast golden plains, then zooms in to a close-up of a mother elephant guiding her calf to drink. Soft, natural lighting and a gentle pan across the scene create a serene, majestic mood, as a calm narration describes their morning routine.",
            "An underwater documentary clip in a coral reef. A sea turtle glides through crystal-clear water over colorful corals while schools of fish scatter. The scene is described with vivid color detail – bright oranges and blues of the reef. Sun rays pierce the water from above, illuminating the turtle in shafts of light. The camera follows in steady tracking shots, occasionally shifting to slow motion to capture the turtle nibbling on seagrass, conveying an intimate look at marine life."
        ]
    },
    "travel": {
        "name": "Travel Vlog or Adventure Video",
        "format": [
            "Destination/setting",
            "Traveler/host",
            "Activities/sights",
            "Shot variety",
            "Atmosphere",
            "Text/voice-over style",
            "Tone"
        ],
        "keywords": [
            "travel", "vlog", "adventure", "explore", "destination", "trip",
            "journey", "tourist", "vacation", "backpack", "city", "country"
        ],
        "examples": [
            "A travel vlog in Tokyo at night. The prompt follows a vlogger walking through Shibuya Crossing, neon signs and crowds all around. Handheld first-person camera captures the energy – bright billboards in vibrant colors, people rushing by. Time-lapse segments show the scramble crossing from above, the flow of people like currents. Then we cut to the vlogger enjoying street food at a night market, shot in close-up to show steaming takoyaki. The video style is energetic and immersive, with quick cuts and POV angles that make the viewer feel present in the bustling city.",
            "An adventure travel montage in New Zealand. It opens with a drone shot soaring over snow-capped mountains and a valley of green. The traveler is seen hiking a ridge (captured in a wide long shot to show scale), then switches to first-person perspective crossing a swinging bridge. Scenes of kayaking in a turquoise lake and camping under a starry sky are described. The prompt highlights natural colors – lush greens, deep blue water, golden sunlight – and uses smooth transitions (a slow fade from the mountain to the lake scene) to create a dreamy, inspiring journey feel."
        ]
    },
    "music": {
        "name": "Music Video Performance",
        "format": [
            "Artist/band",
            "Performance setting",
            "Camera movements",
            "Lighting",
            "Concept/storyline elements",
            "Visual alignment"
        ],
        "keywords": [
            "music", "song", "band", "performance", "concert", "singer",
            "dance", "mv", "clip", "rock", "pop", "hip-hop", "stage"
        ],
        "examples": [
            "A rock music video set in an abandoned warehouse. The band performs on a makeshift stage, the lead singer belting into the mic while the guitarist leaps. Dynamic lighting flashes in time with the drum beats – think strobing red and blue lights in the dark space. The camera is very active: handheld close-ups on the singer's face for the chorus, rapid cuts to the drummer's solo with flying drumsticks, and a 360° tracking shot circling the band during the climactic guitar riff. Sparks fly from a rig behind the stage as the final chord hits, matching the high energy.",
            "A pop music video on a rooftop at sunset. The singer dances on the edge of the roof with the city skyline behind her. Golden hour light casts a warm glow on the scene. The prompt describes smooth, floating camera movements – a continuous crane shot that starts behind the singer, rises up above her during the chorus, and then swoops around to reveal a group of backup dancers. Slow-motion is used on a few beats as she flips her hair, emphasizing emotional moments in the soft pop ballad. The style feels cinematic and emotive, matching the song's uplifting tone."
        ]
    },
    "sports": {
        "name": "Sports Highlight or Action Sequence",
        "format": [
            "Sport/action",
            "Main athlete/participants",
            "Moment/skill",
            "Camera techniques",
            "Dynamic angles",
            "Crowd/stadium effects",
            "Pacing"
        ],
        "keywords": [
            "sports", "game", "match", "athlete", "action", "basketball",
            "football", "soccer", "tennis", "race", "competition", "goal"
        ],
        "examples": [
            "A basketball game highlight: last seconds of the championship. Player 23 sprints down the court and leaps for a slam dunk. The camera follows in slow motion as he takes off, showing sweat and determination on his face. We see an over-the-rim angle of the ball smashing through the hoop. Immediately the view cuts to a wide shot of the arena as the buzzer sounds, crowd erupting. High-contrast lighting highlights the players against the bright arena. The prompt captures the intensity with quick cuts and a dramatic replay from a floor-level camera as the dunk happens.",
            "A skateboarding video at an urban skate park. The scene focuses on one skater about to attempt a big trick: a 360º kickflip off a stair set. As he launches, the prompt describes a slow-motion mid-air shot — the skateboard flips beneath him, sunlight gleaming off its underside. Then a GoPro-style POV shows the landing from the skater's eyes. We get a low-angle shot from the ground as he lands smoothly. The video style is gritty and quick-cut, occasionally switching to fisheye lens to follow the action closely, matching the edgy, exciting tone."
        ]
    },
    "news": {
        "name": "News Report or Broadcast Segment",
        "format": [
            "Context",
            "Anchor/reporter",
            "Topic",
            "Camera angles",
            "Graphics/headlines",
            "Props/surroundings",
            "Tone"
        ],
        "keywords": [
            "news", "broadcast", "report", "anchor", "journalist", "breaking",
            "headline", "interview", "press", "media", "tv", "live"
        ],
        "examples": [
            "A TV news broadcast in a modern studio. An anchor in a navy suit sits at a news desk, with a large screen behind showing the headline 'Global Markets Update'. Even, cool lighting illuminates the desk. The prompt describes the camera on a medium shot of the anchor, who shuffles papers and begins speaking. A ticker tape with scrolling text is visible at the bottom of the frame. Then it switches to a split-screen showing the anchor on one side and footage of stock traders on the other. The style is polished and straightforward, just like a live news broadcast.",
            "A field news report from a storm site. A reporter in a raincoat stands in front of a flooded street, holding a microphone with a network logo. It's windy and raining – you can see raindrops on the camera lens and the reporter's hair whipping. The camera is a handheld shot to convey urgency, occasionally zooming to show rescue workers in the background. On-screen, a graphic in the corner reads 'Breaking News – Flood Aftermath'. The prompt maintains a serious, urgent tone, capturing the look and feel of a live breaking-news segment."
        ]
    },
    "educational": {
        "name": "Educational Explainer or Tutorial",
        "format": [
            "Topic",
            "Presenter/format",
            "Setting",
            "Visual elements",
            "Demonstration focus",
            "Camera focus",
            "Style/tone"
        ],
        "keywords": [
            "tutorial", "explain", "how to", "learn", "teach", "education",
            "lesson", "guide", "step", "instruction", "course", "demo"
        ],
        "examples": [
            "A science explainer video about volcanoes. A presenter in a lab coat stands beside a table with a small volcano model. In a bright studio setting with graphics screens, she pours vinegar into a baking soda volcano model. The prompt describes a close-up as it foams and erupts, then cuts to a graphic overlay showing a cross-section of a real volcano. The visuals are clean and instructive – the camera alternates between the presenter and supportive graphics. The tone is educational and engaging, as if a teacher is giving a mini-lesson.",
            "A cooking tutorial video for making pasta carbonara. It opens with an overhead shot of ingredients laid out neatly on a kitchen counter. Hands appear and begin the process: cracking eggs, grating cheese. The prompt provides a step-by-step visual: a close-up of eggs being whisked, then a cut to the stove where pancetta sizzles in a pan. The kitchen is well-lit with natural light for clarity. The camera occasionally switches to a front angle where the cook briefly appears explaining tips, then back to the overhead view. The style is clear, step-by-step, and friendly, making it easy for viewers to follow along."
        ]
    },
    "gaming": {
        "name": "Video Game Cinematic / Fantasy Cutscene",
        "format": [
            "Theme/genre",
            "Characters/heroes",
            "Environment",
            "Action/dialogue",
            "Camera techniques",
            "Visual effects",
            "Cinematic quality"
        ],
        "keywords": [
            "game", "gaming", "rpg", "fantasy", "sci-fi", "cutscene",
            "cinematic", "trailer", "boss", "quest", "level", "player"
        ],
        "examples": [
            "A video game cutscene in a medieval fantasy realm. The elven queen stands on a balcony of a towering tree palace, overlooking her army gathered below in a moonlit forest. The camera cranes from the crowd up to her, showing her determined expression. She raises a glowing staff – sparkling magical particles swirl around her. The style is hyper-realistic CGI with intricate detail on her flowing gown and the ancient tree architecture. A close-up reveals a tear on her cheek as she gives a silent nod. Then dramatic music swells and the scene fades out. It feels like a pivotal cinematic moment in an RPG, full of awe and emotion.",
            "A sci-fi game cinematic on a distant planet. A space marine in futuristic armor takes off his helmet in a barren alien landscape with two setting suns. The visuals are cinematic and atmospheric – dust blows across the cracked ground, and an enormous spaceship wreckage looms in the background. The prompt describes a slow dolly zoom on the marine's face as he gazes at the wreck, conveying scale and gravity. Suddenly, holographic text appears in front of him. The camera then cuts to an over-the-shoulder shot showing a creature moving in the distance. The style is dramatic and immersive, like a high-end game trailer blending character drama with world-building."
        ]
    },
    "historical": {
        "name": "Historical Drama Scene",
        "format": [
            "Era/setting",
            "Characters",
            "Event/action",
            "Authentic visuals",
            "Color tones",
            "Camera work"
        ],
        "keywords": [
            "historical", "period", "medieval", "victorian", "ancient",
            "war", "king", "queen", "castle", "empire", "dynasty", "era"
        ],
        "examples": [
            "A Victorian-era period drama scene in a grand manor. A lady in a lace gown stands by a window waiting anxiously as rain pours outside. The room is lit by flickering gaslight and candles, giving everything a warm, sepia tone. The prompt describes the camera panning slowly across antique furniture to the woman's face. In the background, a faint silhouette of a man with an umbrella approaches through the rain. The style is emotional and old-fashioned, with a steady, deliberate camera capturing the detail of the period costume and set.",
            "A medieval battle camp at dawn, from a historical epic. Knights in battered armor gather around a campfire, their breath visible in the cold air. Tents and banners bearing a king's crest dot the foggy field. The scene starts with an establishing wide shot of the encampment in the valley, then moves to a deep focus shot of the knights talking – we see both the men in the foreground and rows of horsemen preparing in the distance in focus. Natural light sets a somber mood. The camera gently dollies through the scene as one knight secures his sword, emphasizing the gritty realism and tension before battle."
        ]
    }
}

DEFAULT_CATEGORY = "nature"

VALID_CATEGORIES = list(VIDEO_CATEGORIES.keys())

# Video-specific styles (camera movements, cinematic techniques, etc.)
VIDEO_ONLY_STYLES = {
    "camera_movements": {
        "name": "Camera Movements",
        "options": [
            "Static shot", "Pan", "Tilt", "Zoom in", "Zoom out", "Dolly in", "Dolly out", "Tracking shot", "Trucking shot", "Crane shot",
            "Jib shot", "Steadicam shot", "Handheld shot", "Gimbal shot", "Drone shot", "Aerial shot", "Arc shot", "Whip pan", "Whip tilt",
            "Rack focus", "Push in", "Pull out", "360-degree shot", "POV moving shot", "Tracking POV", "Long take / Oner", "Slow motion movement",
            "Time-lapse pan", "Tabletop spin", "Vertigo shot", "Pedestal move", "Tilt-pan combination", "Roll"
        ]
    },
    "cinematic_techniques": {
        "name": "Cinematic Techniques & Special Effects",
        "options": [
            "Slow motion", "Fast motion", "Time-lapse", "Hyperlapse", "Stop-motion style", "Freeze frame", "Bullet time", "Dolly zoom",
            "One-shot sequence", "Montage sequence", "Split screen", "Green screen compositing", "Chroma key effect", "Match cut", "Jump cut",
            "Smash cut", "Crossfade", "Whip pan transition", "Fade to black", "Dream sequence effect", "Flashback cut", "Fast cut edits",
            "Slow dissolve", "Match dissolve", "Wipe transition", "Graphic overlay", "CGI effects", "Practical effects", "Miniature effects",
            "Pyrotechnics", "Motion capture", "Fourth wall break", "Slow push-in", "Crash zoom", "Speed ramping"
        ]
    },
    "animation_medium": {
        "name": "Animation & Medium Styles",
        "options": [
            "2D animation", "3D animation", "Hand-drawn animation", "Anime style animation", "Cartoon style", "Motion graphics",
            "Stop-motion animation", "Claymation", "Puppetry", "Live-action", "Mixed media", "Rotoscoping", "Cut-out animation",
            "Silhouette animation", "Pixel art animation", "Low-poly CGI", "Vector art style", "Stick-figure animation",
            "Clay sculpture animation", "CGI realism", "Cel animation", "Flipbook style", "Typography animation", "Whiteboard animation",
            "Infographic animation", "Animatronic", "VR animation", "Stop-motion with objects", "Experimental animation",
            "Clay/Puppet hybrid", "High frame rate animation", "Vintage Disney style", "Unreal engine cinematic"
        ]
    },
    "editing_transitions": {
        "name": "Editing & Transitions",
        "options": [
            "Cut", "Hard cut", "Jump cut", "Match cut", "L-cut", "J-cut", "Cross-cutting", "Parallel editing", "Montage",
            "Continuous take", "Fast cutting", "Slow cutting", "Dissolve", "Crossfade", "Fade in", "Fade out", "Wipe", "Iris in/out",
            "Smash cut", "Cutaway", "Insert", "Match dissolve", "Jump dissolve", "Split edit", "Freeze-frame", "Speed ramp",
            "Cut to black", "Flash cut", "Montage sequence", "Continuity editing", "Jumpy editing", "Non-linear narrative", "Slow fade",
            "Cross-cut montage", "Parallel action"
        ]
    }
}

# Combine shared + video-specific styles
VIDEO_STYLES = {**SHARED_STYLES, **VIDEO_ONLY_STYLES}
