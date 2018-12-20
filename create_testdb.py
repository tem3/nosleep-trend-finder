import sqlite3

conn = sqlite3.connect('test.db')

c = conn.cursor()

c.execute('''CREATE TABLE stories(
    story_id text NOT NULL PRIMARY KEY,
    story_title text NOT NULL,
    author_id text NOT NULL,
    created integer NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(author_id))''')


c.execute('''CREATE TABLE authors(
    author_id text NOT NULL PRIMARY KEY,
    author_name text NOT NULL)''')
#c.execute("INSERT INTO stories VALUES (0, 'test title', 1, 393939393)")

c.execute('''CREATE TABLE series(
    series_id integer NOT NULL PRIMARY KEY,
    
conn.commit()

conn.close()
   
