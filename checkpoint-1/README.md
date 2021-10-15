# Checkpoint 1

## Getting Started


## Our Questions
1. What is the TOP5 richest and lowest income neighborhoods?
2. What is the income and CRs(complaint record) per capita?
3. What is the TRRS(tactical response report) per capita?
4. What is the percentage of each race in the community?
5. What is the top 5 streets in allegation counts for each beat area?



## Queries

### What is the TOP5 richest and lowest neighborhoods?
**SOME INSTRUCTION HERE e.g: Run question1.sql or copy and paste the queries below**


* Table of the richest and lowest income:
```sql
DROP TABLE IF EXISTS income_ranl;
CREATE TEMP TABLE income_rank AS(
    SELECT richest.rank AS rank,richest.id AS richest_id, richest.name AS richest_name, richest.median_income AS richest_incom,
           lowest.id AS lowest_id, lowest.name AS lowest_name, lowest.median_income AS lowest_incom
    FROM
        (SELECT ROW_NUMBER() OVER(ORDER BY CAST( replace(replace(median_income, '$',''),',','') AS INT )DESC ) AS rank, name, id, median_income
        FROM  data_area
        WHERE median_income IS NOT NULL
        ORDER BY rank
        LIMIT 5) AS richest
        LEFT JOIN
            (SELECT ROW_NUMBER() OVER(ORDER BY CAST( replace(replace(median_income, '$',''),',','') AS INT )ASC ) AS rank, name, id, median_income
            FROM  data_area
            WHERE median_income IS NOT NULL
            ORDER BY rank
            LIMIT 5) AS lowest
        ON richest.rank = lowest.rank
);

SELECT * FROM income_rank;
```

### What is the income and CRs(complaint record) per capita?
**SOME INSTRUCTION HERE e.g: Run question1.sql or copy and paste the queries below**


```sql
SELECT DISTINCT first_name,last_name,rank,current_salary, complaint_percentile, civilian_allegation_percentile
FROM data_officer
WHERE current_salary IS NOT NULL
ORDER BY current_salary DESC ;
```
* There is a alternative query since the officers' rank is different in data_officer and data_salary:
```sql
SELECT DISTINCT first_name,last_name,data_officer.rank,salary, complaint_percentile, civilian_allegation_percentile
FROM data_officer
   LEFT JOIN data_salary ds on data_officer.id = ds.officer_id
WHERE salary IS NOT NULL
ORDER BY salary DESC ;
```

### What is the TRRS(tactical response report) per capita?
**SOME INSTRUCTION HERE e.g: Run question1.sql or copy and paste the queries below**


* For all officers showing in trr table:
```sql
SELECT  CAST(count(*) AS float)/CAST(count( DISTINCT officer_id) AS float) AS trr_per_capital
FROM trr_trr;
```
* For all offices showing in officer table:
```sql
SELECT a.total_trr/b.total_officer
FROM
   (SELECT CAST(count(*) AS float) AS total_trr
   FROM trr_trr) AS a,
   (SELECT  CAST(count(*) AS float) AS total_officer
   FROM data_officer) AS b;
```

### What is the percentage of each race in the community.
**SOME INSTRUCTION HERE e.g: Run question1.sql or copy and paste the queries below**


```sql
SELECT id,name,A.race,A.ratio
FROM data_area,
   (SELECT dr.area_id, race, CAST(count AS float)/CAST(total AS float) AS ratio
   FROM data_racepopulation dr,
        (SELECT area_id, sum(count) AS total FROM data_racepopulation GROUP BY area_id) AS population
   WHERE dr.area_id = population.area_id) AS A
WHERE  data_area.id = A.area_id;
```

### What is the top 5 streets in allegation counts for each beat area?
**SOME INSTRUCTION HERE e.g: Run question1.sql or copy and paste the queries below**


```sql
SELECT *
FROM
   (SELECT beat_id, add2, rank() Over(PARTITION BY add2 ORDER BY cnt DESC )
   FROM (SELECT beat_id, add2, count(*) AS cnt
       FROM public.data_allegation
       WHERE beat_id IS NOT NULL and add2 IS NOT NULL
       GROUP BY beat_id, add2
   ) a
) b
WHERE rank <= 5
```
