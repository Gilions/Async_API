import os

from dotenv import load_dotenv

load_dotenv()

# Конфигурация Postgres
DSL = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}

# Конфигурация ELK
DSL_ELK = {
    'hosts': [
        'http://{}:{}'.format(os.environ.get('EL_HOST'),
                              os.environ.get('EL_PORT'))
    ]
}
# Время остановки ETL цикла
TIME_OUT = 10

# ELK Индексы
INDEX_SETTINGS = {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer"
                    ]
                }
            }
        }
    }

INDEX_MOVIES = {
    "index": "movies",
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "imdb_rating": {
                "type": "float"
            },
            "genre": {
                "type": "keyword"
            },
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "description": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "director": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "writers_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            }
        }
    },
    "settings": INDEX_SETTINGS
}

INDEX_GENRES = {
    "index": "genres",
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "name": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "description": {
                "type": "text",
                "analyzer": "ru_en"
            }
        }
    },
    "settings": INDEX_SETTINGS
}

INDEX_PERSONS = {
    "index": "persons",
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "full_name": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "birth_date": {
                "type": "date"
            }
        }
    },
    "settings": INDEX_SETTINGS
}

INDICES = {
    'movies': INDEX_MOVIES,
    'genres': INDEX_GENRES,
    'persons': INDEX_PERSONS
}
