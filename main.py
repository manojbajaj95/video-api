from typing import Union

from fastapi import FastAPI
import torchaudio

from utils import decode_base64_to_waveform

app = FastAPI()

from pydantic import BaseModel


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
    # Encoding
    encoded_audio = (
        audio.data
    )  # encode_audio_to_base64(audio_file, resample_rate=16000)  # Resample to 16kHz

    # Decoding
    waveform, sample_rate = decode_base64_to_waveform(encoded_audio)
    torchaudio.save("./output.wav", waveform, sample_rate)
    # TODO:
