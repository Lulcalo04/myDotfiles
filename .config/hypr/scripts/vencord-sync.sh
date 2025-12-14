#!/bin/bash

# El argumento $1 DEBE ser el nombre del tema (ej. "blackgold")
THEME_NAME="$1"

# NOTA: Vencord necesita que el nombre de la clave del tema coincida con el nombre del archivo
# En tu caso, el archivo era "system24-blackgold.theme.css". 
# Necesitas saber qué nombre usa Vencord internamente para activarlo.
# A menudo, Vencord usa el nombre del archivo sin el ".theme.css"
VENCORD_KEY="system24-${THEME_NAME}" # Esto puede variar, verifica en Vesktop si el nombre es diferente

VENCORD_SETTINGS_FILE="$HOME/.config/Vencord/settings.json"

if [ -f "$VENCORD_SETTINGS_FILE" ]; then
    # Usar jq para establecer la lista de 'activeThemes' para que SOLO contenga el nuevo tema.
    # Esto desactivará cualquier tema anterior y activará el nuevo.
    jq --arg THEME "$VENCORD_KEY" '
        .activeThemes = [$THEME]
    ' "$VENCORD_SETTINGS_FILE" > /tmp/vencord_settings.json
    
    mv /tmp/vencord_settings.json "$VENCORD_SETTINGS_FILE"
fi

# El script de Vencord necesita reiniciar la aplicación para que el tema surta efecto,
# pero no podemos forzar el reinicio aquí sin matar la sesión de Discord del usuario.
# El cambio se aplicará la próxima vez que el usuario reinicie Vesktop.
