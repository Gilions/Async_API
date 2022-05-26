# Выгружаем данные по произведениям
FW_SQL = """
SELECT fw.id,
       fw.title,
       fw.description,
       fw.rating,
       fw.type,
       fw.created,
       fw.modified,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'person_id', p.id,
                   'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'actor'),
           '[]'
           ) AS actors,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'person_id', p.id,
                   'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'writer'),
           '[]'
           ) AS writers,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'writer') AS writers_names,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'actor') AS actors_names,
       ARRAY_AGG(DISTINCT g.name) AS genres
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
SELECT DISTINCT g.id, g.name, g.description
FROM genre g
INNER JOIN genre_film_work gfw ON g.id = gfw.genre_id
WHERE {param};
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
