import librosa
import numpy as np

def frame_audio(audio, frame_size):
    frames = librosa.util.frame(audio, frame_length=frame_size, hop_length=frame_size)
    return frames.T

def quantize(frame, bits):
    levels = 2 ** bits
    return (frame * levels).astype(int) / levels

def encode(audio, frame_size, bitrate):
    frames = frame_audio(audio, frame_size)
    encoded = [quantize(f, bitrate) for f in frames]
    return encoded
