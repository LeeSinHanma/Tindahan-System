#!/bin/sh
set -eu

install_dir="$HOME/.local/opt/tindahan-system"
data_root="${XDG_DATA_HOME:-$HOME/.local/share}"
case "$data_root" in /*) ;; *) data_root="$HOME/.local/share" ;; esac
if [ ! -f "$install_dir/.tindahan-install" ]; then
    printf '%s\n' "No recognized installation at $install_dir" >&2
    exit 1
fi
rm -f -- "$data_root/applications/tindahan-system.desktop"
rm -f -- "$data_root/applications/tindahan-system-uninstall.desktop"
if [ -f "$install_dir/.tindahan-desktop-path" ]; then
    desktop_entry=$(cat "$install_dir/.tindahan-desktop-path")
    case "$desktop_entry" in
        /*/tindahan-system.desktop) rm -f -- "$desktop_entry" ;;
    esac
fi
rm -rf -- "$install_dir"
printf '%s\n' "Tindahan System removed. Your database remains in $data_root/tindahan-system."
