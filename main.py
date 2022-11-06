import numpy as np
from PIL import Image
import sys

def read(path):
    data = Image.open(path)
    data.load()
    array = np.asarray(data)
    data.close()
    return array

def write(path, array):
    data = Image.fromarray(array, "RGBA")
    data.save(path)

def convert_bw(array):
    shape = array.shape
    array = array.reshape((-1, 4))
    size = array.shape[0]
    greys = np.mean(array[:, :3], axis = 1)
    greys = greys.reshape((size, 1))
    greys = np.tile(greys, (1,3))
    array[:, :3] = greys
    array = array.reshape(shape)
    return array

def main():
    argc = len(sys.argv)
    if(argc < 3):
        print("Use: python3 main.py in_file out_file")
    in_file = str(sys.argv[1])
    out_file = str(sys.argv[2])
    array = read(in_file)
    array = convert_bw(array)
    write(out_file, array)

main()