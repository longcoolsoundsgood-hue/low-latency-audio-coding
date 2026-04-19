import numpy as np
import random

def simulate_packet_loss(frames, loss_rate):
    output = []

    for real, imag in frames:
        if random.random() < loss_rate:
            # mất gói → zero cả real + imag
            output.append((np.zeros_like(real), np.zeros_like(imag)))
        else:
            output.append((real, imag))

    return output
