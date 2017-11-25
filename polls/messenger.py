from multiprocessing.connection import Client


class Messenger(object):
    _connection = None

    @classmethod
    def _get_connection(cls):
        if not cls._connection:
            cls._connection = Client(('localhost', 6000), authkey=b'secret')
        return cls._connection

    @classmethod
    def open_video(cls, path):
        cls._get_connection().send(['video', path])

    @classmethod
    def open_website(cls, url):
        cls._get_connection().send(['website', url])

    @classmethod
    def close_connecttion(cls):
        cls._get_connection().send('close')
        cls._get_connection().close()
