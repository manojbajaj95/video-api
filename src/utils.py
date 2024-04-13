import base64
import io
import torch
import torchaudio
from torchaudio.io import StreamWriter


def encode_waveform_to_base64(waveform: torch.Tensor, sample_rate):
    """
    Encodes an audio waveform into a Base64 string.

    Args:
        audio_file_path (str): Path to the audio file.
        sample_rate (int): Sampling rate
    Returns:
        str: Base64-encoded string representation of the audio.
    """

    # Simulate in-memory representation (could also be loaded from raw bytes)
    audio_buffer = io.BytesIO()
    torchaudio.save(audio_buffer, waveform, sample_rate, format="wav")

    encoded_bytes = base64.b64encode(audio_buffer.getvalue())
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string


def decode_base64_to_waveform(base64_string):
    """
    Decodes a Base64 string into a PyTorch audio tensor.

    Args:
        base64_string (str): Base64-encoded string representation of the audio.

    Returns:
        torch.Tensor: Audio tensor.
        int: Sample rate of the decoded audio.
    """

    audio_bytes = base64.b64decode(base64_string)
    audio_buffer = io.BytesIO(audio_bytes)
    waveform, sample_rate = torchaudio.load(audio_buffer, format="wav")

    return waveform, sample_rate
