import librosa
import matplotlib.pyplot as plt

from encoder import encode
from network import simulate_packet_loss
from decoder import decode
from metrics import compute_latency, compute_snr

# ===== LOAD AUDIO =====
audio, sr = librosa.load("data/input/speech.wav", sr=None)

# ===== PARAMETERS =====
bitrate = 4
loss_rate = 0.1
frame_sizes = [128, 256, 512, 1024]

latencies = []
snrs = []

# ===== PIPELINE =====
for frame_size in frame_sizes:
    # Encode
    encoded = encode(audio, frame_size, bitrate)

    # Network (packet loss)
    transmitted = simulate_packet_loss(encoded, loss_rate)

    # Decode
    reconstructed = decode(transmitted)

    # Metrics
    latency = compute_latency(frame_size, sr)
    snr = compute_snr(audio, reconstructed)

    latencies.append(latency)
    snrs.append(snr)

    print(f"Frame: {frame_size}, Latency: {latency:.5f}, SNR: {snr:.2f}")

# ===== PLOT =====
plt.plot(latencies, snrs, marker='o')
plt.xlabel("Latency (seconds)")
plt.ylabel("SNR (dB)")
plt.title("Delay vs Quality")
plt.grid()
plt.savefig("results_plot.png")
plt.savefig("data/output/result.png")
print("Saved graph to data/output/result.png")
