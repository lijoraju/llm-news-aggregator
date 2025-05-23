import json
import os

PROFILE_PATH = "data/user_profiles.json"
SUPPORTED_CATEGORIES = [
    "Technology", "Business", "Politics", "Sports",
    "Health", "Science", "Entertainment", "Stock Market"
]

def load_profiles():
    if not os.path.exists(PROFILE_PATH):
        return {}
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)
    
def save_profiles(profiles):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profiles, f, indent=2)

def get_user_interests(user_id):
    profiles = load_profiles()
    return profiles.get(str(user_id), {}).get("interests", [])

def set_user_interests(user_id, interests):
    profiles = load_profiles()
    profiles[str(user_id)] = {"interests": interests}
    save_profiles(profiles)

def remove_user_preferences(user_id):
    profiles = load_profiles()
    user_id_str = str(user_id)
    if user_id_str in profiles:
        del profiles[user_id_str]
        save_profiles(profiles)
        return True
    return False