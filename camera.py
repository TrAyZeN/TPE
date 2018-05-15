from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import numpy as np
import time
import math
from main import *

# Initialize global variables
fpsMax = 30                 # maximum frame per second of the app
focalLength = 731.77        # focal length of my camera in pixel
knownWidth = 0.125          # my object width in meter
vMax = 2                    # maximum speed authorized
hLow = 0
hHigh = 179
sLow = 0
sHigh = 255
vLow = 0
vHigh = 255
xPrev = 0
yPrev = 0
wPrev = 0
hPrev = 0
xCenterPrev = 0
yCenterPrev = 0
zPrev = 0
startTimePrev = 0
selection = 0
contourSelection = 0
contourRotatingSelection = 0

class Camera(Image):

    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        fps = 30
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        global fpsMax, hLow, sLow, vLow, hHigh, sHigh, vHigh, xPrev, yPrev, wPrev, hPrev, xCenterPrev, yCenterPrev, zPrev, startTimePrev, selection, contourSelection, contourRotatingSelection

        ret, frame = self.capture.read()
        self.size = (frame.shape[1], frame.shape[0])
        startTime = time.time()
        deltaTime = startTime - startTimePrev # time between the frame and the previous frame

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower and upper range to track
        hsvMin = np.array([hLow,sLow,vLow])
        hsvMax = np.array([hHigh,sHigh,vHigh])

        mask = cv2.inRange(hsv,hsvMin, hsvMax)
        bmask = cv2.GaussianBlur(mask, (5,5),0)

        # Contours
        ret, thresh = cv2.threshold(bmask, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, 1, 2)

        if len(contours) > 0:       # Prevent from error when there is no contour
            cnt = contours[-1]
            x,y,w,h = cv2.boundingRect(cnt)
            xCenter = x+w/2
            yCenter = y+h/2

            # calculate distance between the camera and the object
            if w > h:
                z = (knownWidth * focalLength) / w
            else:
                z = (knownWidth * focalLength) / h

            # calculate speed
            vector = [abs(xCenterPrev - xCenter), abs(yCenterPrev - yCenter), abs(zPrev - z)]
            vector.append(math.sqrt(vector[0] ** 2 + vector[1] ** 2))
            vector.append(round(math.sqrt(vector[2] ** 2 + vector[3] ** 2), 2))

            scale = (z * vector[3]) / focalLength
            v = scale / deltaTime
            vKm = round(v * 3.6, 2)
            #print("{0} km/h".format(vKm))

            if vKm > vMax:
                print("Slow down")
                if arduino == True:
                    s.write("Slow down")

            elif vKm > 0.5 and vKm < vMax:
                print("Good speed")
                if arduino == True:
                    s.write("Good speed")

            xPrev = x
            yPrev = y
            wPrev = w
            hPrev = h
            xCenterPrev = xCenter
            yCenterPrev = yCenter
            zPrev = z
            startTimePrev = startTime

        if selection == 0:
            if len(contours) > 0:
                if w > 40 and h > 40:
                    if contourSelection == 1:
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        # draw the center of the recangle
                        cv2.circle(frame, (xCenter, yCenter), 2, (0,255,0), 2)
                    if contourRotatingSelection == 1:
                        # rotated rectangle
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.cv.BoxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

            buf1 = cv2.flip(frame, 0)

        elif selection == 1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            bgrEdged = cv2.cvtColor(edged, cv2.COLOR_GRAY2BGR) # convert a single channel image to a 3 channels image

            if len(contours) > 0:
                if w > 40 and h > 40:
                    if contourSelection == 1:
                        cv2.rectangle(bgrEdged,(x,y),(x+w,y+h),(0,255,0),2)
                        # draw the center of the recangle
                        cv2.circle(bgrEdged, (xCenter, yCenter), 2, (0,255,0), 2)
                    if contourRotatingSelection == 1:
                        # rotated rectangle
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.cv.BoxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(bgrEdged, [box], 0, (0, 0, 255), 2)

            buf1 = cv2.flip(bgrEdged, 0)

        elif selection == 2:
            bgrMask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) # convert a single channel image to a 3 channels image

            if len(contours) > 0:
                if w > 40 and h > 40:
                    if contourSelection == 1:
                        cv2.rectangle(bgrMask,(x,y),(x+w,y+h),(0,255,0),2)
                        # draw the center of the recangle
                        cv2.circle(bgrMask, (xCenter, yCenter), 2, (0,255,0), 2)
                    if contourRotatingSelection == 1:
                        # rotated rectangle
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.cv.BoxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(bgrMask, [box], 0, (0, 0, 255), 2)

            buf1 = cv2.flip(bgrMask, 0)

        else:
            buf1 = cv2.flip(frame, 0)

        # convert it to texture
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture
