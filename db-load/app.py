#!/usr/bin/env python3

from sqlalchemy import create_engine
import psycopg2
import pandas as pd

links_df = pd.read_csv(r'/tmp/ml-latest-small/links.csv', header=0)
movies_df = pd.read_csv(r'/tmp/ml-latest-small/movies.csv', header=0)
ratings_df = pd.read_csv(r'/tmp/ml-latest-small/ratings.csv', header=0)
tags_df = pd.read_csv(r'/tmp/ml-latest-small/tags.csv', header=0)

engine = create_engine('postgresql://postgres:postgres@db:5432/postgres')

links_df.to_sql('links', engine)
movies_df.to_sql('movies', engine)
ratings_df.to_sql('ratings', engine)
tags_df.to_sql('tags', engine)