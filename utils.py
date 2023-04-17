import matplotlib.image as mpimg
import numpy as np
from copy import copy

def load_image(path):
    org_image = mpimg.imread(path)
    if np.max(org_image) <= 1:
        org_image *= 255
        org_image = org_image.astype(np.uint8)
    return org_image


def reduce_rgb_values(image, r_value):
    image = copy(image)
    height, width, channel = image.shape
    for h in range(height):
        for w in range(width):
            for c in range(channel):
                value = image[h, w, c]
                difference = value % r_value
                if difference < r_value/2:
                    value -= difference
                else:
                    value += (r_value - difference)
                if value > 255:
                    value -= r_value
                image[h, w, c] = value
                
    return image


def filling_zeros(binary, n):
    difference = (n - len(binary))*"0"
    return difference + binary
