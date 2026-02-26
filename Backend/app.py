from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
from transformers import MarianMTModel, MarianTokenizer
import torch
import edge_tts
import os
import uuid
import asyncio

app = FastAPI()

# CORS CONFIGURATION - Allows communication between the Frontend (Vercel) and Backend (Hugging Face)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI models at startup
device = "cpu"
whisper_model = WhisperModel("tiny", device=device, compute_type="float32")

# Cache to store translation models in memory for faster subsequent requests
translation_cache = {}

def get_translation_model(source_lang, target_lang):
    pair = f"{source_lang}-{target_lang}"
    if pair not in translation_cache:
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
        # Verify if the model exists on the HuggingFace Hub
        try:
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            translation_cache[pair] = (tokenizer, model)
        except Exception as e:
            print(f"Error loading translation model: {e}")
            return None, None
    return translation_cache.get(pair, (None, None))

@app.get("/")
def home():
    return {"status": "Translator API is ONLINE & SYNCED", "model": "Whisper Tiny"}

@app.post("/process")
async def process_audio(
    audio: UploadFile = File(...), 
    target_lang: str = Form("ro"),
    session_id: str = Form(str(uuid.uuid4()))
):
    # 1. Temporarily save the received audio file
    unique_id = str(uuid.uuid4())
    input_file = f"input_{unique_id}.wav"
    
    with open(input_file, "wb") as f:
        f.write(await audio.read())

    try:
        # 2. Speech-to-Text transcription using Faster-Whisper
        segments, info = whisper_model.transcribe(input_file, beam_size=5)
        source_text = " ".join([s.text for s in segments]).strip()
        source_lang = info.language

        # 3. Translation logic
        # Normalize source language for MarianMT 
        s_lang = "en" if "en" in source_lang else source_lang
        
        translated_text = source_text # Default fallback if translation is not required
        
        if s_lang != target_lang:
            tokenizer, model = get_translation_model(s_lang, target_lang)
            if tokenizer and model:
                inputs = tokenizer([source_text], return_tensors="pt", padding=True)
                translated_ids = model.generate(**inputs)
                translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

        # 4. Text-to-Speech (Target voice mapping)
        voices = {
            "ro": "ro-RO-AlinaNeural", 
            "en": "en-US-GuyNeural", 
            "es": "es-ES-AlvaroNeural"
        }
        voice = voices.get(target_lang, "en-US-GuyNeural")
        
        # Cleanup: Remove temporary audio file after processing
        if os.path.exists(input_file):
            os.remove(input_file)

        return {
            "source_text": source_text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "session_id": session_id,
            "status": "success"
        }

    except Exception as e:
        # Ensure file cleanup even if an error occurs
        if os.path.exists(input_file):
            os.remove(input_file)
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    import uvicorn
    # Port 7860 is required for Hugging Face Spaces
    uvicorn.run(app, host="0.0.0.0", port=7860)
