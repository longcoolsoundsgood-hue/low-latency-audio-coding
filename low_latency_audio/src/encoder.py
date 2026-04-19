import librosa
import numpy as np

def frame_audio(audio, frame_size):
    frames = librosa.util.frame(
        audio,
        frame_length=frame_size,
        hop_length=frame_size
    )
    return frames.T

def quantize(x, bits):
    levels = 2 ** bits
    return np.round(x * levels) / levels

def encode(audio, frame_size, bitrate):
    frames = frame_audio(audio, frame_size)
    encoded = []

    for f in frames:
        # FFT
        spectrum = np.fft.fft(f)

        real = np.real(spectrum)
        imag = np.imag(spectrum)

        # Quantize
        real_q = quantize(real, bitrate)
        imag_q = quantize(imag, bitrate)

        encoded.append((real_q, imag_q))

    return encoded
