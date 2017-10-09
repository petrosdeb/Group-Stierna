import laterNavigation as LN
import driving as CRL_CAR
import picamera

LATERALERROR = 10

#Accepted horizontal positioning distance

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

def adapt_steering(position):
    while not position+LATERALERROR> position and position>position-LATERALERROR
        if position >LATERALERROR
            steerfactor = position /10
            if steerfactor > 100
                steerfactor = 100
            else if steerfactor < -100
                steerfactor = -100
            else if steerfactor < 1 and steerfactor > 0
                steerfactor =    1
            else if steerfactor > -1 and steerfactor < 0
                steerfactor = 1
        CRL_CAR.steer(steerfactor)


def receive_edge_position():
    pass

def get_steer():
    pass

