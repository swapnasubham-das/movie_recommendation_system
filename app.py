import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie Recommendation")
st.header('SS Das Movie Recommender System')

def fetch_movie_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=682a6bc426d0dae62f009dad39f47954'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def movie_recommend(movie):
    # Fetch the movie index
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_poster = []
    for movie in movie_list:
        movie_id = movies_df.iloc[movie[0]].movie_id
        recommended_movies.append(movies_df.iloc[movie[0]].title)
        # Fetch poster from API
        recommended_movies_poster.append(fetch_movie_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# Load movies data and similarity matrix
movies_df = pickle.load(open('movies.pkl', 'rb'))

# Check if 'movies.pkl' is a DataFrame; if not, convert to DataFrame
if isinstance(movies_df, pd.DataFrame):
    movies_df = movies_df
else:
    movies_df = pd.DataFrame(movies_df, columns=['title'])

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Extract movie titles
movies_list = movies_df['title'].values

# Select a movie
selected_movie_name = st.selectbox("Select a movie for recommendations:", movies_list)

# Recommend movies
if st.button("Recommend"):
    try:
        movie_name, movie_poster = movie_recommend(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        col6, col7, col8, col9, col10 = st.columns(5)

        with col1:
            st.text(movie_name[0])
            st.image(movie_poster[0])
        with col2:
            st.text(movie_name[1])
            st.image(movie_poster[1])
        with col3:
            st.text(movie_name[2])
            st.image(movie_poster[2])
        with col4:
            st.text(movie_name[3])
            st.image(movie_poster[3])
        with col5:
            st.text(movie_name[4])
            st.image(movie_poster[4])

        with col6:
            st.text(movie_name[5])
            st.image(movie_poster[5])
        with col7:
            st.text(movie_name[6])
            st.image(movie_poster[6])
        with col8:
            st.text(movie_name[7])
            st.image(movie_poster[7])
        with col9:
            st.text(movie_name[8])
            st.image(movie_poster[8])
        with col10:
            st.text(movie_name[9])
            st.image(movie_poster[9])

    except IndexError as e:
        st.error("Error: Movie not found in dataset or indexing issue occurred. Check your data files.")
