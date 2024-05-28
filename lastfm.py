import requests


def get_song_from_api(userName, api_key):
    base_url = "http://ws.audioscrobbler.com/2.0/"

    # Параметры запроса
    params = {
        "method": "user.getrecenttracks",
        "nowplaying": "true",
        "user": userName,
        "api_key": api_key,
        "limit": 1,
        'format': 'json',
    }

    # Выполнение GET-запроса с параметрами
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return None
    return response.json()





def process_json(document):
    current_track = document['recenttracks']['track'][0]
    song_name = current_track['name']
    song_artist = current_track['artist']['#text']

    return {
        'name': song_name,
        'artist': song_artist,
        'nowplaying': '@attr' in current_track,
    }


def check_for_new_song(userName, api_key="460cda35be2fbf4f28e8ea7a38580730"):
    current_track_data = get_song_from_api(userName, api_key)
    if not current_track_data:
        return {'error': "sometign went wrong"}
    return process_json(current_track_data)


if __name__ == "__main__":
    userName = "gunlinux"
    result = check_for_new_song(userName)
    print(result)