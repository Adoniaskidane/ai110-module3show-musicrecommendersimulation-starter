# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Real-world platforms like Spotify and YouTube combine two main approaches. **Collaborative filtering** looks at the behavior of many users (plays, skips, likes, playlist adds) and recommends what similar listeners enjoyed. **Content-based filtering** looks at the attributes of the items themselves (genre, tempo, audio features) and recommends songs similar to what a user already likes. Large systems blend both with signals like listening history and context, then rank millions of candidates by predicted engagement. My version is a small content-based recommender. With no listening history to learn from, it compares each song's attributes directly to a user's stated taste profile. It prioritizes **genre** first, because it is the most stable part of someone's taste. Next comes **mood**, because it captures the listening situation and connects songs across genres. Then **energy**, scored by how *close* a song is to the user's target rather than how high or low it is. Each score also comes with plain-language reasons, so every recommendation can be explained.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo

  My scoring uses `genre`, `mood`, `energy`, and `acousticness`. The other columns (`tempo_bpm`, `valence`, `danceability`) are stored on each `Song` but not scored. In this dataset, tempo and danceability are highly correlated with energy (0.96 and 0.86), so scoring them would count the same "calm vs. intense" trait several times. Valence varies too little (0.48–0.84) to separate songs well. `id`, `title`, and `artist` are used for display only.

- What information does your `UserProfile` store

  - `favorite_genre` (e.g. `"lofi"`)
  - `favorite_mood` (e.g. `"chill"`)
  - `target_energy`: a value from 0.0 to 1.0 describing how energetic the user wants their music to be
  - `likes_acoustic`: `True` or `False`

- How does your `Recommender` compute a score for each song

  Each song gets points from four parts, added together:

  | Feature | Rule | Max points |
  |---|---|---|
  | Genre | Exact match = 2.0; related genre (pop ↔ indie pop, lofi ↔ ambient) = 1.0 | 2.0 |
  | Mood | Exact match = 1.5 | 1.5 |
  | Energy | `1.5 × (1 − abs(song.energy − target_energy))`, which rewards closeness, not just high or low values | 1.5 |
  | Acousticness | `0.5 × acousticness` if the user likes acoustic, otherwise `0.5 × (1 − acousticness)` | 0.5 |

  Genre is weighted slightly above mood because a genre mismatch feels more "wrong" than a mood mismatch. The gap is kept small so mood can still break ties and surface good songs from related genres. Every rule that adds points also adds a reason (e.g. "matches your favorite genre: lofi"), and those reasons become the explanation for the recommendation.

- How do you choose which songs to recommend

  The recommender scores every song in the catalog, sorts them from highest to lowest score, and returns the top `k` (default 5) along with each song's score and explanation.

You can include a simple diagram or bullet list if helpful.

```
UserProfile ─┐
             ├─► score_song() for every song ─► sort by score ─► top k + reasons
songs.csv  ──┘
```

### Algorithm Recipe (final)

**Input:** a user's taste profile (favorite genre, favorite mood, target energy, likes acoustic or not) and the list of songs from `data/songs.csv`.

**Steps, for every song in the list:**

1. Start the song at **0 points** with an empty list of reasons.
2. **Genre:** If the song's genre is the same as the user's favorite, add **+2.0**. If it is a close cousin (pop ↔ indie pop, lofi ↔ ambient), add **+1.0**.
3. **Mood:** If the song's mood is the same as the user's favorite, add **+1.5**.
4. **Energy:** Add up to **+1.5** depending on how close the song's energy is to the user's target. A perfect match gets all 1.5 points. The further away it is, the fewer points it gets.
5. **Acoustic:** Add up to **+0.5**. If the user likes acoustic music, more acoustic songs get more points. If not, less acoustic songs get more points.
6. Every time points are added, write down a short reason, like "matches your favorite genre: lofi".

**Output:** Sort all songs from highest to lowest score and show the **top 5**, each with its score and reasons.

The best possible score is **5.5**. Text is compared in lowercase, so "Lofi" and "lofi" count as a match.

### Biases I Expect

- **Genre can beat everything else.** Genre is the biggest single reward. A song in the "right" genre but with the wrong feel may rank above a great song that matches the user's mood and energy but is in a different genre.
- **Exact words only.** Mood and genre must match word for word. "chill" and "relaxed" mean almost the same thing, but the system treats them as completely different. Genres like "rock" and "metal" get no partial credit because I only listed two related-genre pairs.
- **Some users get better results.** The catalog has 3 lofi songs but only 1 song for most other genres. A lofi fan gets several strong matches. A blues or classical fan gets one match, and the rest of their list is filled by energy alone.
- **No surprises.** The system only recommends what the user already said they like, so it never helps them discover a new genre.
- **Energy does a lot of the work.** Most songs don't match on genre or mood, so their ranking comes down to energy. Two very different songs with similar energy can look equally good.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



