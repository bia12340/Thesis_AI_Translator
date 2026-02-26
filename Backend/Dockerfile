# Use an official lightweight Python image
FROM python:3.10-slim

# Install system dependencies for audio processing
# ffmpeg is essential for Whisper (STT) and Edge-TTS to function correctly
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install Python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all project files from the local directory to the /code directory in the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 7860

# Start the server using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
