from time import sleep
from picamera import PiCamera
from driving import steer
from nav import *


camera = PiCamera()
camera.resolution = (1024,768)
#camera.start_preview()
#camera.capture('test.jpg')
from scipy import misc, ndimage
import numpy as np

def rgb2rg(rgb):

    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


def find_line(filename):
    image = misc.imread(filename)
    image = image.astype('float32')

    sy = ndimage.sobel(image, axis=1, mode='constant')

    height = sy.shape[0]
    num_checks = 20
    delta_height = int(height/num_checks)

    curr_height = 0
    cum_indices = []
    for h in range(num_checks):
        line = rgb2rg(sy[curr_height,:,:])
        indices = []
        for i in range(len(line)):
            slc = line[max(0, i-40):min(len(line)-1, i+40)]

            if np.mean(slc[:15]) == 0 and np.mean(slc[-15:]) == 0 and np.mean(np.abs(slc)) < 20 and not np.mean(np.abs(slc)) == 0 :
                indices.append(i)
        if len(indices) > 5:
            cum_indices.append( np.mean(indices) )
        curr_height += delta_height

    here = np.mean(cum_indices)

    return here




def take_picture():

    camera.capture("picture.jpg")
    x = find_line("picture.jpg")
    print(x)
    return x

def test_steer():
    while(True):
        sleep(2)
        x = take_picture()
        steer(x/10)



test_steer()







