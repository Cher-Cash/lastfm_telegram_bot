from lastfm import check_for_new_song, process_json, get_song_from_api


def safe_result(result_of_request):
    with open('temp.txt', 'w') as file:
        file.write(result_of_request)


def check_file(result_of_request):
    with open('temp.txt', 'r') as file:
        if result_of_request != file.read():
            return True
    return False


def send_message(song):
    print('НАДО СЛАТЬ')


def app():
    data = check_for_new_song("gunlinux","460cda35be2fbf4f28e8ea7a38580730")
    data_line = data['name'] + data['artist']
    if check_file(data_line):
        safe_result(data_line)
        send_message(data_line)
        return
    print('ничего не шлем')


if __name__ == "__main__":
    app()