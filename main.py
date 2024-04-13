from typing import Union
from fastapi import FastAPI
import torchaudio
from src.utils import decode_base64_to_waveform
from pydantic import BaseModel
from models.cleanunet.denoise import denoise, load_model

app = FastAPI()

class Audio(BaseModel):
    data: str | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/audio/denoise")
def denoise_audio(audio: Audio):
    encoded_audio = audio.data 
    # Decoding
    waveform, sample_rate = decode_base64_to_waveform(encoded_audio)
    # net = load_model("/home/ubuntu/video-api/models/cleanunet/weights/pretrained.pkl")
    # denoised_waveform = denoise(net, waveform, sample_rate)
    # # Encode waveform
    # b64_string = encode_waveform_to_base64(denoised_waveform, sample_rate)
    return ""
