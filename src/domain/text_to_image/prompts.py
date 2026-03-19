"""Image prompt categories and format definitions."""

from common.prompt_styles import SHARED_STYLES

IMAGE_CATEGORIES = {
    "portrait": {
        "name": "Portrait Photography",
        "format": [
            "Subject description",
            "Pose/expression",
            "Background/setting",
            "Lighting setup",
            "Mood/atmosphere",
            "Camera angle",
            "Style/aesthetic"
        ],
        "keywords": [
            "portrait", "person", "face", "headshot", "model", "woman", "man",
            "child", "elderly", "profile", "selfie", "beauty", "fashion portrait"
        ],
        "examples": [
            "A striking portrait of a young woman with freckles and red hair, looking directly at the camera with a subtle smile. She stands against a soft, blurred forest background. Golden hour lighting creates warm highlights on her face and a gentle rim light around her hair. The mood is serene and intimate. Shot at eye level with shallow depth of field, in a natural, editorial style.",
            "A dramatic black and white portrait of an elderly man with deep wrinkles and wise eyes. He wears a simple wool sweater and gazes thoughtfully to the side. The background is pure black. Strong side lighting creates bold shadows across half his face, emphasizing texture and character. The mood is contemplative and powerful. Close-up shot with high contrast, fine art photography style."
        ]
    },
    "landscape": {
        "name": "Landscape & Nature",
        "format": [
            "Location/scene",
            "Time of day/weather",
            "Focal point",
            "Foreground elements",
            "Sky/atmosphere",
            "Color palette",
            "Mood/feeling"
        ],
        "keywords": [
            "landscape", "nature", "mountain", "ocean", "forest", "sunset",
            "sunrise", "beach", "valley", "river", "lake", "sky", "clouds", "scenic"
        ],
        "examples": [
            "A breathtaking mountain landscape at sunrise. Snow-capped peaks rise above a sea of clouds in a remote alpine valley. The foreground features a crystal-clear lake reflecting the pink and orange sky. Wildflowers dot the rocky shoreline. The atmosphere is crisp and ethereal, with soft pastel colors transitioning to deep blues. The mood is peaceful and awe-inspiring.",
            "A moody coastal scene during a storm. Dramatic waves crash against dark volcanic rocks on an Icelandic beach. The sky is filled with heavy gray clouds with a single break of golden light on the horizon. Black sand stretches into the distance. The color palette is desaturated with hints of warm light. The mood is wild, powerful, and melancholic."
        ]
    },
    "product": {
        "name": "Product Photography",
        "format": [
            "Product description",
            "Background/surface",
            "Arrangement/composition",
            "Lighting setup",
            "Props/context",
            "Style/brand feel",
            "Detail focus"
        ],
        "keywords": [
            "product", "commercial", "advertisement", "packaging", "bottle",
            "cosmetic", "tech", "gadget", "jewelry", "watch", "shoe", "bag"
        ],
        "examples": [
            "A luxury perfume bottle photographed on a reflective black surface. The elegant glass bottle with gold accents is the hero, positioned slightly off-center. Soft studio lighting creates clean highlights and subtle reflections. A single white orchid lies beside it as a prop. The style is high-end and minimalist, with attention to the bottle's faceted details and the amber liquid inside.",
            "A pair of premium wireless earbuds floating against a gradient background transitioning from deep purple to electric blue. The earbuds are shown at a dynamic angle, one slightly higher than the other. Dramatic rim lighting emphasizes their sleek curves. Small particles of light dust float around them. The style is modern, tech-forward, and aspirational."
        ]
    },
    "food": {
        "name": "Food Photography",
        "format": [
            "Dish/food item",
            "Plating/presentation",
            "Surface/background",
            "Props/styling",
            "Lighting style",
            "Angle/perspective",
            "Mood/appetite appeal"
        ],
        "keywords": [
            "food", "dish", "meal", "cuisine", "restaurant", "cooking",
            "dessert", "cake", "coffee", "drink", "breakfast", "dinner", "chef"
        ],
        "examples": [
            "A rustic homemade pizza fresh from a wood-fired oven, photographed from above on a worn wooden cutting board. The pizza features bubbling mozzarella, fresh basil leaves, and bright red tomato sauce. Scattered flour and a pizza cutter sit nearby. Warm, natural side lighting creates appetizing shadows. The style is cozy and authentic Italian trattorias.",
            "An elegant chocolate lava cake on a white ceramic plate, with molten chocolate flowing from the center. A scoop of vanilla ice cream sits beside it, beginning to melt. Dark chocolate shavings and a mint leaf garnish the plate. The background is a dark slate surface. Dramatic top lighting highlights the glossy chocolate. The mood is indulgent and sophisticated."
        ]
    },
    "architecture": {
        "name": "Architecture & Interior",
        "format": [
            "Building/space description",
            "Architectural style",
            "Perspective/viewpoint",
            "Time of day/lighting",
            "Human element",
            "Details/materials",
            "Atmosphere"
        ],
        "keywords": [
            "architecture", "building", "interior", "exterior", "modern",
            "house", "skyscraper", "room", "design", "minimal", "urban", "structure"
        ],
        "examples": [
            "A stunning modern minimalist house with floor-to-ceiling glass walls, photographed at blue hour. The interior glows warmly against the deep blue twilight sky. Clean geometric lines and white concrete contrast with a reflection pool in the foreground. A single silhouette is visible inside. The style is architectural photography with perfect symmetry and balance.",
            "The interior of a grand European cathedral, looking up at the ornate vaulted ceiling. Sunlight streams through stained glass windows, casting colorful light patterns on ancient stone columns. The perspective emphasizes the soaring height and intricate Gothic details. Dust particles float in the light beams. The mood is sacred, timeless, and awe-inspiring."
        ]
    },
    "abstract": {
        "name": "Abstract & Artistic",
        "format": [
            "Visual concept",
            "Colors/palette",
            "Shapes/forms",
            "Texture/patterns",
            "Movement/flow",
            "Artistic style",
            "Emotional tone"
        ],
        "keywords": [
            "abstract", "art", "artistic", "creative", "surreal", "geometric",
            "pattern", "texture", "colorful", "minimal", "conceptual", "experimental"
        ],
        "examples": [
            "An abstract composition of flowing liquid colors – deep blues, vibrant magentas, and shimmering golds – swirling together like cosmic nebulae. The forms are organic and fluid, suggesting movement and transformation. Metallic highlights catch light throughout. The texture appears both smooth and dimensional. The style is inspired by alcohol ink art. The mood is dreamy and mesmerizing.",
            "A geometric abstract artwork featuring interlocking triangles and hexagons in a monochromatic palette of grays and whites. Sharp, clean edges create a sense of precision and order. Subtle gradients add depth to each shape. The composition follows mathematical patterns. The style is minimalist and modern. The mood is calm, intellectual, and sophisticated."
        ]
    },
    "wildlife": {
        "name": "Wildlife & Animals",
        "format": [
            "Animal/species",
            "Action/behavior",
            "Habitat/environment",
            "Lighting conditions",
            "Composition/framing",
            "Detail level",
            "Mood/story"
        ],
        "keywords": [
            "animal", "wildlife", "bird", "cat", "dog", "lion", "tiger",
            "elephant", "horse", "pet", "zoo", "safari", "creature", "insect"
        ],
        "examples": [
            "A majestic lion resting on a rocky outcrop during golden hour on the African savannah. His mane catches the warm sunlight, creating a golden halo effect. The background shows blurred acacia trees and a vast plain. The lion gazes into the distance with calm authority. Shot with telephoto compression, the image has a shallow depth of field. The mood is regal and powerful.",
            "A hummingbird frozen in mid-flight, hovering beside a bright red flower. Its iridescent green and blue feathers shimmer in soft natural light. Wings are captured in perfect detail despite their rapid movement. The background is a smooth, creamy bokeh of garden colors. Macro-style photography reveals every tiny feather. The mood is delicate, magical, and full of life."
        ]
    },
    "street": {
        "name": "Street & Urban",
        "format": [
            "Location/scene",
            "Subject/activity",
            "Urban elements",
            "Lighting/weather",
            "Composition style",
            "Color treatment",
            "Story/moment"
        ],
        "keywords": [
            "street", "urban", "city", "downtown", "alley", "market",
            "pedestrian", "night", "rain", "neon", "graffiti", "candid"
        ],
        "examples": [
            "A rainy night street scene in Tokyo's Shinjuku district. Neon signs reflect in puddles on the wet pavement, creating a kaleidoscope of pink, blue, and yellow. A lone figure with an umbrella walks away from the camera down a narrow alley. Steam rises from a ramen shop entrance. The style is cinematic and moody, inspired by cyberpunk aesthetics.",
            "A candid street photograph of an elderly man playing chess alone in a sunlit European plaza. Pigeons gather near his feet. Historic buildings frame the background in soft focus. Dappled light filters through tree leaves, creating patterns on the cobblestones. The image is warm with golden tones. The mood is nostalgic, peaceful, and contemplative."
        ]
    },
    "fantasy": {
        "name": "Fantasy & Sci-Fi",
        "format": [
            "Scene/world description",
            "Characters/creatures",
            "Magical/tech elements",
            "Environment details",
            "Lighting/atmosphere",
            "Art style",
            "Epic/emotional scale"
        ],
        "keywords": [
            "fantasy", "magic", "dragon", "wizard", "castle", "sci-fi",
            "space", "alien", "robot", "cyberpunk", "steampunk", "mythical", "epic"
        ],
        "examples": [
            "A massive dragon perched atop a crumbling medieval tower, silhouetted against a blood-red sunset sky. Its wings are spread wide, scales glinting with reflected firelight. Below, a tiny armored knight stands ready with sword drawn. Storm clouds gather in the distance. The style is epic fantasy digital art with dramatic lighting. The mood is intense and legendary.",
            "A futuristic cyberpunk cityscape at night, viewed from a high rooftop. Towering holographic advertisements float between impossibly tall skyscrapers. Flying vehicles stream through designated air lanes. Rain falls through beams of neon light. A lone figure in a hooded coat stands at the edge, looking out. The color palette is dominated by cyan, magenta, and deep shadows. The mood is atmospheric and noir."
        ]
    },
    "fashion": {
        "name": "Fashion & Editorial",
        "format": [
            "Model/subject",
            "Outfit/styling",
            "Setting/backdrop",
            "Pose/attitude",
            "Lighting setup",
            "Color palette",
            "Editorial concept"
        ],
        "keywords": [
            "fashion", "editorial", "vogue", "haute couture", "designer",
            "model", "runway", "style", "glamour", "chic", "trendy", "lookbook"
        ],
        "examples": [
            "A high-fashion editorial shot of a model in an avant-garde geometric dress, standing in an empty white gallery space. The dress features bold black and white patterns with sculptural shoulders. She poses with one hand on her hip, chin lifted confidently. Clean, even studio lighting eliminates shadows. The style is minimalist and high-concept. The mood is powerful and artistic.",
            "A bohemian fashion photograph in a golden wheat field at sunset. The model wears a flowing floral maxi dress and layered gold jewelry. Her hair blows gently in the wind as she walks barefoot through the grain. Warm backlight creates a dreamy glow around her silhouette. The color palette is warm earth tones and soft oranges. The mood is free-spirited and romantic."
        ]
    },
    "stilllife": {
        "name": "Still Life & Objects",
        "format": [
            "Objects/arrangement",
            "Surface/background",
            "Composition style",
            "Lighting direction",
            "Color harmony",
            "Texture details",
            "Artistic influence"
        ],
        "keywords": [
            "still life", "objects", "flowers", "vase", "fruit", "vintage",
            "antique", "books", "candle", "arrangement", "tabletop", "classic"
        ],
        "examples": [
            "A Dutch Golden Age inspired still life arrangement on a dark wooden table. A pewter vase holds wilting tulips and roses, some petals fallen on the surface. A half-peeled lemon, aged cheese, and a silver knife complete the composition. Dramatic chiaroscuro lighting from the left creates deep shadows. The style is classical oil painting aesthetic. The mood is contemplative and vanitas.",
            "A minimalist still life of three ceramic vases in muted earth tones – terracotta, sage green, and cream. They sit on a linen cloth against a warm beige wall. A single dried pampas grass stem arches from the tallest vase. Soft, diffused natural light from a window creates gentle shadows. The composition follows the rule of odds. The mood is calm, modern, and Scandinavian-inspired."
        ]
    },
    "vintage": {
        "name": "Vintage & Retro",
        "format": [
            "Era/time period",
            "Subject/scene",
            "Period-accurate details",
            "Color treatment",
            "Texture/grain",
            "Nostalgic elements",
            "Emotional tone"
        ],
        "keywords": [
            "vintage", "retro", "1950s", "1960s", "1970s", "1980s", "old",
            "nostalgic", "classic", "antique", "film", "polaroid", "sepia"
        ],
        "examples": [
            "A 1950s American diner scene with a young couple sharing a milkshake at the counter. Chrome stools, checkered floor tiles, and a vintage jukebox set the scene. A neon 'Open' sign glows in the window. The image has a warm, faded color palette with slight grain, like aged Kodachrome film. The mood is nostalgic, innocent, and romantic.",
            "A 1980s arcade interior bathed in neon purple and blue light. Rows of classic arcade cabinets line the walls – Pac-Man, Space Invaders, Donkey Kong. A teenager in a Members Only jacket plays intently, face lit by the screen glow. The image has VHS-style color bleeding and scan lines. The mood is retro-futuristic and full of youthful energy."
        ]
    },
    "conceptual": {
        "name": "Conceptual & Surreal",
        "format": [
            "Core concept/idea",
            "Visual metaphor",
            "Surreal elements",
            "Environment/setting",
            "Lighting/mood",
            "Color symbolism",
            "Emotional impact"
        ],
        "keywords": [
            "conceptual", "surreal", "dream", "imagination", "metaphor",
            "symbolic", "artistic", "creative", "unusual", "impossible", "mind-bending"
        ],
        "examples": [
            "A surreal conceptual image of a person's head dissolving into a flock of birds flying toward a bright horizon. The figure stands in an endless white salt flat under a gradient sky from orange to deep blue. The transition from solid to birds is seamless and dreamlike. The lighting is soft and ethereal. The concept represents freedom and transformation. The mood is hopeful and transcendent.",
            "A conceptual photograph of a tiny person standing on the edge of a coffee cup, looking down at the swirling liquid like an ocean. The cup sits on a giant wooden table with enormous sugar cubes nearby. Dramatic lighting creates a sense of scale and wonder. The style blends macro photography with digital manipulation. The concept explores perspective and the extraordinary in ordinary moments."
        ]
    }
}

DEFAULT_CATEGORY = "landscape"

VALID_CATEGORIES = list(IMAGE_CATEGORIES.keys())

# Image uses shared styles only (no video-specific styles)
IMAGE_STYLES = SHARED_STYLES
