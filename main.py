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
from kivy.config import Config
from kivy.graphics import *
import cv2
import serial
import camera

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Config.set('graphics', 'resizable', '0')

# Initialize global variables
arduino = False             # Arduino is initialized or not

try:
    s = serial.Serial(port='COM4', baudrate=115200)
except serial.serialutil.SerialException:
    print("could not open port 'COM4'")
else:
    print("Starting...")
    time.sleep(2)
    s.write('Ready')
    arduino = True

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

        self.cam = camera.Camera(pos=(20, 268))
        self.add_widget(self.cam)

        def updateBut():
            if camera.selection != 0:
                butFrameSkin.unselect()
            if camera.selection != 1:
                butEdgeSkin.unselect()
            if camera.selection != 2:
                butMaskSkin.unselect()

        # button frame
        def pressButFrame(instance):
            camera.selection = 0
            butFrameSkin.select()
            updateBut()

        butFrame = Button(pos=(40, 200), size=(40, 40))
        butFrame.bind(on_press=pressButFrame)
        labFrame = Label(text='Frame', pos=(74, 170), font_name='calibri', font_size=20)
        butFrameSkin = buttonSkin(pos=butFrame.pos, size=butFrame.size)
        butFrameSkin.select()

        # button canny edge
        def pressButEdge(instance):
            camera.selection = 1
            butEdgeSkin.select()
            updateBut()

        butEdge = Button(pos=(40, 150), size=(40, 40))
        butEdge.bind(on_press=pressButEdge)
        labEdge = Label(text='Canny edge', pos=(97, 120), font_name='calibri', font_size=20)
        butEdgeSkin = buttonSkin(pos=butEdge.pos, size=butEdge.size)

        # button mask
        def pressButMask(instance):
            camera.selection = 2
            butMaskSkin.select()
            updateBut()

        butMask = Button(pos=(40, 100), size=(40, 40))
        butMask.bind(on_press=pressButMask)
        labMask = Label(text='Mask', pos=(70, 70), font_name='calibri', font_size=20)
        butMaskSkin = buttonSkin(pos=butMask.pos, size=butMask.size)

        # button contour
        def pressButCnt(instance):
            if camera.contourSelection == 0:
                camera.contourSelection = 1
                butCntSkin.select()
            else:
                camera.contourSelection = 0
                butCntSkin.unselect()

        butCnt = Button(pos=(240, 200), size=(40, 40))
        butCnt.bind(on_press=pressButCnt)
        labCnt = Label(text='Contour', pos=(280, 170), font_name='calibri', font_size=20)
        butCntSkin = buttonSkin(pos=butCnt.pos, size=butCnt.size)

        # button rotating contour
        def pressButRotCnt(instance):
            if camera.contourRotatingSelection == 0:
                camera.contourRotatingSelection = 1
                butRotCntSkin.select()
            else:
                camera.contourRotatingSelection = 0
                butRotCntSkin.unselect()

        butRotCnt = Button(pos=(240, 150), size=(40, 40))
        butRotCnt.bind(on_press=pressButRotCnt)
        labRotCnt = Label(text='Rotating Contour', pos=(320, 120), font_name='calibri', font_size=20)
        butRotCntSkin = buttonSkin(pos=butRotCnt.pos, size=butRotCnt.size)

        # slider hue low
        def sliderHlMove(instance, value):
            if value > sliderHh.value:
                sliderHl.value = sliderHh.value
            camera.hLow = int(sliderHl.value)
            labNumHl.text = str(camera.hLow)

        sliderHl = Slider(range=(0,179), value=0, pos=(680,640), size=(200,100), sensitivity='handle')
        sliderHl.bind(value=sliderHlMove)

        # slider hue high
        def sliderHhMove(instance, value):
            if value < sliderHl.value:
                sliderHh.value = sliderHl.value
            camera.hHigh = int(sliderHh.value)
            labNumHh.text = str(camera.hHigh)

        sliderHh = Slider(range=(0,179), value=179, pos=(680,580), size=(200,100), sensitivity='handle')
        sliderHh.bind(value=sliderHhMove)

        # slider saturation low
        def sliderSlMove(instance, value):
            if value > sliderSh.value:
                sliderSl.value = sliderSh.value
            camera.sLow = int(sliderSl.value)
            labNumSl.text = str(camera.sLow)

        sliderSl = Slider(range=(0,255), value=0, pos=(680,520), size=(200,100), sensitivity='handle')
        sliderSl.bind(value=sliderSlMove)

        # slider saturation high
        def sliderShMove(instance, value):
            if value < sliderSl.value:
                sliderSh.value = sliderSl.value
            camera.sHigh = int(sliderSh.value)
            labNumSh.text = str(camera.sHigh)

        sliderSh = Slider(range=(0,255), value=255, pos=(680,460), size=(200,100), sensitivity='handle')
        sliderSh.bind(value=sliderShMove)

        # slider value low
        def sliderVlMove(instance, value):
            if value > sliderVh.value:
                sliderVl.value = sliderVh.value
            camera.vLow = int(sliderVl.value)
            labNumVl.text = str(camera.vLow)

        sliderVl = Slider(range=(0,255), value=0, pos=(680,400), size=(200,100), sensitivity='handle')
        sliderVl.bind(value=sliderVlMove)

        # slider value high
        def sliderVhMove(instance, value):
            if value < sliderVl.value:
                sliderVh.value = sliderVl.value
            camera.vHigh = int(sliderVh.value)
            labNumVh.text = str(camera.vHigh)

        sliderVh = Slider(range=(0,255), value=255, pos=(680,340), size=(200,100), sensitivity='handle')
        sliderVh.bind(value=sliderVhMove)

        labSliderHl = Label(text='Hue Low', pos=(900, 640), font_name='calibri', font_size=20)
        labSliderHh = Label(text='Hue High', pos=(900, 580), font_name='calibri', font_size=20)
        labSliderSl = Label(text='Saturation Low', pos=(905, 520), font_name='calibri', font_size=20)
        labSliderSh = Label(text='Saturation High', pos=(905, 460), font_name='calibri', font_size=20)
        labSliderVl = Label(text='Value Low', pos=(900, 400), font_name='calibri', font_size=20)
        labSliderVh = Label(text='Value High', pos=(900, 340), font_name='calibri', font_size=20)
        labNumHl = Label(text=str(int(sliderHl.value)), pos=(655, 665), font_name='calibri', font_size=20)
        labNumHh = Label(text=str(int(sliderHh.value)), pos=(655, 605), font_name='calibri', font_size=20)
        labNumSl = Label(text=str(int(sliderSl.value)), pos=(655, 545), font_name='calibri', font_size=20)
        labNumSh = Label(text=str(int(sliderSh.value)), pos=(655, 485), font_name='calibri', font_size=20)
        labNumVl = Label(text=str(int(sliderVl.value)), pos=(655, 425), font_name='calibri', font_size=20)
        labNumVh = Label(text=str(int(sliderVh.value)), pos=(655, 365), font_name='calibri', font_size=20)

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
        self.add_widget(labSliderHl)
        self.add_widget(labSliderHh)
        self.add_widget(labSliderSl)
        self.add_widget(labSliderSh)
        self.add_widget(labSliderVl)
        self.add_widget(labSliderVh)
        self.add_widget(butFrameSkin)
        self.add_widget(butEdgeSkin)
        self.add_widget(butMaskSkin)
        self.add_widget(labNumHl)
        self.add_widget(labNumHh)
        self.add_widget(labNumSl)
        self.add_widget(labNumSh)
        self.add_widget(labNumVl)
        self.add_widget(labNumVh)
        self.add_widget(butCnt)
        self.add_widget(butCntSkin)
        self.add_widget(labCnt)
        self.add_widget(butRotCnt)
        self.add_widget(butRotCntSkin)
        self.add_widget(labRotCnt)


class buttonSkin(Image):

    def __init__(self, **kwargs):
        super(buttonSkin, self).__init__(**kwargs)

        img = cv2.imread("../resources/buttonSkin.png")

        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

    def select(self, **kwargs):
        img = cv2.imread("resources/buttonSkinSelected.png")

        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

    def unselect(self, **kwargs):
        img = cv2.imread("resources/buttonSkin.png")

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
        camera.Camera().capture.release()

if __name__ == '__main__':
    TpeApp().run()
