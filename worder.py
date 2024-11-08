from collections.abc import Iterable
from typing import Optional
import sqlite3


# TODO write docs
class WordAcessor:
    def __init__(self, db_name: str) -> None:
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.create()

    def __del__(self) -> None:
        self.con.close()

    def __len__(self) -> int:
        return self.count()

    def create(self, table_name: str = "word_table") -> None:
        query = (f"CREATE TABLE IF NOT EXISTS {table_name} "
                 "(word TEXT(32), translation TEXT(32), repeats INTEGER, "
                 "UNIQUE (word), UNIQUE(translation));")
        self.table_name = table_name
        self.cur.execute(query)

    def insert(self, words: Iterable) -> None:
        if not isinstance(words, Iterable):
            raise TypeError(f'can only insert iterable, not {type(words).__name__}')
        self.cur.executemany("INSERT OR IGNORE INTO "
                             f"{self.table_name} VALUES "
                             "(?, ?, ?)", words)
        self.con.commit()

    def getall(self) -> Iterable:
        return self.cur.execute(
                f"SELECT * FROM {self.table_name} ORDER BY repeats")

    def count(self) -> int:
        return tuple(
                self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
                )[0][0]

    def increment(self, words: Iterable) -> None:
        for word in words:
            self.cur.execute(
                    f"UPDATE {self.table_name} SET repeats = repeats + 1"
                    " WHERE word = ?", (word,))
            self.con.commit()

    def reset(self, words: Iterable) -> None:
        for word in words:
            self.cur.execute(
                    f"UPDATE {self.table_name} SET repeats = 0"
                    " WHERE word = ?", (word,))
            self.con.commit()
