import streamlit as st
import librosa
import soundfile as sf
import tempfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.encoder import encode
from src.decoder import decode
from src.network import simulate_packet_loss
from src.metrics import compute_latency, compute_snr

# ===== TITLE =====
st.title("🎧 Low-Latency Audio Coding Demo")

st.markdown("""
Interactive demo to explore the trade-off between **latency** and **audio quality (SNR)**.
Adjust parameters and observe results in real time.
""")

# ===== INPUT =====
st.sidebar.header("⚙️ Parameters")

audio_type = st.sidebar.selectbox("Audio Type", ["speech.wav", "music.wav"])
bitrate = st.sidebar.slider("Bitrate", 2, 8, 4)
loss_rate = st.sidebar.slider("Packet Loss Rate", 0.0, 0.5, 0.1)

frame_sizes = [128, 256, 512, 1024]

# ===== RUN BUTTON =====
if st.sidebar.button("Run Simulation"):

    st.subheader("⏳ Processing...")

    # Load audio
    audio, sr = librosa.load(f"data/input/{audio_type}", sr=None)

    latencies = []
    snrs = []

    # ===== RUN FULL TEST =====
    for fs in frame_sizes:
        encoded = encode(audio, fs, bitrate)
        transmitted = simulate_packet_loss(encoded, loss_rate)
        reconstructed = decode(transmitted)

        latency = compute_latency(fs, sr)
        snr = compute_snr(audio, reconstructed)

        latencies.append(latency)
        snrs.append(snr)

    # ===== TABLE =====
    st.subheader("📊 Results Table")

    df = pd.DataFrame({
        "Frame Size": frame_sizes,
        "Latency (s)": latencies,
        "SNR (dB)": snrs
    })

    st.dataframe(df)

    # ===== GRAPH =====
    st.subheader("📈 Latency vs SNR")

    fig, ax = plt.subplots()
    ax.plot(latencies, snrs, marker='o')
    ax.set_xlabel("Latency (seconds)")
    ax.set_ylabel("SNR (dB)")
    ax.set_title("Trade-off: Latency vs Quality")

    st.pyplot(fig)

    # ===== SELECT FRAME TO LISTEN =====
    st.subheader("🎧 Audio Comparison")

    selected_fs = st.selectbox("Select Frame Size to Listen", frame_sizes)

    encoded = encode(audio, selected_fs, bitrate)
    transmitted = simulate_packet_loss(encoded, loss_rate)
    reconstructed = decode(transmitted)

    # Save temp audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, reconstructed, sr)

    st.write(f"Frame Size: {selected_fs}")
    st.audio(temp_file.name)

    st.write("Original Audio")
    st.audio(f"data/input/{audio_type}")

    # ===== INSIGHT =====
    st.subheader("🧠 Insights")

    if loss_rate == 0:
        st.write("No packet loss → quality mainly depends on bitrate and frame size.")
    elif loss_rate < 0.15:
        st.write("Moderate packet loss → noticeable degradation.")
    else:
        st.write("High packet loss → strong degradation and audio distortion.")

    st.write("Larger frame sizes improve SNR but increase latency.")