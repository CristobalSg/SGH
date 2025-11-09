#!/bin/bash
echo "🚀 Iniciando SGH Algo Agent..."

# Iniciar la aplicación
if [ "$test" == "true" ]; then
    echo "🧪 Ejecutando pruebas con pytest..."
    exec pytest -v
else
    echo "🌟 Iniciando FastAPI..."
    exec uvicorn main:app --host 0.0.0.0 --port 9000
fi