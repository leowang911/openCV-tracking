# import the necessary packages

import numpy as np
import imutils
import cv2
import xlwt


book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

i=0
j=0
xdata=[]
ydata=[]

Lower = (100, 0, 0)
Upper = (180, 255, 255)

camera = cv2.VideoCapture("highspeed.mp4")



# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, Lower, Upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("mask",mask)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            xdata.append(x)
            ydata.append(y)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


sheet1.write(0,0,"frame")
sheet1.write(0,1, "x")
sheet1.write(0,2, "y")

for x1 in xdata:
    sheet1.write(i+1,0,i)
    sheet1.write(i+1, 1, x1)
    i+=1
for y1 in ydata:
    sheet1.write(j+1, 2, y1)
    j+=1
    
    
book.save("drop_data_opencv.xls")
camera.release()
cv2.destroyAllWindows()

