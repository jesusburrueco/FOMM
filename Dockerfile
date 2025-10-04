# Usar Python 3.12 oficial
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 10000

# Carpeta de la app
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY setup.sh .
COPY bot.py .
COPY first-order-model ./first-order-model

# Instalar dependencias y FOMM
RUN apt-get update && apt-get install -y git wget ffmpeg && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    bash setup.sh

# Exponer puerto
EXPOSE 10000

# Comando para iniciar bot
CMD ["python", "bot.py"]
