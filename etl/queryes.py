# Выгружаем данные по произведениям
FW_SQL = """
SELECT fw.id as uuid,
       fw.title,
       fw.description,
       fw.rating as imdb_rating,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'uuid', p.id,
                   'full_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'actor'),
           '[]'
           ) AS actors,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'uuid', p.id,
                   'full_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'writer'),
           '[]'
           ) AS writers,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'uuid', p.id,
                   'full_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'director'),
           '[]'
           ) AS directors,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'uuid', g.id,
                   'name', g.name
                   )
               ) FILTER (WHERE g.id IS NOT NULL),
           '[]'
           ) AS genre
FROM content.film_work fw
         LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
         LEFT JOIN content.genre g ON g.id = gfw.genre_id
         LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
         LEFT JOIN content.person p ON p.id = pfw.person_id
WHERE {param}
GROUP BY fw.id
ORDER BY fw.modified;
"""

# Выгружаем данные по жанрам
GENRE_SQL = """
SELECT DISTINCT
    g.id as uuid,
    g.name
FROM genre g
INNER JOIN genre_film_work gfw ON g.id = gfw.genre_id
WHERE {param};
"""

# Выгружаем данные по людям
PERSON_SQL = """
SELECT DISTINCT
    pp.id as uuid,
    pp.full_name,
    pfw.role,
    array_agg(DISTINCT pfw.id::text) as film_ids
FROM person pp
INNER JOIN person_film_work pfw ON pp.id = pfw.person_id
WHERE {param}
GROUP BY pp.id, pp.full_name, pfw.role;
"""

# Записываем данные последнего запуска процесса
INSERT_ETL = """
INSERT INTO external.etl_services (process, start)
VALUES ('{process}', '{start}') ON CONFLICT (process) DO UPDATE SET start =EXCLUDED.start
"""

# получаем дату последнего запуска процесса
SELECT_ETL = """
SELECT start
FROM external.etl_services
WHERE process = '{process}';
"""
