#!/usr/bin/env python3
import socket
import os
import sys
import json
import subprocess
import time

import html

def get_active_window():
    try:
        output = subprocess.check_output(['hyprctl', 'activewindow', '-j'], text=True)
        return json.loads(output)
    except:
        return {}

def process_window(window):
    if not window:
        return ""
        
    cls = window.get('class', '')
    title = window.get('title', '')
        
    # Regla: WhatsApp (chrome-web.whatsapp -> WhatsApp)
    if 'whatsapp' in cls.lower():
        return "WhatsApp"

    # Regla: Chromium (Chromium: Page Title)
    if 'chromium' in cls.lower():
        clean_title = title.replace(' - Chromium', '').replace(' - chromium', '')
        return html.escape(f"Chromium: {clean_title}")

    if 'ghostty' in cls.lower():
        # Si el titulo empieza con / o ~ suele ser una carpeta (idle)
        # O si es muy corto y es solo el nombre
        if title.startswith('/') or title.startswith('~') or title.startswith('./'):
            return html.escape(f"Ghostty: {title}")
        
        if title.startswith('luca@omarchy:'):
            clean_title = title.replace('luca@omarchy:', '').replace('luca@omarchy', '')
            return html.escape(f"Ghostty: {clean_title}")
        # Si no, asumimos que es un comando activo
        return html.escape(title)
        
    # Regla General: Devolver solo el nombre del programa (Class)
    return html.escape(cls)

def main():
    # Loop principal
    signature = os.environ.get('HYPRLAND_INSTANCE_SIGNATURE')
    socket_path = f"/tmp/hypr/{signature}/.socket2.sock"

    # Imprimir estado inicial
    current = process_window(get_active_window())
    print(current)
    sys.stdout.flush()

    if not signature or not os.path.exists(socket_path):
        # Fallback a polling si no hay socket
        while True:
            time.sleep(1)
            new_val = process_window(get_active_window())
            if new_val != current:
                current = new_val
                print(current)
                sys.stdout.flush()

    # Listen to socket
    while True:
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(socket_path)
                buffer = ""
                while True:
                    data = s.recv(4096).decode('utf-8', errors='ignore')
                    if not data:
                        break
                    
                    buffer += data
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        # Actualizar en cambio de ventana o cambio de título
                        if line.startswith('activewindow>>') or line.startswith('windowtitle>>'):
                            new_val = process_window(get_active_window())
                            if new_val != current:
                                current = new_val
                                print(current)
                                sys.stdout.flush()
        except Exception:
            time.sleep(1) 
            # Reintentar conexión
            pass

if __name__ == "__main__":
    main()
