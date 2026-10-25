#!/bin/sh
set -eu

package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
install_dir="$HOME/.local/opt/tindahan-system"
data_root="${XDG_DATA_HOME:-$HOME/.local/share}"
case "$data_root" in /*) ;; *) data_root="$HOME/.local/share" ;; esac
desktop_dir="$data_root/applications"

if [ "$package_dir" = "$install_dir" ]; then
    printf '%s\n' 'This copy is already installed.'
    exit 0
fi
if [ -e "$install_dir" ] && [ ! -f "$install_dir/.tindahan-install" ]; then
    printf '%s\n' "Refusing to replace an unrecognized folder: $install_dir" >&2
    exit 1
fi
mkdir -p "$HOME/.local/opt" "$desktop_dir"
staging_dir=$(mktemp -d "$HOME/.local/opt/.tindahan-install.XXXXXX")
trap 'rm -rf -- "$staging_dir"' EXIT HUP INT TERM
cp -R "$package_dir/." "$staging_dir/"
touch "$staging_dir/.tindahan-install"
if [ -d "$install_dir" ]; then
    # Preserve databases from older executable-adjacent layouts for first-run migration.
    for name in pos.db pos.db-wal pos.db-shm; do
        if [ -f "$install_dir/$name" ]; then cp -p "$install_dir/$name" "$staging_dir/$name"; fi
    done
    rm -rf -- "$install_dir"
fi
mv -- "$staging_dir" "$install_dir"

# Desktop-entry quoting is separate from shell quoting; escape both levels.
desktop_exec=$(printf '%s' "$install_dir/POS-System" | sed 's/\\/\\\\\\\\/g; s/"/\\\\"/g; s/`/\\\\`/g; s/\$/\\\\$/g; s/%/%%/g')
cat > "$desktop_dir/tindahan-system.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Tindahan System
Comment=POS, inventory, and cash services
Exec="$desktop_exec"
Icon=accessories-calculator
Terminal=false
Categories=Office;Finance;
EOF
if [ -x "$install_dir/Tindahan-Uninstall.run" ]; then
    uninstall_exec="${desktop_exec%POS-System}Tindahan-Uninstall.run"
    cat > "$desktop_dir/tindahan-system-uninstall.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Uninstall Tindahan System
Exec="$uninstall_exec"
Icon=edit-delete
Terminal=false
Categories=Office;Finance;
EOF
fi
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$desktop_dir" || true
fi
printf '%s\n' "Installed in $install_dir" 'Open Tindahan System from your application menu.'
