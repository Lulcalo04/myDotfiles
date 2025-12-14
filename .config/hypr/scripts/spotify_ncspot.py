#!/usr/bin/env python3
import subprocess
import json
import os
import re

# --- Definir el reproductor ---
PLAYER_NAME = "ncspot" 
# Alternativamente, puedes usar "playerctl" para que use el reproductor activo, si solo usas ncspot:
# PLAYER_NAME = "$(playerctl shell)" 

# -------------------
# Helper functions
# (No necesitan cambios)
# -------------------
def get(cmd):
    try:
        # Usamos f-string para inyectar el nombre del reproductor en playerctl
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
    except:
        return ""

def escape(text):
    if text:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ""

def strip_html(s):
    return re.sub(r"<.*?>", "", s)

def center_text(text, width):
    # Treat emojis as double width for approximate visual centering
    temp = re.sub(r"[^\w\s<>/]", "XX", strip_html(text))
    pad = max((width - len(temp)) // 2, 0)
    return " " * pad + text

# -------------------
# Load colors
# (No necesitan cambios)
# -------------------
css_file = os.path.expanduser("~/.config/waybar/style.css")
def get_css_color(var_name, css_file):
    try:
        with open(css_file, "r") as f:
            for line in f:
                match = re.match(rf"@define-color\s+{var_name}\s+([#\w]+);", line.strip())
                if match:
                    return match.group(1)
    except:
        pass
    return None

theme_colors = {
    "artist": "#F5C2E7",
    "song": "#89B4FA",
    "status_playing": "#A6E3A1",
    "status_stopped": "#F9E2AF",
    "line": get_css_color("line", css_file) or "#cdd6f4",
    "volume": get_css_color("volume", css_file) or "#FFD700",
    # CAMBIAMOS EL NOMBRE DE LA CABECERA DEL TOOLTIP
    "ncspot_header": "#a6d189", 
    "album": "#F9E2AF"
}

# -------------------
# Ncspot info
# -------------------
# MODIFICADO: Usar PLAYER_NAME
status = get(f"playerctl --player={PLAYER_NAME} status") or "Stopped"
title = escape(get(f"playerctl --player={PLAYER_NAME} metadata title") or "")
artist = escape(get(f"playerctl --player={PLAYER_NAME} metadata artist") or "")
album = escape(get(f"playerctl --player={PLAYER_NAME} metadata album") or "")
released = get(f"playerctl --player={PLAYER_NAME} metadata xesam:contentCreated") or ""
year = re.match(r"(\d{4})", released).group(1) if released and re.match(r"(\d{4})", released) else ""
position = get(f"playerctl --player={PLAYER_NAME} position") or "0"
length = get(f"playerctl --player={PLAYER_NAME} metadata mpris:length") or "0"

# Ncspot (al ser TUI) no siempre expone el volumen vía playerctl de forma fiable.
# Usaremos un valor fijo o intentaremos obtenerlo, pero lo más probable es que falle.
# Mantenemos el código por si acaso:
volume = get(f"playerctl --player={PLAYER_NAME} volume") or "0"


# -------------------
# Format times
# -------------------
try:
    length_sec = int(length) // 1000000
    length_formatted = f"{length_sec // 60}:{length_sec % 60:02d}"
except:
    length_formatted = "0:00"

try:
    pos_sec = int(float(position))
    pos_formatted = f"{pos_sec // 60}:{pos_sec % 60:02d}"
except:
    pos_formatted = "0:00"

# -------------------
# Ncspot icon and status
# -------------------
# MODIFICADO: Cambiamos el icono de Spotify por uno genérico de música o el de Spotify si lo prefieres
ncspot_icon = "" 
status_glyph = "▶" if status.lower() == "playing" else "⏸"
status_color = theme_colors['status_playing'] if status.lower() == "playing" else theme_colors['status_stopped']

# -------------------
# Player row icons
# -------------------
row_emojis = ["🎵", "👤", "💿", "⏱️"]  # Song, Artist, Album, Position

# -------------------
# Volume text (plain) for centering
# ncspot puede devolver 0/1, si devuelve 0, lo cambiamos por un texto genérico o lo ocultamos
if float(volume) > 0:
    volume_text = f"🔊 Volume: {int(float(volume)*100)}%"
else:
    volume_text = "🔊 ncspot volume (TUI)" # Mensaje si no puede obtener el volumen

# -------------------
# Determine dynamic line width
# -------------------
all_lengths = [
    len(title), len(artist), len(album),
    len(f"{pos_formatted} / {length_formatted}"),
    # MODIFICADO: Cambiamos el texto
    len(f"{ncspot_icon} ncspot {status_glyph} {status.capitalize()}"), 
    len(volume_text)
]
line_width = max(all_lengths) + 6  # extra padding for emojis/margin

# -------------------
# Build tooltip
# -------------------
# MODIFICADO: Cambiamos el texto
header_line = center_text(f"<span foreground='{theme_colors['ncspot_header']}'>{ncspot_icon} ncspot</span> " 
                          f"<span foreground='{status_color}'>{status_glyph} {status.capitalize()}</span>", line_width)

# Thin separator (dynamic)
separator_line = f"<span foreground='{theme_colors['line']}'>{'─'*line_width}</span>"

# Song info (left-aligned with icons)
song_line = f"{row_emojis[0]} <span foreground='{theme_colors['song']}'>{title}</span>"
artist_line = f"{row_emojis[1]} <span foreground='{theme_colors['artist']}'>{artist}</span>"
album_line = f"{row_emojis[2]} <span foreground='{theme_colors['album']}'>{album}{' ('+year+')' if year else ''}</span>"
time_line = f"{row_emojis[3]} <span foreground='white'>{pos_formatted} / {length_formatted}</span>"

# Volume row (centered correctly)
volume_line = center_text(f"<span foreground='{theme_colors['volume']}'>{volume_text}</span>", line_width)

# Combine all parts
tooltip = "\n".join([
    header_line,
    separator_line,
    song_line,
    artist_line,
    album_line,
    time_line,
    separator_line,
    volume_line
])

# -------------------
# Bar text
# -------------------
# -------------------
# Bar text
# -------------------
if len(artist) > 15:
    artist = artist[:15] + "..."
if len(title) > 20:
    title = title[:20] + "..."

if title == "" and artist == "":
    text = ""
    css_class = "hidden"
else:
    text = f"<span foreground='{theme_colors['artist']}'>{artist}</span> — <span foreground='{theme_colors['song']}'><i>{title}</i></span>"
    css_class = "playing"

# -------------------
# Output JSON
# -------------------
print(json.dumps({
    "text": text,
    "tooltip": tooltip if text else "",
    "class": css_class,
    "markup": "pango",
    # MODIFICADO: Los comandos de control ahora apuntan a PLAYER_NAME
    "on-click": f"playerctl --player={PLAYER_NAME} play-pause",
    "on-right-click": f"playerctl --player={PLAYER_NAME} next",
    "on-middle-click": f"playerctl --player={PLAYER_NAME} previous"
}))
