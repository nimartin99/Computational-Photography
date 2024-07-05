"""Utility functions to add image noise."""

import numpy as np


def add_gaussian_noise(image: np.ndarray,
                       mean: float = 0,
                       sigma: float = 0.1,
                       color: bool = True) -> np.ndarray:
    """Add gaussian noise to an image.
    
    Args:
        image:
            Input (clean) image.
            This is expected to be a floating point image with ranges between 0 and 1.
        mean:
            Mean of gaussian distribution.
        sigma:
            standard deviation of gaussian distribution.
        color:
            Output different noise in all channels.
            If false only greyscale noise is added.

    Returns:
        Noisy image as np array.
    """
    if color:
        target_shape = image.shape
    else:
        target_shape = tuple(list(image.shape[:-1]) + [1])
    noise = np.random.normal(mean, sigma, target_shape)

    return np.clip(image + noise, 0, 1)
