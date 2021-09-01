import configparser

from mysql.connector import connect


class DataBase:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('setting.ini')

        self.connect = connect(
            host=config.get('DataBase', 'host'),
            user=config.get('DataBase', 'user'),
            password=config.get('DataBase', 'password'),
            database=config.get('DataBase', 'database')
        )

    def save_track_info(self, tg_id, url, artist_name, song_name):
        with self.connect.cursor() as cursor:
            cursor.execute("INSERT INTO tg_id_audio(tg_id, url, artist_name, song_name) VALUES(%s, %s, %s, %s);",
                           (tg_id, url, artist_name, song_name))
            self.connect.commit()

    def search_track_audio_id(self, url):
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT tg_id FROM tg_id_audio WHERE url=%s;", (url,))
            tg_id_audio = cursor.fetchall()
            self.connect.commit()
            if tg_id_audio:
                return list(tg_id_audio[0])[0]
            else:
                return None

    def save_image_info(self, tg_id, url):
        with self.connect.cursor() as cursor:
            cursor.execute("INSERT INTO tg_id_image(tg_id_image, image_url) VALUES(%s, %s);", (tg_id, url,))
        self.connect.commit()

    def search_image_id(self, url):
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT tg_id_image FROM tg_id_image WHERE image_url=%s;", (url,))
            tg_id_image = cursor.fetchall()
            self.connect.commit()
            if tg_id_image:
                return list(tg_id_image[0])[0]
            else:
                return None
