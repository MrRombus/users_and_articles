import unittest
import article.logg
import logging

from info.data_work import DataWork

log = logging.getLogger('data_work')

class TestDataWork(unittest.TestCase):
    def setUp(self):
        self._data_work = DataWork("test_data_work.txt", log)

    def test_set_current_user(self):
        self._data_work.set_current_user('User_1')
        with open("test_data_work.txt", 'r', encoding='utf-8') as f:
            current_user = f.read().split('\n')
            user_1 = current_user[0]
            self.assertEqual(user_1, 'User_1')

    def test_get_current_user(self):
        self._data_work.set_current_user('User_1')
        user = self._data_work.get_current_user()
        self.assertEqual(user, 'User_1')

        
if __name__ == '__main__':
    unittest.main()