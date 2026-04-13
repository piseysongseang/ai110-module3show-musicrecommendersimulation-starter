from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


USER_TASTE_PROFILE: Dict = {
    "favorite_genre":    "lofi",   
    "favorite_mood":     "chill", 

    "target_energy":       0.40,   
    "target_tempo":        80.0,   
    "target_valence":      0.60,  
    "target_danceability": 0.58,  
    "target_acousticness": 0.75,  

    "w_genre":        0.25,
    "w_mood":         0.20,
    "w_energy":       0.20,
    "w_tempo":        0.10,
    "w_valence":      0.10,
    "w_danceability": 0.10,
    "w_acousticness": 0.05,
}


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += 2.0
        reasons.append(f"genre match ({song['genre']}): +2.0")
    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += 1.0
        reasons.append(f"mood match ({song['mood']}): +1.0")


    energy_sim = 1.0 - abs(song.get("energy", 0) - user_prefs.get("target_energy", 0.5))
    score += energy_sim
    reasons.append(f"energy similarity: +{energy_sim:.2f}")

    tempo_diff = abs(song.get("tempo_bpm", 100) - user_prefs.get("target_tempo", 100))
    tempo_sim = max(0.0, 1.0 - tempo_diff / 60.0) * 0.5
    score += tempo_sim
    reasons.append(f"tempo similarity: +{tempo_sim:.2f}")

    valence_sim = (1.0 - abs(song.get("valence", 0) - user_prefs.get("target_valence", 0.5))) * 0.5
    score += valence_sim
    reasons.append(f"valence similarity: +{valence_sim:.2f}")

    dance_sim = (1.0 - abs(song.get("danceability", 0) - user_prefs.get("target_danceability", 0.5))) * 0.5
    score += dance_sim
    reasons.append(f"danceability similarity: +{dance_sim:.2f}")

    acousticness = song.get("acousticness", 0.5)
    target_ac = user_prefs.get("target_acousticness", 0.5)
    if target_ac >= 0.5 and acousticness >= 0.60:
        score += 0.5
        reasons.append(f"acoustic match ({acousticness:.2f}): +0.50")
    elif target_ac < 0.5 and acousticness < 0.40:
        score += 0.5
        reasons.append(f"electronic match ({acousticness:.2f}): +0.50")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """_summary_

    Args:
        user_prefs (Dict): _description_
        songs (List[Dict]): _description_
        k (int, optional): _description_. Defaults to 5.

    Returns:
        List[Tuple[Dict, float, str]]: _description_
    """
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
