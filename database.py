import sqlite3
from typing import Dict
import time


class BitcoinPriceDatabase:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE bitcoin_price (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            currency TEXT NOT NULL,
            price REAL NOT NULL,
            delta_1h REAL NOT NULL,
            delta_24h REAL NOT NULL,
            delta_7d REAL NOT NULL,
            delta_30d REAL NOT NULL,
            timestamp REAL NOT NULL
        )
        """)
        self.conn.commit()

    def insert_bitcoin_price(self, price_data: Dict[str, float]):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO bitcoin_price (currency, price, delta_1h, delta_24h, delta_7d, delta_30d, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (price_data['currency'], price_data['price'], price_data['delta_1h'], price_data['delta_24h'], price_data['delta_7d'], price_data['delta_30d'], time.time()))
        self.conn.commit()

    def get_bitcoin_price(self, currency: str) -> Dict[str, float]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT currency, price, delta_1h, delta_24h, delta_7d, delta_30d, timestamp
        FROM bitcoin_price
        WHERE currency = ?
        """, (currency,))
        row = cursor.fetchone()
        if row is not None:
            return {
                'currency': row[0],
                'price': row[1],
                'delta_1h': row[2],
                'delta_24h': row[3],
                'delta_7d': row[4],
                'delta_30d': row[5],
                'timestamp': row[6]
            }

        return None
