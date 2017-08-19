#!/usr/bin/env python3

"""
This is the third project in Udacity's Full Stack Web Developer Nanodegree.
When running the python file you will be presented with the result from three
different database queries:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors
"""
import sys
from datetime import date

import psycopg2


def print_info(database_name, queries):
    """
    Creates a database connection and prints information based on view queries
    """
    database, cursor = database_connect(database_name=database_name)

    for idx, query in enumerate(queries):
        print_query(cursor=cursor, query=query)
        if idx + 1 != len(queries): # Add a line separator if not the last item
            print('\n')

    database_disconnect(database=database, cursor=cursor)


def database_connect(database_name):
    """
    Connect to the PostgreSQL database.
    Returns a database connection.
    """
    try:
        database = psycopg2.connect(database=database_name)
        cursor = database.cursor()
        return database, cursor
    except psycopg2.Error as err:
        print("Unable to connect to database. Exiting ...")
        print(err)
        sys.exit(1)


def database_disconnect(database, cursor):
    """
    Close cursor and database connections
    """
    if not cursor.closed:
        cursor.close()
    if database.closed != 0:
        database.close()


def fetch_query(cursor, view):
    """
    Open a database connection and queries it with a pre defined view.
    Returns all database rows from view query.
    """
    cursor.execute("SELECT * from " + view)
    posts = cursor.fetchall()
    return posts


def get_formated_date(date_to_format):
    """
    Returns a formated date containg day of month suffix (th, st, nd...)
    """
    # Solution based on
    # https://stackoverflow.com/questions/739241/date-ordinal-output
    day = date_to_format.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = ['st', 'nd', 'rd'][day % 10 - 1]

    return date_to_format.strftime('%B %d' + suffix + ', %Y')


def print_query(cursor, query):
    """
    Prints query results
    """
    print(query.headline())

    results = fetch_query(cursor=cursor, view=query.view)
    for result in results:
        title = result[0]
        value = result[1]

        if isinstance(title, date):
            title = get_formated_date(title)

        print("%s -- %s %s" % (title, value, query.suffix))


class Query:
    """
    Creates an query object
    """

    def __init__(self, question, view, suffix):
        self.question = question
        self.view = view
        self.suffix = suffix

    def headline(self):
        """
        Creates a tacky headline witch a lot of stars surrounding it.
        Why tacky? Because it's eye catching!
        """
        capitalized = self.question.upper()
        text = "** %s **" % capitalized
        top_and_bottom = "*" * len(text)
        headline = "%s\n%s\n%s" % (top_and_bottom, text, top_and_bottom)
        return headline


if __name__ == '__main__':
    DBNAME = "news"
    QUERIES = [
        Query(
            question="What are the most popular three articles of all time?",
            view="pop_articles",
            suffix="views"
        ),
        Query(
            question="Prints the most popular article authors of all time",
            view="pop_authors",
            suffix="views"
        ),
        Query(
            question="On which days did more than 1% of requests " +
            "lead to errors?",
            view="one_percent_errors",
            suffix="% errors"
        )]

    print_info(database_name=DBNAME, queries=QUERIES)
