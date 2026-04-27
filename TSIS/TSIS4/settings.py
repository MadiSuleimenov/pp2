# settings.py — загрузка/сохранение настроек из settings.json
import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

DEFAULTS = {
    "snake_color": [0, 200, 0],
    "grid":        False,
    "sound":       True,
}


def load() -> dict:
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {**DEFAULTS, **data}
    except Exception:
        return dict(DEFAULTS)


def save(s: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)
