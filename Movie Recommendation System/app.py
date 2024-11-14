import streamlit as st
import pickle
import pandas as pd
import requests



# Function to fetch poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c0640e898a872cbf57edf634ba8d957a&language=en-US'.format(movie_id))
    data = response.json()
    # st.text(data)
    # st.text('https://api.themoviedb.org/3/movie/{}?api_key=c0640e898a872cbf57edf634ba8d957a&language=en-US'.format(movie_id))
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies
def recommend(movie):
   movie_index = movies[movies['title'] == movie].index[0]
   distances=similarity[movie_index]
   movies_list  = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

   recommended_movies = []
   recommended_movies_posters = []

   for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
   return recommended_movies,recommended_movies_posters


# Load movies and similarity data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Add movie_id column if it's missing
if 'movie_id' not in movies.columns:
    movies['movie_id'] = range(1, len(movies) + 1)

similarity= pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommendation System')

selected_movie_name= st.selectbox(
    'Choose a movie title of your choice',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])