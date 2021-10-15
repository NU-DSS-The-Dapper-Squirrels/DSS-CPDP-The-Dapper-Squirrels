# Checkpoint 1

## Getting Started

By executing the `src/analysis_questions.sql`, the data query will be processed.

## Our Questions

1. [What is the TOP5 richest and lowest income neighborhoods?](#what-is-the-top5-richest-and-lowest-neighborhoods)
2. [What is the income and CRs(complaint record) per capita?](#what-is-the-income-and-crscomplaint-record-per-capita)
3. [What is the TRRS(tactical response report) per capita?](#what-is-the-trrstactical-response-report-per-capita)
4. [What is the percentage of each race in the community?](#what-is-the-percentage-of-each-race-in-the-community)
5. [What is the top 5 streets in allegation counts for each beat area?](#what-is-the-top-5-streets-in-allegation-counts-for-each-beat-area)

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

### What are the neighborhoods’ income and CRs(complaint record) per capita?
**SOME INSTRUCTION HERE e.g: Run question1.sql or copy and paste the queries below**


```sql
SELECT dar.median_income,dar.name
FROM data_allegation da
LEFT JOIN data_area dar On dar.id = da.beat_id
WHERE dar.median_income IS NOT NULL ;
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
    (SELECT beat_id, add2, cnt, RANK() OVER(PARTITION BY beat_id ORDER BY cnt DESC) AS rank
    FROM (SELECT beat_id, add2, COUNT(*) AS cnt
        FROM public.data_allegation
        WHERE beat_id IS NOT NULL AND add2 IS NOT NULL
        GROUP BY beat_id, add2
    ) a
) b
WHERE beat_id IS NOT NULL AND add2 IS NOT NULL AND rank <= 5
;
```
