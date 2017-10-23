#### Code for BARCODE detection  ######
import cv,sys

def __init__():
    test()

#Test-function to test getXPosition(filename)
# Param: image with a possible barcode
# Output: Will print the calculated x-value
def test():
    x=getXPosition('typ.jpg')
    print(x)

def getXPosition(image):

    imgco = cv.LoadImage(image)
    img=cv.CreateImage(cv.GetSize(imgco),8,1)
    imgx = cv.CreateImage(cv.GetSize(img),cv.IPL_DEPTH_16S,1)
    imgy = cv.CreateImage(cv.GetSize(img),cv.IPL_DEPTH_16S,1)
    thresh = cv.CreateImage(cv.GetSize(img),8,1)

    ### Convert image to grayscale ###
    cv.CvtColor(imgco,img,cv.CV_BGR2GRAY)

    ### Finding horizontal and vertical gradient ###
    cv.Sobel(img,imgx,1,0,3)
    cv.Abs(imgx,imgx)
    cv.Sobel(img,imgy,0,1,3)
    cv.Abs(imgy,imgy)
    cv.Sub(imgx,imgy,imgx)
    cv.ConvertScale(imgx,img)

    ### Low pass filtering ###
    cv.Smooth(img,img,cv.CV_GAUSSIAN,7,7,0)

    ### Applying Threshold ###
    cv.Threshold(img,thresh,100,255,cv.CV_THRESH_BINARY)
    cv.Erode(thresh,thresh,None,2)
    cv.Dilate(thresh,thresh,None,5)

    ### Contour finding with max. area ###
    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(thresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    area = 0
    while contour:
        max_area = cv.ContourArea(contour)
        if max_area>area:
            area = max_area
            bar = list(contour)
        contour=contour.h_next()

    ### If the code sould be used without a graphical interface
    ### some code below needs to be removed
    ### Draw bounding rectangles ###
    bound_rect = cv.BoundingRect(bar)
    pt1 = (bound_rect[0], bound_rect[1])
    pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
    cv.Rectangle(imgco, pt1, pt2, cv.CV_RGB(0,255,255), 2)
    pt = ((pt2[0]-pt1[0]),(pt2[1]-pt1[1]))
    middle = ((pt[0]/2+pt1[0]),(pt[1]/2+pt1[1]))
    cv.ShowImage('img',imgco)
    cv.WaitKey(0)
    return middle[0]

test()