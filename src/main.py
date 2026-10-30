"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    # --- Core taste profiles ---
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
    # A late-night study listener who wants calm, mostly acoustic music.
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    "my_profile": {
        "favorite_genre": "reggae",
        "favorite_mood": "focused",
        "target_energy": 0.8,
        "likes_acoustic": True,
    },

    # --- Adversarial / edge-case profiles ---
    # Conflicting: wants high energy but a sad mood. The only "sad" song
    # (Back Porch Blues) is low energy, so mood and energy pull apart.
    "Edge: Energetic but Sad": {
        "favorite_genre": "blues",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    # Genre and mood that appear nowhere in the catalog: ranking falls
    # back entirely on energy + acousticness.
    "Edge: Unknown Genre (k-pop)": {
        "favorite_genre": "k-pop",
        "favorite_mood": "dreamy",
        "target_energy": 0.70,
        "likes_acoustic": True,
    },
    # Contradictory texture: metal fan who claims to love acoustic sound.
    "Edge: Acoustic Metalhead": {
        "favorite_genre": "metal",
        "favorite_mood": "aggressive",
        "target_energy": 0.98,
        "likes_acoustic": True,
    },
    # Out-of-range energy (1.5): energy points can go negative for calm songs.
    "Edge: Energy Out of Range": {
        "favorite_genre": "edm",
        "favorite_mood": "euphoric",
        "target_energy": 1.5,
        "likes_acoustic": False,
    },
    # Messy casing/whitespace: does "  LoFi " still match "lofi"?
    "Edge: Messy Input Casing": {
        "favorite_genre": "  LoFi ",
        "favorite_mood": "CHILL",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


MAX_SCORE = 6.0  # EXPERIMENT: genre 1.0 + mood 1.5 + energy 3.0 + acoustic 0.5
WIDTH = 64


def print_recommendations(name, user_prefs, recommendations) -> None:
    """Print the profile and ranked songs with score bars and bullet-point reasons."""
    print()
    print("=" * WIDTH)
    print(f"  🎵  Top Recommendations — {name}")
    print("=" * WIDTH)
    print(
        f"  Profile: {user_prefs['favorite_genre']} · {user_prefs['favorite_mood']}"
        f" · energy {user_prefs['target_energy']:.2f}"
        f" · {'acoustic' if user_prefs['likes_acoustic'] else 'non-acoustic'}"
    )
    print("-" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        filled = round(score / MAX_SCORE * 20)
        bar = "█" * filled + "░" * (20 - filled)
        print()
        print(f"  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"      {song['genre']} / {song['mood']}")
        print(f"      Score: {score:.2f} / {MAX_SCORE}  {bar}")
        print("      Why:")
        for reason in explanation.split("; "):
            print(f"        • {reason}")

    print()
    print("=" * WIDTH)


if __name__ == "__main__":
    main()
