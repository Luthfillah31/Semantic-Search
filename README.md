<div align="center">
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Film%20Projector.png" alt="Film Projector" width="120" height="120" />
<h1>🎬 CineVerse Finder: Your AI Movie Guru 🔮</h1>
<p><strong>🔎 Ditch keyword searches! This app uses semantic AI to find movies based on plot, mood, or just a vibe. ✨</strong></p>
</div>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python" alt="Python Version">
<img src="https://img.shields.io/badge/Streamlit-1.35%2B-red.svg?style=for-the-badge&logo=streamlit" alt="Streamlit Version">
<img src="https://img.shields.io/badge/Pinecone-Vector_DB-blue.svg?style=for-the-badge&logo=pinecone" alt="Pinecone">
<img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
</p>

<p align="center">
<a href="#-the-problem">The Problem</a> •
<a href="#-the-solution">The Solution</a> •
<a href="#-key-features">Key Features</a> •
<a href="#-how-it-works">How It Works</a> •
<a href="#-tech-stack">Tech Stack</a>
</p>

## 🤔 The Problem: "What Should I Watch Tonight?"

You know the feeling. You're in the mood for a "dystopian sci-fi movie with a philosophical twist and a cool robot sidekick," but typing that into a normal search bar gives you... well, junk. 😩

Keyword-based search is broken. It matches words, not *meaning*. You miss out on hidden gems just because you didn't use the *exact* right keyword in the movie's description.

## ✨ The Solution: Search by Concept!

**CineVerse Finder** revolutionizes movie discovery. Powered by **semantic search**, it goes beyond simple keyword matching to understand the *context* and *meaning* behind a query. Find movies based on their **overview, tagline, associated keywords, cast, or genre** to uncover the perfect film.

<div align="center">
<h3>✨ App Preview ✨</h3>
<img src="https://github.com/user-attachments/assets/bc5bafd9-97cd-4504-bdc7-07f396434540" alt="A screenshot of the CineVerse Finder application, showing a search bar and movie results displayed in a clean card format." width="800"/>
<br>
<p><strong><a href="https://semantic-search-by-luthfillah.streamlit.app/" target="_blank">🚀 View the Live App!</a></strong></p>
</div>

## 🚀 Key Features

* **🧠 Semantic Search:** Describe a movie using its **overview, tagline, keywords, cast, or genre**. The system's AI will understand the query's intent and find films that match the described characteristics.

* **🎨 Gorgeous UI:** A sleek, modern, and intuitive interface built with Streamlit that makes finding movies a joy.

* **🃏 Detailed Movie Cards:** Get all the essential info at a glance—poster, rating, runtime, and overview—without leaving the page.

* **⚡ Blazingly Fast:** Powered by Pinecone's vector database for real-time search results, even with thousands of movies.

## 🛠️ How It Works: The Tech Magic

This project combines a few powerful technologies to create its magic:

1.  **🧠 Data Aggregation & Embedding:** The system first fetches comprehensive data for each movie from the TMDB API, including its overview, tagline, genres, keywords, and cast. This combined text is then converted into a "vector embedding" using a Sentence Transformer model. This vector numerically represents the semantic meaning of the movie's profile.

2.  **🌲 Pinecone Vector Database:** All these movie vectors are stored in a Pinecone index, a database designed for lightning-fast similarity searches.

3.  **💬 User Query Processing:** When a user enters a search query, their text is converted into a query vector using the *same* Sentence Transformer model.

4.  **🎯 Vector Similarity Search:** This query vector is sent to Pinecone, which then performs a similarity search against the indexed movie vectors to find the closest semantic matches.

5.  **🎬 Streamlit UI:** Finally, the results are beautifully displayed in a user-friendly web app built with Streamlit.

## 💻 Tech Stack

This project was brought to life using these amazing technologies:

| Technology             | Role                       |
| ---------------------- | -------------------------- |
| **Python** | Core Language              |
| **Streamlit** | Interactive Web App UI     |
| **Pinecone** | Vector Database            |
| **Sentence-Transformers** | NLP Model for Embeddings   |
| **Pandas** | Data Manipulation          |

## 💾 Data Source

This project leverages the official [The Movie Database (TMDb) API](https://www.themoviedb.org/documentation/api) to fetch up-to-date and rich information for thousands of movies. A huge thank you to TMDb for providing this fantastic resource!

<br>

<div align="center">
<h3>Happy Watching! 🍿</h3>
</div>
