import requests
import sqlite3
import sys
from lastfm import LastFMApi
from config import config
from datetime import datetime


class User:
    def __init__(self, user, lastfm, chat_id, user_id=None):
        self.user = user
        self.chat_id = chat_id
        self.user_id = user_id
        self.lastfmapi = LastFMApi(lastfm)

    def write_db_user(self):
        with sqlite3.connect('testdb.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (username, lastfm, chat_id) VALUES (?, ?, ?)',
                           (self.user, self.lastfmapi.userName, self.chat_id)
                           )
            connection.commit()
        return

    def last_song(self):
        with sqlite3.connect('testdb.sqlite') as connection:
            cursor = connection.cursor()
            get_last_song_query = """
                        SELECT song, artist
                        FROM played
                        WHERE user_id = ?
                        ORDER BY created_at DESC
                        LIMIT 1;
                        """
            cursor.execute(get_last_song_query, (self.user_id,))
            last_song_result = cursor.fetchone()
        return last_song_result

    def process(self):
        print('name', self.lastfmapi.userName)
        song_dict = self.lastfmapi.check_for_new_song()
        print('song from lastfm', song_dict)
        song = song_dict['name']
        artist = song_dict['artist']
        last_song = self.last_song()
        print('last_song', last_song)
        chat_id = self.chat_id
        if (song, artist) != last_song and song_dict['nowplaying']:
            write_song(self.user_id, song, artist)
            User.send_message(self, song, artist)

    def send_message(self, *args):
        # Ваш токен бота
        TOKEN = config['token']
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        params = {
            'chat_id': self.chat_id,
            'text': f'{args[0]} - {args[1]}'
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            print(f'{args[0]} - {args[1]}')
        else:
            print('Ошибка отправки сообщения:', response.text)

    @staticmethod
    def get_user_from_db(id):
        with sqlite3.connect('testdb.sqlite') as connection:
            cursor = connection.cursor()
            select_user = """
                    SELECT *
                    FROM users
                    WHERE id = ?
                    LIMIT 1;
                    """
            cursor.execute(select_user, (id,))
            user = cursor.fetchone()
        return user

    @staticmethod
    def get_all_users():
        with sqlite3.connect('testdb.sqlite') as connection:
            cursor = connection.cursor()
            select_users = "SELECT * FROM users"
            cursor.execute(select_users)
            users = cursor.fetchall()
        return users


def app():
    if len(sys.argv) == 4:
        username = sys.argv[1]
        lastfm = sys.argv[2]
        chat_id = sys.argv[3]
        user = User(username, lastfm, chat_id)
        user.write_db_user()
        return
    main_loop()


def write_song(user_id, song, artist):
    with sqlite3.connect('testdb.sqlite') as connection:
        cursor = connection.cursor()
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_query = "INSERT INTO played (song, artist, user_id, created_at) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, (song, artist, user_id, created_at))
        connection.commit()
    return


def main_loop():
    users = User.get_all_users()
    for user in users:
        normal_user = User(user[1], user[2], user[3], user[0])
        User.process(normal_user)
    return


if __name__ == "__main__":
    app()
