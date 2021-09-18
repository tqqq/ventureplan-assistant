# coding=utf-8

import sqlite3
import datetime
from vp_manager.config.const import DB_PATH, FFR_UNKNOWN, FFR_NOT_SURE, TABLE_NAME
from vp_manager.utils.exceptions import VPException

"""
Table arrangement:  Arrangement and lowest health for each mission with 4+1
    id: primary key
    m_id: mission id
    m_level: mission level
    f_id: follower id
    f_level: follow level
    s_level: soldier level
    fail_health: below this health, must fail
    win_health: higher than this health, must win
    arrange: win arrangement, example: "1202x", 1:tank-soldier, 2: heal-soldier, x: the follower, 0: empty
"""

# TODO: insert, delete, select, update

conn = sqlite3.connect(DB_PATH)  # db connection


def get_win_arranges(mission, followers, s_level):
    """
        select * from arrangement where m_id=m_id and m_level=m_level and s_level=s_level and
        ((f_id=f[0].id and f_level=f[0].level) or (f_id=f[1].id and f_level=f[1].level))

    """
    m_id, m_level = mission['id'], mission['level']

    sub_judge = ' OR '.join([f'(f_id={fl["id"]} and f_level={fl["level"]})' for fl in followers])

    sql_str = f'''SELECT * FROM arrangement WHERE m_id={m_id} and m_level={m_level} AND s_level={s_level} AND ''' + \
              f'''({sub_judge})'''
    cursor = conn.cursor()
    cursor.execute(sql_str)
    results = cursor.fetchall()
    cursor.close()
    for r in results:
        print(r)

    return []


def update_arrangement(mission, follower, s_level):
    m_id, m_level = mission['id'], mission['level']
    f_id, f_level, f_health = follower['id'], follower['level'], follower['health']
    arrange, status = follower['arrangement'] or '', follower['status']

    win_health, fail_health = 10000, 0
    if not arrange:
        fail_health = f_health
    else:
        win_health = f_health

    if status == FFR_UNKNOWN:
        insert_sql = f'''INSERT INTO {TABLE_NAME} VALUES (null, {m_id}, {m_level}, {f_id}, {f_level}, ''' + \
                     f'''{s_level}, {fail_health}, {win_health}, '{arrange}')'''
        sql_str = insert_sql
    elif status == FFR_NOT_SURE:
        update_str = f'win_health={win_health}, arrange=\'{arrange}\'' if arrange else f'fail_health={fail_health}'
        update_sql = f'''UPDATE {TABLE_NAME} SET {update_str} WHERE m_id={m_id} AND ''' + \
                     f'''m_level={m_level} AND f_id={f_id} AND f_level={f_level} AND s_level={s_level}'''
        sql_str = update_sql
    else:
        raise VPException(f'wrong follower status: {status}')
    cursor = conn.cursor()
    cursor.execute(sql_str)
    cursor.close()
    conn.commit()
    # TODO: log


def _test_db():
    mission = {
        'id': 110,
        'level': 48
    }

    follower_1 = {  # 增加一条记录：500血以上必胜
        'id': 210,
        'level': 47,
        'health': 500,
        'arrangement': '121x1',
        'status': FFR_UNKNOWN
    }

    follower_2 = {  # 更新一条记录，300血以上必胜，更新阵容
        'id': 210,
        'level': 47,
        'health': 300,
        'arrangement': '111x2',
        'status': FFR_NOT_SURE
    }
    follower_3 = {  # 更新一条记录， 215血以下必败
        'id': 210,
        'level': 47,
        'health': 215,
        'arrangement': '',
        'status': FFR_NOT_SURE
    }

    sql_str = '''SELECT * FROM arrangement'''
    # update_arrangement(mission, follower_1, s_level='45')
    # update_arrangement(mission, follower_2, s_level='45')
    update_arrangement(mission, follower_3, s_level='45')

    cursor = conn.cursor()
    cursor.execute(sql_str)
    results = cursor.fetchall()
    cursor.close()
    for r in results:
        print(r)


# if __name__ == '__main__':
#     _test_db()

