import os.path
import sqlite3
from typing import Dict


class mydb:
    dbfile = None
    conn = None
    LOG = None
    initDB = False

    def __init__(self, path: str, logger) -> None:
        self.dbfile = path
        self.LOG = logger

        if not os.path.isfile(self.dbfile):
            self.initDB = True
            self.LOG.warning(f"No such database file {self.dbfile}, will need to initialize tables")

        try:
            self.LOG.debug(f"Connecting to db {self.dbfile}")
            self.conn = sqlite3.connect(path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            if self.initDB:
                logger.info("Initializing empty DBS")
                c = self.conn.cursor()
                c.execute('''
                             CREATE TABLE PWDS
                             ([generated_id] INTEGER primary key autoincrement,
                              [entity_name] text,
                              [entity_username] text,
                              [password] text,
                              [ticket] text,
                              [date] date);                             
                            ''')
            self.LOG.debug("Connected to DB.")
        except Exception as e:
            self.LOG.error(e)
            self.LOG.critical(f"Exception when opening file {self.dbfile}")

    def getallpwds(self):
        self.LOG.debug("Getting all pwds")
        cur = self.conn.cursor()
        cur.execute("select * from pwds where deleted <> 1")
        rows = cur.fetchall()
        return rows

    def deletpwd(self, current_id: int):
        cur = self.conn.cursor()
        try:
            cur.execute("update pwds set deleted=1 where generated_id = ?", (current_id,))
            self.conn.commit()
        except Exception as e:
            self.LOG.error(e)
            self.LOG.critical(f"Exception when finding pwd {self.dbfile}")
            self.LOG.critical(e)


    def findbyid(self, current_id: int) -> Dict:
        self.LOG.debug(f"Looking for pwd with id: {current_id}")

        cur = self.conn.cursor()
        try:
            cur.execute("select * from pwds where generated_id = ?", (current_id,))
            rows = cur.fetchall()
            res = {"generated_id": rows[0][0],
                    "entity_name": rows[0][1],
                    "entity_username": rows[0][2],
                    "password": rows[0][3],
                    "ticket": rows[0][4],
                    "date": rows[0][5]}
            return res
        except Exception as e:
            self.LOG.error(e)
            self.LOG.critical(f"Exception when finding pwd {self.dbfile}")
            self.LOG.critical(e)

    def AddInfo(self, entity_name: str, entity_username: str, password: str, ticket: str, generated_id: int) -> None:
        self.LOG.debug(f"Adding pwd for {entity_name}: {entity_username}")
        cur = self.conn.cursor()
        try:
            if generated_id is None:
                cur.execute(
                    "insert into pwds (entity_name, entity_username, password, ticket, date) values (?, ?, ?, ?, "
                    "DateTime('now'))",
                    (entity_name, entity_username, password, ticket))
                self.conn.commit()
                self.LOG.success("Added")
            else:
                self.LOG.debug(f"Updating info for {generated_id}")
                # TODO ADD UPDATE

        except Exception as e:
            self.LOG.error(e)
            self.LOG.critical(f"Exception when adding pwd {self.dbfile}")
            self.LOG.critical(e)
