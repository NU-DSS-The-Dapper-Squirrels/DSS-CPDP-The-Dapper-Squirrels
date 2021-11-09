```sql
SELECT json_build_object(
    'type','FeatureCollection',
    'features', json_agg(json_build_object(
        'type','MultiPolygon',
        'coordinates',p.polygon,
        'properties',json_build_object(
            'name',p.id
                    )::jsonb
        )
        )
    )
FROM (SELECT data_area.polygon as polygon,c.id
                FROM (SELECT a.count/(a.count+b.count) AS percent, a.beat_id as id
                        FROM
                             (SELECT CAST(count(*) AS float), beat_id
                             FROM data_officerassignmentattendance
                             WHERE present_for_duty = true
                             GROUP BY data_officerassignmentattendance.beat_id) AS a,
                             (SELECT CAST(count(*) AS float), beat_id
                             FROM data_officerassignmentattendance
                             WHERE present_for_duty = false
                             GROUP BY data_officerassignmentattendance.beat_id) AS b
                WHERE a.beat_id=b.beat_id) c
                    LEFT JOIN data_area ON c.id = data_area.id) p;
```
