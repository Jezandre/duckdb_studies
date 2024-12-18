# 1. Installation

- Windows & Linux:
    1. Navigate to [Duckdb Releases @github](https://github.com/duckdb/duckdb/releases)
    2. Download the appropriate distribution
    3. Unpack & Install

Additional instruction for [Windows](https://duckdb.org/docs/installation/?version=latest&environment=cli&installer=binary&platform=win)

- MacOS: 
    1. Install [homebrew](https://brew.sh)
    2. ```sh 
        brew install duckdb
        ```

# 2. Demo

1. Open terminal

2. ```sh
    duckdb demo1.duckdb
    ```

3. Lets have a look at available extensions 
    ```sql
        DESCRIBE
            SELECT *
                FROM duckdb_extensions();
        ```

4. Which ones do we have installed & ready to be used?
    ```sql
    SELECT extension_name, loaded, installed 
        from duckdb_extensions()
            ORDER BY installed DESC, loaded DESC;
    ```

5. Lets install & load `httpfs` so we can query data directly from the web
    ```sql
    INSTALL httpfs; 
    LOAD httpfs;
    ```

6. What is the availale amount of memory to our duckdb instance?
    ```sql
    select current_setting('memory_limit');
    ```
    Lets increase it!

    ```sql
    SET memory_limit='30GB';
    ```

6. Time to query some data!

    ```sql
    SELECT count(*)
        FROM read_csv_auto('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2023.csv');
    ```

7. Lets explore duckdbs output formats & change to a new one:

    ```sh
    .help mode
    ```

    ```sh
    .mode line
    ```

    ```sql
    SELECT * 
        FROM read_csv_auto('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2023.csv')
        LIMIT 1;
    ```

8. Switching back to `duckbox` mode & querying a new data insight
    ```sh
    .mode duckbox
    ```

    ```sql
    select winner_ioc, loser_ioc, winner_hand, loser_hand, count(distinct(tourney_id)) as num_winners, avg(winner_age) as avg_winner_age, max(loser_age) as max_loser_age
        from read_csv_auto('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2023.csv')
            group by all;
    ```

9. Lets go more interactive & automated!

-> Quit duckdb with Ctrl+D
-> run:

    ```sh
        duckdb -csv \
        -s "select winner_ioc, loser_ioc, winner_hand, loser_hand, count(distinct(tourney_id)) as num_winners, avg(winner_age) as avg_winner_age, max(loser_age) as max_loser_age
        from read_csv_auto('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2023.csv')
            group by all;"\
          > results_2023.csv
    ```

    ```sh
    head -n 5 results_2023.csv
    ```

10. Why write into `csv` when `parquet` is faster & takes less space?
    
    ```sh
        duckdb \
        -s "COPY (select winner_ioc, loser_ioc, winner_hand, loser_hand, count(distinct(tourney_id)) as num_winners, avg(winner_age) as avg_winner_age, max(loser_age) as max_loser_age
        from read_csv_auto('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2023.csv')
            group by all) TO '/dev/stdout' (FORMAT PARQUET)"\
          > /results_2023.parquet
    ```

    Lets read the results:
    ```sh
    duckdb -s "FROM 'results_2023.parquet' LIMIT 3"
    ```