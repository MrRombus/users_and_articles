import sqlite3
import datetime
import logging
#import logg

from .exceptions_articles import UserDoestNotExists, ArticleDoesNotExists


class ArticleStorage:
    def __init__(self, conn, log):
        self._conn = conn
        self._log = log
        self._cursor = self._conn.cursor()

    def create(self):
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS User(
                id INTEGER PRIMARY KEY,
                nickname TEXT UNIQUE,
                name TEXT,
                surname TEXT
            )
        """)

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Hashes(
                hash TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES User(id)
            )
        """)

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Article(
                id INTEGER PRIMARY KEY,
                headline TEXT UNIQUE,
                content TEXT,
                publication_date TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES User(id)
            )
        """)

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Comments(
                id INTEGER PRIMARY KEY,
                content TEXT,
                publication_date TEXT,
                user_id INTEGER NOT NULL,
                article_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES User(id)
                FOREIGN KEY (article_id) REFERENCES Article(id)
            )
        """)

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS LikesDislikes(
                id INTEGER PRIMARY KEY,
                like_dislike TEXT,
                set_date TEXT,
                user_id INTEGER NOT NULL,
                article_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES User(id)
                FOREIGN KEY (article_id) REFERENCES Article(id)
            )
        """)

        self._conn.commit()
        self._log.info('Created four tables')

    def drop(self):
        self._cursor.execute("""
           DROP TABLE IF EXISTS User
        """)
        self._cursor.execute("""
           DROP TABLE IF EXISTS Article
        """)
        self._cursor.execute("""
            DROP TABLE IF EXISTS Comments
        """)
        self._cursor.execute("""
            DROP TABLE IF EXISTS LikesDislikes
        """)
        self._conn.commit()
        self._log.info('tables were deleted')

    def _find_user_id(self, nickname):
        self._cursor.execute("""
            SELECT id FROM User WHERE nickname=?
        """, (nickname,))
        try:
            user_id = self._cursor.fetchone()[0]
        except:
            self._log.info(f'User {nickname} not found')
            raise UserDoestNotExists
        return user_id

    def _find_article_id(self, headline):
        self._cursor.execute("""
            SELECT id FROM Article WHERE headline=?
        """, (headline,))
        try:
            article_id = self._cursor.fetchone()[0]
        except:
            self._log.info(f'Article {headline} not found')
            raise ArticleDoesNotExists
        return article_id

    def is_user(self, nickname):
        self._cursor.execute("""
            SELECT id FROM User WHERE nickname=?
        """, (nickname,))
        try:
            user_id = self._cursor.fetchone()[0]
        except:
            self._log.info(f'User {nickname} not found')
            return False
        return True

    # def add_user(self, nickname, name, surname):
    #     try:
    #         self._cursor.execute(f"""
    #             INSERT INTO User(nickname, name, surname) VALUES ('{nickname}', '{name}', '{surname}')
    #         """)
    #         self._conn.commit()
    #         self._log.info('User was created')
    #         return True
    #     except sqlite3.IntegrityError:
    #         self._log.warning('User exists!')
    #         return False

    def register_user(self, nickname, name, surname, hash):
        try:
            self._cursor.execute(f"""
                INSERT INTO User(nickname, name, surname) VALUES ('{nickname}', '{name}', '{surname}')
            """)
            self._conn.commit()
            user_id = self._find_user_id(nickname)
            self._cursor.execute(f"""
                INSERT INTO Hashes(hash, user_id) VALUES ('{hash}', '{user_id}')
            """)
            self._conn.commit()
            self._log.info('User was created')
            return True
        except sqlite3.IntegrityError:
            self._log.warning('User exists!')
            return False

    def publish(self, nickname, headline, content, date=str(datetime.datetime.now())):
        try:
            user_id = self._find_user_id(nickname)
            self._cursor.execute(f"""
                INSERT INTO Article(headline, content, publication_date, user_id) VALUES ('{headline}', '{content}', '{date}', {user_id})
            """)
            self._conn.commit()
            self._log.info(f'Article {headline} is published')
            return True
        except sqlite3.IntegrityError:
            self._log.warning(f'Article {headline} already exists!')
            return False
        

    def show_articles(self, nickname=None):
        if nickname:
            user_id = self._find_user_id(nickname)
            self._cursor.execute("""
                SELECT * FROM Article WHERE user_id=?
            """, (user_id,))
            articles = self._cursor.fetchall()
            print(articles)
        else:
            self._cursor.execute("""
                SELECT * FROM Article
            """)
            articles = self._cursor.fetchall()
            print(articles)
        self._log.info('Articles were shown')

    def delete_article(self, headline):
        try:
            id_article = self._find_article_id(headline)
            self._cursor.execute("""
                DELETE FROM Article WHERE id=?
            """, (id_article,))
            self._conn.commit()
            self._log.info(f'Article {headline} has been deleted')
            return True
        except ArticleDoesNotExists:
            self._log.warning(f'Article {headline} not found')
            return False
        except sqlite3.OperationalError:
            self._log.warning('Table not found')
            return False

    def delete_user(self, nickname):
        try:
            user_id = self._find_user_id(nickname)

            self._cursor.execute("""
                DELETE from Article Where user_id=?
            """, (user_id,))
        
            self._cursor.execute("""
                DELETE from User Where id=?
            """, (user_id,))
            self._conn.commit()
            self._log.info(f'User {nickname} has been deleted')
            return True
        except UserDoestNotExists:
            self._log.warning(f'User {nickname} not found')
            return False
        except sqlite3.OperationalError:
            self._log.warning('Table not found')
            return False

    def edit_article(self, headline, nickname, new_text):
        id_article = self._find_article_id(headline)
        user_id = self._find_user_id(nickname)
        self._cursor.execute("""
            SELECT user_id FROM Article WHERE id=?
        """, (id_article,))
        #user_id_2 = self._cursor.fetchone()
        if user_id == self._cursor.fetchone()[0]:
            self._cursor.execute("""
                UPDATE Article SET content=? WHERE id=?
            """, (new_text, id_article))
            self._conn.commit()
            self._log.info(f'Article {headline} has been edited')
            return True
        else:
            return False

    def add_comment(self, nickname, headline, text, date=str(datetime.datetime.now())):
        user_id = self._find_user_id(nickname)
        article_id = self._find_article_id(headline)
        self._cursor.execute(f"""
            INSERT INTO Comments(content, publication_date, user_id, article_id) VALUES ('{text}', '{date}', {user_id}, {article_id})
        """)
        self._conn.commit()
        self._log.info(f'Comment from user {nickname} has been created')
        return True

    def get_comments(self, headline=None):
        if headline:
            article_id = self._find_article_id(headline)
            self._cursor.execute("""
                SELECT * FROM Comments WHERE article_id=?
            """, (article_id,))
            comments = self._cursor.fetchall()
            self._log.info('Comments from article {headline} were shown')
            return comments
        else:
            self._cursor.execute("""
                SELECT * FROM Comments
            """)
            comments = self._cursor.fetchall()
            self._log.info('Comments were shown')
            return comments

    def set_like_or_dislike(self, mark, nickname, headline, date=str(datetime.datetime.now())):
        user_id = self._find_user_id(nickname)
        article_id = self._find_article_id(headline)
        self._cursor.execute("""
            SELECT like_dislike FROM LikesDislikes WHERE user_id=? AND article_id=?
        """, (user_id, article_id))
        if self._cursor.fetchall():
            self._log.info(f'Mark from user {nickname} already set on {headline}')
            return False
        else:
            self._cursor.execute(f"""
                INSERT INTO LikesDislikes(like_dislike, set_date, user_id, article_id) VALUES ('{mark}', '{date}', {user_id}, {article_id})
            """)
            self._conn.commit()
            self._log.info(f'{mark} from user {nickname} has been set on {headline}')
            return True

    def get_likes_and_dislikes(self, headline):
        like = 0
        dislike = 0
        article_id = self._find_article_id(headline)
        self._cursor.execute("""
            SELECT id FROM LikesDislikes WHERE like_dislike=? AND article_id=?
        """, ('like', article_id))
        like = len(self._cursor.fetchall())

        self._cursor.execute("""
            SELECT id FROM LikesDislikes WHERE like_dislike=? AND article_id=?
        """, ('dislike', article_id))
        dislike = len(self._cursor.fetchall())

        self._log.info(f'Likes and dislikes of the article {headline} were shown')
        # print(f'?? ???????????? {headline}: ???????????? = {like}, ?????????????????? = {dislike}')
        return (like, dislike)

    def get_users(self):
        try:
            self._cursor.execute("""
                SELECT nickname FROM User
                ORDER BY id
            """)
            users = [user[0] for user in self._cursor.fetchall()]
            self._log.info('All users were got')
            return users
        except sqlite3.OperationalError:
            self._log.warning('Table User does not exist')
            return None

    def get_articles(self, nickname=None):
        if nickname:
            user_id = self._find_user_id(nickname)
            self._cursor.execute("""
                SELECT headline FROM Article WHERE user_id=?
            """,(user_id,))
            articles = [article[0] for article in self._cursor.fetchall()]
            self._log.info('All articles were got')
            return articles
        else:
            self._cursor.execute("""
                SELECT headline FROM Article
                ORDER BY id
            """)
            articles = [article[0] for article in self._cursor.fetchall()]
            self._log.info('All articles were got')
            return articles

    def get_article_text(self, headline):
        self._cursor.execute("""
            SELECT content FROM Article WHERE headline=?
        """,(headline,))
        text = self._cursor.fetchone()
        if text:            
            self._log.info('Text articles was got')
            return text[0]
        else:
            raise ArticleDoesNotExists

    def all_users_articles(self):
        self._cursor.execute("""
            SELECT User.id, User.nickname, User.name, User.surname, Article.headline, Article.content, Article.publication_date FROM User
            LEFT JOIN Article ON User.id = Article.user_id
        """)
        articles = self._cursor.fetchall()
        print(articles)
        self._log.info('Article and all users were shown')

    def edit_user(self, nickname, new_nickname=None, new_name=None, new_surname=None):
        try:
            user_id = self._find_user_id(nickname)
            self._cursor.execute("""
                UPDATE User SET nickname=?, name=?, surname=? WHERE id=?
            """, (new_nickname, new_name, new_surname, user_id))
            self._conn.commit()
        except UserDoestNotExists:
            self._log.warning('User does not exist')
            return False
        return True

    def get_user_info(self, nickname):
        try:
            user_id = self._find_user_id(nickname)
            self._cursor.execute("""
                SELECT nickname, name, surname FROM User WHERE id=?
            """, (user_id, ))
            user_info = self._cursor.fetchone()
            return user_info
        except UserDoestNotExists:
            self._log.warning('User does not exist')
            return None


if __name__ == '__main__':
    conn = sqlite3.connect('ArticleStorage.sqlite3') 
    u_storage_log = logging.getLogger('u_storage')
