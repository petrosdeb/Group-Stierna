Description of the files:

test.jpg : This is just a test .jpg image containing a barcode to test the code with.

control.py: 

         main() - initializing picamera, captures images every 0.4 sec. Then it uses
                  adapt_steering(get_xposition(captured_image)) to steer the moped. This will loop until
                  the process is terminated.

         adapt_steering(x-value) - takes a x-value and sets direction of steering depending on value.

navigation.py:

         test(image) - takes a image as param and runs get_xposition, returns the x-position of the barcode
                   if there is a barcode detected. 
                   Tips: Use test.jpg to test the code.

         get_xposition(image) - takes a image as param, returns the x-position of the barcode if there is a 
                  barcode detected. To open a preview of the picture with the barcode marked change "DESKTOPMODE = True ".
         
         
