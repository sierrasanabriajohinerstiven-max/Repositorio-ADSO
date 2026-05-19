#!/bin/bash
set -e

# Crear el directorio instance con permisos de escritura
mkdir -p /app/instance
chmod 777 /app/instance

echo "=== DEBUG: Database directory ==="
echo "Directory /app/instance exists: $(test -d /app/instance && echo YES || echo NO)"
echo "Directory /app/instance writable: $(test -w /app/instance && echo YES || echo NO)"
echo "================================="

# Ejecutar la aplicación
exec python run.py
