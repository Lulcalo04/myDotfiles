#!/bin/bash
# collect.sh
# Copies dotfiles from your system (~/.config) to this repository.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$REPO_DIR/.config"

# Create repo config dir if it doesn't exist
mkdir -p "$CONFIG_DIR"

echo "Collecting dotfiles to $CONFIG_DIR..."

# Function to clear destination and copy
copy_dir() {
    src="$1"
    name="$2"
    shift 2
    excludes=("${@}") # List of directory names to remove after copy
    
    dest="$CONFIG_DIR/$name"
    
    echo "  Processing $name..."
    
    if [ ! -d "$src" ]; then
        echo "    WARNING: Source '$src' not found!"
        return
    fi
    
    # Clean old repo copy to simulate sync
    rm -rf "$dest"
    mkdir -p "$(dirname "$dest")"
    
    # Copy recursively
    cp -R "$src" "$dest"
    
    # Handle excludes (post-copy deletion)
    for excl in "${excludes[@]}"; do
        if [ -e "$dest/$excl" ]; then
            echo "    Excluding $excl..."
            rm -rf "$dest/$excl"
        fi
    done
}

# --- Collections ---

# 1. Waybar
copy_dir "$HOME/.config/waybar" "waybar"

# 2. Walker
copy_dir "$HOME/.config/walker" "walker"

# 3. Vesktop (Settings & Themes)
copy_dir "$HOME/.config/vesktop/settings" "vesktop/settings"
copy_dir "$HOME/.config/vesktop/themes" "vesktop/themes"

# 4. Omarchy (Exclude 'current')
copy_dir "$HOME/.config/omarchy" "omarchy" "current"

# 5. Hypr (Exclude 'current')
copy_dir "$HOME/.config/hypr" "hypr" "current"

echo "------------------------------------------------"
echo "Done! Dotfiles collected in $CONFIG_DIR"
