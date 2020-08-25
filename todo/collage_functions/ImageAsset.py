import os
from PIL import Image, ImageFilter
import sys
sys.path.append('/Users/dorothyqu/PycharmProjects/thesis/crfasrnn_pytorch')
from todo.collage_functions import masking


class ImageAsset:
    def __init__(self, filename, x, y, tint, filter, transparency, rotation):
        self.x = x
        self.y = y
        self.tint = tint
        self.rotate = 0
        self.name = filename
        self.img = Image.open(self.name)
        self.width, self.height = self.img.size
        if self.width > 1000 or self.height > 1000:
            image = Image.open(self.name)
            image.thumbnail((500, 500))
            image.save(self.name)
            self.img = load_image(self.name)
            self.width, self.height = self.img.size
        self.filter = filter
        self.transparency = transparency
        self.rotation = rotation

    def mask(self):
        masking.crop(self.name, os.path.splitext(self.name)[0] + "crop.png")
        self.img = load_image(os.path.splitext(self.name)[0]+"crop.png")

    def blackwhite(self):
        masking.blackwhitemask(self.name, os.path.splitext(self.name)[0] + "blackwhite.png")
        self.img = load_image(os.path.splitext(self.name)[0] + "blackwhite.png")

    def place(self, background):
        if self.tint != None:
            colors, a = self.tint
            if colors != None:
                r, g, b = colors
                tint(r, g, b, a)
            else:
                tint(255, a)
        else:
            no_tint()
        if self.filter == "BLUR":
            PILimage = Image.open(self.name)
            PILimage = PILimage.filter(ImageFilter.GaussianBlur(radius=2))
            PILimage.save(os.path.splitext(self.name)[0]+"blur.png")
            self.img = load_image(os.path.splitext(self.name)[0]+"blur.png")
        if self.filter == "EMBOSS":
            PILimage = Image.open(self.name)
            PILimage = PILimage.filter(ImageFilter.EMBOSS)
            PILimage.save(os.path.splitext(self.name)[0]+"emboss.png")
            self.img = load_image(os.path.splitext(self.name)[0]+"emboss.png")
        rotate(math.radians(self.rotation))
        image(self.img, (self.x - self.width/2,self.y - self.height/2))
        rotate(math.radians(360-self.rotation))
