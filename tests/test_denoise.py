import wave
import torch
import torchaudio
from models.cleanunet.denoise import denoise, load_model


if __name__=="__main__":
  audio_path = "./5.wav"
  waveform, sample_rate = torchaudio.load(audio_path)
  net = load_model("/home/ubuntu/video-api/models/cleanunet/weights/pretrained.pkl")
  denoised_waveform = denoise(net, waveform, sample_rate)
  print(denoised_waveform.shape)
  torchaudio.save(f"./test_denoised.wav", denoised_waveform, sample_rate)
