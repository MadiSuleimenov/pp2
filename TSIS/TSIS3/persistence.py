import json, os

BASE_DIR = os.path.dirname(__file__)

SETTINGS_FILE    = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  "red",
    "difficulty": "normal",
}


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # merge with defaults so new keys always exist
        return {**DEFAULT_SETTINGS, **data}
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)


def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def add_score(name, score, distance, coins):
    board = load_leaderboard()
    board.append({"name": name, "score": score,
                  "distance": distance, "coins": coins})
    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=2)
