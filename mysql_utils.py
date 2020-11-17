import sqlite3
import time
from datetime import date, datetime, time
from typing import Union

import mysql.connector

def insert_database(path: str, table: str, data: dict):
    database = sqlite3.connect(path)
    keys = ', '.join(data.keys())
    holder = ', '.join(['?'] * len(data.keys()))
    command = f'insert into {table} ({keys}) values ({holder})'
    values = list(data.values())
    try:
        database.execute(command, values)
    except Exception as error:
        print(error)
    database.commit()
    database.close()


def auto_insert_database(config: dict,
                         data: dict,
                         table: Union[str, None] = None):
    data = key_to_lower(data)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    # check table
    table_query = "show tables"
    cursor.execute(table_query)
    tables = set(cursor)
    if (table,) not in tables:
        auto_create_table(cursor, data, table)
    # check column
    else:
        column_query = f'desc `{table}`'
        cursor.execute(column_query)
        columns = set(map(lambda c: c[0].lower(), cursor))
        keys = set(data.keys())
        diff = keys - columns
        len_diff = len(diff)
        if len_diff > 0:
            auto_add_column(cursor, diff, data, table)
    # insert data
    keys = ', '.join(map(lambda k: f'`{k}`', data.keys()))
    holder = ', '.join(map(lambda k: f'%({k})s' if data[k] is not None else 'null', data.keys()))
    insert_query = f'insert into `{table}` ({keys}) values ({holder})'
    data = convert_unknown_type_to_str(data)
    cursor.execute(insert_query, data)
    cnx.commit()
    cursor.close()
    cnx.close()


def key_to_lower(data: dict):
    new_dict = {}
    for k, v in data.items():
        new_dict[k.lower()] = v
    return new_dict


def convert_unknown_type_to_str(data: dict):
    new_dict = {}
    for k, v in data.items():
        if v is None:
            continue
        new_dict[k] = str(v) if convert_type(type(v)) == 'text' else v
    return new_dict


def convert_type(python_type: type) -> str:
    if python_type == int:
        mysql_type = 'int'
    elif python_type == float:
        mysql_type = 'double'
    elif python_type == str:
        mysql_type = 'text'
    elif python_type == bool:
        mysql_type = 'boolean'
    elif python_type == date:
        mysql_type = 'date'
    elif python_type == datetime:
        mysql_type = 'datetime'
    elif python_type == time:
        mysql_type = 'time'
    else:
        mysql_type = 'text'
    return mysql_type


def auto_create_table(cursor, data: dict, table: str):
    field_defines = ','.join(map(lambda item: f'`{item[0]}` {convert_type(type(item[1]))} null', data.items()))
    create_query = f"create table `{table}`(`table_no` int NOT NULL AUTO_INCREMENT, {field_defines}, " \
                   f"PRIMARY KEY (`table_no`))"
    cursor.execute(create_query)


def auto_add_column(cursor, diff_keys: set, data: dict, table: str):
    add_query = "alter table `{}` add `{}` {} null"
    for key in diff_keys:
        cursor.execute(add_query.format(table, key, convert_type(type(data[key]))))


def get_table_count(config: dict, table: str):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    # check table
    table_query = f"select max(`table_no`) from `{table}`"
    cursor.execute(table_query)
    count = list(cursor)[0]
    cursor.close()
    cnx.close()
    return count


def query_table_where_table_no_greater_than(config: dict, table: str, table_no: int):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = f"select * from `{table}` where `table_no` > {table_no}"
    cursor.execute(query)
    result = list(cursor)
    cursor.close()
    cnx.close()
    return result
