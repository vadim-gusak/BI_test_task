drop_table_sales = '''
DROP TABLE IF EXISTS sales;
'''

drop_table_calendar = '''
DROP TABLE IF EXISTS calendar;
'''


create_sales_table = '''
CREATE TABLE IF NOT EXISTS sales (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    store     TEXT,
    sale_date DATE,
    sales     REAL
);
'''


create_calendar_table = '''
CREATE TABLE IF NOT EXISTS calendar (
  d date UNIQUE NOT NULL,
  last_month_d date UNIQUE,
  last_year_d date UNIQUE
);
'''

add_dates_in_calendar = '''
INSERT INTO calendar (d, last_month_d, last_year_d)
SELECT *
FROM (
  WITH RECURSIVE dates(d) AS (
    VALUES('2010-01-01')
    UNION ALL
    SELECT date(d, '+1 day')
    FROM dates
    WHERE d < '2020-01-01'
  )
  SELECT 
      d,
      case when strftime('%m', date(d, '-1 month')) = strftime('%m', d) then null else date(d, '-1 month') end last_month_d,
      case when strftime('%m', date(d, '-1 year')) <> strftime('%m', d) then null else date(d, '-1 year') end last_year_d
  FROM dates
);
'''
