import pandas as pd
import os
import sqlite3

from requests import *

DATA_FOLDER = 'data'
DATA_FILE_NAME = 'ИсходныеДанныеИПримерыОтчетов.xlsx'
DATA_SHEET_NAME = 'Исходные данные'
RESULT_FOLDER = 'result'
DB_FILE = 'db_file.db'
COLUMNS_TO_RENAME = {'Склад': 'store', 'ДатаКлюч': 'sale_date', 'Продажи рублей': 'sales'}
SQL_SALES_TABLE_NAME = 'sales'

source_data_path = os.path.join(os.getcwd(), DATA_FOLDER, DATA_FILE_NAME)
db_path = os.path.join(os.getcwd(), RESULT_FOLDER, DB_FILE)


def main():
    df = pd.read_excel(source_data_path, sheet_name=DATA_SHEET_NAME)
    df.rename(columns=COLUMNS_TO_RENAME, inplace=True)
    create_db_file()
    add_data_to_db(df)


def create_db_file() -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(drop_table_sales)
    cursor.execute(drop_table_calendar)
    cursor.execute(create_sales_table)
    cursor.execute(create_calendar_table)
    cursor.execute(add_dates_in_calendar)
    connection.commit()
    connection.close()


def add_data_to_db(df: pd.DataFrame) -> None:
    connection = sqlite3.connect(db_path)
    df.to_sql(SQL_SALES_TABLE_NAME, connection, if_exists='append', index=False)
    connection.close()


if __name__ == '__main__':
    main()
