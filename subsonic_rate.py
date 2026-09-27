#!/usr/bin/env python3
# Copyright (C) 2026 Captain Li <captainli321@users.noreply.github.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Subsonic rating script — sets star rating for the currently playing track."""
import sys
import traceback

import requests

from subsonic_common import (
    SUBSONIC_URL,
    get_auth_params,
    get_session,
    load_state,
    notify,
    save_state,
)


def main():
    if len(sys.argv) < 2:
        print("Usage: subsonic-rate <rating 0-5>")
        return

    try:
        new_rating = int(sys.argv[1])
        if not (0 <= new_rating <= 5):
            print("Usage: subsonic-rate <rating 0-5>")
            return
    except ValueError:
        return

    state = load_state()
    if state is None:
        notify("⏸️ 无法评分", "当前没有正在播放的歌曲")
        return

    song_id = state.get("id")
    current_rating = state.get("rating", 0)
    title = state.get("title", "Unknown")
    artist = state.get("artist", "Unknown")

    if new_rating != 0 and current_rating > 0:
        notify(
            "💡 该歌曲已经评过分了",
            f"当前: {current_rating}星\n{title} - {artist}\n(若要修改请先按快捷键清除)",
        )
        return

    try:
        params = get_auth_params("linux_rate")
        params["id"] = song_id
        params["rating"] = new_rating

        session = get_session()
        res = session.get(
            f"{SUBSONIC_URL}/rest/setRating", params=params, timeout=5
        )
        data = res.json()

        if data.get("subsonic-response", {}).get("status") == "ok":
            state["rating"] = new_rating
            save_state(state)

            if new_rating == 0:
                notify("🚫 已取消评分", f"🎵 {title}")
            else:
                notify(f"✅ 评分成功: {new_rating}星", f"🎵 {title}")
        else:
            error_msg = (
                data.get("subsonic-response", {})
                .get("error", {})
                .get("message", "未知错误")
            )
            notify("❌ 评分失败", f"服务器返回错误: {error_msg}")
    except Exception as e:
        print(f"[rate] setRating error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        notify("❌ 评分失败", "网络请求超时或中断")


if __name__ == "__main__":
    main()
