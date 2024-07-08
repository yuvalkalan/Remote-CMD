import datetime


MAX_LOG = 100


class Log:
    def __init__(self):
        self._log = []
        self._log_index = 0

    def append(self, other):
        current_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')
        log_str = f'{current_time} -> {other}'
        print(log_str)
        if len(self._log) >= MAX_LOG:
            self._log[self._log_index] = log_str
            self._log_index = (self._log_index + 1) % MAX_LOG
        else:
            self._log.append(log_str)
        return self


log = Log()