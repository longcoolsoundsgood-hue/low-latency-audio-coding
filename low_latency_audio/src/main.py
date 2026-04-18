import librosa
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
import os

from encoder import encode
from network import simulate_packet_loss
from decoder import decode
from metrics import compute_latency, compute_snr

# ===== USER INPUT =====
print("=== AUDIO CODING TEST SYSTEM ===")
bitrate = int(input("Enter bitrate (e.g. 2, 4, 8): "))
loss_rate = float(input("Enter packet loss rate (0 → 1): "))

# ===== FILES =====
files = ["speech.wav", "music.wav"]

# ===== PARAMETERS =====
frame_sizes = [128, 256, 512, 1024]

# Create output folder if not exists
os.makedirs("data/output", exist_ok=True)

# ===== MAIN LOOP =====
for file in files:
    print(f"\n===== Processing {file} =====")

    audio, sr = librosa.load(f"data/input/{file}", sr=None)

    latencies = []
    snrs = []

    for frame_size in frame_sizes:
        # Encode
        encoded = encode(audio, frame_size, bitrate)

        # Simulate network
        transmitted = simulate_packet_loss(encoded, loss_rate)

        # Decode
        reconstructed = decode(transmitted)

        # Metrics
        latency = compute_latency(frame_size, sr)
        snr = compute_snr(audio, reconstructed)

        latencies.append(latency)
        snrs.append(snr)

        print(f"Frame: {frame_size}, Latency: {latency:.5f}, SNR: {snr:.2f}")

    # ===== SAVE AUDIO =====
    output_audio_path = f"data/output/reconstructed_{file}"
    sf.write(output_audio_path, reconstructed, sr)
    print(f"Saved audio to {output_audio_path}")

    # ===== PLAY AUDIO =====
    print("Playing reconstructed audio...")
    sd.play(reconstructed, sr)
    sd.wait()

    # ===== PLOT =====
    plt.figure()
    plt.plot(latencies, snrs, marker='o')
    plt.xlabel("Latency (seconds)")
    plt.ylabel("SNR (dB)")
    plt.title(f"Delay vs Quality ({file})")
    plt.grid()

    output_plot_path = f"data/output/result_{file}.png"
    plt.savefig(output_plot_path)
    print(f"Saved graph to {output_plot_path}")

print("\n=== DONE ===")
