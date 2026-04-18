import numpy as np

def decode(frames):
    if frames is None or len(frames) == 0:
        return np.array([])

    reconstructed_frames = []

    for real_q, imag_q in frames:
        # Reconstruct complex spectrum
        spectrum = real_q + 1j * imag_q

        # Inverse FFT
        frame = np.fft.ifft(spectrum)

        # Take real part
        reconstructed_frames.append(np.real(frame))

    return np.concatenate(reconstructed_frames)
