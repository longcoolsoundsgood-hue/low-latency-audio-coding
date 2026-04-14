import numpy as np

def compute_latency(frame_size, sr):
    return frame_size / sr

def compute_snr(original, reconstructed):
    min_len = min(len(original), len(reconstructed))
    noise = original[:min_len] - reconstructed[:min_len]
    return 10 * np.log10(
        np.sum(original[:min_len]**2) / (np.sum(noise**2) + 1e-9)
    )
