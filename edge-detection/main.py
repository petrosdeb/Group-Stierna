'''
Module for identifying an edge between two different colors
'''

from scipy import misc, ndimage
import matplotlib.pyplot as plt
import numpy as np

def rgb2rg(rgb):
    '''
    returns the dot-product
    '''
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def find_line(filename):
    '''
    Takes a filename as input and returns the x-position of the edge,
    as well as displaying it in a pop-up image
    '''
    image = misc.imread(filename)
    image = image.astype('float32')

    sy_sobel = ndimage.sobel(image, axis=1, mode='constant')

    height = sy_sobel.shape[0]
    num_checks = 20
    delta_height = int(height/num_checks)

    curr_height = 0
    cum_indices = []
    amount = 0
    while amount < range(num_checks):
        amount += 1
        line = rgb2rg(sy_sobel[curr_height, :, :])
        indices = []
        for i in range(len(line)):
            slc = line[max(0, i-40):min(len(line)-1, i+40)]

            if np.mean(slc[:15]) == 0 and np.mean(slc[-15:]) == 0 and np.mean(np.abs(slc)) < 20:
                if not np.mean(np.abs(slc)) == 0:
                    indices.append(i)
        if len(indices) > 5:
            cum_indices.append(np.mean(indices))
        curr_height += delta_height
    here = np.mean(cum_indices)

    plt.imshow(image)
    plt.axvline(x=here)
    plt.show()
    return here


find_line('djungle-lady.jpg')
find_line('putin-lady.jpg')
find_line('intersection-lady.jpg')
find_line('vinslov-my-lady.jpg')
