import sqlite3

connection = sqlite3.connect("HarvardReferenceGenerator.db")

db = connection.cursor()

db.execute("""CREATE TABLE newUrls (
        url TEXT PRIMARY KEY,
        expected_author TEXT NOT NULL,
        expected_title TEXT NOT NULL,
        expected_website_name TEXT NOT NULL,
        expected_publication_year INTEGER NOT NULL,
        user_email TEXT NOT NULL);""")

db.execute("""CREATE TABLE sortedUrls (
        url TEXT PRIMARY KEY,
        expected_author TEXT NOT NULL,
        expected_title TEXT NOT NULL,
        expected_website_name TEXT NOT NULL,
        expected_publication_year INTEGER NOT NULL,
        user_email TEXT NOT NULL);""")

connection.commit()
connection.close()