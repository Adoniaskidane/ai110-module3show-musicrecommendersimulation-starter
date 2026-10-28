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

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
