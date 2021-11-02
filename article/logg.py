import logging

u_storage_log = logging.getLogger('u_storage')
u_storage_log.setLevel(logging.INFO)

handler = logging.FileHandler('log/users_articles.log', encoding='utf-8')

formatter = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s')

handler.setFormatter(formatter)

u_storage_log.addHandler(handler)