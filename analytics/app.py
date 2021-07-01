#!/usr/bin/env python3

from flask import Flask
from flask import render_template

import psycopg2
import datetime

app = Flask(__name__)

try:
    connection = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="postgres")

    cursor = connection.cursor()

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

@app.template_filter('ctime')
def timectime(s):
    return datetime.datetime.fromtimestamp(s)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/1')
def get_all_movies_count():
    sql = """
        SELECT count(*) 
        FROM public.movies
    """
    
    cursor.execute(sql)

    row = cursor.fetchone()

    return render_template('1.html', question='1', count=row[0])

@app.route('/2')
def get_most_common_genres(N=1):
    sql = """
        SELECT "genre", count(*) as "count"
        FROM (
            SELECT unnest(string_to_array("genres", '|')) as "genre"
            FROM "public"."movies"
        ) m
        GROUP BY "genre"
        ORDER BY "count" desc
        LIMIT {}
    """.format(N)

    cursor.execute(sql)

    rows = cursor.fetchall()
    return render_template('2.html', question='2', rows=rows)

@app.route('/3')
def get_top_movies(N=10):
    sql = """
        SELECT "title", "score", "count"
        FROM (
            SELECT "movieId", avg("rating") as "score", count(*) as "count"
            FROM "public"."ratings"
            GROUP BY "movieId"
            HAVING count(*) >= 10
            ORDER BY "score" DESC
            LIMIT {}
        ) r 
        LEFT JOIN "public"."movies" m
        ON r."movieId" = m."movieId"
        ORDER BY "score" DESC
    """.format(N)

    cursor.execute(sql)

    rows = cursor.fetchall()
    return render_template('3.html', question='3', rows=rows)

@app.route('/4')
def get_most_rating_users(N=5):
    sql = """
        SELECT "userId", count(*) as "count"
        FROM "public"."ratings"
        GROUP BY "userId"
        ORDER BY "count" desc
        LIMIT {}
    """.format(N)

    cursor.execute(sql)

    rows = cursor.fetchall()
    return render_template('4.html', question='4', rows=rows)

def get_ratings(mode):
    sql = """
        SELECT "title", "timestamp"
        FROM "public"."ratings" r
        LEFT JOIN "public"."movies" m
        ON r."movieId" = m."movieId"
        WHERE "timestamp" = ( 
            SELECT {}("timestamp") 
            FROM "public"."ratings" 
        )
        ORDER BY "title"
    """.format(mode)

    cursor.execute(sql)

    return cursor.fetchall()

@app.route('/5')
def get_oldest_and_newest_ratings():
    oldest = get_ratings(mode='min')
    newest = get_ratings(mode='max')
    
    return render_template('5.html', question='5', oldest=oldest, newest=newest)

@app.route('/6', defaults={'year': 1990})
@app.route('/6/<year>')
def get_movies_by_year(year):
    sql = """
        SELECT "title"
        FROM "public"."movies"
        WHERE "title" LIKE '% ({})'
        ORDER BY "title"
    """.format(year)

    cursor.execute(sql)

    rows = cursor.fetchall()
    return render_template('6.html', question='6', year=year, rows=rows)
