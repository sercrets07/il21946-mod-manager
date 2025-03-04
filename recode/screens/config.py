import os
import json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "recode", "config.json")


def save_game_path(path):
    """Save the selected game directory to a JSON config file."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump({"game_path": path}, file, indent=4)
        print(f"✅ Game path saved successfully: {path}")
    except Exception as e:
        print(f"❌ Error saving game path: {e}")


def load_game_path():
    """Load the saved game directory path from config.json."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                data = json.load(file)
                game_path = data.get("game_path", "")
                
                if game_path:
                    print(f"🔍 Loaded game path: {game_path}")
                    return game_path
        except Exception as e:
            print(f"❌ Error reading game path: {e}")
    
    return ""  # Return empty string if no path is found


def get_game_conf_file():
    """Get the path to conf.ini if the game path exists."""
    game_path = load_game_path()
    if game_path:
        return os.path.join(game_path, "conf.ini")  # ✅ Construct the conf.ini path dynamically
    return None  # ✅ No game path found, return None


# ✅ Dynamically determine GAME_CONF_FILE
GAME_CONF_FILE = get_game_conf_file()
