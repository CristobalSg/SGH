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
echo "🌟 Iniciando FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000