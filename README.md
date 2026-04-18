# Low-Latency Audio Coding Demo

This project implements a simplified audio coding system to study the trade-off between latency and audio quality in communication systems.

The system includes encoding, packet loss simulation, decoding, and evaluation using Signal-to-Noise Ratio (SNR) and latency.

## Features

- Frame-based audio processing
- Frequency-domain encoding using FFT
- Packet loss simulation
- Latency estimation
- SNR (Signal-to-Noise Ratio) evaluation
- Interactive demo using Streamlit

## System Overview

The processing pipeline:

Audio → Frame segmentation → FFT → Quantization → Packet Loss Simulation → Decoding (iFFT) → Output audio

## Key Parameters

- Bitrate: Controls quantization level
- Frame size: Affects latency and frequency resolution
- Packet loss rate: Simulates network conditions

## Metrics

- Latency:
  Estimated as frame_size / sample_rate

- SNR:
  Measures the quality of reconstructed audio compared to the original

## Trade-off

- Smaller frame size:
  - Lower latency
  - Lower audio quality

- Larger frame size:
  - Higher latency
  - Better audio quality

- Higher packet loss:
  - Significant degradation in audio quality

## Project Structure
low-latency-audio-coding/
│
├── app.py
├── requirements.txt
│
├── src/
│ ├── encoder.py
│ ├── decoder.py
│ ├── network.py
│ ├── metrics.py
│ └── main.py
│
├── data/
│ ├── input/
│ └── output/

## Installation

Clone the repository:
git clone https://github.com/longcoolsoundsgood-hue/low-latency-audio-coding.git
cd low-latency-audio-coding

Install dependencies:
pip install -r requirements.txt

## Run the Interactive Demo
streamlit run app.py

Then open the browser at:
http://localhost:8501

## How to Use

1. Select audio type (speech or music)
2. Adjust bitrate
3. Set packet loss rate
4. Run simulation
5. View:
   - Results table
   - Latency vs SNR graph
   - Reconstructed audio
   - Original audio

## Observations

- Increasing frame size improves SNR due to better frequency resolution
- Packet loss significantly reduces audio quality
- Music signals are more sensitive to packet loss than speech
- There is a clear trade-off between latency and audio quality

## Notes

This is a simplified codec for educational purposes. It does not include advanced techniques such as psychoacoustic modeling or compression standards like MP3 or AAC.

## Author

Truong Tuan Kiet 202414631
Vu Hai Long 202414639
