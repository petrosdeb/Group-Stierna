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
        while True:
            capture()
            adapt_steering(LN.getXPosition('current-image.jpg'))

    def capture():
        camera = picamera.PiCamera()
        camera.resolution = (1024, 768)
        camera.capture('current-image.jpg')

    #Using 512 as the middle of the picture. Since the resolution is 1024. This part need correction due to positive X-axis only.
    def adapt_steering(position):
        while not 512+LATERALERROR> position and position>512-LATERALERROR:
            if position > LATERALERROR+512:
                steerfactor = 512+position /10
                if steerfactor > 100:
                    steerfactor = 100
                elif steerfactor < -100:
                    steerfactor = -100
                elif steerfactor < 1 and steerfactor > 0:
                    steerfactor = 1
                elif steerfactor > -1 and steerfactor < 0:
                    steerfactor = 1
            CRL_CAR.steer(steerfactor)
    
    #the steering has to depend on the current position in relation to the preceding car, the current position, the time delta between the pictures and the distance to the preceding car
def modified_adapt_steering(current_pos, prev_pos, time, distance):
    #we control let the first turning rate we receive be the maximal and let that represent 100
    #on the scale of -100 to 100 on the steering, the value on the steer is the percentage of the maximal turning rate
    turning_rate = (current_pos - prev_pos)/time
    if(abs(turning_rate) > maximal_turning_rate):
        maximal_turning_rate = abs(turning_rate)
        
    steer_value = 100*turning_rate/maximal_turning_rate
    steer(steer_value)
    
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

