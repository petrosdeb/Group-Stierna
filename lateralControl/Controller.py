
from builtins import print
from lateralControl import lateralNavigation

from lateralControl import LateralControl as lateral_control

from driving import steer
from nav import *

from time import sleep

from picamera import PiCamera


'''
Initially meant for lateral control. Interacts with the LateralControl, which represents the model, and driving, 
where the interaction with the system takes place.
Can be expanded to handle longitudional control aswell.
'''

class Controller:
    camera = PiCamera()
    edge = lateralNavigation.image_processor()
    lc = lateral_control()
    
    def init_camera(self):
        self.camera.resolution = (1024, 768)
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        
    def capture_image(self):
        self.camera.capture('latest.jpg')
    
    def capture_sequence(self):
        pass
    
    '''
    path to image file, the position of the edge is returned
    '''
    def get_edge_position(self, path):
        return self.edge.find_line(path)
    
    '''
    steer of the MOPED is set. The wanted steering angle is calculated in LateralControl
    '''
    def set_steer(self):
        steer(lc.get_steer())
    
    def send_to_model(self, data):
        lc.receive_edge_position(data)
    
    '''
    Integrate with longitudional
    '''
    def run(self):
        self.init_camera(self)
        while True:
            self.capture_image()
            self.send_to_model(self, self.get_edge_position(self, 'latest.jpg'))
            if lc.should_steer():
                #keep constant speed
                self.set_steer(self)
            else:
                #apply acc, but must not stay here. Parallelize computations if possible