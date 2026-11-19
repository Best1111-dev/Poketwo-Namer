import asyncio
import csv
import io
import json
import os
from pathlib import Path

import aiohttp

from config import POKEMON_CSV_URL, IMAGE_URL_TEMPLATE, SPRITE_DIR, REFERENCE_JSON

Path(SPRITE_DIR).mkdir(parents=True, exist_ok=True)


async def _download(session, url, destination):
    if os.path.exists(destination) and os.path.getsize(destination) > 100:
        return True
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status != 200:
                return False
            content = await response.read()
            if len(content) < 100:
                return False
            Path(destination).write_bytes(content)
            return True
    except (aiohttp.ClientError, asyncio.TimeoutError, OSError):
        return False


async def build_reference_database(force=False):
    """Fetch official Poketwo CSV metadata and cache available official image files."""
    headers = {"User-Agent": "PoketwoSpawnRecognizer/1.0"}
    timeout = aiohttp.ClientTimeout(total=45)
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        async with session.get(POKEMON_CSV_URL) as response:
            response.raise_for_status()
            csv_text = await response.text()

        rows = list(csv.DictReader(io.StringIO(csv_text)))
        entries = []
        for row in rows:
            # The repository's loader only registers enabled Pokémon.
            if "enabled" not in row:
                continue
            try:
                pokemon_id = int(row["id"])
            except (KeyError, ValueError):
                continue
            name = row.get("name.en") or row.get("slug") or f"Pokemon {pokemon_id}"
            slug = row.get("slug") or name.lower().replace(" ", "-")
            entries.append({
                "id": pokemon_id,
                "name": name,
                "slug": slug,
                "image_url": IMAGE_URL_TEMPLATE.format(pokemon_id=pokemon_id),
            })

        semaphore = asyncio.Semaphore(12)
        async def fetch_one(entry):
            path = os.path.join(SPRITE_DIR, f'{entry["id"]}.png')
            if force:
                try:
                    os.remove(path)
                except FileNotFoundError:
                    pass
            async with semaphore:
                entry["cached"] = await _download(
                    session, entry["image_url"], path
                )
            return entry

        entries = await asyncio.gather(*(fetch_one(e) for e in entries))

    # Keep only entries whose official image exists and downloaded correctly.
    entries = [e for e in entries if e["cached"]]
    for entry in entries:
        entry.pop("cached", None)

    Path(REFERENCE_JSON).parent.mkdir(parents=True, exist_ok=True)
    Path(REFERENCE_JSON).write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return entries


def load_reference_database():
    if not os.path.exists(REFERENCE_JSON):
        return []
    try:
        return json.loads(Path(REFERENCE_JSON).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
