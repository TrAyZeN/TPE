from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import numpy as np
import time
import math
from main import *

# Initialize global variables
fps = 30                        # refresh rate of the app
FOCAL_LENGTH = 731.77           # focal length of my camera in pixel
OBJECT_WIDTH = 0.125            # my object width in meter
MAX_SPEED = 2                   # maximum speed authorized
hue_low = 0
hue_high = 179
saturation_low = 0
saturation_high = 255
value_low = 0
value_high = 255
prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0
prev_x_center = 0
prev_y_center = 0
prev_z = 0
prev_start_time = 0
selection = 0
contour_selection = 0
rotating_contour_selection = 0
x = 0
y = 0
w = 0
h = 0

class Camera(Image):

    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        global hue_low, saturation_low, value_low, hue_high, saturation_high,\
            value_high,prev_x, prev_y, prev_w, prev_h, prev_x_center,\
            prev_y_center, prev_z, prev_start_time, x, y, w, h

        ret, frame = self.capture.read()
        self.size = (frame.shape[1], frame.shape[0])
        start_time = time.time()
        delta_time = start_time - prev_start_time # time between the frame and the previous frame

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower and upper range to track
        hsv_min = np.array([hue_low,saturation_low,value_low])
        hsv_max = np.array([hue_high,saturation_high,value_high])

        mask = cv2.inRange(hsv,hsv_min, hsv_max)
        bmask = cv2.GaussianBlur(mask, (5,5),0)

        # Contours
        ret, thresh = cv2.threshold(bmask, 127, 255, 0)
        _, contours, _ = cv2.findContours(thresh, 1, 2)

        if len(contours) > 0:       # Prevent from error when there is no contour
            self.cnt = contours[-1]
            x, y, w, h = cv2.boundingRect(self.cnt)
            self.xCenter = x + w/2
            self.yCenter = y + h/2

            # calculate distance between the camera and the object
            if w > h:
                z = (OBJECT_WIDTH*FOCAL_LENGTH) / w
            else:
                z = (OBJECT_WIDTH*FOCAL_LENGTH) / h

            # calculate speed
            vector = [abs(prev_x_center - self.xCenter), abs(prev_y_center - self.yCenter), abs(prev_z - z)]
            vector.append(math.sqrt(vector[0]**2 + vector[1]**2))
            vector.append(round(math.sqrt(vector[2]**2 + vector[3]**2), 2))

            scale = (z*vector[3]) / FOCAL_LENGTH
            v = scale / delta_time
            speed_km = round(v * 3.6, 2)
            #print("{0} km/h".format(speed_km))

            if speed_km > MAX_SPEED:
                print("slow down")
                if arduino == True:
                    s.write("slow down")

            elif speed_km > 0.5 and speed_km < MAX_SPEED:
                print("Good speed")
                if arduino == True:
                    s.write("Good speed")

            prev_x = x
            prev_y = y
            prev_w = w
            prev_h = h
            prev_x_center = self.xCenter
            prev_y_center = self.yCenter
            prev_z = z
            prev_start_time = start_time

        if selection == 0:
            self.draw_contours(contours, frame)      # variable x referenced before assignement
            buf1 = cv2.flip(frame, 0)

        elif selection == 1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            bgrEdged = cv2.cvtColor(edged, cv2.COLOR_GRAY2BGR) # convert a single channel image to a 3 channels image

            self.draw_contours(contours, bgrEdged)
            buf1 = cv2.flip(bgrEdged, 0)

        elif selection == 2:
            bgrMask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) # convert a single channel image to a 3 channels image

            self.draw_contours(contours, bgrMask)
            buf1 = cv2.flip(bgrMask, 0)

        else:
            buf1 = cv2.flip(frame, 0)

        # convert it to texture
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

    def draw_contours(self, contours, frame):
        if len(contours) > 0:
            #global x, y, w, h
            if w > 40 and h > 40:
                if contour_selection == 1:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                    # draw the center of the recangle
                    cv2.circle(frame, (self.xCenter, self.yCenter), 2, (0,255,0), 2)
                if rotating_contour_selection == 1:
                    # rotated rectangle
                    rect = cv2.minAreaRect(self.cnt)
                    box = cv2.boxPoints(rect) # cv.
                    box = np.int0(box)
                    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
