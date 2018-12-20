import praw
import sqlite3
import time 
from prawbot_creds import client_id, client_secret, password, user_agent, username



reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     password=password, user_agent=user_agent,
                     username=username)



def open_db_connection(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    return conn, c

def close_db_connection(conn):
    conn.close()

def get_submission_info(submission):
    submission_info = (submission.id, submission.title, submission.author.id,
                               submission.created_utc)
    return submission_info

def get_author_info(author):
    author_info = (author.id, author.name)
    return author_info
    
def add_new_stories():
    conn, c = open_db_connection('test.db')
    subreddit = reddit.subreddit('nosleep')
    nosleep_stream = subreddit.stream.submissions()
    
    for submission in nosleep_stream:
        if not submission.stickied:
            print(submission.link_flair_css_class)
            print(submission.link_flair_text)
            submission_info = get_submission_info(submission)
            author_info = get_author_info(submission.author)
            print(submission_info, author_info)
            c.execute('INSERT OR IGNORE INTO stories(story_id, story_title, author_id, created)\
                      VALUES (?,?,?,?)', submission_info)
            c.execute('INSERT OR IGNORE INTO authors(author_id, author_name)\
                        VALUES (?,?)', author_info)
            insert_series(c, submission, author)
            conn.commit()
   
    close_db_connection(conn)
                               
def insert_series(c, submission, author):
    
    c.execute('SELECT * FROM series WHERE author_id = ? ORDER BY title_stem', (author.id,))
    stored_stems = [a[1] for a in c.fetchall()]
    title = submission.title
    title_stem_list = title.split()[0:3]
    print(title_stem_list)
    title_stem = " ".join(title_stem_list)
    print(title_stem)
    if title_stem not in stored_stems:
        c.execute('INSERT OR IGNORE INTO series (title_stem, author_id) VALUES (?,?)', (title_stem, author.id))

    
def add_hot_stories():
    conn, c = open_db_connection('hot.db')
    subreddit = reddit.subreddit('nosleep')
    while True:
        nosleep_stream = subreddit.hot(limit=10)
        for submission in nosleep_stream:
            if not submission.stickied:
                flair_type = submission.link_flair_css_class
                submission_info = get_submission_info(submission)
                author_info = get_author_info(submission.author)
                print(submission_info, author_info)
                c.execute('INSERT OR IGNORE INTO stories(story_id, story_title, author_id, created)\
                          VALUES (?,?,?,?)', submission_info)
                c.execute('INSERT OR IGNORE INTO authors(author_id, author_name)\
                            VALUES (?,?)', author_info)
                if flair_type == 'flair-series':
                    insert_series(c, submission, submission.author)
                conn.commit()
        time.sleep(16)
    close_db_connection(conn)

if __name__ == '__main__':
    add_hot_stories()
