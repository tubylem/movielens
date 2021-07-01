# Data Engineer Aptitude Test

## Motivation
The solution was made for the purpose of recruitment.

## Description of the task
The task is to simulate situation when you run some data transformations based on data stored in different environment than your transformation script runs.

### To achieve this please follow below steps:

1. Create two docker containers  - one with configured relational database and second from which you‘ll run your data transformations in your preferable programming language.
2. Prepare docker compose that allows to run such setup.
3. Download an appropriate publicly available, non-commercial data set form (https://grouplens.org/datasets/movielens/latest/  ml-latest-small.zip) and import it to your database.

## Description of the solution

The solution contains three containers:

1. The relational database to store data
2. The process to load data from `CSV` files to database
3. The web application to share outputs

### Database (db)
I have chosen the open-source `PostgresSQL` database, because the authors of the project claim it is "The World's Most Advanced Open Source Relational Database", but every relational database should be sufficient for this task.

### Database initial load (db-load)
The initial process of loading data has been created in a separate container, which runs when the database is ready for accepting new connections. 

The `Python` script was used to read data from `CSV` files and put all records to the database.

* For reading data from CSV files the `pandas` library was used.
* For writing data to the database the `sqlalchemy` library was used.

It was not necessary to explicitly specify the database structure, but of course in the production solution it is most advisable.

### Sharing the results (analytics)
A Flask application has been created to answer the questions asked.

The answers are generated in real time and some of them are parametrized.

To access the database `PostgresSQL` the `psycopg2` library was used.

## Prerequisites
* The access to the Internet is required to pull `docker` images and download the movielens `CSV` files. 
* Docker engine
* Docker compose

## How to run it?
To run the solution, you need to type in the terminal or the command line:

    git clone https://github.com/tubylem/movielens.git
    cd movielens
    docker-compose up

## How to use it?
Open the web browser [http://localhost:5000/](http://localhost:5000/)

All questions should be shown. 

If you want to find out the answer, click on the specific question.

## To do list
* Unit tests
* Pull database credentials from the repository
* Check if tables already exist or remove tables before initial load
* Specify correct primary keys in tables