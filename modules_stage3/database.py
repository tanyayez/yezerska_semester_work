import sqlite3
class Database:
    def __init__(self, dbname):
        '''
        Initialize new database
        '''
        self.dbname = dbname

    def new_fill(self, catg, total):
        '''
        Update total value of certain category
        '''
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        c.execute('SELECT total FROM categories WHERE category=?', (catg,))
        old = c.fetchone()
        new = old[0] + total
        c.execute('''UPDATE categories SET total = ? WHERE category = ?''', (new, catg))
        conn.commit()
        conn.close()

    def new_entry(self, lst):
        '''
        Add new item to db
        '''
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        c.executemany('INSERT INTO data VALUES (?,?,?,?)', (lst,))
        conn.commit()
