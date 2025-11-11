#!/bin/bash
echo "🚀 Iniciando SGH Backend..."

# Esperar a que PostgreSQL esté listo - SIN CREDENCIALES EXPUESTAS
echo "⏳ Esperando PostgreSQL..."
while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
    echo "PostgreSQL no está listo, esperando..."
    sleep 2
done

echo "✅ PostgreSQL listo!"

# Ejecutar migraciones
echo "📊 Ejecutando migraciones de Alembic..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migraciones ejecutadas correctamente"
else
    echo "❌ Error ejecutando migraciones"
    exit 1
fi

# Iniciar la aplicación
if [ "$test" == "true" ]; then
    echo "🧪 Ejecutando pruebas con pytest..."
    exec pytest -v
else
    echo "👩‍💻 Inicializando usuario administrador..."
    python scripts/bootstrap_admin.py

    if [ "$BACK_ENV" == "development" ] || [ "$NODE_ENV" == "development" ]; then
        echo "🔧 Modo Desarrollo Activado"
        exec fastapi dev main.py --host 0.0.0.0 --port ${BACKEND_PORT:-8000}
    else
        echo "🌟 Iniciando FastAPI..."
        exec uvicorn main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000}
    fi
fi