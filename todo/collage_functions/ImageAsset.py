import os
import PIL
import numpy as np
import cv2
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
        self.img = Image.open(self.name).convert('RGBA')
        self.width, self.height = self.img.size
        if self.width > 1000 or self.height > 1000:
            self.name.thumbnail((500, 500))
            self.name.save(self.name)
            self.width, self.height = self.img.size
        self.filter = filter
        self.transparency = transparency
        self.rotation = rotation

    def mask(self):
        masking.crop(self.name, os.path.splitext(self.name)[0] + "crop.png")
        self.img = Image.open(os.path.splitext(self.name)[0]+"crop.png").convert('RGBA')

    def blackwhite(self):
        masking.blackwhitemask(self.name, os.path.splitext(self.name)[0] + "blackwhite.png")
        self.img = Image.open(os.path.splitext(self.name)[0] + "blackwhite.png").convert('RGBA')

    def colorize(self, r, g, b, a):
        # read the target file
        target_img = cv2.imread(self.name)

        # create an image with a single color
        colored_img = np.full(target_img.shape, (r, g, b), np.uint8)

        # add the filter  with a weight factor of 20% to the target image
        fused_img = cv2.addWeighted(target_img, 1-a, colored_img, a, 0)

        cv2.imwrite(os.path.splitext(self.name)[0] + "tinted.png", fused_img)
        self.img = Image.open(os.path.splitext(self.name)[0] + "tinted.png").convert('RGBA')

    def place(self, background):
        if self.tint != None:
            colors, a = self.tint
            if colors != None:
                r, g, b = colors
                self.colorize(r, g, b, a)
            else:
                self.colorize(255, 255, 255, a)
        if self.filter == "BLUR":
            PILimage = Image.open(self.name)
            PILimage = PILimage.filter(ImageFilter.GaussianBlur(radius=2))
            PILimage.save(os.path.splitext(self.name)[0]+"blur.png")
            self.img = Image.open(os.path.splitext(self.name)[0]+"blur.png")
        if self.filter == "EMBOSS":
            PILimage = Image.open(self.name)
            PILimage = PILimage.filter(ImageFilter.EMBOSS)
            PILimage.save(os.path.splitext(self.name)[0]+"emboss.png")
            self.img = Image.open(os.path.splitext(self.name)[0]+"emboss.png")

        # weird rotation stuff to keep the background transparent
        self.img = self.img.rotate(self.rotation, expand = True, fillcolor = (0, 0, 0, 0))

        # paste the image
        Image.Image.paste(background, self.img, (int(self.x - self.width/2), int(self.y - self.height/2)), mask=self.img)
