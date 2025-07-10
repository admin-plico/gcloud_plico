import sqlite3
import os
db_path = os.getcwd()
conn = sqlite3.connect(os.path.join(db_path, 'db_pr.sqlite'))
cur = conn.cursor()

"""
to keep a record of the last image number the database must store the containing folder name as unique
store the last number ain add 1 to cout column each time it processes an image from that folder
"""


def instantiate_image_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS last_serial (
            id INTEGER PRIMARY KEY,
            project TEXT UNIQUE,
            last_id INTEGER
            )
        """)
    conn.commit()


def new_project(project_name):
    cmd = f'''INSERT OR IGNORE INTO last_serial(
     project,
     last_id
     )
     VALUES (?, ?)'''
    val = (project_name, 0)
    cur.execute(cmd, val)
    conn.commit()
    return 0


def set_last_id(project_name, last_id):
    cmd = "UPDATE last_serial SET last_id=? WHERE project=?"
    values = (last_id, project_name)
    cur.execute(cmd, values)
    conn.commit()


def get_last_id(project_name):
    cmd = F'SELECT last_id  FROM last_serial WHERE project=?'
    cur.execute(cmd, (project_name,))
    value = cur.fetchone()
    if value:
        last_id = value[0]
    else:
        last_id = new_project(project_name)
    return last_id


def return_last_and_update(project_name):
    last_id = get_last_id(project_name)
    next_id = last_id + 1
    set_last_id(project_name, next_id)
    return next_id

