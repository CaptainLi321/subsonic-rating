#!/usr/bin/env python3
# Copyright (C) 2026 Captain Li <captainli321@users.noreply.github.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Subsonic now-playing daemon — polls the server and writes state on track change."""
import os
import sys
import time
import traceback

import requests

from subsonic_common import (
    SUBSONIC_URL,
    STATE_FILE,
    get_auth_params,
    get_session,
    notify,
    save_state,
)


def main():
    cache_id = ""
    session = get_session()
    while True:
        try:
            params = get_auth_params("linux_daemon")
            res = session.get(
                f"{SUBSONIC_URL}/rest/getNowPlaying", params=params, timeout=5
            )
            data = res.json()

            now_playing = data.get("subsonic-response", {}).get("nowPlaying", {})
            entry = now_playing.get("entry", [])

            if isinstance(entry, list) and len(entry) > 0:
                song = entry[0]
            elif isinstance(entry, dict):
                song = entry
            else:
                song = None

            if song:
                current_id = song.get("id")
                if current_id != cache_id:
                    cache_id = current_id
                    title = song.get("title", "Unknown")
                    artist = song.get("artist", "Unknown")
                    rating = song.get("userRating", song.get("rating", 0))

                    save_state({
                        "id": cache_id,
                        "title": title,
                        "artist": artist,
                        "rating": rating,
                    })

                    rating_str = f"{rating} 星" if rating > 0 else "未评分"
                    notify(
                        "🎵 正在播放",
                        f"标题: {title}\n艺术家: {artist}\n评分: {rating_str}",
                    )
            else:
                if cache_id != "":
                    cache_id = ""
                    if os.path.exists(STATE_FILE):
                        os.remove(STATE_FILE)
        except Exception as e:
            print(
                f"[daemon] {time.strftime('%H:%M:%S')} poll error: {e}",
                file=sys.stderr,
            )
            traceback.print_exc(file=sys.stderr)

        time.sleep(3)


if __name__ == "__main__":
    main()
