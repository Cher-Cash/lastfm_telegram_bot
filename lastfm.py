import requests


class LastFMApi:

    def __init__(self, userName, api_key="460cda35be2fbf4f28e8ea7a38580730"):
        self.userName = userName
        self.__api_key = api_key
        self.__base_url = "http://ws.audioscrobbler.com/2.0/"

    def check_for_new_song(self):
        current_track_data = self.__get_song_from_api()
        if not current_track_data:
            return {"error": "sometign went wrong"}
        return self.__process_json(current_track_data)

    def __get_song_from_api(self):
        # Параметры запроса
        params = {
            "method": "user.getrecenttracks",
            "nowplaying": "true",
            "user": self.userName,
            "api_key": self.__api_key,
            "limit": 1,
            "format": "json",
        }
        # Выполнение GET-запроса с параметрами
        response = requests.get(self.__base_url, params=params)
        if response.status_code != 200:
            return None
        return response.json()

    def __process_json(self, document):
        current_track = document["recenttracks"]["track"][0]
        song_name = current_track["name"]
        song_artist = current_track["artist"]["#text"]
        return {
            "name": song_name,
            "artist": song_artist,
            "nowplaying": "@attr" in current_track,
        }


if __name__ == "__main__":
    lasfmapi = LastFMApi("gunlinux")
    last_song = lasfmapi.check_for_new_song()
