import duckdb

atp_duck = duckdb.connect('atp.duck.db')

atp_duck.sql("INSTALL httpfs")
atp_duck.sql("LOAD httpfs")

csv_files = [
    f"https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_{year}.csv"
    for year in range(1968,2024)
]
atp_duck.execute("""
CREATE OR REPLACE TABLE matches AS 
SELECT * FROM read_csv_auto($1, types={'winner_seed': 'VARCHAR', 'loser_seed': 'VARCHAR'})
""", [csv_files])