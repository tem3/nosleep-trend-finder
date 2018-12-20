import praw
import sqlite3

from prawbot_creds import client_id, client_secret, password, user_agent, username



reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     password=password, user_agent=user_agent,
                     username=username)



def open_db_connection():
    conn = sqlite3.connect('test.db')
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
    conn, c = open_db_connection()
    subreddit = reddit.subreddit('nosleep')
    nosleep_stream = subreddit.stream.submissions()
    
    for submission in nosleep_stream:
        if not submission.stickied:
            print(submission.link_flair_text)
            submission_info = get_submission_info(submission)
            author_info = get_author_info(submission.author)
            print(submission_info, author_info)
            c.execute('INSERT OR IGNORE INTO stories(story_id, story_title, author_id, created)\
                      VALUES (?,?,?,?)', submission_info)
            c.execute('INSERT OR IGNORE INTO authors(author_id, author_name)\
                        VALUES (?,?)', author_info)
            conn.commit()
   
    close_db_connection(conn)
##            print('Date: {}, Title: {}, author name: {},\
##                  author id: {}, submission_id: {}'.format(submission.created_utc,
##                                                                                        submission.title,
##                                                                                       submission.author,
##                                                                                       submission.author.id,
##                                                                                       submission.id))




if __name__ == '__main__':
    add_new_stories()
