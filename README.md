# Logs Analysis Project
This is the third project in Udacity's Full Stack Web Developer Nanodegree.

When running the python file you will be presented with the result from three different database queries:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors

Open output_example.txt to see a dump of the expected output after running log_analysis.py.

# Setup
## Software
Make sure the software listed beneath is installed on your computer.

[Python 3.6.x](https://www.python.org/downloads/)

[PostgreSQL 9.6.x](https://www.postgresql.org/download/)

## Test data
Download and unzip [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). 
Build the database by running ```psql -d news -f newsdata.sql```

## Views
The Python code does not build queries itself, rather it relies on views. These views has to be pre generated before running the code.
To load the views you have to start psql in the news database:
```
psql -d news
```
Then start loading the views by running the commands listed under.

### View used for solving "What are the most popular three articles of all time?"
```
CREATE VIEW pop_articles AS
SELECT articles.title,
       COUNT(log.path) AS views
FROM articles
LEFT JOIN log ON '/article/' || articles.slug = log.path
GROUP BY articles.title
ORDER BY views DESC
LIMIT 3;
```

### View used for solving "Who are the most popular article authors of all time?"
```
CREATE VIEW pop_authors AS
SELECT authors.name,
       article_author.views
FROM authors,
  (SELECT articles.author,
          COUNT(log.path) AS views
   FROM articles
   LEFT JOIN log ON '/article/' || articles.slug = log.path
   GROUP BY articles.author
   ORDER BY views DESC) AS article_author
WHERE article_author.author = authors.id;
```

### View used for solving "On which days did more than 1% of requests lead to errors?"
```
CREATE VIEW one_percent_errors AS WITH
NORMAL AS
  (SELECT date(TIME) AS log_date,
          COUNT(*) AS day_logs
   FROM log
   GROUP BY log_date), errors AS
  (SELECT DATE(TIME) AS log_date,
          COUNT(TIME) AS day_error_logs
   FROM log
   WHERE to_number(substr(status, 1, 3), '999') >= 400
   GROUP BY log_date),
                       calc AS
  (SELECT ((errors.day_error_logs * 100.) / normal.day_logs) AS percent,
          normal.log_date AS log_date
   FROM
   NORMAL
   JOIN errors USING (log_date))
SELECT calc.log_date,
       ROUND(calc.percent::NUMERIC,1)
FROM calc
WHERE (calc.percent > 1);
```

# How to run the application

Here's a couple of alternatives on how to run the application.

## Using command prompt

### cd into the project folder
Open a command prompt and navigate to the udacity-logs-analysis-project folder

### Run the application
Type

```
python log_analysis.py
```

## Using the Python IDLE
* File --> Open...
* Navigate to log_analysis.py
* Press Ok

A new windows pops up, in that window:
* Select Run --> Run Module
