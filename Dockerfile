# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar las dependencias del sistema necesarias para compilar ciertos paquetes si es necesario
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Crear el directorio instance para la base de datos SQLite
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Exponer el puerto en el que se ejecuta la aplicación
EXPOSE 5000

# Crear directorio instance en runtime (después de volume mounts) y ejecutar la app
CMD ["sh", "-c", "mkdir -p /app/instance && python run.py"]
