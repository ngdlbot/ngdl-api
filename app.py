# -*- coding: utf-8 -*-
#
# Copyright (C) 2023, SsNiPeR1, ngdlbot
#
# This program is free software, licensed under the GNU General Public
# License, version 3 or later. See the files COPYING and LICENSE for
# more information.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.


from flask import Flask, Response

import json
import requests
from bs4 import BeautifulSoup as bs


app = Flask(__name__)


@app.route("/")
@app.route("/api/v1")
@app.route("/api/v1/")
@app.route("/ngdl-api/api/v1/")
def index():
    return Response(
        json.dumps(
            {
                "status": "ok",
                "data": "Welcome to ngdlbot API, see https://t.me/ngdlbot_api for more info",
            }
        ),
        mimetype="application/json",
    )  # We return a welcome message.


@app.route(
    "/api/v1/get_url/<int:song_id>"
)  # The main API endpoint, it returns the song's title, artist, ID and URL.
@app.route(
    "/ngdl-api/api/v1/get_url/<int:song_id>"
)
def dl(song_id: int):
    song_info = {}
    link = "https://audio.ngfiles.com"
    response = requests.get(
        f"https://www.newgrounds.com/audio/listen/{song_id}"  # We have to download our page to extract the song's title, artist and its URL.
    )
    if response.status_code != 200:
        return json.dumps({"status": "error", "data": "Invalid ID"})
    soup = bs(
        response.text, "lxml"
    )  # I don't actually know about how this code works, it just works.
    song_info["artist"] = soup.find("div", class_="item-details-main").find("a").text
    song_info["title"] = soup.find("title").text
    song_info["id"] = song_id
    page = str(soup)
    i = page.find("audio.ngfiles.com") + len("audio.ngfiles.com/")
    while not link.endswith(
        ".mp3"
    ):  # I literally can't explain code above, it just works.
        if page[i] != "\\":
            link += page[i]
        i += 1
    song_info["filename"] = link

    return Response(
        json.dumps({"status": "ok", "data": song_info}), mimetype="application/json"
    )  # We return the song's title, artist, ID and URL.


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
