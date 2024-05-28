from xml.dom import minidom

import requests


def get_song_from_api(username, api_key):
    currentTrackURL = (
        'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&nowplaying=\"true\"&user={0}&api_key={1}&limit=1'.format(
            str(userName), str(api_key)))
    result = requests.get(currentTrackURL)
    return result.text

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
    song_info = process_xml(current_track_xml)
    return song_info


if __name__ == "__main__":
    userName = "gunlinux"
    result = check_for_new_song(userName)
    print(result)