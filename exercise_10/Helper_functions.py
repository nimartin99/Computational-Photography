# Helper functions
import os
from tqdm import tqdm
import numpy as np
import math
import cv2
import struct
from skimage.io import imread
import matplotlib.pyplot 
#-------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------
def import_bin_files(path: str)->np.ndarray:
    """Reads the.bin image at the given path in form of an ndarray
    Args:
        path:
            Full path to the .bin image that will be read.
    Returns:
            A float32 image of shape [H, W, C]
    """
    with open(path, 'rb') as fid:
        #read from buffer the header  
        header_bytes = fid.read( 3*4)  # read 3 integers       
        data_array = np.frombuffer(header_bytes, np.int32)
        #print("\ndata_array:\n",data_array)
        #print("\nshape",data_array.shape)
        H=data_array[0]
        #print("\nH:",H)
        W=data_array[1]
        #print("W:",W)
        C=data_array[2]
        #print("C:", C)
        image=np.zeros([H,W,C],dtype=np.float32)
        for i in range (C):
            data_bytes = fid.read(H*W*4)  # read next buffer, already skips the header
            data= np.frombuffer(data_bytes, dtype=np.float32, count=H*W)
            image[:,:,i]=data.reshape([H,W])#reshape
            #print("\nimage:\n",image, ", shape:", image.shape)
    fid.close()
   
    return image 

#------------------------------------------------------------------------------------------------------------- 
def create_image_dataset(path:str)->np.ndarray:
    """Creates an image dataset from images read by import_bin-files
    Args:
        path:
            Full path to the .bin image that will be read.
    Returns:
            A float32 image dataset of shape [8,32, H, W, C]
    """
    image_dataset=np.zeros([8,32,196,200,3])
    
    for i in range(8):
        for j in range(32):
            filename = os.path.join(path, "rf_{y:03d}_{x:03d}.bin".format(y=i, x=j))
            #filename=str('rf_'+'{0:03}'.format(i)+'_'+'{0:03}'.format(j)+'.bin')
            #print(filename)
            #filename=str(Path+filename)
            
            image=import_bin_files(filename)
            
            image_dataset[i,j,:,:,:]=image
            
    return image_dataset

#--------------------------------------------------------------------------------------------------------------
def write_bin(image:np.ndarray, path:str):
    """Writes an np.ndarray into a .bin file on the given path
    Args:
        image:
              Image that will be written as a .bin file.
        path:
            Full location path where the .bin file will be written .
    Returns:
          
    """

    with open(path, 'wb') as f:
       l = image.shape[0]*image.shape[1]*image.shape[2]
       print("l:",l)

       header = np.array([image.shape[0], image.shape[1], image.shape[2]])
       print("header:",header)
       header_bin = struct.pack("I"*3, *header)
       f.write(header_bin)

       image_bin = struct.pack("f"*l,*np.reshape(image, (l,1), order='F'))
       print("image_bin shape:",len(image_bin))
       f.write(image_bin)
    
       f.close()

#--------------------------------------------------------------------------------------------------------------

def tp2xyz(theta: int, phi: int) -> np.ndarray:
    """Generate a properly rotated and scaled vector which points into the direction of the light source for any given pair
           of angles theta and phi.
    Args:
        theta:
              int value defines elevation.
        phi:
            int value defines rotation direction.
    Returns:
          Lighting direction vector of shape [1,3]
    """
    # create a vector from the angles
    x = math.cos(phi) * math.sin(theta)
    y = math.sin(phi) * math.sin(theta)
    z = math.cos(theta)
    v = np.array([x, y, z])
    # set up a rotation matrix
    M = np.eye(4)
    # rotate around Y axis 90 degrees
    # cos(pi/2)
    ca = 0
    # sinus(pi/2)
    sa = 1.0
    M1 = np.array([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])
    # rotate around X axis -90 degrees
    # cos(-pi/2)
    ca = 0
    # sin(-pi/2)
    sa = -1.0
    M2 = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
    # now transform the vector
    rv = M1 @ M2 @ v
    return rv
#--------------------------------------------------------------------------------------------------------------

def read_bin(path:str):
    """Reads the.bin file that is written with write_bin file
    Args:
        path:
            Full path to the .bin image that will be read.
    """
    # Define width and height
    w, h, c = 196,200,3
    exported_image=np.zeros([h,w,c])
    # Read file using numpy "fromfile()"
    with open(path, mode='rb') as f:
        for i in range(c):
            exported_image[:,:,i] = np.fromfile(f,dtype=np.float32,count=w*h).reshape([h,w])
#[h,w,c]
    return exported_image

# ALTERNATIVE IMPLEMENTATIONS---------------------------------------------------------------------------------
'''
#-------------------------------------------------------------------------------------------------------------   
def import_bin_files3(filename):

    # Define width and height
    w, h, c = 196,200,3

    # Read file using numpy "fromfile()"
    with open(filename, mode='rb') as f:
        exported_image = np.fromfile(f,dtype=np.float32,count=w*h).reshape(h,w)

    return exported_image
#--------------------------------------------------------------------------------------------------------------
def import_bin_files4(file_path: str) -> np.ndarray:
    """Exemplary implementation of binary file reading with header.
  Args:
    file_path:
        Path of .bin file.
  Returns:
    Float image.
  """
    with open(file_path, 'rb') as file_handle:
            
        header_bytes = file_handle.read(4 * 3)  # read 3 integers
        header = np.frombuffer(header_bytes, dtype=np.uint32)  # interpret as int
        h, w, c = header[0], header[1], header[2]  # TODO: might be different order?
        
        image_bytes = file_handle.read()  # read the rest of the file
        image = np.frombuffer(image_bytes, dtype=np.float32, count=h*w*c)  # interpret as float
        #print("image shape:", image.shape)
        image = image.reshape([h, w, c])  # reshape according to header information
        #print("image shape:", image.shape)

        
    return image
'''

