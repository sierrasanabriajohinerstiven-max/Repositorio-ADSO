# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar las dependencias del sistema necesarias para compilar ciertos paquetes si es necesario
RUN apt-get update && apt-get install -y \
    build-essential \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Convertir line endings y dar permisos de ejecución al entrypoint
RUN dos2unix /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Crear el directorio instance para la base de datos SQLite
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Exponer el puerto en el que se ejecuta la aplicación
EXPOSE 5000

# Usar entrypoint para crear directorios en tiempo de ejecución (después de los volume mounts)
ENTRYPOINT ["/app/entrypoint.sh"]
