-- This file is a temporary notebook for storing queries.
-- TODO: delete when project is solved


-- Finds # logs with error code >= 400:
SELECT date(time) AS log_date,
       count(time) AS num_errors
FROM log
WHERE to_number(substr(status, 1, 3), '999') >= 400
GROUP BY log_date;

-- Returns total count of logs for each day
SELECT date(time) AS log_date,
       count(time) AS num_logs
FROM log
GROUP BY log_date;

-- Not working yet, but we're getting somewhere..
SELECT log_date, round((100. * err.num_logs / normal.num_logs)::numeric,1) AS err_percent
FROM (
    SELECT date(time) AS log_date, count(time) AS num_logs
    from log
    GROUP BY log_date
) AS normal 
LEFT JOIN (
    SELECT date(time) AS log_date,
    count(time) AS num_logs
    FROM log
    WHERE to_number(substr(status, 1, 3), '999') >= 400
    GROUP BY log_date
) AS err USING (log_date);



-- Almost done
SELECT log_date, ROUND((100. * err.num_logs / normal.num_logs)::NUMERIC,1) AS err_percent
FROM (
    SELECT date(time) AS log_date, count(time) AS num_logs
    from log
    GROUP BY log_date
) AS normal 
LEFT JOIN (
    SELECT date(time) AS log_date,
    count(time) AS num_logs
    FROM log
    WHERE to_number(substr(status, 1, 3), '999') >= 400
    GROUP BY log_date
) AS err USING (log_date);


-- select time::date as date, 
-- sum(case when to_number(substr(status, 1, 3), '999' then 1) >= 400) as err,
-- count(*) as total
-- from log
-- group by date;

-- (err / total)

WITH x AS (
    SELECT date(time) AS log_date, sum(case when status like '%404%' then 1 else 0 end) as errs
    from log
    group by log_date
),
y AS (
    SELECT date(time) AS log_date, count(*) as total
    from log
    group by log_date
),
z AS (
    SELECT ((x.errs * 100.) / y.total) as percent, y.log_date as log_date
    from y join x USING (log_date)
)
SELECT z.log_date, z.percent from z WHERE (z.percent > 1);