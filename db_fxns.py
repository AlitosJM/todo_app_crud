import sqlite3
# https://stackoverflow.com/questions/393554/python-sqlite3-and-concurrency
# https://python-forum.io/Thread-Error-SQLite-objects-created-in-a-thread-can-only-be-used-in-that-same-thread

conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

# Database
# Table
# Field/beta_columns
# DataType


def create_table(table='tasktable'):
    c.execute(
        f'CREATE TABLE IF NOT EXISTS {table}(task TEXT, task_status TEXT, task_due_date DATE)')


def add_data(task, task_status, task_due_date):
    c.execute('INSERT INTO tasktable(task, task_status, task_due_date) VALUES (?,?,?)',
              [task, task_status, task_due_date])
    conn.commit()


def view_all_data(table='tasktable'):
    c.execute(f'SELECT * FROM {table}')
    data = c.fetchall()
    return data


def view_unique_column(table='tasktable', column='task'):
    c.execute("SELECT DISTINCT {0} FROM {1}".format(column, table))
    return c.fetchall()


def get_tasks(task):
    c.execute('SELECT * FROM tasktable WHERE task="{0}"'.format(task))
    # c.execute('SELECT * FROM tasktable WHERE task=?', (task))
    data = c.fetchall()
    return data


def edit_task_data(new_task, new_task_status, new_task_date, task, task_status, task_due_date):
    c.execute("UPDATE tasktable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",
              (new_task, new_task_status, new_task_date, task, task_status, task_due_date))
    conn.commit()
    data = c.fetchall()
    return data


def delete_data(task):
    c.execute('DELETE FROM tasktable WHERE task="{}"'.format(task))
    conn.commit()
