import requests
import os
from lastfm import check_for_new_song
from config import config


def safe_result(result_of_request):
    with open('temp.txt', 'w') as file:
        file.write(result_of_request)


def check_file(result_of_request):
    if not os.path.isfile('temp.txt'):
        file = open('temp.txt', 'w')
        file.close()
    with open('temp.txt', 'r') as file:
        if result_of_request != file.read():
            return True
    return False


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


def app():
    data = check_for_new_song("gunlinux", "460cda35be2fbf4f28e8ea7a38580730")
    data_line = data['name'] + data['artist']
    if check_file(data_line):
        safe_result(data_line)
        send_message(data['name'], data['artist'])
        return


if __name__ == "__main__":
    app()
