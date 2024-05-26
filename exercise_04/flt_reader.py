"""Load .flt images"""
import struct
import numpy as np


def read_flt_image(flt_path):
    with open(flt_path, "rb") as f:
        header = f.read(4 * 3)
        height, width, channels = struct.unpack("III", header)
        result = np.zeros([height, width, channels], dtype=np.float32)
        for c in range(channels):
            buffer = f.read(height * width * 4)
            channel = np.frombuffer(
                buffer,
                dtype=np.float32,
            ).reshape([height, width], order="C")

            result[:, :, c] = channel
        return result
