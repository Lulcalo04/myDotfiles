# My Omarchy Dotfiles

Welcome to my personal configuration repository! This collection features my custom setups for Hyprland, Waybar, and other essential tools.

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Omarchy](https://img.shields.io/badge/Omarchy-2d3436?style=for-the-badge&logo=archlinux&logoColor=%231793D1)

## 📂 Structure

The repository mirrors the standard `~/.config` structure:

```
.
├── .config/
│   ├── hypr/          # Hyprland configuration
│   ├── omarchy/       # Omarchy settings
│   ├── walker/        # Walker application launcher
│   ├── waybar/        # Waybar status bar
│   └── vesktop/       # Vesktop (Discord) themes & settings
├── scripts/
│   ├── collect.sh     # BACKUP: Sync from your system to the repository
│   └── install.sh     # RESTORE: Creates symbolic links in your system
└── README.md
```

### 📥 Installation (Restore)

To apply these configurations to a new system or restore links:

```bash
./scripts/install.sh
```

> **Note:** This script create symbolic links (`ln -s`) from this repository to your `~/.config/` directory. If you already have config files, it will back them up with a `.bak` extension.

### 📤 Collection (Backup)

To save your current system changes back to this repository:

```bash
./scripts/collect.sh
```

> **Note:** This copies your current files into the repo. Useful before pushing changes to GitHub.
