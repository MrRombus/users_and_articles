import logging


class DataWork:
    def __init__(self, info_file, log):
        self._log = log
        self._info_file = info_file

    def set_current_user(self, nickname):
        with open(self._info_file, 'w', encoding='utf-8') as f:
            f.write(nickname + '\n')
            self._log.info(f'User {nickname} was authorized')

    def get_current_user(self):
        with open(self._info_file, 'r', encoding='utf-8') as f:
            data = f.read().split('\n')

        try:
            user = data[0]
            self._log.info(f'Nickname {user} was received')
            return user
        except IndexError:
            return None