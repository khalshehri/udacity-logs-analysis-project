import psycopg2

DBNAME = "news"


def query_db(view):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * from " + view)
    posts = c.fetchall()
    db.close()
    return posts


POP_ARTICLES = query_db(view='pop_articles')

for article in POP_ARTICLES:
    print(article[0] + ' -- ' + str(article[1]) + ' views')

    print('')


POP_AUTHORS = query_db(view='pop_authors')

for author in POP_AUTHORS:
    print(author[0] + ' -- ' + str(author[1]) + ' views')
