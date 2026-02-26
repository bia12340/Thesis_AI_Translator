# Folosim o versiune ușoară de Python
FROM python:3.10-slim

# Instalăm dependențele de sistem pentru audio și FFmpeg (esențial pentru Whisper și Edge-TTS)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Setăm folderul de lucru în server
WORKDIR /code

# Copiem requirements.txt și instalăm librăriile
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiem restul fișierelor (app.py) din folderul local în folderul /code din server
COPY . .

# Expunem portul pe care rulează FastAPI
EXPOSE 7860

# Pornim serverul folosind uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]