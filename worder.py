from collections.abc import Iterable
import sqlite3


class WordAcessor:
    def __init__(self, db_name: str, create_table: bool = True):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        if create_table:
            self.create()

    def __del__(self):
        self.con.close()
        self.cur = None

    def create(self, table_name: str = "word_table"):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} \
        (word TEXT(32), translation TEXT(32), repeats INTEGER, \
        UNIQUE (word), UNIQUE(translation));"
        self.table_name = table_name
        self.cur.execute(query)

    def insert(self,
               words: Iterable,
               flush: bool = True) -> bool:
        if not isinstance(words, Iterable):
            return False
        self.cur.executemany(f"INSERT OR IGNORE INTO \
                {self.table_name} VALUES \
                (?, ?, ?)", words)
        if flush:
            self.con.commit()
        return True

    def getall(self) -> Iterable:
        return self.cur.execute(f"SELECT * FROM {self.table_name} \
                ORDER BY repeats")
