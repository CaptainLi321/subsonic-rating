#!/usr/bin/env python3
# Copyright (C) 2026 Captain Li <captainli321@users.noreply.github.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Shared constants and helpers for subsonic-rating scripts.

Configuration is loaded from JSON files checked in order:
  1. $SUBSONIC_RATING_CONFIG env var
  2. ~/.config/subsonic-rating/config.json
  3. /etc/subsonic-rating/config.json
  4. hardcoded defaults (fallback)
"""
import hashlib
import json
import os
import subprocess
import time
import requests

# ── defaults (used when no config file is found) ──

_DEFAULTS = {
    "server_url": "http://localhost:4533",
    "username": "",
    "password": "",
    "state_file": "/tmp/subsonic_state.json",
}


def _load_config():
    """Load config from the first available source, falling back to defaults."""
    paths = []

    env_path = os.environ.get("SUBSONIC_RATING_CONFIG")
    if env_path:
        paths.append(env_path)

    xdg_config = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    paths.append(os.path.join(xdg_config, "subsonic-rating", "config.json"))
    paths.append("/etc/subsonic-rating/config.json")

    for p in paths:
        try:
            with open(p, "r") as f:
                cfg = json.load(f)
            # validate required keys
            for k in ("server_url", "username", "password"):
                if k not in cfg:
                    raise KeyError(f"missing required key: {k}")
            return cfg
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            continue

    return dict(_DEFAULTS)


_config = _load_config()

# exported module-level constants (populated from config or defaults)
SUBSONIC_URL = _config["server_url"]
SUBSONIC_USER = _config["username"]
SUBSONIC_PASS = _config["password"]
STATE_FILE = _config.get("state_file", _DEFAULTS["state_file"])


def get_auth_params(client_name):
    """Build MD5-salted auth params for a Subsonic API request."""
    salt = str(int(time.time() * 1000)) + "python"
    token = hashlib.md5((SUBSONIC_PASS + salt).encode("utf-8")).hexdigest()
    return {
        "u": SUBSONIC_USER,
        "t": token,
        "s": salt,
        "v": "1.15.0",
        "c": client_name,
        "f": "json",
    }


def get_session():
    """Create a requests.Session, automatically bypassing environment proxy for loopback addresses."""
    s = requests.Session()
    if "127.0.0.1" in SUBSONIC_URL or "localhost" in SUBSONIC_URL:
        s.trust_env = False
    return s


def notify(title, message):
    """Send a desktop notification via notify-send."""
    subprocess.run(["notify-send", "-a", "Subsonic", title, message])


def load_state():
    """Read current playing state from STATE_FILE. Returns dict or None."""
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None


def save_state(data):
    """Atomically write state dict to STATE_FILE."""
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.rename(tmp, STATE_FILE)
