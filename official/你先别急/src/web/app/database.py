import sqlite3
from secret import flag_func
import resource
import json

ORIGINAL_DATABASE = "./data.db"

def main(token, sqlexp):
    source = sqlite3.connect(ORIGINAL_DATABASE)
    dest = sqlite3.connect(":memory:")
    source.backup(dest)
    source.close()

    # limitation
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    resource.setrlimit(resource.RLIMIT_AS, (8 * 1024 * 1024, 8 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))

    flag = flag_func(token)
    dest_cur = dest.cursor()
    dest_cur.execute("INSERT INTO flag VALUES (?)", (flag,))
    dest.commit()
    res = dest_cur.execute(sqlexp)
    res = res.fetchone()
    if not res:
        print("\"x\"")
    else:
        print(json.dumps(res[0])[:8192])

    dest.close()


if __name__ == "__main__":
    # trust user input here
    token = input()
    sqlexp = input()
    main(token, sqlexp)
