import psycopg2

DBNAME = "news"


def query_db(view):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * from " + view)
    posts = c.fetchall()
    db.close()
    return posts

def create_headline(text):
    text = ('** ' + text + ' **').upper()
    return ('*' * len(text)) + '\n' + text + '\n' + ('*' * len(text))


print(create_headline('What are the most popular three articles of all time?'))
POP_ARTICLES = query_db(view='pop_articles')
for article in POP_ARTICLES:
    print(article[0] + ' -- ' + str(article[1]) + ' views')

print('\n')
print(create_headline('Who are the most popular article authors of all time?'))
POP_AUTHORS = query_db(view='pop_authors')
for author in POP_AUTHORS:
    print(author[0] + ' -- ' + str(author[1]) + ' views')

print('\n')
print(create_headline('On which days did more than 1% of requests lead to errors?'))
print('Not yet implemented...')
