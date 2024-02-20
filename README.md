# Тестовое задание на разработчика BI

Для выполнения задания решил воспользоваться SQLite. Скрипт в файле `main.py` читает файл с исходными данными, создаёт файл с базой данных, создаёт в ней необходимые таблицы и сохраняет в эти таблицы данные. Скрипт удаляет таблицы, если они были ранее созданы, т. е. перзаписывает данные в БД при каждом запуске. В `report.xlsx` настроен путь к файлу БД (с помощью ODBC драйвера) на моем локальном ПК и написаны SQL запросы (продублировал в этом файле ниже).

Исходные данные и текст задания находятся в папке `data`.

Итоговый файл БД SQLite и отчет в формате Excel находятся в папке `result`.

Использовал `Python 3.11`, `pandas 2.2`, `openpyxl 3.1.2` (см. `pyproject.toml`).

### SQL

#### Отчет по дням

```sql
with cur_sales as (
    select *
    from sales
    inner join calendar on date(sales.sale_date) = calendar.d
),

lm_sales as (
    select *
    from sales
    inner join calendar on date(sales.sale_date) = calendar.last_month_d
),

ly_sales as (
    select *
    from sales
    inner join calendar on date(sales.sale_date) = calendar.last_year_d
)

select 
    case 
        when (cs.store is null and lys.store is null) then lms.store 
        when (cs.store is null and lms.store is null) then lys.store 
        else cs.store 
    end store,
    case 
        when (cs.d is null and lys.d is null) then lms.d 
        when (cs.d is null and lms.d is null) then lys.d 
        else cs.d 
    end d,
    cs.sales cur_sales,
    lys.sales ly_sales,
    lms.sales lm_sales
from cur_sales cs
full join lm_sales lms on cs.d = lms.d and cs.store = lms.store
full join ly_sales lys on cs.d = lys.d and (cs.store = lys.store or lms.store = lys.store)
order by 1, 2
```

#### Отчет по месяцам

```sql
with grouped_sales as (
	select date(c.d, 'start of month') m, s.store, sum(s.sales) sales
	from sales s 
	join calendar c on date(s.sale_date) = c.d 
	group by s.store, date(c.d, 'start of month')
),
months as (
	select distinct date(c.d, 'start of month') m
	from calendar c
),
stores as (
	select distinct store from grouped_sales
),
months_stores as (
	select *
	from months, stores
)
select 
	ms.store, 
	strftime('%Y', ms.m) year,
	strftime('%m', ms.m) month,
	gs1.sales cur_sales, 
	gs2.sales ly_sales, 
	gs3.sales lm_sales
from months_stores ms
left join grouped_sales gs1 on ms.m = gs1.m and ms.store = gs1.store
left join grouped_sales gs2 on date(ms.m, '-1 year') = gs2.m and ms.store = gs2.store
left join grouped_sales gs3 on date(ms.m, '-1 month') = gs3.m and ms.store = gs3.store
where not (gs1.sales is null and gs2.sales is null and gs3.sales is null)
order by ms.store, ms.m
```