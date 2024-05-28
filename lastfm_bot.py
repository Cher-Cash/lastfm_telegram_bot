from lastfm import check_for_new_song, process_json, get_song_from_api


def safe_result(result_of_request):
    file = open('temp.txt', 'w')
    file.write(result_of_request)
    file.close()
    return


def check_file(result_of_request):
    file = open('temp.txt', 'r')
    if result_of_request != file.read():
        safe_result(result_of_request)
        file.close()
        return True
    file.close()
    return False


def app():
    data = check_for_new_song("gunlinux","460cda35be2fbf4f28e8ea7a38580730")
    data_line = data['name'] + data['artist']
    if check_file(data_line):
        safe_result(data_line)
        print('НАДО СЛАТЬ')
        return
    print('ничего не шлем')
    return


if __name__ == "__main__":
    app()