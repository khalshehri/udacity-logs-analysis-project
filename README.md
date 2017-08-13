Query to get most read articles

CREATE VIEW most_popular_articles AS
  SELECT articles.title, COUNT(log.path) AS views
    FROM articles LEFT JOIN log
    ON '/article/' || articles.slug = log.path
    GROUP BY articles.title
    ORDER BY views desc;