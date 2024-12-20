import streamlit as st
import duckdb
from streamlit_searchbox import st_searchbox

# atp_duck = duckdb.connect('atp.duck.db', read_only=True)
atp_duck = duckdb.connect('atp.duck.db')

def search_players(search_term):
    query = '''
    SELECT DISTINCT winner_name AS player
    FROM matches
    WHERE player ilike '%' || $1 || '%'
    UNION
    SELECT DISTINCT loser_name AS player
    FROM matches
    WHERE player ilike '%' || $1 || '%'
    '''
    values = atp_duck.execute(query, parameters=[search_term]).fetchall()
    return [value[0] for value in values]


st.title("🎾ATP Head to Head 🎾")

left, right = st.columns(2)
with left:
    player1 = st_searchbox(search_players, label="Player 1", key="player1_search")
with right:
    player2 = st_searchbox(search_players, label="Player 2", key="player2_search")

st.markdown("***")

if player1 and player2:
    matches_for_players = atp_duck.execute("""
    SELECT tourney_date,tourney_name, surface, round, winner_name, score
    FROM matches
    WHERE (loser_name  = $1 AND winner_name = $2) OR
          (loser_name  = $2 AND winner_name = $1)
    ORDER BY tourney_date DESC
    """, [player1, player2]).fetchdf()
    if len(matches_for_players) == 0:
        st.header(f"{player1} vs {player2}")
        st.error("No matches found between these players.")
    else:
        player1_wins = matches_for_players[matches_for_players.winner_name == player1].shape[0]
        player2_wins = matches_for_players[matches_for_players.winner_name == player2].shape[0]
        st.header(f"{player1} {player1_wins}-{player2_wins} {player2}")
        
        left, right = st.columns(2)
        with left:
            st.markdown(f'#### By Surface')
            by_surface = atp_duck.sql("""
            SELECT winner_name AS player, surface, count(*) AS wins
            FROM matches_for_players
            GROUP BY ALL
            """).fetchdf()
            st.dataframe(by_surface.pivot(index="surface", columns="player" ,values="wins"))
        with right:
            st.markdown(f'#### By Round')
            by_surface = atp_duck.sql("""
            SELECT winner_name AS player, round, count(*) AS wins
            FROM matches_for_players
            GROUP BY ALL
            """).fetchdf()
            st.dataframe(by_surface.pivot(index="round", columns="player" ,values="wins"))
        st.markdown(f'#### Matches')
        st.dataframe(matches_for_players)