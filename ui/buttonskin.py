from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
import os

class ButtonSkin(Image):
    """ButtonSkin class, the texture of the ButtonSkin change if the button is selected or not"""

    def __init__(self, **kwargs):
        """Initialize the button skin and the texture with the unselected image"""

        super(ButtonSkin, self).__init__(**kwargs)
        img = cv2.imread(os.getcwd() + "/resources/button_skin.png")
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt="bgr")
        image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        # display image from the texture
        self.texture = image_texture

    def select(self, **kwargs):
        """Set the texture of the button skin with the selected image"""

        img = cv2.imread(os.getcwd() + "/resources/button_skin_selected.png")
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt="bgr")
        image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        # display image from the texture
        self.texture = image_texture

    def unselect(self, **kwargs):
        """Set the texture of the button skin with the unselected image"""

        img = cv2.imread(os.getcwd() + "/resources/button_skin.png")
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt="bgr")
        image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        # display image from the texture
        self.texture = image_texture
