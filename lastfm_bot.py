import requests, sqlite3, os, sys
from lastfm import check_for_new_song
from config import config
from datetime import datetime


def send_message(name, artist):
    # Ваш токен бота
    TOKEN = config['token']
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    chat_id = config['chat_id']
    params = {
        'chat_id': chat_id,
        'text': f'{name} - {artist}'
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        print(f'{name} - {artist}')
    else:
        print('Ошибка отправки сообщения:', response.text)

def write_db_user(username, lastfm, chatid):
    print('write db user')
    connection = sqlite3.connect('testdb.sqlite')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, lastfm, chat_id) VALUES (?, ?, ?)', (username, lastfm, chatid))
    connection.commit()
    connection.close()
    return



def process(user):
    print(user)
    song_dict = check_for_new_song(user[2])
    print(song_dict)
    song = song_dict['name']
    artist = song_dict['artist']
    last_song = user_last_song(user[0])
    if (song, artist) == last_song and song_dict['nowplaying']:
        write_song(user, song, artist)
        send_message(song, artist)



def user_last_song(user_id):
    connection = sqlite3.connect('testdb.sqlite')
    cursor = connection.cursor()
    get_last_song_query = """
        SELECT song, artist
        FROM played
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 1;
        """
    cursor.execute(get_last_song_query, (user_id,))
    last_song_result = cursor.fetchone()
    connection.close()
    return last_song_result


def write_song(user, song, artist):
    user_id = user[0]
    connection = sqlite3.connect('testdb.sqlite')
    cursor = connection.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_query = "INSERT INTO played (song, artist, user_id, created_at) VALUES (?, ?, ?, ?)"
    cursor.execute(insert_query, (song, artist, user_id, created_at))
    connection.commit()
    connection.close()

def main_loop():
    print('main loop')
    conn = sqlite3.connect('testdb.sqlite')
    cursor = conn.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        process(user)

def app():
    if len(sys.argv) == 4:
        username = sys.argv[1]
        lastfm = sys.argv[2]
        chat_id = sys.argv[3]
        write_db_user(username, lastfm, chat_id)
        return
    main_loop()


if __name__ == "__main__":
    app()
