"""
    Developped by TrAyZeN
    This programm is under developpement
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import *
import cv2
import numpy as np
import time
import math
import serial

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Config.set('graphics', 'resizable', '0')

# Initialize global variables
selection = 0
contourSelection = 0
contourRotatingSelection = 0
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
frameTimePrev = 0
focalLength = 731.77        # focal length of my camera in pixel
knownWidth = 0.125          # my object width in meter

class RootWidget(Widget):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        with self.canvas:
            # draw the background
            Color(90/255.0, 92/255.0, 94/255.0, mode='rgb')
            Rectangle(pos=(0, 0), size=(1024, 768))
            # draw a frame for the image
            Color(0, 0, 0, mode='rgb')
            Rectangle(pos=(17, 265), size=(646, 486))

        self.cam = Camera(pos=(20, 268))
        self.add_widget(self.cam)

        def updateBut():
            if selection != 0:
                butFrameSkin.unselect()
            if selection != 1:
                butEdgeSkin.unselect()
            if selection != 2:
                butMaskSkin.unselect()

        # button frame
        def pressButFrame(instance):
            global selection
            selection = 0
            butFrameSkin.select()
            updateBut()

        butFrame = Button(pos=(40, 200), size=(40, 40))
        butFrame.bind(on_press=pressButFrame)
        labFrame = Label(text='Frame', pos=(74, 170), font_name='calibri', font_size=20)
        butFrameSkin = buttonSkin(pos=butFrame.pos, size=butFrame.size)
        butFrameSkin.select()

        # button canny edge
        def pressButEdge(instance):
            global selection
            selection = 1
            butEdgeSkin.select()
            updateBut()

        butEdge = Button(pos=(40, 150), size=(40, 40))
        butEdge.bind(on_press=pressButEdge)
        labEdge = Label(text='Canny edge', pos=(97, 120), font_name='calibri', font_size=20)
        butEdgeSkin = buttonSkin(pos=butEdge.pos, size=butEdge.size)

        # button mask
        def pressButMask(instance):
            global selection
            selection = 2
            butMaskSkin.select()
            updateBut()

        butMask = Button(pos=(40, 100), size=(40, 40))
        butMask.bind(on_press=pressButMask)
        labMask = Label(text='Mask', pos=(70, 70), font_name='calibri', font_size=20)
        butMaskSkin = buttonSkin(pos=butMask.pos, size=butMask.size)

        # button contour
        def pressButCnt(instance):
            global contourSelection
            if contourSelection == 0:
                contourSelection = 1
                butCntSkin.select()
            else:
                contourSelection = 0
                butCntSkin.unselect()

        butCnt = Button(pos=(240, 200), size=(40, 40))
        butCnt.bind(on_press=pressButCnt)
        labCnt = Label(text='Contour', pos=(280, 170), font_name='calibri', font_size=20)
        butCntSkin = buttonSkin(pos=butCnt.pos, size=butCnt.size)

        # button rotating contour
        def pressButRotCnt(instance):
            global contourRotatingSelection
            if contourRotatingSelection == 0:
                contourRotatingSelection = 1
                butRotCntSkin.select()
            else:
                contourRotatingSelection = 0
                butRotCntSkin.unselect()

        butRotCnt = Button(pos=(240, 150), size=(40, 40))
        butRotCnt.bind(on_press=pressButRotCnt)
        labRotCnt = Label(text='Rotating Contour', pos=(320, 120), font_name='calibri', font_size=20)
        butRotCntSkin = buttonSkin(pos=butRotCnt.pos, size=butRotCnt.size)

        # slider hue low
        def sliderHlMove(instance, value):
            global hLow
            if value > sliderHh.value:
                sliderHl.value = sliderHh.value
            hLow = int(sliderHl.value)
            labNum1.text = str(hLow)

        sliderHl = Slider(range=(0,179), value=0, pos=(680,640), size=(200,100), sensitivity='handle')
        sliderHl.bind(value=sliderHlMove)

        # slider hue high
        def sliderHhMove(instance, value):
            global hHigh
            if value < sliderHl.value:
                sliderHh.value = sliderHl.value
            hHigh = int(sliderHh.value)
            labNum2.text = str(hHigh)

        sliderHh = Slider(range=(0,179), value=179, pos=(680,580), size=(200,100), sensitivity='handle')
        sliderHh.bind(value=sliderHhMove)

        # slider saturation low
        def sliderSlMove(instance, value):
            global sLow
            if value > sliderSh.value:
                sliderSl.value = sliderSh.value
            sLow = int(sliderSl.value)
            labNum3.text = str(sLow)

        sliderSl = Slider(range=(0,255), value=0, pos=(680,520), size=(200,100), sensitivity='handle')
        sliderSl.bind(value=sliderSlMove)

        # slider saturation high
        def sliderShMove(instance, value):
            global shigh
            if value < sliderSl.value:
                sliderSh.value = sliderSl.value
            sHigh = int(sliderSh.value)
            labNum4.text = str(sHigh)

        sliderSh = Slider(range=(0,255), value=255, pos=(680,460), size=(200,100), sensitivity='handle')
        sliderSh.bind(value=sliderShMove)

        # slider value low
        def sliderVlMove(instance, value):
            global vLow
            if value > sliderVh.value:
                sliderVl.value = sliderVh.value
            vLow = int(sliderVl.value)
            labNum5.text = str(vLow)

        sliderVl = Slider(range=(0,255), value=0, pos=(680,400), size=(200,100), sensitivity='handle')
        sliderVl.bind(value=sliderVlMove)

        # slider value high
        def sliderVhMove(instance, value):
            global vHigh
            if value < sliderVl.value:
                sliderVh.value = sliderVl.value
            vHigh = int(sliderVh.value)
            labNum6.text = str(vHigh)

        sliderVh = Slider(range=(0,255), value=255, pos=(680,340), size=(200,100), sensitivity='handle')
        sliderVh.bind(value=sliderVhMove)

        labSlider1 = Label(text='Hue Low', pos=(900, 640), font_name='calibri', font_size=20)
        labSlider2 = Label(text='Hue High', pos=(900, 580), font_name='calibri', font_size=20)
        labSlider3 = Label(text='Saturation Low', pos=(905, 520), font_name='calibri', font_size=20)
        labSlider4 = Label(text='Saturation High', pos=(905, 460), font_name='calibri', font_size=20)
        labSlider5 = Label(text='Value Low', pos=(900, 400), font_name='calibri', font_size=20)
        labSlider6 = Label(text='Value High', pos=(900, 340), font_name='calibri', font_size=20)
        labNum1 = Label(text=str(int(sliderHl.value)), pos=(655, 665), font_name='calibri', font_size=20)
        labNum2 = Label(text=str(int(sliderHh.value)), pos=(655, 605), font_name='calibri', font_size=20)
        labNum3 = Label(text=str(int(sliderSl.value)), pos=(655, 545), font_name='calibri', font_size=20)
        labNum4 = Label(text=str(int(sliderSh.value)), pos=(655, 485), font_name='calibri', font_size=20)
        labNum5 = Label(text=str(int(sliderVl.value)), pos=(655, 425), font_name='calibri', font_size=20)
        labNum6 = Label(text=str(int(sliderVh.value)), pos=(655, 365), font_name='calibri', font_size=20)

        self.add_widget(butFrame)
        self.add_widget(labFrame)
        self.add_widget(butEdge)
        self.add_widget(labEdge)
        self.add_widget(butMask)
        self.add_widget(labMask)
        self.add_widget(sliderHl)
        self.add_widget(sliderHh)
        self.add_widget(sliderSl)
        self.add_widget(sliderSh)
        self.add_widget(sliderVl)
        self.add_widget(sliderVh)
        self.add_widget(labSlider1)
        self.add_widget(labSlider2)
        self.add_widget(labSlider3)
        self.add_widget(labSlider4)
        self.add_widget(labSlider5)
        self.add_widget(labSlider6)
        self.add_widget(butFrameSkin)
        self.add_widget(butEdgeSkin)
        self.add_widget(butMaskSkin)
        self.add_widget(labNum1)
        self.add_widget(labNum2)
        self.add_widget(labNum3)
        self.add_widget(labNum4)
        self.add_widget(labNum5)
        self.add_widget(labNum6)
        self.add_widget(butCnt)
        self.add_widget(butCntSkin)
        self.add_widget(labCnt)
        self.add_widget(butRotCnt)
        self.add_widget(butRotCntSkin)
        self.add_widget(labRotCnt)


class Camera(Image):

    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        fps = 30
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        global selection, contourSelection, contourRotatingSelection, hLow, sLow, vLow, hHigh, sHigh, vHigh, xPrev, yPrev, wPrev, hPrev, xCenterPrev, yCenterPrev, zPrev, frameTimePrev

        ret, frame = self.capture.read()
        self.size = (frame.shape[1], frame.shape[0])
        frameTime = time.time()
        t = frameTime - frameTimePrev # time between the frame and the previous frame

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
            v = scale / t
            vKm = round(v * 3.6, 2)
            print("{0} km/h".format(vKm))

        if selection == 0:
            if w > 40 and h > 40 and len(contours) > 0:
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

            if w > 40 and h > 40 and len(contours) > 0:
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

            if w > 40 and h > 40 and len(contours) > 0:
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

        xPrev = x
        yPrev = y
        wPrev = w
        hPrev = h
        xCenterPrev = xCenter
        yCenterPrev = yCenter
        zPrev = z
        frameTimePrev = frameTime


class buttonSkin(Image):

    def __init__(self, **kwargs):
        super(buttonSkin, self).__init__(**kwargs)

        img = cv2.imread("ressources/buttonSkin.png")

        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

    def select(self, **kwargs):
        img = cv2.imread("ressources/buttonSkinSelected.png")

        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

    def unselect(self, **kwargs):
        img = cv2.imread("ressources/buttonSkin.png")

        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture


class TpeApp(App):

    def build(self):
        return RootWidget()

    def on_stop(self):
        Camera().capture.release()

if __name__ == '__main__':
    TpeApp().run()
