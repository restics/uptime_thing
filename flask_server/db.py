from dataclasses import dataclass
import sqlite3
from logger import logger
@dataclass
class Card:
    id : int
    name : str
    url : str
    description : str = ""
    status : str = "UPDATING"
    latency : int = -1

    def to_json(self):
        return {
            'id' : self.id,
            'name': self.name,
            'url' : self.url,
            'description' : self.description,
            'status' : self.status,
            'latency' : self.latency
        }

class CardRepository:
    def __init__(self):
        self.db_path = 'data.db'
        # Just create the table once on init
        with sqlite3.connect(self.db_path) as con:
            con.execute("""
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                url TEXT,
                description TEXT,
                status TEXT,
                latency INTEGER
            )
            """)

    def get_card_by_id(self, id):
        with sqlite3.connect(self.db_path) as con:
            res = con.execute("SELECT * FROM card WHERE id = ?", (id,))
            row = res.fetchone()
            if row:
                return Card(id=row[0], name=row[1], url=row[2],
                            description=row[3], status=row[4], latency=row[5])
        return None
    
    def get_all_cards(self):
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute("SELECT * FROM card").fetchall()
            return [Card(id=r[0], name=r[1], url=r[2],
                        description=r[3], status=r[4], latency=r[5]) for r in rows]

    def add_card(self, name, url, description = ""):
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "INSERT INTO card (name, url, description, status, latency) VALUES (?, ?, ?, 'UPDATING', -1)",
                (name, url, description)  # was missing entirely
            )
            con.commit()
        return {'status' : 'Success!'}

    def del_card_by_id(self, id):
        with sqlite3.connect(self.db_path) as con:
            con.execute("DELETE FROM card WHERE id = ?", (id,))
            con.commit()
        return {'status' : 'Success!'}

    def update_card(self, card : Card):
        with sqlite3.connect(self.db_path) as con:
            con.execute("""
            UPDATE card 
            SET name = ?,
                url = ?,
                description = ?,
                status = ?,
                latency = ?
            WHERE id = ?
            """,
            (card.name, card.url, card.description, card.status, card.latency, card.id))
            con.commit()
        return {'status' : 'Success!'}


        