import sqlite3
import logging

import article.logg
from article.article import ArticleStorage

if __name__ == '__main__':
    conn = sqlite3.connect('article/ArticleStorage.sqlite3')
    u_storage_log = logging.getLogger('u_storage')   

    article_storage = ArticleStorage(conn, u_storage_log)

    article_storage.create()
    article_storage.add_user('Вася228', 'Вася', 'Петров')
    article_storage.add_user('Levinson', 'Лев', 'Игнатов')
    article_storage.add_user('Rombus', 'Игорь', 'Печенев')
    article_storage.add_user('Misha_K', 'Миша', 'Киселёв')
    article_storage.add_user('Cat', 'Анна', 'Белова')
    article_storage.publish('Вася228', 'Космос', 'текст о космосе')
    article_storage.publish('Cat', 'Уход за домашними животнами', 'кормить и поить')
    article_storage.publish('Misha_K', 'Рецепты вкусной еды', """Продукты
    (объем стакана – 200 мл)
    Для коржа:
    Кефир (комнатной температуры) – 1 стакан (200 г)
    Яйца СО (комнатной температуры) – 2 шт.
    Сахар – 0,75-1 стакан (150-200 г)
    Мука – 1 стакан (130 г)
    Разрыхлитель – 10 г
    Какао-порошок – 2 ст. ложки с горкой
    Масло растительное рафинированное – 2 ст. ложки
    Соль – 0,25 ч. ложки
    *
    Для творожно-сметанного крема:
    Творог (не зернистый) – 2-2,5 стакана (300-400 г)
    Сметана 20% – 2 стакана (350 г)
    Сахар – 0,5-0,75 стакана (100-150 г)
    Ванильный сахар – 20-30 г
    *
    Для шоколадной глазури:
    Сметана 20% – 3 ст. ложки (120-150 г)
    Сахар – 3 ст. ложки с горкой
    Какао-порошок – 1 ст. ложка с горкой
    Масло сливочное – 20 г""")

    article_storage.publish('Misha_K', 'Садоводство', 'текст о садоводстве')
    article_storage.show_articles('Вася228')
    article_storage.show_articles('Misha_K')

    article_storage.all_users_articles()
    
    article_storage.add_comment('Misha_K', 'Космос', '+')
    article_storage.set_like_or_dislike('like', 'Вася228', 'Садоводство')
    article_storage.set_like_or_dislike('like', 'Вася228', 'Рецепты вкусной еды')
    article_storage.set_like_or_dislike('like', 'Rombus', 'Садоводство')
    article_storage.set_like_or_dislike('dislike', 'Levinson', 'Садоводство')
    article_storage.set_like_or_dislike('dislike', 'Levinson', 'Космос')
    article_storage.set_like_or_dislike('dislike', 'Rombus', 'Космос')
    article_storage.set_like_or_dislike('like', 'Cat', 'Уход за домашними животнами')
