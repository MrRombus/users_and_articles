import logging

#u_storage_log u_storage
u_storage_log = logging.getLogger('u_storage')
u_storage_log.setLevel(logging.INFO)

handler = logging.FileHandler('log/users_articles.log', encoding='utf-8')

formatter = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s')

handler.setFormatter(formatter)

u_storage_log.addHandler(handler)

#data_work_log data_work
data_work_log = logging.getLogger('data_work')
data_work_log.setLevel(logging.INFO)

handler_dw = logging.FileHandler('log/data_work.log', encoding='utf-8')

formatter_dw = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s')

handler_dw.setFormatter(formatter_dw)

data_work_log.addHandler(handler_dw)
