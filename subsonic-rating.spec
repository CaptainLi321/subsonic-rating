Name:           subsonic-rating
Version:        1.1.2
Release:        1%{?dist}
Summary:        Subsonic rating scripts and daemon for KDE Wayland
License:        GPL-3.0-or-later
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3, python3-requests, libnotify

%description
A set of scripts to provide Subsonic now-playing notifications and rating shortcuts via KDE global shortcuts. Designed for Fedora Wayland.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user
mkdir -p $RPM_BUILD_ROOT/usr/share/applications

install -m 755 subsonic_daemon.py $RPM_BUILD_ROOT/usr/bin/subsonic-daemon
install -m 755 subsonic_rate.py $RPM_BUILD_ROOT/usr/bin/subsonic-rate
install -m 644 subsonic_common.py $RPM_BUILD_ROOT/usr/bin/subsonic_common.py
install -m 644 subsonic-watcher.service $RPM_BUILD_ROOT/usr/lib/systemd/user/
install -m 644 subsonic-rating.desktop $RPM_BUILD_ROOT/usr/share/applications/

%post
echo "====================================================================="
echo "Subsonic Rating installed successfully!"
echo ""
echo "To start the background daemon, please run the following commands:"
echo "  systemctl --user daemon-reload"
echo "  systemctl --user enable --now subsonic-watcher.service"
echo ""
echo "Then, open KDE System Settings -> Shortcuts -> Applications"
echo "to configure your global rating shortcuts."
echo "====================================================================="

%files
%license LICENSE
%doc README.md config.example.json
/usr/bin/subsonic-daemon
/usr/bin/subsonic-rate
/usr/bin/subsonic_common.py
/usr/lib/systemd/user/subsonic-watcher.service
/usr/share/applications/subsonic-rating.desktop

%changelog
* Sat Sep 26 2026 Captain Li <captainli321@users.noreply.github.com> - 1.1.2-1
- Decoupled configuration to ~/.config/subsonic-rating/config.json
- Extracted subsonic_common module
- Fixed loopback proxy bypass and atomic state writes

* Wed Jun 24 2026 Captain Li <captainli321@users.noreply.github.com> - 1.1.1-2
- Added post-installation message to remind user to start the service

* Wed Jun 24 2026 Captain Li <captainli321@users.noreply.github.com> - 1.1.1-1
- Added comprehensive README.md documentation
- Project file organization

* Wed Jun 24 2026 Captain Li <captainli321@users.noreply.github.com> - 1.1-1
- Include standard desktop file with rating Actions (0-5) for KDE Shortcuts

* Wed Jun 24 2026 Captain Li <captainli321@users.noreply.github.com> - 1.0-1
- Initial RPM build for Fedora KDE Wayland
