# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge at a talent show who gives every song a score card. The user tells it four things about their taste:

- their **favorite genre** (like pop or lofi)
- their **favorite mood** (like happy or chill)
- how much **energy** they want, from 0 (very calm) to 1 (very intense)
- whether they **like acoustic** music or prefer electronic sounds

Then the judge looks at every song in the catalog, one at a time, and hands out points:

| What it checks | Points |
|---|---|
| Same genre as the user's favorite | 2.0 |
| A close cousin genre (pop and indie pop, or lofi and ambient) | 1.0 |
| Same mood as the user's favorite | 1.5 |
| Energy close to what the user wants | up to 1.5 (the closer, the more points) |
| Acoustic sound that fits the user's taste | up to 0.5 |

A perfect song scores 5.5. Every time a song earns points, the judge writes down why (for example, "genre match: lofi (+2.0)"). The user doesn't just see a list. They see *why* each song made it.

When every song has a score, the judge sorts them from highest to lowest and shows the top 5.

**Why these weights?** Genre gets the most points because it is the most stable part of someone's taste. Getting metal when you asked for lofi feels broken. Mood comes next because it describes the moment you're in. Energy gives points for *closeness*, not for being high or low. A calm listener should get calm songs, not the loudest ones.

**What I left out on purpose:** Each song also has tempo, danceability, and "positivity" (valence) numbers. Tempo and danceability mostly rise and fall with energy, so counting them would reward the same thing three times. Valence barely changes between songs in this catalog. These values are stored but not scored.

**Changes from the starter:** The starter code only had empty placeholders that returned nothing. I wrote the song loader, the scoring rules above, the ranking step, and a clean terminal display. The whole thing runs as a simple command-line program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

**Weakness: a one-song filter bubble for most genres.** Fifteen of the 17 genres in the catalog have exactly one song, and an exact genre + mood match is worth 3.5 points while a song matching neither can never score more than 2.0. That means a fan of almost any genre gets the same single song locked at #1 no matter how badly it fits the rest of their taste: for my reggae/focused/energy 0.8 profile, Island Breeze Riddim ranked first even though it missed my mood and was 0.20 off my energy target, and the "Energetic but Sad" profile got a slow blues song at #1 because it was the only blues/sad track. Positions 2–5 are then filled almost entirely by energy closeness, so a rock fan and a metal fan see nearly the same list of loud songs from whatever genres happen to be in the dataset. Lofi listeners (3 songs) get a far more personalized top 5 than everyone else, so the system quietly favors users whose taste matches the best-represented genres.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profile Outputs

Output of `python3 src/main.py`, which runs the recommender for three core taste profiles and five adversarial / edge-case profiles designed to trick the scoring logic.

#### High-Energy Pop

Sunrise City matches on every feature. Rooftop Lights earns related-genre credit. #4–5 rank on energy alone.

```
================================================================
  🎵  Top Recommendations — High-Energy Pop
================================================================
  Profile: pop · happy · energy 0.85 · non-acoustic
----------------------------------------------------------------

  #1  Sunrise City  —  Neon Echo
      pop / happy
      Score: 5.37 / 5.5  ████████████████████
      Why:
        • genre match: pop (+2.0)
        • mood match: happy (+1.5)
        • energy 0.82 vs target 0.85 (+1.46)
        • non-acoustic sound (+0.41)

  #2  Rooftop Lights  —  Indigo Parade
      indie pop / happy
      Score: 4.19 / 5.5  ███████████████░░░░░
      Why:
        • related genre: indie pop (+1.0)
        • mood match: happy (+1.5)
        • energy 0.76 vs target 0.85 (+1.36)
        • non-acoustic sound (+0.33)

  #3  Gym Hero  —  Max Pulse
      pop / intense
      Score: 3.85 / 5.5  ██████████████░░░░░░
      Why:
        • genre match: pop (+2.0)
        • energy 0.93 vs target 0.85 (+1.38)
        • non-acoustic sound (+0.47)

  #4  Storm Runner  —  Voltline
      rock / intense
      Score: 1.86 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.91 vs target 0.85 (+1.41)
        • non-acoustic sound (+0.45)

  #5  Fiesta en la Calle  —  Sol Caliente
      latin / playful
      Score: 1.85 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.85 vs target 0.85 (+1.50)
        • non-acoustic sound (+0.35)

================================================================
```

#### Chill Lofi

Two lofi/chill tracks are nearly tied at the top. The related-genre rule lifts ambient Spacewalk Thoughts above lofi Focus Flow.

```
================================================================
  🎵  Top Recommendations — Chill Lofi
================================================================
  Profile: lofi · chill · energy 0.40 · acoustic
----------------------------------------------------------------

  #1  Library Rain  —  Paper Lanterns
      lofi / chill
      Score: 5.35 / 5.5  ███████████████████░
      Why:
        • genre match: lofi (+2.0)
        • mood match: chill (+1.5)
        • energy 0.35 vs target 0.40 (+1.42)
        • acoustic sound (+0.43)

  #2  Midnight Coding  —  LoRoom
      lofi / chill
      Score: 5.32 / 5.5  ███████████████████░
      Why:
        • genre match: lofi (+2.0)
        • mood match: chill (+1.5)
        • energy 0.42 vs target 0.40 (+1.47)
        • acoustic sound (+0.35)

  #3  Spacewalk Thoughts  —  Orbit Bloom
      ambient / chill
      Score: 4.28 / 5.5  ████████████████░░░░
      Why:
        • related genre: ambient (+1.0)
        • mood match: chill (+1.5)
        • energy 0.28 vs target 0.40 (+1.32)
        • acoustic sound (+0.46)

  #4  Focus Flow  —  LoRoom
      lofi / focused
      Score: 3.89 / 5.5  ██████████████░░░░░░
      Why:
        • genre match: lofi (+2.0)
        • energy 0.40 vs target 0.40 (+1.50)
        • acoustic sound (+0.39)

  #5  Coffee Shop Stories  —  Slow Stereo
      jazz / relaxed
      Score: 1.90 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.37 vs target 0.40 (+1.46)
        • acoustic sound (+0.45)

================================================================
```

#### Deep Intense Rock

Storm Runner wins clearly. With only one rock song in the catalog, #3–5 are just loud songs from other genres.

```
================================================================
  🎵  Top Recommendations — Deep Intense Rock
================================================================
  Profile: rock · intense · energy 0.90 · non-acoustic
----------------------------------------------------------------

  #1  Storm Runner  —  Voltline
      rock / intense
      Score: 5.43 / 5.5  ████████████████████
      Why:
        • genre match: rock (+2.0)
        • mood match: intense (+1.5)
        • energy 0.91 vs target 0.90 (+1.48)
        • non-acoustic sound (+0.45)

  #2  Gym Hero  —  Max Pulse
      pop / intense
      Score: 3.43 / 5.5  ████████████░░░░░░░░
      Why:
        • mood match: intense (+1.5)
        • energy 0.93 vs target 0.90 (+1.46)
        • non-acoustic sound (+0.47)

  #3  Bassline Overdrive  —  Pulse Theory
      edm / euphoric
      Score: 1.90 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.96 vs target 0.90 (+1.41)
        • non-acoustic sound (+0.48)

  #4  Ashes and Iron  —  Grave Signal
      metal / aggressive
      Score: 1.87 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.98 vs target 0.90 (+1.38)
        • non-acoustic sound (+0.49)

  #5  Sunrise City  —  Neon Echo
      pop / happy
      Score: 1.79 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.82 vs target 0.90 (+1.38)
        • non-acoustic sound (+0.41)

================================================================
```

#### Edge: Energetic but Sad

**Conflicting preferences.** Back Porch Blues wins despite energy 0.38 vs a 0.90 target: genre + mood (3.5 pts) outweigh the max energy reward (1.5). None of #2–5 are sad.

```
================================================================
  🎵  Top Recommendations — Edge: Energetic but Sad
================================================================
  Profile: blues · sad · energy 0.90 · non-acoustic
----------------------------------------------------------------

  #1  Back Porch Blues  —  Willie Hollow
      blues / sad
      Score: 4.31 / 5.5  ████████████████░░░░
      Why:
        • genre match: blues (+2.0)
        • mood match: sad (+1.5)
        • energy 0.38 vs target 0.90 (+0.72)
        • non-acoustic sound (+0.09)

  #2  Storm Runner  —  Voltline
      rock / intense
      Score: 1.93 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.91 vs target 0.90 (+1.48)
        • non-acoustic sound (+0.45)

  #3  Gym Hero  —  Max Pulse
      pop / intense
      Score: 1.93 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.93 vs target 0.90 (+1.46)
        • non-acoustic sound (+0.47)

  #4  Bassline Overdrive  —  Pulse Theory
      edm / euphoric
      Score: 1.90 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.96 vs target 0.90 (+1.41)
        • non-acoustic sound (+0.48)

  #5  Ashes and Iron  —  Grave Signal
      metal / aggressive
      Score: 1.87 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.98 vs target 0.90 (+1.38)
        • non-acoustic sound (+0.49)

================================================================
```

#### Edge: Unknown Genre (k-pop)

**Nothing in the catalog matches.** All scores are ~1.5/5.5, yet the system still presents a confident top 5 driven only by energy and acousticness.

```
================================================================
  🎵  Top Recommendations — Edge: Unknown Genre (k-pop)
================================================================
  Profile: k-pop · dreamy · energy 0.70 · acoustic
----------------------------------------------------------------

  #1  Dusty Highway Home  —  Cedar & Pine
      country / nostalgic
      Score: 1.65 / 5.5  ██████░░░░░░░░░░░░░░
      Why:
        • energy 0.55 vs target 0.70 (+1.28)
        • acoustic sound (+0.37)

  #2  Island Breeze Riddim  —  Tide Kings
      reggae / uplifting
      Score: 1.59 / 5.5  ██████░░░░░░░░░░░░░░
      Why:
        • energy 0.60 vs target 0.70 (+1.35)
        • acoustic sound (+0.24)

  #3  Rooftop Lights  —  Indigo Parade
      indie pop / happy
      Score: 1.58 / 5.5  ██████░░░░░░░░░░░░░░
      Why:
        • energy 0.76 vs target 0.70 (+1.41)
        • acoustic sound (+0.17)

  #4  Night Drive Loop  —  Neon Echo
      synthwave / moody
      Score: 1.53 / 5.5  ██████░░░░░░░░░░░░░░
      Why:
        • energy 0.75 vs target 0.70 (+1.42)
        • acoustic sound (+0.11)

  #5  Coffee Shop Stories  —  Slow Stereo
      jazz / relaxed
      Score: 1.45 / 5.5  █████░░░░░░░░░░░░░░░
      Why:
        • energy 0.37 vs target 0.70 (+1.01)
        • acoustic sound (+0.45)

================================================================
```

#### Edge: Acoustic Metalhead

**Contradictory texture.** `likes_acoustic` is effectively ignored. The metal track still scores 5.01, and #2–5 are separated by ~0.03.

```
================================================================
  🎵  Top Recommendations — Edge: Acoustic Metalhead
================================================================
  Profile: metal · aggressive · energy 0.98 · acoustic
----------------------------------------------------------------

  #1  Ashes and Iron  —  Grave Signal
      metal / aggressive
      Score: 5.01 / 5.5  ██████████████████░░
      Why:
        • genre match: metal (+2.0)
        • mood match: aggressive (+1.5)
        • energy 0.98 vs target 0.98 (+1.50)
        • acoustic sound (+0.01)

  #2  Bassline Overdrive  —  Pulse Theory
      edm / euphoric
      Score: 1.48 / 5.5  █████░░░░░░░░░░░░░░░
      Why:
        • energy 0.96 vs target 0.98 (+1.47)
        • acoustic sound (+0.01)

  #3  Fiesta en la Calle  —  Sol Caliente
      latin / playful
      Score: 1.45 / 5.5  █████░░░░░░░░░░░░░░░
      Why:
        • energy 0.85 vs target 0.98 (+1.30)
        • acoustic sound (+0.15)

  #4  Gym Hero  —  Max Pulse
      pop / intense
      Score: 1.45 / 5.5  █████░░░░░░░░░░░░░░░
      Why:
        • energy 0.93 vs target 0.98 (+1.43)
        • acoustic sound (+0.03)

  #5  Storm Runner  —  Voltline
      rock / intense
      Score: 1.45 / 5.5  █████░░░░░░░░░░░░░░░
      Why:
        • energy 0.91 vs target 0.98 (+1.40)
        • acoustic sound (+0.05)

================================================================
```

#### Edge: Energy Out of Range

**Invalid input (1.5) is accepted.** Every energy reward shrinks, and calm songs would get *negative* energy points. The target should be clamped to 0–1.

```
================================================================
  🎵  Top Recommendations — Edge: Energy Out of Range
================================================================
  Profile: edm · euphoric · energy 1.50 · non-acoustic
----------------------------------------------------------------

  #1  Bassline Overdrive  —  Pulse Theory
      edm / euphoric
      Score: 4.67 / 5.5  █████████████████░░░
      Why:
        • genre match: edm (+2.0)
        • mood match: euphoric (+1.5)
        • energy 0.96 vs target 1.50 (+0.69)
        • non-acoustic sound (+0.48)

  #2  Ashes and Iron  —  Grave Signal
      metal / aggressive
      Score: 1.21 / 5.5  ████░░░░░░░░░░░░░░░░
      Why:
        • energy 0.98 vs target 1.50 (+0.72)
        • non-acoustic sound (+0.49)

  #3  Gym Hero  —  Max Pulse
      pop / intense
      Score: 1.12 / 5.5  ████░░░░░░░░░░░░░░░░
      Why:
        • energy 0.93 vs target 1.50 (+0.65)
        • non-acoustic sound (+0.47)

  #4  Storm Runner  —  Voltline
      rock / intense
      Score: 1.06 / 5.5  ████░░░░░░░░░░░░░░░░
      Why:
        • energy 0.91 vs target 1.50 (+0.61)
        • non-acoustic sound (+0.45)

  #5  Sunrise City  —  Neon Echo
      pop / happy
      Score: 0.89 / 5.5  ███░░░░░░░░░░░░░░░░░
      Why:
        • energy 0.82 vs target 1.50 (+0.48)
        • non-acoustic sound (+0.41)

================================================================
```

#### Edge: Messy Input Casing

**Handled correctly.** `.strip().lower()` normalizes the input, so results are identical to Chill Lofi. Only the header shows the raw string.

```
================================================================
  🎵  Top Recommendations — Edge: Messy Input Casing
================================================================
  Profile:   LoFi  · CHILL · energy 0.40 · acoustic
----------------------------------------------------------------

  #1  Library Rain  —  Paper Lanterns
      lofi / chill
      Score: 5.35 / 5.5  ███████████████████░
      Why:
        • genre match: lofi (+2.0)
        • mood match: chill (+1.5)
        • energy 0.35 vs target 0.40 (+1.42)
        • acoustic sound (+0.43)

  #2  Midnight Coding  —  LoRoom
      lofi / chill
      Score: 5.32 / 5.5  ███████████████████░
      Why:
        • genre match: lofi (+2.0)
        • mood match: chill (+1.5)
        • energy 0.42 vs target 0.40 (+1.47)
        • acoustic sound (+0.35)

  #3  Spacewalk Thoughts  —  Orbit Bloom
      ambient / chill
      Score: 4.28 / 5.5  ████████████████░░░░
      Why:
        • related genre: ambient (+1.0)
        • mood match: chill (+1.5)
        • energy 0.28 vs target 0.40 (+1.32)
        • acoustic sound (+0.46)

  #4  Focus Flow  —  LoRoom
      lofi / focused
      Score: 3.89 / 5.5  ██████████████░░░░░░
      Why:
        • genre match: lofi (+2.0)
        • energy 0.40 vs target 0.40 (+1.50)
        • acoustic sound (+0.39)

  #5  Coffee Shop Stories  —  Slow Stereo
      jazz / relaxed
      Score: 1.90 / 5.5  ███████░░░░░░░░░░░░░
      Why:
        • energy 0.37 vs target 0.40 (+1.46)
        • acoustic sound (+0.45)

================================================================
```

### Profile Comparisons

These comparisons use the original weights (genre 2.0, mood 1.5, energy 1.5, acoustic 0.5), which produced the outputs above. My own profile (`my_profile`: reggae, focused, energy 0.8, likes acoustic) ranked Island Breeze Riddim, Focus Flow, Rooftop Lights, Fiesta en la Calle and Sunrise City.

**High-Energy Pop vs. Chill Lofi:** These two lists have no songs in common. The pop listener gets loud, electronic tracks (energy 0.76–0.93), and the lofi listener gets quiet, acoustic ones (energy 0.28–0.42). That makes sense because the two profiles want opposite things on every setting, so the system correctly sends them to opposite ends of the catalog.

**High-Energy Pop vs. Deep Intense Rock:** These lists overlap a lot. Gym Hero, Storm Runner and Sunrise City appear in both because both listeners want loud, non-acoustic music. The difference is *why* Gym Hero gets in. The pop fan gets it for the "pop" label, and the rock fan gets it for the "intense" mood. That makes sense: the #1 song changes to match each genre, but below that, "loud music is loud music."

**Deep Intense Rock vs. Energetic but Sad:** Both want energy around 0.9 and electronic sound, and places #2–5 are nearly the same loud songs. But the sad listener's #1 is Back Porch Blues, a slow, quiet song. It wins because it's the only song labeled both "blues" and "sad," and those labels are worth more than matching the energy. This only half makes sense: the system honors the words the user chose but ignores how energetic they wanted the music to be.

**Deep Intense Rock vs. Acoustic Metalhead:** Both get almost the same list of loud songs, even though the metalhead says they *love* acoustic music. Liking acoustic sound is worth only half a point, and every high-energy song in the catalog is electronic, so that preference has nothing to act on. This makes sense mathematically but shows that a small preference can be silently ignored.

**High-Energy Pop vs. my_profile:** Both want energy around 0.8, so places #3–5 overlap (Rooftop Lights, Fiesta en la Calle, Sunrise City). Those songs aren't there because they're pop or reggae. They're simply "about the right energy," and the system uses them as filler once it runs out of label matches. My list runs out after two songs because there's only one reggae song and one "focused" song.

**my_profile vs. Energetic but Sad:** Both show the same pattern. The user's genre has exactly one song in the catalog, so that song is automatically #1 even when it's the wrong energy (Island Breeze Riddim is 0.60 vs. my 0.80, and Back Porch Blues is 0.38 vs. 0.90). This is the filter bubble described in Section 6.

**Chill Lofi vs. Unknown Genre (k-pop):** The lofi listener gets four strong matches scoring above 3.8. The k-pop listener's best song scores only 1.65 out of 5.5, because neither "k-pop" nor "dreamy" exists in the catalog. The k-pop list is ordered by energy alone and still looks just as confident on screen, which is misleading: the honest answer would be "we don't have anything for you."

**Deep Intense Rock vs. Energy Out of Range (1.5):** Both get loud songs in a sensible order, but every score in the out-of-range list is lower (for example, Ashes and Iron gets 1.21 vs. 1.87). Asking for energy above the maximum doesn't break the ranking, but it shrinks every song's energy reward, so the scores stop meaning what they should.

**Chill Lofi vs. Messy Input Casing:** These outputs are identical. The second profile typed "  LoFi " and "CHILL" with odd capitals and spaces, and the system cleaned that up before comparing. This confirms that small typing differences don't change the recommendations.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
