import streamlit as st
import pandas as pd
import math
from pinecone import Pinecone

# --- Page Configuration ---
st.set_page_config(
    page_title="CineVerse Finder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for a Polished, Modern Theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* General App Styling */
    html, body, [class*="st-"] {
        font-family: 'Roboto', sans-serif;
    }

    .stApp {
        /* Add a background image */
        background-image: linear-gradient(rgba(11, 11, 11, 0.85), rgba(11, 11, 11, 0.85)), url('https://images.unsplash.com/photo-1574267432553-f3e2780e0c64?auto=format&fit=crop');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #ffffff;
    }

    /* --- Titles and Headers --- */
    .dynamic-title {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        padding-top: 2rem;
        background: linear-gradient(90deg, #8A2BE2, #9932CC, #ffffff, #8A2BE2);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-animation 5s ease infinite;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* NEW: Subtitle styling */
    .app-subtitle {
        text-align: center;
        color: #bdbdbd;
        font-size: 1.1rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
    }

    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Base h2 style */
    h2 {
        color: #ffffff;
        border-bottom: 2px solid #8A2BE2;
        padding-bottom: 10px;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        font-size: 2.2rem;
    }

    /* NEW: Special class for gradient text on section headers */
    .gradient-text-header {
        background: linear-gradient(90deg, #e0c3fc, #8ec5fc, #e0c3fc);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-animation 8s ease-in-out infinite;
    }

    /* --- Enhanced Main Search Bar (UPDATED) --- */
    /* This targets the container div of the text input with key="main_search" */
    div[data-testid="stTextInput"][key="main_search"] > div {
        background-color: #2a2a2e;
        border-radius: 50px; /* Pill shape */
        padding: 0.5rem 1.5rem;
        border: 2px solid #555;
        transition: border-color 0.3s, box-shadow 0.3s;
        
        /* Add an SVG search icon as a background image */
        background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="%23999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"%3E%3Ccircle cx="11" cy="11" r="8"%3E%3C/circle%3E%3Cline x1="21" y1="21" x2="16.65" y2="16.65"%3E%3C/line%3E%3C/svg%3E');
        background-repeat: no-repeat;
        background-position: left 1.25rem center; /* Position the icon */
        padding-left: 3.5rem; /* Add padding to make space for the icon */
    }
    
    /* Style the search bar when it's focused */
    div[data-testid="stTextInput"][key="main_search"] > div:focus-within {
        border-color: #8A2BE2;
        box-shadow: 0 0 15px rgba(138, 43, 226, 0.5);
        
        /* Change the icon color to match the border when focused */
        background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="%238A2BE2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"%3E%3Ccircle cx="11" cy="11" r="8"%3E%3C/circle%3E%3Cline x1="21" y1="21" x2="16.65" y2="16.65"%3E%3C/line%3E%3C/svg%3E');
    }

    /* This targets the actual <input> element itself */
    div[data-testid="stTextInput"][key="main_search"] input {
        background-color: transparent !important;
        border: none !important;
        font-size: 1.2rem; /* Larger font */
        color: #ffffff;
        /* The padding-left here is relative to its container's padding */
        padding-left: 0.5rem; 
    }

    /* --- Enhanced Filter Container --- */
    .filter-container {
        background-color: rgba(31, 31, 31, 0.7); /* Semi-transparent dark background */
        backdrop-filter: blur(5px); /* Frosted glass effect */
        border-radius: 12px;
        padding: 1.5rem 2rem;
        border: 1px solid #444;
        margin-top: 1.5rem;
    }
    .filter-container .stTextInput > div > div > input,
    .filter-container .stSelectbox > div > div {
        background-color: #2a2a2e;
        border-radius: 8px;
    }

    /* --- Movie Card Styling --- */
    .movie-card {
        background-color: #1c1c1e;
        border-radius: 12px;
        overflow: hidden;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        border: 1px solid #333;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .movie-card:hover {
        transform: scale(1.05) translateY(-5px);
        box-shadow: 0px 15px 30px rgba(138, 43, 226, 0.4);
        z-index: 10;
    }
    .poster-container {
        position: relative;
    }
    .poster-container img {
        width: 100%;
        display: block;
    }
    .poster-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 50%;
        background: linear-gradient(to top, rgba(11, 11, 11, 0.9), transparent);
    }
    .card-content {
        padding: 1rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .movie-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .movie-meta {
        font-size: 0.85rem;
        color: #aaa;
        margin-bottom: 0.75rem;
    }
    .movie-genres {
        font-style: italic;
        font-size: 0.8rem;
        color: #ccc;
    }

    /* --- Button Styling --- */
    .stButton > button {
        background-color: #8A2BE2;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
        padding: 10px 0;
        margin-top: auto; /* Pushes button to the bottom */
        transition: background-color 0.3s, transform 0.2s;
    }
    .stButton > button:hover {
        background-color: #9932CC;
        transform: scale(1.02);
    }
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* --- Dialog/Modal Styling --- */
    [data-testid="stDialog"] > div {
        background: radial-gradient(circle, #2d2d2d 0%, #1a1a1a 100%);
        border-radius: 15px;
        border: 1px solid #444;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'num_movies_to_display' not in st.session_state:
    st.session_state.num_movies_to_display = 10

# --- Resource Initialization ---
@st.cache_resource
def init_pinecone():
    """Initialize connection to Pinecone."""
    api_key = st.secrets.get("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY secret not found. Please set it in your Streamlit secrets.")
    
    pc = Pinecone(api_key=api_key)
    index = pc.Index("movie")
    return index

# --- Data Loading ---
@st.cache_data
def load_data(url):
    """Load movie data from a URL or local path and preprocess it."""
    df = pd.read_csv(url)
    df['poster_url'] = 'https://image.tmdb.org/t/p/w500' + df['poster_path']
    df['genres_list'] = df['genres'].str.split(', ').apply(lambda x: tuple(x) if isinstance(x, list) else tuple())
    df['id'] = df['id'].astype(str)
    df['overview'] = df['overview'].fillna('')
    # Add a year column for easier filtering
    df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year.fillna(0).astype(int)
    return df

@st.cache_data
def get_all_genres(df):
    """Get a list of all unique genres from the dataframe."""
    all_genres = set()
    for genres in df['genres_list'].dropna():
        all_genres.update(genres)
    return sorted(list(all_genres))


# --- Main Application ---
pinecone_index = init_pinecone() 
DATA_URL = "MovieData.csv"
movie_df = load_data(DATA_URL)
all_genres = get_all_genres(movie_df)


# --- UI Layout ---
# UPDATED: The title is now wrapped in a link to reset the page state.
st.markdown('<a href="." style="text-decoration: none;"><h1 class="dynamic-title">🎬 CineVerse Finder</h1></a>', unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Discover your next favorite movie through smart and semantic search.</p>", unsafe_allow_html=True)


# --- Search and Filter Section ---
with st.container():
    main_search = st.text_input(
        "Search for a movie...",
        "",
        key="main_search",
        placeholder="e.g., a mind-bending sci-fi movie or a movie with christian bale as batman",
        label_visibility="collapsed"
    )
    
    st.markdown("---")

    # Wrap filters in a visually enhanced container
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        title_search = st.text_input("Filter by title...", placeholder="Inception")
    with col2:
        genre_filter = st.selectbox("Filter by genre...", options=["All"] + all_genres)
    with col3:
        # Create a list of years for the dropdown
        years = ["All"] + sorted(movie_df[movie_df['year'] > 0]['year'].unique(), reverse=True)
        year_filter = st.selectbox(
            "Filter by release year...", 
            options=years
        )
    st.markdown('</div>', unsafe_allow_html=True)


# --- Movie Display Logic ---
if main_search:
    # UPDATED: Use markdown for a styled header, separating the icon
    st.markdown('<h2>🔎 <span class="gradient-text-header">Search Results</span></h2>', unsafe_allow_html=True)
    st.session_state.num_movies_to_display = 10 
    
    # This search logic needs to be adapted for your vector DB's API
    # The following is a placeholder based on the original code's intent
    # You would replace this with your actual Pinecone query logic
    try:
        # Placeholder for Pinecone query logic
        # You need to implement the actual embedding and query here
        # For now, we'll simulate a text search on the dataframe
        st.session_state.num_movies_to_display = 10 
    
        results = pinecone_index.search(
            namespace="movies", 
            query={
                "inputs": {"text": main_search}, 
                "top_k": 100
            },
            fields=["Combined"]
        )
        ids_list = list(map(lambda item: item['_id'], results['result']['hits']))

        if not ids_list:
            st.warning("No movies found for your search query.")
            movies_to_display = pd.DataFrame()
        else:
            search_results_df = movie_df[movie_df['id'].isin(ids_list)]
            search_results_df = search_results_df.set_index('id').loc[ids_list].reset_index()
            movies_to_display = search_results_df.head(100) # Display top 100 text search matches

    except Exception as e:
        st.error(f"Could not perform search: {e}")
        movies_to_display = pd.DataFrame()

else:
   
    st.markdown('<h2>📅 <span class="gradient-text-header">Latest Releases</span></h2>', unsafe_allow_html=True)
    
    filtered_df = movie_df.copy()
    if title_search:
        filtered_df = filtered_df[filtered_df['title'].str.contains(title_search, case=False, na=False)]
    if genre_filter != "All":
        filtered_df = filtered_df[filtered_df['genres_list'].apply(lambda x: genre_filter in x)]
   
    if year_filter != "All":
        filtered_df = filtered_df[filtered_df['year'] == year_filter]

    # Sort by release date (newest first)
    sorted_movies = filtered_df.sort_values(by=["release_date"], ascending=[False])
    movies_to_display = sorted_movies.head(st.session_state.num_movies_to_display)


# --- Display Grid ---
if not movies_to_display.empty:
    for i in range(0, len(movies_to_display), 5):
        cols = st.columns(5)
        batch = movies_to_display.iloc[i:i+5]
        for j, movie in enumerate(batch.itertuples()):
            col = cols[j]
            with col:
                st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
                
                st.markdown('<div class="poster-container">', unsafe_allow_html=True)
                st.image(movie.poster_url, use_container_width=True)
                st.markdown('<div class="poster-overlay"></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="card-content">', unsafe_allow_html=True)
                st.markdown(f'<p class="movie-title">{movie.title}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="movie-meta">{movie.year} | ⭐ {movie.vote_average:.1f} | {movie.runtime} min</p>', unsafe_allow_html=True)
                
                genres_to_show = movie.genres_list[:3] if isinstance(movie.genres_list, tuple) else []
                st.markdown(f'<p class="movie-genres">{", ".join(genres_to_show)}</p>', unsafe_allow_html=True)
                
                if st.button("More Details", key=f"details_{movie.Index}"):
                    st.session_state.selected_movie = movie
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True) # close card-content
                st.markdown('</div>', unsafe_allow_html=True) # close movie-card
else:
    if not main_search:
        st.info("No movies match your current filters. Try adjusting them!")


# --- "Load More" Button (only show if not searching) ---
if not main_search and not movies_to_display.empty:
    st.markdown("<br>", unsafe_allow_html=True)
    # Check if there are more movies to load from the filtered set
    if st.session_state.num_movies_to_display < len(sorted_movies):
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Load More 🍿", use_container_width=True):
                st.session_state.num_movies_to_display += 10
                st.rerun()


# --- Movie Details Dialog (Modal) ---
if st.session_state.selected_movie is not None:
    movie = st.session_state.selected_movie

    @st.dialog(f"Details for {movie.title}")
    def show_movie_details():
        # Top section with poster and primary info
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(movie.poster_url, use_container_width=True, caption="Movie Poster")
        with col2:
            st.markdown(f"### {movie.title} ({movie.year})")
            if movie.tagline and pd.notna(movie.tagline):
                st.markdown(f"*{movie.tagline}*")
            st.markdown(f"**Rating:** ⭐ {movie.vote_average:.1f}/10 ({movie.vote_count:,} votes)")
            st.markdown(f"**Runtime:** {movie.runtime} minutes")
            st.markdown(f"**Genres:** {movie.genres}")
            
        st.markdown(f"**Overview:** {movie.overview}")
        
        # Use columns for a cleaner layout of financial data
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.markdown(f"**Budget:** ${movie.budget:,}" if movie.budget > 0 else "**Budget:** Not Available")
        with info_col2:
            st.markdown(f"**Revenue:** ${movie.revenue:,}" if movie.revenue > 0 else "**Revenue:** Not Available")

        st.markdown(f"**Original Language:** {movie.original_language.upper()}")

        # Safely display production companies if data exists
        if hasattr(movie, 'production_companies') and pd.notna(movie.production_companies) and movie.production_companies != '[]':
            st.markdown(f"**Production Companies:** {movie.production_companies}")
        else:
            st.markdown("**Production Companies:** Information not available.")

        st.markdown("<br>", unsafe_allow_html=True) # Add some space before the button

        # Close button
        if st.button("Close", key=f"close_dialog_{movie.Index}", use_container_width=True):
            st.session_state.selected_movie = None
            st.rerun()

    show_movie_details()
