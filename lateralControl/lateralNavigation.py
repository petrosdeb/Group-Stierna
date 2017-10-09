'''
Utility class for identifying an edge in an image
'''


from scipy import misc, ndimage
import matplotlib.pyplot as plt
import numpy as np


class image_processor(object):
    image =  None
    x_coordinate = None
    
    def rgb2rg(self, rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    
    def find_line(self, filename):
        
        self.image = misc.imread(filename)
        self.image = self.image.astype('float32')

        sy = ndimage.sobel(self.image, axis=1, mode='constant')

        height = sy.shape[0]
        num_checks = 20
        delta_height = int(height/num_checks)

        curr_height = 0
        cum_indices = []
        for h in range(num_checks):
            line = self.rgb2rg(self, sy[curr_height,:,:])
            indices = []
            for i in range(len(line)):
                slc = line[max(0, i-40):min(len(line)-1, i+40)]

                if np.mean(slc[:15]) == 0 and np.mean(slc[-15:]) == 0 and np.mean(np.abs(slc)) < 20 and not np.mean(np.abs(slc)) == 0 :
                    indices.append(i)
            if len(indices) > 5:
                cum_indices.append( np.mean(indices) )
            curr_height += delta_height

        self.x_coordinate = np.mean(cum_indices)

        return self.x_coordinate
    
    def display_results(self):
        plt.imshow(self.image)
        plt.axvline(x = self.x_coordinate)
        plt.show()
