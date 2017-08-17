"""
This is the third project in Udacity's Full Stack Web Developer Nanodegree.
When running the python file you will be presented with the result from three
different database queries:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors
"""
import psycopg2

DBNAME = "news"


def query_db(db_name, view):
    """
    Opens a database connection and queries it with a pre defined view.
    """
    database = psycopg2.connect(database=db_name)
    cursor = database.cursor()
    cursor.execute("SELECT * from " + view)
    posts = cursor.fetchall()
    database.close()
    return posts


def create_headline(text):
    """
    Creates a tacky headline witch a lot of stars surrounding it.
    Why tacky? Because it's eye catching!
    """
    text = ('** ' + text + ' **').upper()
    return ('*' * len(text)) + '\n' + text + '\n' + ('*' * len(text))


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

    return d.strftime('%B %d' + suffix + ', %Y')


print(create_headline('What are the most popular three articles of all time?'))
POP_ARTICLES = query_db(db_name=DBNAME, view='pop_articles')
for article in POP_ARTICLES:
    print(article[0] + ' -- ' + str(article[1]) + ' views')

print('\n')
print(create_headline('Who are the most popular article authors of all time?'))
POP_AUTHORS = query_db(db_name=DBNAME, view='pop_authors')
for author in POP_AUTHORS:
    print(author[0] + ' -- ' + str(author[1]) + ' views')

print('\n')
print(create_headline(
    'On which days did more than 1% of requests lead to errors?'))
OVER_1_PERCENT_ERRORS = query_db(db_name=DBNAME, view='one_percent_errors')
for errors in OVER_1_PERCENT_ERRORS:
    d = errors[0]
    print(get_formated_date(d) + ' -- ' + str(errors[1]) + '% errors')
