import sqlite3

def create():
    try:
        c.execute("""CREATE TABLE mytable
                 (start, end, score)""")
    except:
        pass

def insert():
    c.execute("""INSERT INTO mytable (start, end, score)
              values(1, 99, 123)""")

def select(verbose=True):
    sql = "SELECT * FROM mytable"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print row

db_path = 'db.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
create()
insert()
conn.commit() #commit needed
select()
c.close()