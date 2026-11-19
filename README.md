# Poketwo-Matcher
**Not AI** matcher for Poketwo spawn images on Discord; instead, it uses OpenCV in Python.

This means it requires **much less CPU and RAM**. In fact, you can run it on your computer or any free-tier online server/VPS. 

## Introductions:
Poketwo is a popular Discord bot that spawns Pokémon with images. You need to guess the name to catch the Pokémon. 

However, most "Namers" use CNN (convolutional neural network), which are computationally expensive on any CPU. My method using ORB (from OpenCV) is not only computationally cheaper but also faster to use. 

## Example of how to use the matcher:
**Step 1:** Make sure your bot code and a folder named "SPRITE_DIR" are in the same directory as matcher2.py and database.py.

**Step 2:** Set up an "on_message" listener for poketwo's message and get the images

**Step 3:** Call the matcher:

```python
from database import load_reference_database, build_reference_database
from matcher2 import PokemonMatcher

# 1. Load or build your reference entries
entries = load_reference_database()
if not entries:
    # (If running asynchronously, you would await build_reference_database())
    pass

# 2. Initialize the matcher
matcher = PokemonMatcher(entries)

# 3. Read your target image as bytes
with open("path_to_pokemon_image.png", "rb") as f:
    image_bytes = f.read()

# 4. Identify the Pokémon (limit returns the top N results)
results = matcher.identify(image_bytes, limit=1)

if results:
    best_match = results[0]
    print(f"Identified: {best_match['name']} (ID: {best_match['id']})")
    print(f"Confidence: {best_match['confidence']:.3f}")
else:
    print("Could not identify this Pokémon.")
```

## Note:
You are free to use these codes any way you like (e.g. creating namer/mass inc bots for your server). But I would appreciate it if you let me know at https://discord.gg/F7JJG8cw8w.

Likewise, if you have any questions, feel free to ask in the Discord server. 

