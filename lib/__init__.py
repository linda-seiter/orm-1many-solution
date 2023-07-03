import sqlite3

CONN = sqlite3.connect('lib/companies.db')
CURSOR = CONN.cursor()
