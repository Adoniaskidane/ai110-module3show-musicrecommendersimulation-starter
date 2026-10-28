"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: a late-night study listener who wants calm,
    # mostly acoustic music with a gentle groove.
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,        # 0-1, low-key but not sleepy
        "target_tempo_bpm": 80,       # relaxed walking pace
        "target_valence": 0.60,       # 0-1, mildly positive
        "target_danceability": 0.60,  # 0-1, light head-nod groove
        "target_acousticness": 0.80,  # 0-1, warm, organic sound
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


MAX_SCORE = 5.5  # genre 2.0 + mood 1.5 + energy 1.5 + acoustic 0.5
WIDTH = 64


def print_recommendations(user_prefs, recommendations) -> None:
    """Print the profile and ranked songs with score bars and bullet-point reasons."""
    print()
    print("=" * WIDTH)
    print("  🎵  Top Recommendations")
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
