import streamlit as st
import librosa
import soundfile as sf
import tempfile
import pandas as pd
import matplotlib.pyplot as plt

from src.encoder import encode
from src.decoder import decode
from src.network import simulate_packet_loss
from src.metrics import compute_latency, compute_snr

st.title("🎧 Low-Latency Audio Coding Demo")

# ===== SIDEBAR =====
st.sidebar.header("⚙️ Parameters")

audio_type = st.sidebar.selectbox("Audio Type", ["speech.wav", "music.wav"])
bitrate = st.sidebar.slider("Bitrate", 2, 8, 4)
loss_rate = st.sidebar.slider("Packet Loss Rate", 0.0, 0.5, 0.1)

frame_sizes = [128, 256, 512, 1024]

# ===== SESSION =====
if "results" not in st.session_state:
    st.session_state.results = None

# ===== RUN =====
if st.sidebar.button("Run Simulation"):

    audio, sr = librosa.load(f"data/input/{audio_type}", sr=None)

    latencies = []
    snrs = []
    audio_outputs = {}

    for fs in frame_sizes:
        encoded = encode(audio, fs, bitrate)
        transmitted = simulate_packet_loss(encoded, loss_rate)
        reconstructed = decode(transmitted)

        latency = compute_latency(fs, sr)
        snr = compute_snr(audio, reconstructed)

        latencies.append(latency)
        snrs.append(snr)

        audio_outputs[fs] = reconstructed

    st.session_state.results = {
        "latencies": latencies,
        "snrs": snrs,
        "audio": audio_outputs,
        "sr": sr,
        "audio_type": audio_type
    }

# ===== DISPLAY =====
if st.session_state.results is not None:

    data = st.session_state.results

    st.subheader("📊 Results")
    df = pd.DataFrame({
        "Frame Size": frame_sizes,
        "Latency (s)": data["latencies"],
        "SNR (dB)": data["snrs"]
    })
    st.dataframe(df)

    st.subheader("📈 Latency vs SNR")
    fig, ax = plt.subplots()
    ax.plot(data["latencies"], data["snrs"], marker='o')
    ax.set_xlabel("Latency (s)")
    ax.set_ylabel("SNR (dB)")
    ax.set_title("Trade-off")

    st.pyplot(fig)

    # ===== AUDIO SELECT (KHÔNG RELOAD) =====
    st.subheader("🎧 Audio Comparison")

    selected_fs = st.selectbox("Select Frame Size", frame_sizes)

    reconstructed = data["audio"][selected_fs]

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, reconstructed, data["sr"])

    st.write(f"Frame Size: {selected_fs}")
    st.audio(temp_file.name)

    st.write("Original Audio")
    st.audio(f"data/input/{data['audio_type']}")

    # ===== INSIGHT =====
    st.subheader("🧠 Insights")

    if loss_rate == 0:
        st.write("No packet loss → quality depends on bitrate & frame size.")
    elif loss_rate < 0.15:
        st.write("Moderate packet loss → noticeable degradation.")
    else:
        st.write("High packet loss → strong distortion.")

    st.write("Larger frame size → better SNR but higher latency.")
