-- 1. What are the TOP5 richest and lowest income neighborhoods?
DROP TABLE IF EXISTS income_rank;
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
-- 2. What are the neighborhoods’ income and CRs(complaint record) per capita?
-- 3. What is the TRRS(tactical response report) per capita?
-- 4. What is the percentage of each race in the community?
-- 5. What are the top 5 streets in allegation counts for each beat area?
DROP TABLE IF EXISTS top_streets;
CREATE TEMP TABLE top_streets AS(
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
);

SELECT * FROM top_streets;