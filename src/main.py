"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs, USER_TASTE_PROFILE


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = USER_TASTE_PROFILE

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 48)
    print("  Top Recommendations")
    print("=" * 48)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} — {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 6.00")
        print("    Reasons:")
        for reason in explanation.split(", "):
            print(f"      • {reason}")

    print("\n" + "=" * 48)


if __name__ == "__main__":
    main()
