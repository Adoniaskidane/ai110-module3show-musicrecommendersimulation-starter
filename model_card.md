# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**TuneJudge 1.0**

It works like a judge at a talent show. Every song gets a score card, and the best five win.

---

## 2. Goal / Task

**Goal:** TuneJudge suggests 5 songs that fit a listener's taste. It does not predict ratings or learn from clicks. It just compares each song to what the user said they like.

**What it assumes about the user:** It assumes your taste fits into four answers: one favorite genre, one favorite mood, an energy level from 0 to 1, and whether you like acoustic sound. Real taste is messier than that.

---

## 3. Data Used

- **Size:** 20 songs in `data/songs.csv`. The starter had 10, and I added 10 more to cover more styles.
- **Features per song:** title, artist, genre, mood, energy, tempo (BPM), valence (positivity), danceability, and acousticness.
- **Genres:** 17 genres, from pop and lofi to metal, classical, reggae, and latin.
- **Moods:** 16 moods, like happy, chill, intense, sad, and nostalgic.

**Limits:**
- Most genres have only **one** song. Lofi has 3 and pop has 2.
- Energy is lumpy. Most songs are either calm (0.2–0.5) or loud (0.75–1.0). Only two sit in the middle.
- All the high-energy songs are electronic. There is no loud acoustic music.
- Each song gets just one genre and one mood. A song can't be "happy *and* playful."
- No lyrics, language, era, or artist popularity. The songs and numbers are made up for practice.

---

## 4. Algorithm Summary

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

## 5. Observed Behavior / Biases

**What works well:**
- **Clear, common tastes work well.** High-Energy Pop, Chill Lofi, and Deep Intense Rock all got the obvious best song at #1 with a near-perfect score.
- **Calm vs. loud is handled well.** The pop and lofi listeners got completely different lists, which matches intuition.
- **Close genres help.** Ambient songs show up for lofi fans, and indie pop shows up for pop fans.
- **Every pick comes with reasons.** You can see exactly where each point came from, so nothing is a mystery.
- **Messy typing is fine.** "  LoFi " and "CHILL" give the same results as "lofi" and "chill."

**Main weakness: a one-song filter bubble.** Most genres have only one song. A genre + mood match is worth 3.5 points, but a song that matches neither can never get more than 2.0. So that one song is locked at #1, even if it fits badly. For my reggae profile, Island Breeze Riddim won even though it missed my mood and my energy. Spots 2–5 are then filled by "about the right energy" songs from any genre. Lofi fans have 3 songs, so they get a much more personal list than everyone else.

**Other patterns I noticed:**
- **Labels beat feel.** A user who wants energetic sad music gets a slow blues song at #1. The words "blues" and "sad" are worth more than the energy.
- **Small preferences get ignored.** "Likes acoustic" is worth only 0.5 points. A metal fan who loves acoustic sound gets the same loud electronic songs anyway.
- **No match still looks confident.** A k-pop fan gets a top 5 with scores around 1.5 out of 5.5. It looks like a real answer, but nothing actually fits.
- **All-or-nothing words.** "Playful" gets zero credit for a "happy" user, even though they're close.
- **No input checks.** An energy of 1.5 is accepted. It quietly lowers every score instead of giving an error.

---

## 6. Evaluation Process

**Profiles I tested (9 total):**
- 3 normal profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock.
- My own profile: reggae, focused, energy 0.8, likes acoustic.
- 5 tricky "edge case" profiles: Energetic but Sad, Unknown Genre (k-pop), Acoustic Metalhead, Energy Out of Range (1.5), and Messy Input Casing.

**What I looked for:** Does #1 make sense? Do the reasons add up to the score? Do different users get different lists? Can a strange profile trick the system?

**Experiment, the weight shift:** I halved genre (2.0 → 1.0) and doubled energy (1.5 → 3.0). I checked that the math still worked: every score equaled the sum of its reasons, and the max became 6.0. The results were mostly *different*, not *better*. For my profile, Focus Flow jumped to #1 even though its energy (0.40) is far from my 0.80. Scores also got squeezed together, so good and weak matches looked more alike. My takeaway: genre and mood decide #1, and energy mostly shuffles the weaker picks.

**Other checks:** The 2 starter tests in `tests/test_recommender.py` pass.

**What surprised me:** How often one label decides everything. Also, the system never says "I don't have a good match." It always sounds sure.

The comparisons below explain how the profiles' results differ. The full terminal output for each profile is in the Appendix at the end.

### Profile Comparisons


These comparisons use the original weights (genre 2.0, mood 1.5, energy 1.5, acoustic 0.5), which produced the outputs in the Appendix. My own profile (`my_profile`: reggae, focused, energy 0.8, likes acoustic) ranked Island Breeze Riddim, Focus Flow, Rooftop Lights, Fiesta en la Calle and Sunrise City.

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

## 7. Intended Use and Non-Intended Use

**Intended use:**
- A classroom project for learning how recommenders score and rank things.
- Testing "what if" questions, like what happens when a user's wishes conflict.

**Not intended for:**
- Real users or a real music app. The catalog has only 20 songs.
- Judging whether a song or genre is good. A low score only means "not a match for this profile."
- Any decision that matters, like picking music for an event or paying artists.

---

## 8. Ideas for Improvement

1. **Add more songs per genre.** At least 5 songs per genre would break the one-song filter bubble and give each user real choices.
2. **Give partial credit for similar moods.** "Happy" should earn some points for "playful" or "uplifting," like the related-genre rule does for genres.
3. **Be honest about weak matches.** If the best score is low, say "no strong match" instead of showing a confident top 5. Also reject energy values outside 0–1.

Other ideas: let users pick more than one favorite genre, and make sure the top 5 isn't all from the same style.

---

## Personal Reflection

I learned that a recommender is really just a set of point rules plus a sort. The hard part is choosing the points. Small weight changes can flip who wins.

The biggest surprise was how much the *data* matters. My scoring was fine for lofi, but most genres had only one song. That made the system feel unfair to those users, and it wasn't the code's fault.

Now when an app recommends something odd, I wonder what labels it's matching on. I also wonder what songs it simply doesn't have.

---

## Appendix: Profile Outputs

Output of `python3 src/main.py` for three core taste profiles and five edge-case profiles designed to trick the scoring logic. These use the original weights (genre 2.0, mood 1.5, energy 1.5, acoustic 0.5).

### High-Energy Pop

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

### Chill Lofi

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

### Deep Intense Rock

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

### Edge: Energetic but Sad

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

### Edge: Unknown Genre (k-pop)

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

### Edge: Acoustic Metalhead

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

### Edge: Energy Out of Range

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

### Edge: Messy Input Casing

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
