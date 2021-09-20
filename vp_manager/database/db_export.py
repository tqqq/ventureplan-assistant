# coding=utf-8
import os
import sqlite3
import csv

from vp_manager.config.const import TABLE_NAME


def export_db():
    conn = sqlite3.connect('venture_plan.sqlite')

    sql_str = f'''select * from {TABLE_NAME}'''


    try:
        cursor = conn.cursor()
        cursor.execute(sql_str)
        results = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(str(e))
        return []

    with open('data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(results)



if __name__ == '__main__':
    export_db()
