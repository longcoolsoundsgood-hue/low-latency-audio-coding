import numpy as np

def decode(frames):
    """
    Reconstruct audio signal from list of frames.
    Each frame is assumed to be a numpy array.
    """
    
    # Check if input is empty
    if frames is None or len(frames) == 0:
        print("Warning: No frames to decode")
        return np.array([])
    
    # Convert frames to numpy arrays (in case they are lists)
    processed_frames = []
    for f in frames:
        processed_frames.append(np.array(f))
    
    # Concatenate all frames into one signal
    reconstructed = np.concatenate(processed_frames)
    
    return reconstructed
