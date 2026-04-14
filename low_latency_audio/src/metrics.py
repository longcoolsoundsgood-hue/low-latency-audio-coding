import numpy as np

def compute_latency(frame_size, sample_rate):
    """
    Estimate processing latency based on frame size.
    Latency ≈ frame_size / sample_rate
    """
    
    if sample_rate <= 0:
        raise ValueError("Sample rate must be positive")
    
    latency = frame_size / sample_rate
    return latency


def compute_snr(original_signal, reconstructed_signal):
    """
    Compute Signal-to-Noise Ratio (SNR) in dB.
    SNR = 10 * log10(signal_power / noise_power)
    """
    
    if original_signal is None or reconstructed_signal is None:
        print("Warning: Invalid input signals")
        return 0
    
    # Ensure same length
    min_len = min(len(original_signal), len(reconstructed_signal))
    
    if min_len == 0:
        print("Warning: Empty signal")
        return 0
    
    original = original_signal[:min_len]
    reconstructed = reconstructed_signal[:min_len]
    
    # Calculate noise
    noise = original - reconstructed
    
    # Compute power
    signal_power = np.sum(original ** 2)
    noise_power = np.sum(noise ** 2)
    
    # Avoid division by zero
    if noise_power == 0:
        return float('inf')
    
    snr = 10 * np.log10(signal_power / noise_power)
    
    return snr
