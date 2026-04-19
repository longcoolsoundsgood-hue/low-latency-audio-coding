import librosa
import matplotlib.pyplot as plt
import soundfile as sf
import os

from encoder import encode
from network import simulate_packet_loss
from decoder import decode
from metrics import compute_latency, compute_snr

print("=== AUDIO CODING TEST SYSTEM ===")

bitrate = int(input("Enter bitrate (2,4,8): "))
loss_rate = float(input("Enter packet loss rate (0→1): "))

files = ["speech.wav", "music.wav"]
frame_sizes = [128, 256, 512, 1024]

os.makedirs("data/output", exist_ok=True)

for file in files:
    print(f"\n===== Processing {file} =====")

    audio, sr = librosa.load(f"data/input/{file}", sr=None)

    latencies = []
    snrs = []

    for fs in frame_sizes:
        encoded = encode(audio, fs, bitrate)
        transmitted = simulate_packet_loss(encoded, loss_rate)
        reconstructed = decode(transmitted)

        latency = compute_latency(fs, sr)
        snr = compute_snr(audio, reconstructed)

        latencies.append(latency)
        snrs.append(snr)

        print(f"Frame {fs}: Latency={latency:.5f}s | SNR={snr:.2f}dB")

    # save audio cuối cùng
    sf.write(f"data/output/reconstructed_{file}", reconstructed, sr)

    # plot
    plt.figure()
    plt.plot(latencies, snrs, marker='o')
    plt.xlabel("Latency (s)")
    plt.ylabel("SNR (dB)")
    plt.title(f"Latency vs SNR ({file})")
    plt.grid()

    plt.savefig(f"data/output/result_{file}.png")

print("\n=== DONE ===")
