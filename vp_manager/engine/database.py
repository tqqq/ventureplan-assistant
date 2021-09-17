# coding=utf-8

import sqlite3

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
    update_time: 
"""


# TODO: insert, delete, select, update

conn = None  # db connection


def get_win_arranges(m_id, m_level, followers, s_level):
    """
        select * from arrangement where m_id=m_id and m_level=m_level and s_level=s_level and
        ((f_id=f[0].id and f_level=f[0].level) or (f_id=f[1].id and f_level=f[1].level))

    """

    return []


def get_win_arrange(m_id, m_level, f_id, f_level, s_level):
    record = (1, 1, 47, 1, 47, 47, 123, 999, '1201x', '2021-01-01')
    return [record]


def update_arrangement(m_id, m_level, f_id, f_level, s_level, f_health, arrange):
    # TODO: update in new thread
    pass
