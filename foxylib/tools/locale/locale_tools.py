import locale
from contextlib import contextmanager


class LocaleToolkit:
    @classmethod
    @contextmanager
    # https://stackoverflow.com/questions/18593661/how-do-i-strftime-a-date-object-in-a-different-locale
    def setlocale(cls, name):
        # LOCALE_LOCK = threading.Lock()
        # with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)