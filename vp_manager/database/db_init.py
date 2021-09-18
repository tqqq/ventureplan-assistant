# coding=utf-8
import os
import sqlite3

from vp_manager.config.const import TABLE_NAME


def init_db():
    conn = sqlite3.connect('venture_plan.sqlite')

    cur = conn.cursor()
    cur.execute(
        f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id bigint primary key, m_id int, m_level int, f_id int, f_level int, ''' +
        '''s_level int, fail_health int, win_health int, arrange char(20), update_time date)''')
    cur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
