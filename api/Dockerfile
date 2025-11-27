# 1. Imagen base
FROM python:3.9-slim

# 2. Variable de entorno (Mejora logs)
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /usr/src/app

# 4. Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto de la aplicación Flask
COPY . .

# 6. Exponer el puerto
EXPOSE 5000

# 7. Ejecutar la API con Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "main:app"]
#1 hilo por cada maquina creada