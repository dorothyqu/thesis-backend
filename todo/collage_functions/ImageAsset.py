import os
from os import path 
import pathlib
import PIL
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageFile
import sys
sys.path.append('/Users/dorothyqu/PycharmProjects/thesis/crfasrnn_pytorch')
import importlib
masking = importlib.import_module("thesis-backend.todo.collage_functions.masking")

ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageAsset:
    def __init__(self, filename, x, y, tint, filter, transparency, rotation):
        self.x = x
        self.y = y
        self.tint = tint
        self.rotate = 0

        # names  
        self.name = filename 
        self.basename = os.path.basename(self.name)
        self.img = Image.open(self.name)

        # convert image to png if not a png 
        if not self.name.endswith('.png'): 
            self.name = os.path.splitext(filename)[0] + ".png"
            self.img.save(self.name)
            self.img = Image.open(self.name).convert('RGBA')
            # delete old file 
            os.remove(filename)

        self.editpath = str(pathlib.Path(self.name).parent.absolute()) + "/edited/"

        self.width, self.height = self.img.size
        if self.width > 1000 or self.height > 1000:
            self.img.thumbnail((500, 500))
            self.img.save(self.name)
            self.width, self.height = self.img.size
            self.rename(self.name)
        self.filter = filter
        self.transparency = transparency
        self.rotation = rotation
    
    # go through all the motions of renaming 
    def rename(self, newname): 
        self.name = newname
        self.basename = os.path.basename(self.name)
        self.img = Image.open(newname).convert('RGBA')

    def mask(self):
        edited = self.editpath + os.path.splitext(self.basename)[0] + "crop.png"
        if not path.exists(edited): 
            masking.crop(self.name, edited)
        self.rename(edited)

    def blackwhite(self):
        edited = self.editpath + os.path.splitext(self.basename)[0] + "blackwhite.png"
        if not path.exists(edited): 
            masking.blackwhitemask(self.name, edited)
        self.rename(edited)

    def pointillism(self):
        edited = self.editpath + os.path.splitext(self.basename)[0] + "point.png"
        if not path.exists(edited):
            masking.point(self.name, edited)
        self.rename(edited)

    def colorize(self, r, g, b, a):
        # read the target file
        target_img = cv2.imread(self.name)
        # create an image with a single color
        colored_img = np.full(target_img.shape, (r, g, b), np.uint8)
        # add the filter  with a weight factor of 20% to the target image
        fused_img = cv2.addWeighted(target_img, 1-a, colored_img, a, 0)

        # add transparency back 
        alpha = self.img.split()[-1]

        # First create the image with alpha channel
        rgba = cv2.cvtColor(fused_img, cv2.COLOR_RGB2RGBA)

        # Then assign the mask to the last channel of the image
        rgba[:, :, 3] = alpha

        edited = self.editpath + os.path.splitext(self.basename)[0] + "tinted.png"
        cv2.imwrite(edited, rgba)
        self.rename(edited)

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

        # weird rotation stuff to keep the background transparent
        self.img = self.img.rotate(self.rotation, expand = True, fillcolor = (0, 0, 0, 0))

        # paste the image, with transparency 
        overlay_mask = self.img.split()[3].point(lambda i: i * self.transparency / 100.)
        Image.Image.paste(background, self.img, (int(self.x - self.width/2), int(self.y - self.height/2)), mask=self.img)
