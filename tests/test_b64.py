import torchaudio
from src.utils import decode_base64_to_waveform, encode_waveform_to_base64


if __name__=="__main__":
  audio_path = "./recording.m4a"
  waveform, sample_rate = torchaudio.load(audio_path)
  print(waveform.shape)
  encoded_string = encode_waveform_to_base64(waveform, sample_rate)
  print(len(encoded_string))
  de_waveform, _ = decode_base64_to_waveform(encoded_string)
  print(de_waveform.shape)
  torchaudio.save("./test.wav", de_waveform, sample_rate)
  print(encoded_string[:100])