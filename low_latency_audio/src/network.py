import numpy as np
import random

def simulate_packet_loss(frames, loss_rate):
    out = []
    for f in frames:
        if random.random() < loss_rate:
            out.append(np.zeros_like(f))
        else:
            out.append(f)
    return out
