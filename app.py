import streamlit as st
import pickle
import pandas as pd
import requests


def link(title):
    title = title.lower()
    for k in range(len(title)):
        if title[k] != ' ' and type(title[k]) != str:
            title.replace(title[k], '')
    return '-'.join(title.split())


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=API_KEY&language=en-US')
    data = response.json()
    try:
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    except:
        pass


def recommend(movie, m):
    movies_list = sorted(list(enumerate(similarity[movies[movies['title'] == movie].index[0]])), reverse=True, key=lambda x: x[1])[1: m + 1]
    recommended_id = [movies.iloc[j[0]].movie_id for j in movies_list]
    recommended_movies = [movies.iloc[j[0]].title for j in movies_list]
    recommended_posters = [fetch_poster(movies.iloc[j[0]].movie_id) for j in movies_list]
    return recommended_id, recommended_movies, recommended_posters


movies = pd.DataFrame(pickle.load(open('movie_list.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.write('Indraneel Dey')
st.write('Indian Institute of Technology, Madras')
st.title('Movie Recommendation System')
selected_movie = st.selectbox('Type or select the movie you like', movies['title'].values)
choice = st.number_input('Select the number of recommendations you want', min_value=2, max_value=5)
id_ans = int(movies[movies['title'] == selected_movie]['movie_id'])
movie_url = f'https://www.themoviedb.org/movie/{id_ans}-{link(selected_movie)}'
st.write('You can click on the title of a movie to visit its TMDB page')
st.write(f'Selected movie: [{selected_movie}]({movie_url})')

if st.button('Recommend'):
    col = st.columns(choice)
    ids, names, posters = recommend(selected_movie, choice)
    for i in range(choice):
        with col[i]:
            url = f'https://www.themoviedb.org/movie/{ids[i]}-{link(names[i])}'
            st.write(f'[{names[i]}]({url})')
            try:
                st.image(posters[i])
            except:
                pass
