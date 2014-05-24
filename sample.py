#!/usr/bin/python

import json
import codecs
from jinja2 import Template
from apiclient.discovery import build
from apiclient.errors import HttpError
import os


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = os.environ["GOOGLE_API_KEY"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=35
    ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)

    return videos


def main():
    songs = json.load(codecs.open("songs.json", "r", "utf-8"))
    song_set = set([item[0] for item in songs])

    for line in codecs.open("songlist.txt", "r", "utf-8"):
        name = line.strip()

        if name in song_set:
            continue

        results = youtube_search(line.strip())

        if len(results) == 0:
            print u"ERROR - No results for {}".format(name)
            continue

        print u"FOUND - Video for {}".format(name)
        songs.append([name, results[0]['id']['videoId']])
        json.dump(songs, codecs.open("songs.json", "w", "utf-8"))

    with codecs.open('index.html', 'w', 'utf-8') as w:
        template = Template(open('templates/index.html').read())
        w.write(template.render(videos=songs))

if __name__ == "__main__":
    main()
