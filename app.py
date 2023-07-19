import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_cover(game_id):
    response = requests.get('https://api.rawg.io/api/games/{}?key=ca5490cff7094f1dabcb0f6b3a555ab8'.format(game_id))
    data = response.json()
    if 'background_image' in data:
        return data['background_image']
    else:
        return 'https://images.app.goo.gl/vijxNmJUM3Nss7Fm6'


def recommend(game):
    game_index = games[games['Title'] == game].index[0]
    distances = similarity[game_index]
    games_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_games = []
    recommended_games_covers = []
    for i in games_list:
        game_id = games.iloc[i[0]].ID
        recommended_games.append(games.iloc[i[0]].Title)
        recommended_games_covers.append(fetch_cover(game_id))
    return recommended_games, recommended_games_covers

games_list = pickle.load(open('games_dict.pkl', 'rb'))
games = pd.DataFrame(games_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Video Game Recommender')

picked_game = st.selectbox('Pick A Game', games['Title'].values)

if st.button('Recommend'):
    recommendations = recommend(picked_game)
    recommended_games, recommended_game_covers = recommendations

    col1, col2, col3, col4, col5 = st.columns(5,gap="small")
    with col1:
        st.text(recommended_games[0])
        st.image(recommended_game_covers[0])
    with col2:
        st.text(recommended_games[1])
        st.image(recommended_game_covers[1])
    with col3:
        st.text(recommended_games[2])
        st.image(recommended_game_covers[2])
    with col4:
        st.text(recommended_games[3])
        st.image(recommended_game_covers[3])
    with col5:
        st.text(recommended_games[4])
        st.image(recommended_game_covers[4])

