import os

POKETWO_BOT_ID = int(os.getenv("POKETWO_BOT_ID", "716390085896962058"))

GITHUB_RAW = "https://raw.githubusercontent.com/poketwo/data/master"
POKEMON_CSV_URL = f"{GITHUB_RAW}/csv/pokemon.csv"
IMAGE_URL_TEMPLATE = f"{GITHUB_RAW}/images/{{pokemon_id}}.png"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(BASE_DIR, "data", "sprites")
REFERENCE_JSON = os.path.join(BASE_DIR, "data", "reference.json")
