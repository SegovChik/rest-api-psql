import os
DB_USER = 'test_user'
DB_PASS = 'password'
DB_NAME = 'test_db'


DB_URL = 'postgresql+psycopg2://test_user:password@db:5432/test_db'

ACTOR_FIELDS = ['id', 'name', 'gender', 'date_of_birth']
MOVIE_FIELDS = ['id', 'name', 'year', 'genre']

# date of birth format
DATE_FORMAT = '%d.%m.%Y'
