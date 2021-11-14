import unittest
import article.logg
import logging
import sqlite3

from article.exceptions_articles import UserExists, UserDoestNotExists, ArticleDoesNotExists

conn = sqlite3.connect('ArticleStorageTest.sqlite3')
u_storage_log = logging.getLogger('u_storage')


from article.article import ArticleStorage

class TestArticleStorage(unittest.TestCase):
    def setUp(self):
        self._article_storage = ArticleStorage(conn, u_storage_log)
        self._article_storage.create()

    def test_add_user(self):        
        self.assertTrue(self._article_storage.add_user('user_1', 'vasya', 'petrov'))

    def test_add_double_user(self):
        self._article_storage.add_user('Vasya', 'T', 'T')
        self.assertFalse(self._article_storage.add_user('Vasya', 'T', 'T'))

    def test_publish_done(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self.assertTrue(self._article_storage.publish('user_1', 'Space', 'Text about space'))

    def test_publish_none_user(self):
        with self.assertRaises(UserDoestNotExists):
            self._article_storage.publish('user', 'head', 'text')

    def test_delete_article(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        test = self._article_storage.delete_article('Space')
        print(test)
        self.assertTrue(test)

    def test_edit_article(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        test = self._article_storage.edit_article('Space', 'Text about text')
        print(test)
        print('1111')
        self.assertTrue(test)

    def test_ArticleDoesNotExists(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self.assertFalse(self._article_storage.delete_article('Space1'))

    def test_add_comment(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self.assertTrue(self._article_storage.add_comment('user_1', 'Space', '+'))
        self.assertTrue(self._article_storage.add_comment('user_1', 'Space', '-'))

    def test_get_comments(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self._article_storage.publish('user_1', 'Space 2', 'Text about space 2')
        self._article_storage.add_comment('user_1', 'Space', '+')
        self._article_storage.add_comment('user_1', 'Space 2', '-')
        self.assertEqual(len(self._article_storage.get_comments('Space 2')), 1)

    def test_get_comments(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self._article_storage.add_comment('user_1', 'Space', '+')
        self._article_storage.add_comment('user_1', 'Space', '-')
        self.assertEqual(len(self._article_storage.get_comments()), 2)

    def test_not_user(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        with self.assertRaises(UserDoestNotExists):
            self._article_storage.add_comment('user_2', 'Space', '+')

    def test_not_article(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        with self.assertRaises(ArticleDoesNotExists):
            self._article_storage.add_comment('user_1', 'Space2', '+')

    def test_set_like_or_dislike(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self.assertTrue(self._article_storage.set_like_or_dislike('like', 'user_1', 'Space'))

    def test_set_like_or_dislike_2(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self._article_storage.set_like_or_dislike('like', 'user_1', 'Space')
        self.assertFalse(self._article_storage.set_like_or_dislike('like', 'user_1', 'Space'))

    def test_get_users_len(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self.assertEqual(len(self._article_storage.get_users()), 1)

    def test_get_users(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.add_user('user_2', '123', '456')
        self.assertEqual(self._article_storage.get_users(), ['user_1', 'user_2'])

    def test_get_all_articles(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self.assertEqual(self._article_storage.get_articles(),['Space'])

    def test_get_all_user_articles(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self._article_storage.add_user('user_2', 'petya', '1234')
        self._article_storage.publish('user_2', 'Sea', 'Text about sea')
        self.assertEqual(self._article_storage.get_articles('user_2'),['Sea'])

    def test_get_text_articles(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self._article_storage.add_user('user_2', 'petya', '1234')
        self._article_storage.publish('user_2', 'Sea', 'Text about sea')
        self.assertEqual(self._article_storage.get_article_text('Space'), 'Text about space')
        self.assertEqual(self._article_storage.get_article_text('Sea'), 'Text about sea')

    def test_delete_user(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.add_user('user_2', 'petya', '1234')
        self._article_storage.delete_user('user_1')
        self.assertEqual(self._article_storage.get_users(), ['user_2'])

    def test_delete_user_2(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.add_user('user_2', 'petya', '1234')
        self._article_storage.delete_user('user_3')
        self.assertFalse(self._article_storage.delete_user('user_3'))

    def test_delete_cascade(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.add_user('user_2', 'petya', '1234')
        self._article_storage.add_user('user_3', 'vova', 'petrov')

        self._article_storage.publish('user_1', 'Space', 'Text about space')
        self._article_storage.publish('user_1', 'Space_2', 'Text about space_2')
        self._article_storage.publish('user_2', 'Medicine', 'Text about medicine')
        self._article_storage.publish('user_3', 'Databases', 'Text about databases')

        self._article_storage.delete_user('user_1')

        self.assertEqual(self._article_storage.get_users(), ['user_2', 'user_3'])
        self.assertEqual(self._article_storage.get_articles(), ['Medicine', 'Databases'])

        self._article_storage.delete_user('user_2')

        self.assertEqual(self._article_storage.get_users(), ['user_3'])
        self.assertEqual(self._article_storage.get_articles(), ['Databases'])

    def test_edit_user(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self.assertEqual(self._article_storage.get_users(), ['user_1'])
        self._article_storage.edit_user('user_1', 'user_2', 'vana', 'ivanov')
        self.assertEqual(self._article_storage.get_users(), ['user_2'])

    def test_edit_user_2(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self.assertFalse(self._article_storage.edit_user('user_2', 'user_2', 'vana', 'ivanov'), False)

    def test_get_user_info(self):
        self._article_storage.add_user('user_1', 'vasya', 'petrov')
        self._article_storage.add_user('user_2', 'petya', '1234')
        self._article_storage.add_user('user_3', 'vova', 'petrov')

        self.assertEqual(self._article_storage.get_user_info('user_1'), ('user_1', 'vasya', 'petrov'))
        self.assertEqual(self._article_storage.get_user_info('user_2'), ('user_2', 'petya', '1234'))
        self.assertEqual(self._article_storage.get_user_info('user_3'), ('user_3', 'vova', 'petrov'))

    def test_get_non_exists_articles(self):
        with self.assertRaises(ArticleDoesNotExists):
            self._article_storage.get_article_text('qwe')

    def tearDown(self):
        self._article_storage.drop()


if __name__ == '__main__':
    unittest.main()