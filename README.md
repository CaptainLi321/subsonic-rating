# Subsonic Rating for KDE Plasma (Wayland)

A lightweight set of Python scripts and systemd user services providing Subsonic / Navidrome now-playing desktop notifications and global rating shortcuts seamlessly integrated with the KDE Plasma 6 (Wayland) desktop environment.

---

## 🌟 Features

- **Now Playing Daemon (`subsonic-daemon`)**: Polls your Subsonic/Navidrome server for the currently playing track. When a track changes, it updates the state locally (`/tmp/subsonic_state.json`) and triggers `notify-send` to display a native KDE notification with the song title, artist, and current rating.
- **Rating Script (`subsonic-rate`)**: Allows setting a star rating (0-5) for the currently playing track via command line or global shortcuts. Rating changes are instantly synced to the server with confirmation notifications.
- **KDE Global Shortcuts Integration**: Ships with a standard Desktop Entry and Desktop Actions. Easily map global shortcuts (`Ctrl+Alt+1~5` to rate, `Ctrl+Alt+Backspace` to cancel) via GUI or `kwriteconfig6`.
- **Decoupled Configuration**: Supports loading credentials and server URL from `~/.config/subsonic-rating/config.json` without modifying source files.
- **Proxy-Aware**: Automatically bypasses system HTTP/all-proxy settings for local endpoints (`localhost` / `127.0.0.1`) to prevent 502 Bad Gateway errors when Clash / proxy tools are active.

---

## 📦 Components

- `subsonic_daemon.py`: The background daemon polling `getNowPlaying`.
- `subsonic_rate.py`: The CLI script sending `setRating`.
- `subsonic_common.py`: Shared utilities for authentication, config loading, and atomic state file handling.
- `subsonic-watcher.service`: Systemd user unit ensuring daemon persistence.
- `subsonic-rating.desktop`: Standard FreeDesktop entry defining rating actions (`rate0`–`rate5`).
- `config.example.json`: Sample configuration file template.

---

## 🚀 Installation & Setup

### 1. Install via RPM

Download the latest `.noarch.rpm` from [GitHub Releases](https://github.com/captainli321/subsonic-rating/releases) and install:

```bash
sudo dnf install -y subsonic-rating-1.1.2-1.fc43.noarch.rpm
```

### 2. Configure Credentials

Create `~/.config/subsonic-rating/config.json`:

```bash
mkdir -p ~/.config/subsonic-rating
cp config.example.json ~/.config/subsonic-rating/config.json
chmod 600 ~/.config/subsonic-rating/config.json
```

Edit `~/.config/subsonic-rating/config.json` with your server URL and credentials:

```json
{
  "server_url": "http://127.0.0.1:4533",
  "username": "your-username",
  "password": "your-password",
  "state_file": "/tmp/subsonic_state.json"
}
```

### 3. Enable Systemd User Service

```bash
systemctl --user daemon-reload
systemctl --user enable --now subsonic-watcher.service
```

Check service status:
```bash
systemctl --user status subsonic-watcher.service
```

---

## ⌨️ Configuring Shortcuts in KDE

### Option A: One-line CLI Configuration (Recommended)

```bash
kwriteconfig6 --file kglobalshortcutsrc --group "services" --group "subsonic-rating.desktop" --key "_launch" "none"
kwriteconfig6 --file kglobalshortcutsrc --group "services" --group "subsonic-rating.desktop" --key "rate0" "Ctrl+Alt+Backspace"
kwriteconfig6 --file kglobalshortcutsrc --group "services" --group "subsonic-rating.desktop" --key "rate1" "Ctrl+Alt+1"
kwriteconfig6 --file kglobalshortcutsrc --group "services" --group "subsonic-rating.desktop" --key "rate2" "Ctrl+Alt+2"
kwriteconfig6 --file kglobalshortcutsrc --group "services" --group "subsonic-rating.desktop" --key "rate3" "Ctrl+Alt+3"
kwriteconfig6 --file kglobalshortcutsrc --group "services" --group "subsonic-rating.desktop" --key "rate4" "Ctrl+Alt+4"
kwriteconfig6 --file kglobalshortcutsrc --group "services" --group "subsonic-rating.desktop" --key "rate5" "Ctrl+Alt+5"

# Reload KDE global shortcuts daemon
qdbus6 org.kde.KGlobalAccel /kglobalaccel org.kde.KGlobalAccel.reloadConfig
```

### Option B: Via KDE System Settings (GUI)

1. Open **System Settings** -> **Keyboard** -> **Shortcuts**.
2. Click on **Applications** -> **Add Application** and search for `Subsonic Rating`.
3. Expand `Subsonic Rating` to assign shortcuts:
   - **Cancel Rating (0 Stars)**: `Ctrl+Alt+Backspace`
   - **Rate 1 Star**: `Ctrl+Alt+1`
   - **Rate 2 Stars**: `Ctrl+Alt+2`
   - **Rate 3 Stars**: `Ctrl+Alt+3`
   - **Rate 4 Stars**: `Ctrl+Alt+4`
   - **Rate 5 Stars**: `Ctrl+Alt+5`

---

## 🛠️ Building RPM Locally

```bash
VERSION="1.1.2"
rpmdev-setuptree
cp subsonic-rating.spec ~/rpmbuild/SPECS/

mkdir -p "/tmp/subsonic-rating-${VERSION}"
cp -r subsonic_daemon.py subsonic_rate.py subsonic_common.py \
      subsonic-watcher.service subsonic-rating.desktop \
      config.example.json README.md LICENSE "/tmp/subsonic-rating-${VERSION}/"

tar -czvf ~/rpmbuild/SOURCES/subsonic-rating-${VERSION}.tar.gz -C /tmp "subsonic-rating-${VERSION}"
rpmbuild -ba ~/rpmbuild/SPECS/subsonic-rating.spec
```

The resulting package will be in `~/rpmbuild/RPMS/noarch/subsonic-rating-1.1.2-1.fc43.noarch.rpm`.

---

## 📄 License

GPL-3.0-or-later. See [LICENSE](LICENSE) for details.
