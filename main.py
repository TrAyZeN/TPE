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
    s = serial.Serial(port='COM4', baudrate=115200)     # initialize the connection with arduino
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

        def update_but():
            if camera.selection != 0:
                frame_button_skin.unselect()
            if camera.selection != 1:
                canny_button_skin.unselect()
            if camera.selection != 2:
                mask_button_skin.unselect()

        # button frame
        def press_frame_button(instance):
            camera.selection = 0
            frame_button_skin.select()
            update_but()

        frame_button = Button(pos=(40, 200), size=(40, 40))
        frame_button.bind(on_press=press_frame_button)
        frame_label = Label(text='Frame', pos=(74, 170), font_name='calibri', font_size=20)
        frame_button_skin = ButtonSkin(pos=frame_button.pos, size=frame_button.size)
        frame_button_skin.select()

        # button canny edge
        def press_canny_button(instance):
            camera.selection = 1
            canny_button_skin.select()
            update_but()

        canny_button = Button(pos=(40, 150), size=(40, 40))
        canny_button.bind(on_press=press_canny_button)
        canny_label = Label(text='Canny edge', pos=(97, 120), font_name='calibri', font_size=20)
        canny_button_skin = ButtonSkin(pos=canny_button.pos, size=canny_button.size)

        # button mask
        def press_mask_button(instance):
            camera.selection = 2
            mask_button_skin.select()
            update_but()

        mask_button = Button(pos=(40, 100), size=(40, 40))
        mask_button.bind(on_press=press_mask_button)
        mask_label = Label(text='Mask', pos=(70, 70), font_name='calibri', font_size=20)
        mask_button_skin = ButtonSkin(pos=mask_button.pos, size=mask_button.size)

        # button contour
        def press_contour_button(instance):
            if camera.contour_selection == 0:
                camera.contour_selection = 1
                contour_button_skin.select()
            else:
                camera.contour_selection = 0
                contour_button_skin.unselect()

        contour_button = Button(pos=(240, 200), size=(40, 40))
        contour_button.bind(on_press=press_contour_button)
        contour_label = Label(text='Contour', pos=(280, 170), font_name='calibri', font_size=20)
        contour_button_skin = ButtonSkin(pos=contour_button.pos, size=contour_button.size)

        # button rotating contour
        def press_rotating_countour_button(instance):
            if camera.rotating_contour_selection == 0:
                camera.rotating_contour_selection = 1
                rotating_countour_button_skin.select()
            else:
                camera.rotating_contour_selection = 0
                rotating_countour_button_skin.unselect()

        rotating_countour_button = Button(pos=(240, 150), size=(40, 40))
        rotating_countour_button.bind(on_press=press_rotating_countour_button)
        rotating_countour_label = Label(text='Rotating Contour', pos=(320, 120), font_name='calibri', font_size=20)
        rotating_countour_button_skin = ButtonSkin(pos=rotating_countour_button.pos, size=rotating_countour_button.size)

        # slider hue low
        def move_hue_low_slider(instance, value):
            if value > hue_high_slider.value:
                hue_low_slider.value = hue_high_slider.value
            camera.hue_low = int(hue_low_slider.value)
            hue_low_num_label.text = str(camera.hue_low)

        hue_low_slider = Slider(range=(0,179), value=0, pos=(680,640), size=(200,100), sensitivity='handle')
        hue_low_slider.bind(value=move_hue_low_slider)

        # slider hue high
        def move_hue_high_slider(instance, value):
            if value < hue_low_slider.value:
                hue_high_slider.value = hue_low_slider.value
            camera.hue_high = int(hue_high_slider.value)
            hue_high_num_label.text = str(camera.hue_high)

        hue_high_slider = Slider(range=(0,179), value=179, pos=(680,580), size=(200,100), sensitivity='handle')
        hue_high_slider.bind(value=move_hue_high_slider)

        # slider saturation low
        def move_saturation_low_slider(instance, value):
            if value > saturation_high_slider.value:
                saturation_low_slider.value = saturation_high_slider.value
            camera.saturation_low = int(saturation_low_slider.value)
            saturation_low_num_label.text = str(camera.saturation_low)

        saturation_low_slider = Slider(range=(0,255), value=0, pos=(680,520), size=(200,100), sensitivity='handle')
        saturation_low_slider.bind(value=move_saturation_low_slider)

        # slider saturation high
        def move_saturation_high_slider(instance, value):
            if value < saturation_low_slider.value:
                saturation_high_slider.value = saturation_low_slider.value
            camera.saturation_high = int(saturation_high_slider.value)
            saturation_high_num_label.text = str(camera.saturation_high)

        saturation_high_slider = Slider(range=(0,255), value=255, pos=(680,460), size=(200,100), sensitivity='handle')
        saturation_high_slider.bind(value=move_saturation_high_slider)

        # slider value low
        def move_value_low_slider(instance, value):
            if value > value_high_slider.value:
                value_low_slider.value = value_high_slider.value
            camera.value_low = int(value_low_slider.value)
            value_low_num_label.text = str(camera.value_low)

        value_low_slider = Slider(range=(0,255), value=0, pos=(680,400), size=(200,100), sensitivity='handle')
        value_low_slider.bind(value=move_value_low_slider)

        # slider value high
        def value_high_sliderMove(instance, value):
            if value < value_low_slider.value:
                value_high_slider.value = value_low_slider.value
            camera.value_high = int(value_high_slider.value)
            value_high_num_label.text = str(camera.value_high)

        value_high_slider = Slider(range=(0,255), value=255, pos=(680,340), size=(200,100), sensitivity='handle')
        value_high_slider.bind(value=value_high_sliderMove)

        hue_low_label = Label(text='Hue Low', pos=(900, 640), font_name='calibri', font_size=20)
        hue_high_label = Label(text='Hue High', pos=(900, 580), font_name='calibri', font_size=20)
        saturation_low_label = Label(text='Saturation Low', pos=(905, 520), font_name='calibri', font_size=20)
        saturation_high_slider_label = Label(text='Saturation High', pos=(905, 460), font_name='calibri', font_size=20)
        value_low_label = Label(text='Value Low', pos=(900, 400), font_name='calibri', font_size=20)
        value_high_label = Label(text='Value High', pos=(900, 340), font_name='calibri', font_size=20)
        hue_low_num_label = Label(text=str(int(hue_low_slider.value)), pos=(655, 665), font_name='calibri', font_size=20)
        hue_high_num_label = Label(text=str(int(hue_high_slider.value)), pos=(655, 605), font_name='calibri', font_size=20)
        saturation_low_num_label = Label(text=str(int(saturation_low_slider.value)), pos=(655, 545), font_name='calibri', font_size=20)
        saturation_high_num_label = Label(text=str(int(saturation_high_slider.value)), pos=(655, 485), font_name='calibri', font_size=20)
        value_low_num_label = Label(text=str(int(value_low_slider.value)), pos=(655, 425), font_name='calibri', font_size=20)
        value_high_num_label = Label(text=str(int(value_high_slider.value)), pos=(655, 365), font_name='calibri', font_size=20)

        self.add_widget(frame_button)
        self.add_widget(frame_label)
        self.add_widget(canny_button)
        self.add_widget(canny_label)
        self.add_widget(mask_button)
        self.add_widget(mask_label)
        self.add_widget(hue_low_slider)
        self.add_widget(hue_high_slider)
        self.add_widget(saturation_low_slider)
        self.add_widget(saturation_high_slider)
        self.add_widget(value_low_slider)
        self.add_widget(value_high_slider)
        self.add_widget(hue_low_label)
        self.add_widget(hue_high_label)
        self.add_widget(saturation_low_label)
        self.add_widget(saturation_high_slider_label)
        self.add_widget(value_low_label)
        self.add_widget(value_high_label)
        self.add_widget(frame_button_skin)
        self.add_widget(canny_button_skin)
        self.add_widget(mask_button_skin)
        self.add_widget(hue_low_num_label)
        self.add_widget(hue_high_num_label)
        self.add_widget(saturation_low_num_label)
        self.add_widget(saturation_high_num_label)
        self.add_widget(value_low_num_label)
        self.add_widget(value_high_num_label)
        self.add_widget(contour_button)
        self.add_widget(contour_button_skin)
        self.add_widget(contour_label)
        self.add_widget(rotating_countour_button)
        self.add_widget(rotating_countour_button_skin)
        self.add_widget(rotating_countour_label)


class ButtonSkin(Image):

    def __init__(self, **kwargs):
        super(ButtonSkin, self).__init__(**kwargs)
        img = cv2.imread("resources/buttonSkin.png")

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
