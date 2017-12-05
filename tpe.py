"""
    Developped by TrAyZeN
"""

import cv2
import numpy as np
import time
import math

# Initialize variables
frameNb = 0
frameTime = [0]
fpsM = 0
xPrev = 0
yPrev = 0
wPrev = 0
hPrev = 0
xCenterPrev = 0
yCenterPrev = 0
zPrev = 0
focalLength = 731.77        # focal length of my camera in pixel
knownWidth = 0.125          # my object width in meter
vMax = 10                   # maximum speed authorized
cap = cv2.VideoCapture(0)

def nothing(x):
    pass

# Create the trackbars window
trackbars = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow("trackbars")

hlt = "Hue Low"
hht = "Hue High"
slt = "Saturation Low"
sht = "Saturation High"
vlt = "Value Low"
vht = "Value High"

# Create trackbars
cv2.createTrackbar(hlt, "trackbars", 0, 179, nothing)
cv2.createTrackbar(hht, "trackbars", 0, 179, nothing)
cv2.createTrackbar(slt, "trackbars", 0, 255, nothing)
cv2.createTrackbar(sht, "trackbars", 0, 255, nothing)
cv2.createTrackbar(vlt, "trackbars", 0, 255, nothing)
cv2.createTrackbar(vht, "trackbars", 0, 255, nothing)

def setTb(hl, hh, sl, sh, vl, vh):
    cv2.setTrackbarPos(hlt, "trackbars", hl)
    cv2.setTrackbarPos(hht, "trackbars", hh)
    cv2.setTrackbarPos(slt, "trackbars", sl)
    cv2.setTrackbarPos(sht, "trackbars", sh)
    cv2.setTrackbarPos(vlt, "trackbars", vl)
    cv2.setTrackbarPos(vht, "trackbars", vh)

# Setting hh, sh, vh to track everything on the screen
setTb(0, 179, 0, 255, 0, 255)

while True:
    ret, frame = cap.read()

    # calculate fps
    frameTime.append(time.time())
    prevframeNb = frameNb - 1
    t = frameTime[frameNb] - frameTime[prevframeNb]     # time between the frame and the previous frame
    fps = 1 / abs(t)        # calculating fps

    if fpsM > 0:
        fpsM = ((frameNb + 1) * fpsM + fps)/(frameNb + 2)       # average fps
    else:
        fpsM = fps

    # Blur the image
    blur = cv2.GaussianBlur(frame, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbars value to define hsvMin and hsvMax
    hLow = cv2.getTrackbarPos(hlt, "trackbars")
    hHigh = cv2.getTrackbarPos(hht, "trackbars")
    sLow = cv2.getTrackbarPos(slt, "trackbars")
    sHigh = cv2.getTrackbarPos(sht, "trackbars")
    vLow = cv2.getTrackbarPos(vlt, "trackbars")
    vHigh = cv2.getTrackbarPos(vht, "trackbars")

    # lower and upper range to track
    hsvMin = np.array([hLow,sLow,vLow])
    hsvMax = np.array([hHigh,sHigh,vHigh])

    mask = cv2.inRange(hsv,hsvMin, hsvMax)
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    result = cv2.bitwise_and(frame,frame, mask = bmask)

    # Contours
    ret, thresh = cv2.threshold(bmask, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, 1, 2)

    if len(contours) > 0:       # Prevent from error when there is no contour
        cnt = contours[-1]
        x,y,w,h = cv2.boundingRect(cnt)
        if w > 40 and h > 40:
            #print x,y,w,h
            cv2.rectangle(result,(x,y),(x+w,y+h),(0,255,0),2)
            # draw the center of the recangle
            xCenter = x+w/2
            yCenter = y+h/2
            cv2.circle(result, (xCenter, yCenter), 2, (0,255,0), 2)
            # rotated rectangle
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(result, [box], 0, (0, 0, 255), 2)

            # calculate distance
            if w > h:
                z = (knownWidth * focalLength) / w
            else:
                z = (knownWidth * focalLength) / h

            # calculate speed
            vector = [abs(xCenterPrev - xCenter), abs(yCenterPrev - yCenter), abs(zPrev - z)]
            vector.append(math.sqrt(vector[0] ** 2 + vector[1] ** 2))
            vector.append(round(math.sqrt(vector[2] ** 2 + vector[3] ** 2), 2))

            echelle = (z * vector[3]) / focalLength
            v = echelle / t
            vKm = round(v * 3.6, 2)
            print "{0} km/h".format(vKm)

            if vKm > vMax:
                print "Slow down"
            else:
                print "Keep your speed"

    fpsStr = str(round(fpsM, 2)) + " fps"
    cv2.putText(frame, fpsStr, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    # Display every windows
    cv2.imshow("original", frame)
    cv2.imshow("trackbars", trackbars)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    frameNb = frameNb + 1
    xPrev = x
    yPrev = y
    wPrev = w
    hPrev = h
    xCenterPrev = xCenter
    yCenterPrev = yCenter
    zPrev = z

    # Keyboard inputs
    k = cv2.waitKey(1) & 0xFF
    if k == 27:             # Press ESC key to quit
        break
    elif k == ord('b'):     # Shortcut to track my blue handspinner :D
        setTb(106, 179, 98, 174, 37, 200)

    elif k == ord('r'):     # Shortcut to reset trackbars
        setTb(0, 179, 0, 255, 0, 255)

cap.release()
cv2.destroyAllWindows()
