import psycopg2

DBNAME = "news"


def query_db(view):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * from " + view)
    posts = c.fetchall()
    db.close()
    return posts


POP_ARTICLES = query_db(view='most_popular_articles')

for article in POP_ARTICLES:
    print(article[0] + ' -- ' + str(article[1]) + ' views')
