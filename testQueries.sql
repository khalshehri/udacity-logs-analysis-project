-- This file is a temporary notebook for storing queries.
-- TODO: delete when project is solved


-- Finds # logs with error code >= 400:
SELECT date(time) AS log_date, count(time) AS num_errors
  FROM log 
  WHERE to_number(substr(status, 1, 3), '999') >= 400
  GROUP BY log_date;

-- Returns total count of logs for each day
SELECT date(time) AS log_date, count(time) AS num_logs 
  FROM log GROUP BY log_date;
