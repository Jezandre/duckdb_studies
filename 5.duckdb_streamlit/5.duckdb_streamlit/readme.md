# Integrating duckdb with Streamlit

In this case we'll be reproducing the functionality of Head2Head tennis players comparison from here:
https://www.atptour.com/en/players/atp-head-2-head

A pair of players to use as an example: 
CARLOS ALCARAZ VS HOLGER RUNE

We'll be using Streamlit & DuckDB for that

1. cd into project's dir

2. ```python3 -m venv .streamlitenv```

3. ```source .streamlitenv/bin/activate```

4. ```pip3 install -r requirements.txt```

5. ```python3 dataloading.py```

    Getting the data we need & populating duckdb database with it

6. ```python3 -m streamlit run app.py```

7. Explore the App in UI (use browser)
    
    Navigate to: `http://172.20.10.2:8501`

8. Ctrl+C to shut down the App

9. `deactivate` to switch off our streamlit venv