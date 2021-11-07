class DataWork:
    def __init__(self, info_file):
        self._info_file = info_file

    def set_current_user(self, nickname):
        with open(self._info_file, 'w', encoding='utf-8') as f:
            f.write(nickname + '\n')

    def get_current_user(self):
        with open(self._info_file, 'r', encoding='utf-8') as f:
            data = f.read().split('\n')

        try:
            user = data[0]
            return user
        except IndexError:
            return None