#!/bin/bash

DEVICE="intel_backlight"
ACTION="$1" # "+5%" o "5%-"
MIN_PERCENT=10
COOLDOWN_FILE="/tmp/brightness_cooldown"
COOLDOWN_TIME=0.15 # 0.15 segundos

# --- 1. Control de Cooldown ---
CURRENT_TIME=$(date +%s.%N)
if [ -f "$COOLDOWN_FILE" ]; then
    LAST_TIME=$(cat "$COOLDOWN_FILE")
    ELAPSED=$(echo "$CURRENT_TIME - $LAST_TIME" | bc)
    
    # Si ha pasado menos de COOLDOWN_TIME, salir
    if (($(echo "$ELAPSED < $COOLDOWN_TIME" | bc -l))); then
        exit 0
    fi
fi
echo "$CURRENT_TIME" > "$COOLDOWN_FILE"

# --- 2. Aplicar el Cambio de Brillo ---

if [ "$ACTION" == "5%-" ]; then
    # Bajar brillo: Verificar si el nuevo nivel es menor al mínimo
    CURRENT_PERCENT=$(brightnessctl -d $DEVICE get | awk -v max="$(brightnessctl -d $DEVICE max)" '{printf "%d", ($1/max)*100}')
    
    NEW_PERCENT=$(echo "$CURRENT_PERCENT - 5" | bc)
    
    if [ "$NEW_PERCENT" -lt "$MIN_PERCENT" ]; then
        # Forzar al mínimo (10%)
        brightnessctl -d $DEVICE set $MIN_PERCENT%
    else
        # Aplicar el cambio
        brightnessctl -d $DEVICE set $ACTION
    fi
elif [ "$ACTION" == "+5%" ]; then
    # Subir brillo: Aplicar el cambio directamente (no hay límite superior)
    brightnessctl -d $DEVICE set $ACTION
fi
