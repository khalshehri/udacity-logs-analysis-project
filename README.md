Query to get most read articles

CREATE VIEW pop_articles AS
  SELECT articles.title, COUNT(log.path) AS views
    FROM articles LEFT JOIN log
    ON '/article/' || articles.slug = log.path
    GROUP BY articles.title
    ORDER BY views desc;


CREATE VIEW pop_authors AS
  SELECT authors.name, article_author.views
    FROM authors,
    (SELECT articles.author, COUNT(log.path) AS views
        FROM articles LEFT JOIN log
        ON '/article/' || articles.slug = log.path
        GROUP BY articles.author
        ORDER BY views desc) article_author
    WHERE article_author.author = authors.id;




SELECT * FROM log WHERE to_number(substr(status, 1, 3), '999') >= 400;