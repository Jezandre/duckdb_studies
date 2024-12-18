# Exploring duckdb innovations & SQL dialect using chinook database

[More on data here](https://www.sqlitetutorial.net/sqlite-sample-database/)

1. Make sure duckdb is installed & cd into dir with chinook.db

2. ./duckdb chinook.db or duckdb chinook.db

3. ```sql 
    show tables;
    ```
    or the duckbd way:
    ```sql
    .tables
    ```

4. ```sql
    describe select * from invoices;
    ```
5. Let's create a view of average check per coutry per day.

    ```sql
    create or replace view v_average_checks as
        select BillingCountry, date_trunc('day', InvoiceDate) as day, avg(Total) as avg_check
            from invoices
            group by BillingCountry, day;
    ```
    `SUMMARIZE = innovation`. It's a quick way to grasp the features' properties.

    ```sql
    SUMMARIZE v_average_checks;
    ```

6. Excluding what we DO NOT need is easier than listing what we NEED!
    `EXCLUDE = innovation!`

    ```sql
    select * exclude (BillingAddress, BillingCity, BillingState) from invoices limit 5;
    ```

7. ```sql
    select * replace(round(avg_check)::int as avg_check)
        from v_average_checks;
    ```
    `REPLACE = innovation!`

8. Using `REGEX` to query data faster
    ```sql
    select columns('Billing.*') from invoices limit 5;
    ```

    `COLUMNS=innovation`
9. Combining `EXCLUDE` & `COLUMS` is also easy:

    ```sql
    select distinct(columns(* exclude(InvoiceId, CustomerId, InvoiceDate, Total))) from invoices limit 5;
    ```

10. `Grouping by` is as easy as ever with `group by all`

    ```sql
    select BillingCountry, BillingState, BillingPostalCode, sum(Total)
        from invoices
            group by 1,2,3;
    ```
    vs
    ```sql
    select BillingCountry, BillingState, BillingPostalCode, sum(Total)
        from invoices
            group by ALL;
    ```

    `GROUP BY ALL=innovation`

11. A feature useful for Data Science & Analytics: `SAMPLE`

    ```sql
    select Total 
        from invoices
            where Total>10
                USING sample 15% (bernoulli);
    ```
## Window functions

12. Time to learn some `WINDOW FUNCTIONS` in duckdb!

    Getting top-3 days with highest average checks for countries
    ```sql
    with ranked_checks as (
        select *,
            dense_rank()
            OVER(partition by BillingCountry order by avg_check desc) as rank
                from v_average_checks
                where extract('year' from day)=2011
    )
    select * from ranked_checks where rank <=3
        order by BillingCountry, rank asc;
    ```

13. Calculating monthly moving average for average checks in countries

    ```sql
    select BillingCountry, day, avg_check,
        avg(avg_check) over(partition by BillingCountry
                            order by day asc
                            range between interval 30 days preceding 
                            and interval 0 days following) as avg_check_30_days_moving_average
                            from v_average_checks
                                order by BillingCountry, day asc;
    ```

## PIVOT tables in duckdb

14. What if you are working on TimeSeries modelling and need your data to follow a specific format?

`PIVOT` got you covered!
What were the average & minimum checks per year per country?

    ```sql
    PIVOT v_average_checks
        on year(day)
        using avg(avg_check) as avg_check, min(avg_check) as worst_avg_check;
    ```

## Producing date-related table structures automatically with duckdb

15. ```sql
    FROM generate_series('2011-01-01'::date, '2014-12-31'::date, INTERVAL '1 day');
    ```
No need to use `SELECT`: just go for `FROM` straight away!
`One more innovation from duckdb!`

16. ```sql
        .exit
        ```