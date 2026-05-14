# 🎬 MoodFlix — Mood-Based Movie Recommender

> Find your perfect movie based on how you're feeling tonight.

## 💡 About
MoodFlix is a movie recommendation system that recommends movies based on your mood instead of a movie name. the user selects a mood like Adventure or Romance, picks an era (New / Mid / Classic), and instantly gets top 10 movie recommendations with live posters, ratings and match percentage.

## 🧠 How It Works
took the TMDB 5000 movies dataset and merged it with the credits dataset. extracted genres, keywords, cast and director for each movie and combined them into one tags column. applied CountVectorizer to convert the tags into number vectors and used cosine similarity to find similar movies.

the unique part — instead of searching by movie name, created 6 mood keyword strings and converted them into vectors using the same vocabulary. cosine similarity then finds which movies are closest to each mood vector and returns the top 10.

## 🎭 6 Moods
- 🤯 Mind Bending — Sci-fi, Thriller, Mystery
- 🚀 Adventure — Action, Fantasy, Epic
- ❤️ Romance — Love, Drama, Emotion
- 😂 Comedy — Funny, Lighthearted, Fun
- 😨 Edge of Seat — Horror, Suspense, Dark
- 😢 Emotional — Sad, Family, Deep

## ⭐ Features
- mood-based recommendations (no movie name needed)
- era filter — New Age / Golden Mid / Classics
- live movie posters via TMDB API
- match % score for each recommendation
- cinematic UI built with Streamlit

## 🛠️ Tech Stack
Python · Pandas · Scikit-learn · NLTK · Streamlit · TMDB API · Pickle


## 📊 Dataset
TMDB 5000 Movies — https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

## 🔗 Live Demo
https://movie-recommendation-system-kx2lcextbkwqexyzee5vfs.streamlit.app/

## 👨‍💻 Author
Mohammed Anas — AIML Student, Lords Institute of Engineering and Technology, Hyderabad
