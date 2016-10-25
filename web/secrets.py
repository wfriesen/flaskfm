import os

database_uri = os.environ.get(
    'POSTGRES_URI',
    'postgresql://docker:docker@db/docker'
)
