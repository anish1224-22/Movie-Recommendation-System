import pandas as pd
import streamlit as st
import pickle
import requests

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarit.pkl','rb'))


def fetchPoster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b1c29881630ec85c3c0b570978d39d31"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
  index=movies[movies['title']==movie].index[0]
  distances = similarity[index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  recommended_movies=[]
  recommended_movies_posters=[]
  for i in movies_list:
    movie_id=movies.iloc[i[0]].movie_id
    recommended_movies_posters.append(fetchPoster(movie_id))
    recommended_movies.append(movies.iloc[i[0]].title)
  return recommended_movies,recommended_movies_posters
st.title('Movie Recommendation System')
selected_movie_name = st.selectbox(
    "What's your movie taste?",
    movies['title'].values)

if st.button('Recommendations'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
