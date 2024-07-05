import glob
import os

import imageio
import numpy as np
import torch
from torch.utils.data import Dataset

# Fix seed.
torch.manual_seed(42)


class BSDS500(Dataset):
    """BSDS500 Berkley segmentation image dataset.
    
    This is a simple dataset implementation only loading
    the image data part of the BSDS dataset.
    
    Data augmentation can be enabled by passing a list of transforms.
    
    Args:
        img_dir:
            Folder containing jpeg images.
        transform:
            A composition or a single element from the torchvision.transforms
            module. These transforms can be used for preprocessing and
            image augmentation.
    
    """
    def __init__(self, img_dir: str, transform: torch.nn.Sequential = None):
        self.img_dir = img_dir
        self.transform = transform
        self.img_path_list = glob.glob(os.path.join(img_dir, "*.jpg"))

    def __len__(self):
        return len(self.img_path_list)

    def __getitem__(self, idx):
        """This is called during each iteration.
        
        Args:
            idx: Index of example requested.
        
        Returns:
            Image tensor of shape [C, H, W].
        
        """
        img_path = self.img_path_list[idx]
        img = imageio.imread(img_path).astype(np.float32) / 255
        # Permute to channel-first layout.
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img)
        if self.transform:
            # Apply transforms.
            img = self.transform(img)
            return img
        
        return img
