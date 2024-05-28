from xml.dom import minidom

import requests


def get_song_from_api(userName, api_key, format_json=False):
    base_url = "http://ws.audioscrobbler.com/2.0/"

    # Параметры запроса
    params = {
        "method": "user.getrecenttracks",
        "nowplaying": "true",
        "user": userName,
        "api_key": api_key,
        "limit": 1,
    }
    if format_json:
        params['format'] = 'json'

    # Выполнение GET-запроса с параметрами
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None
    if format_json:
        return response.json()
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


def process_json(document):
    current_track = document['recenttracks']['track'][0]
    song_name = current_track['name']
    song_artist = current_track['artist']['#text']

    return {
        'name': song_name,
        'artist': song_artist,
        'nowplaying': '@attr' in current_track,
    }


def check_for_new_song(userName, api_key="460cda35be2fbf4f28e8ea7a38580730", format_json=True):
    current_track_data = get_song_from_api(userName, api_key, format_json=format_json)
    if not current_track_data:
        return {'error': "sometign went wrong"}
    if format_json:
        return process_json(current_track_data)
    return process_xml(current_track_data)


if __name__ == "__main__":
    userName = "gunlinux"
    result = check_for_new_song(userName)
    print(result)