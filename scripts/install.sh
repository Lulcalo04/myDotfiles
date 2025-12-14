#!/bin/bash
# install.sh
# Creates symbolic links from this repo to your system configuration.
# BACKUPS will be created if files already exist.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$REPO_DIR/.config"
TARGET_DIR="$HOME/.config"

echo "Installing dotfiles from $CONFIG_DIR to $TARGET_DIR..."

link_item() {
    src="$1"
    dest="$2"
    
    # Check if we are linking a directory
    if [ -d "$src" ]; then
        # If dest is a directory but NOT a symlink, and we are trying to link a directory over it...
        # We usually want to replace it, UNLESS we are doing fine-grained linking.
        # But this function is for direct linking.
        :
    fi
    
    echo "  Processing $(basename "$src")..."
    
    mkdir -p "$(dirname "$dest")"
    
    if [ -e "$dest" ] || [ -L "$dest" ]; then
        if [ -L "$dest" ]; then
            current_link=$(readlink -f "$dest")
            if [ "$current_link" == "$src" ]; then
                echo "    Already linked."
                return
            fi
        fi
        
        echo "    Backing up existing $(basename "$dest") to .bak"
        rm -rf "${dest}.bak"
        mv "$dest" "${dest}.bak"
    fi
    
    ln -s "$src" "$dest"
    echo "    Linked $dest -> $src"
}

# Recursively link contents of a directory (for hygiene)
# Usage: link_contents source_dir target_dir
link_contents() {
    src_dir="$1"
    dest_dir="$2"
    
    echo "  Linking contents of $(basename "$src_dir")..."
    mkdir -p "$dest_dir"

    for item in "$src_dir"/*; do
        [ -e "$item" ] || continue
        base_item=$(basename "$item")
        link_item "$item" "$dest_dir/$base_item"
    done
}

# --- Installation ---

# 1. Waybar: Link the whole folder
link_item "$CONFIG_DIR/waybar" "$TARGET_DIR/waybar"

# 2. Walker: Link the whole folder
link_item "$CONFIG_DIR/walker" "$TARGET_DIR/walker"

# 3. Vesktop: Link settings & themes separately
#    We don't want to nuke the whole vesktop dir if it has other stuff
mkdir -p "$TARGET_DIR/vesktop"
link_item "$CONFIG_DIR/vesktop/settings" "$TARGET_DIR/vesktop/settings"
link_item "$CONFIG_DIR/vesktop/themes" "$TARGET_DIR/vesktop/themes"

# 4. Omarchy: Link internal items individually (preserves 'current' if it exists on system)
link_contents "$CONFIG_DIR/omarchy" "$TARGET_DIR/omarchy"

# 5. Hypr: Link internal items individually (preserves 'current' if it exists on system)
link_contents "$CONFIG_DIR/hypr" "$TARGET_DIR/hypr"

echo "------------------------------------------------"
echo "Done! Dotfiles installed."
