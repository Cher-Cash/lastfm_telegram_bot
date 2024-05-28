from xml.dom import minidom

import requests


def get_song_from_api(userName, api_key):
    base_url = "http://ws.audioscrobbler.com/2.0/"

    # Параметры запроса
    params = {
        "method": "user.getrecenttracks",
        "nowplaying": "true",
        "user": userName,
        "api_key": api_key,
        "limit": 1
    }

    # Выполнение GET-запроса с параметрами
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None
    return response.text


def process_xml(data):
    document = minidom.parseString(data)
    current_track = document.getElementsByTagName('track')[0]
    song_name = current_track.getElementsByTagName('name')[0]
    song_artist = current_track.getElementsByTagName('artist')[0]
    return {
        'name': song_name.firstChild.nodeValue,
        'artist': song_artist.firstChild.nodeValue,
        'nowplaying': current_track.getAttribute('nowplaying') == 'true'
    }


def check_for_new_song(userName, api_key="460cda35be2fbf4f28e8ea7a38580730"):
    current_track_xml = get_song_from_api(userName, api_key)
    if not current_track_xml:
        return {'error': "sometign went wrong"}
    song_info = process_xml(current_track_xml)
    return song_info


if __name__ == "__main__":
    userName = "gunlinux"
    result = check_for_new_song(userName)
    print(result)