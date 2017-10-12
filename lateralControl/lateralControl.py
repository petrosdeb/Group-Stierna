import laterNavigation as LN
import driving as CRL_CAR
import picamera

LATERALERROR = 10

#Accepted horizontal positioning distance

class LateralControl:
    
    current_position = None
    previous_position = None
    

    def __init__():
        main()

    def main():
        while true:
            capture()
            image = misc.imread('current-image.jpg')
            image = image.astype('float32')
            adapt_steering(LN.find(image))

    def capture():
        camera = picamera.PiCamera()
        camera.resolution = (1024, 768)
        camera.capture('current-image.jpg')

    #Using 512 as the middle of the picture. Since the resolution is 1024. This part need correction due to positive X-axis only.
    def adapt_steering(position):
        while not 512+LATERALERROR> position and position>512-LATERALERROR
            if position > LATERALERROR+512
                steerfactor = 512+position /10
                if steerfactor > 100
                    steerfactor = 100
                else if steerfactor < -100
                    steerfactor = -100
                else if steerfactor < 1 and steerfactor > 0
                    steerfactor =    1
                else if steerfactor > -1 and steerfactor < 0
                    steerfactor = 1
            CRL_CAR.steer(steerfactor)

    #new edge position on image
    def receive_edge_position(data):
        previous_position = current_position
        current_position = data
    
    #return true if position of vehicle has to be adapted
    def should_steer():
        pass

    #return steering angle to be applied to vehicle
    def get_steer():
        pass

