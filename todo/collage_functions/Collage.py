import json
import pathlib
import random
import PIL
from PIL import Image
import numpy as np
import importlib
# from thesis-backend.todo.collage_functions import colorpalette, positions
colorpalette = importlib.import_module("thesis-backend.todo.collage_functions.colorpalette")
positions = importlib.import_module("thesis-backend.todo.collage_functions.positions")
temp = importlib.import_module("thesis-backend.todo.collage_functions.ImageAsset")
ImageAsset = temp.ImageAsset
# from thesis-backend.todo.collage_functions.ImageAsset import ImageAsset
import os

PATH_TO_APPEND = str(pathlib.Path(__file__).parent.absolute()) + "/"
CANVAS_SIZE = (900, 1100)
class Collage:
    # create all the genes within a collage
    def __init__(self, genes):
        self.genes = genes
        # get values
        imagenames = genes["imagenames"]
        p = genes["p"]
        color = genes["color"]
        palette = genes["palette"]
        images = genes["images"]
        edits = genes["edits"]
        textures = genes["textures"]
        texturenames = genes["texturenames"]
        brushes = genes["brushes"]
        brushnames = genes["brushnames"]
        backgrounds = genes["backgrounds"]

        self.imagenames = imagenames # a list of all the image names in a path
        self.p = p
        self.color = color
        self.palette = palette # what kind of palette do we want
        self.imglist = [] # represent all the images we are going to be showing

        # this is a list of all images represented as 0 (not present) 1 (present)
        self.images = images

        # number of possible images there could be
        self.n = self.images.count(1)

        # all the edits done to each image
        # crop (0 or 1)
        # blur (0 or 1)
        # rotate (0 to 360)
        # tint (0 or color from palette)
        self.edits = edits
        self.mask = edits[0]
        self.blur = edits[1]
        self.rotate = edits[2]
        self.tint = edits[3]
        self.point = edits[4]

        # textures – to add random textures? First is the background, second is the overlay, third is...
        self.textures = textures
        self.texturenames = texturenames
        self.backgrounds = backgrounds 

        self.brushes = brushes
        self.brushnames = brushnames

        # bunch of random things, like repeating an image?
        self.random = None

        # where the collage is stored
        self.collage = None

    # call this to automatically set up everything
    def setup(self):
        global pos
        pos = positions.get_locations(self.n, self.p)
        print(pos)
        colors = colorpalette.get_palette(self.color, self.palette)

        # TODO: represent transparency and other edits 
        x = 0 # to iterate through the nodes
        # go through every image and either represent it or don't
        for i in range(len(self.images)):
            print(self.imagenames[i])
            # print(self.imagenames[i], pos[x][0], pos[x][1], self.rotate[i])
            if self.images[i] == 1:
                self.imglist.append(ImageAsset(self.imagenames[i], pos[x][0], pos[x][1], (random.choice(colors), .4), None, 200, self.rotate[i]))
                if self.mask[i] == 1:
                    self.imglist[-1].mask()
                if self.tint[i] == 1:
                    self.imglist[-1].blackwhite()
                if self.point[i] == 1:
                    self.imglist[-1].pointillism()
                x+=1
            else: # change the extension to png anyways 
                if not self.imagenames[i].endswith('.png'): 
                    img = Image.open(self.imagenames[i])
                    name = os.path.splitext(self.imagenames[i])[0] + ".png"
                    img.save(name)
                    # delete old file 
                    os.remove(self.imagenames[i])
                    self.imagenames[i] = name 

    # call this to automatically draw everything
    def draw(self):
        # draw the background
        r, g, b = self.color
        background = Image.new('RGBA', CANVAS_SIZE, (r, g, b, 255))

        # get the background texture
        for i in range(len(self.backgrounds)):
            if self.textures[i] == 1:
                overlay = Image.open(self.texturenames[i]).convert('RGBA')
                print("adding background")
                print(self.texturenames[i])
                w, h = overlay.size 
                if w < CANVAS_SIZE[0]: 
                    wpercent = (CANVAS_SIZE[0]/float(w))
                    hsize = int((float(h)*float(wpercent)))
                    overlay = overlay.resize((CANVAS_SIZE[0],hsize), PIL.Image.ANTIALIAS)
                w, h = overlay.size 
                if h < CANVAS_SIZE[1]: 
                    wpercent = (CANVAS_SIZE[1]/float(h))
                    hsize = int((float(w)*float(wpercent)))
                    overlay = overlay.resize((CANVAS_SIZE[1],hsize), PIL.Image.ANTIALIAS)
                overlay_mask = overlay.split()[3].point(lambda i: i * 50 / 100.)
                background.paste(overlay, (0, 0), mask=overlay_mask)
        
        # bkg = Image.open(self.texturenames[self.textures[0]])
        # width, height = bkg.size
        # if width > 1000 or height > 1100:
        #     if width > height:
        #         bkg = bkg.rotate(90)
        #         # now make the width as large as 1000
        #         bkg = bkg.resize((1000, width*1000/height))
        #     else:
        #         bkg = bkg.resize((1000, height * 1000 / width))

        #     width, height = bkg.size
        #     if height < 1100:
        #         bkg = bkg.resize((width*1100/height, 1100))
        #     bkg = bkg.crop((0, 0, 1000, 1100))
        #     bkg.save(self.texturenames[self.textures[0]])
        # bkg = Image.open(self.texturenames[self.textures[0]])
        # background.paste(bkg, (0, 0))

        # get brush positions
        brush_pos = positions.get_locations(len(self.brushes), self.p)
        x = 0
        for i in range(len(self.brushes)):
            if self.brushes[i] == 1:
                brush = Image.open(self.brushnames[i]).convert('RGBA')
                brush_mask = brush.split()[3].point(lambda i: i * 80 / 100.)
                width, height = brush.size
                background.paste(brush, (int(brush_pos[x][0] - width/2), int(brush_pos[x][1] - height/2)), mask=brush_mask)
                x+=1 

        for i in self.imglist:
            i.place(background)

        for i in range(len(self.textures)):
            if self.textures[i] == 1:
                overlay = Image.open(self.texturenames[i]).convert('RGBA')
                print("adding texture")
                print(self.texturenames[i])
                w, h = overlay.size 
                if w < CANVAS_SIZE[0]: 
                    wpercent = (CANVAS_SIZE[0]/float(w))
                    hsize = int((float(h)*float(wpercent)))
                    overlay = overlay.resize((CANVAS_SIZE[0],hsize), PIL.Image.ANTIALIAS)
                w, h = overlay.size 
                if h < CANVAS_SIZE[1]: 
                    wpercent = (CANVAS_SIZE[1]/float(h))
                    hsize = int((float(w)*float(wpercent)))
                    overlay = overlay.resize((CANVAS_SIZE[1],hsize), PIL.Image.ANTIALIAS)
                overlay_mask = overlay.split()[3].point(lambda i: i * 5 / 100.)
                background.paste(overlay, (0, 0), mask=overlay_mask)

        # overlay = Image.open(self.texturenames[self.textures[1]]).convert('RGBA')
        # overlay_mask = overlay.split()[3].point(lambda i: i * 30 / 100.)
        # background.paste(overlay, (0, 0), mask=overlay_mask)

        self.collage = background

    # do this after collage initialization to update filenames --> .png
    def renameFiles(self): 
        self.imagenames = [os.path.splitext(f)[0] + ".png" for f in self.imagenames]

    def saveGenes(self, fName): 
        with open(fName, 'w+') as outfile:
            json.dump({
                "imagenames": self.imagenames,
                "p": self.p,
                "color": self.color,
                "palette": self.palette,
                "images": self.images,
                "edits": self.edits,
                "textures": self.textures,
                "texturenames": self.texturenames,
                "brushes": self.brushes,
                "brushnames": self.brushnames,
                "backgrounds": self.backgrounds
            }, outfile, indent=2)

    # create an offspring that is similar to the original parent
    # return the json file with the parent name + 1
    def createOffspring(self, fName):
        # to create offspring:
        # images: changing 0->1 and vice versa is a probability of... .3?
        images = [self.geneRandomizer(i, .1) for i in self.images]
        textures = [self.geneRandomizer(i, .05) for i in self.textures]
        backgrounds = [self.geneRandomizer(i, .05) for i in self.backgrounds]
        brushes = [self.geneRandomizer(i, .03) for i in self.brushes]

        # p: change it on a normal distribution
        p = np.random.normal(self.p, .1)

        # color: equal chance to be random, same color, and 3 colors in between
        color = self.offspringColor()

        # palette: keeping = .5, changing to another one/staying the same = .5
        if random.randrange(2) == 0:
            palette = self.palette
        else:
            palette = random.randint(1, 4)

        # edits:
        edits = []
        # crop (0 or 1) has a .2 chance of changing
        edits.append([self.geneRandomizer(i, .1) for i in self.mask])
        # blur (0 or 1) has a .2 chance of changing
        edits.append([self.geneRandomizer(i, .2) for i in self.blur])
        # rotate (0 to 360) changes on a normal distribution, .3 chance of being random
        # distribution
        edits.append([self.rotationGene(i) for i in self.rotate])

        # tint (0 or color from palette) .3 chance to be something else?
        edits.append([self.geneRandomizer(i, .3) for i in self.tint])

        # pointillism (0 or color from palette) .3 chance to be something else?
        edits.append([self.geneRandomizer(i, .05) for i in self.point])

        with open(fName, 'w+') as outfile:
            json.dump({
                "imagenames": self.imagenames,
                "p": p,
                "color": color,
                "palette": palette,
                "images": images,
                "edits": edits,
                "textures": textures,
                "texturenames": self.texturenames,
                "brushes": brushes,
                "brushnames": self.brushnames,
                "backgrounds": backgrounds
            }, outfile, indent=2)

    # input: numerical value and probability of a number changing
    def geneRandomizer(self, value, p):
        # 0 = don't change, 1 = change
        if random.choices([0, 1], [1 - p, p]) == [1]:
            if value == 1:
                return 0
            else:
                return 1
        else:
            return value

    def offspringColor(self):
        (r, g, b) = self.color
        randcolor = colorpalette.randomcolor()
        (r1, g1, b1) = randcolor
        # 0 = original color, 1 = first mix, 2 = second mix, 3 = third mix, 4 = random color
        colorchoice = random.randrange(5)
        if colorchoice == 0:
            return self.color
        if colorchoice == 4:
            return randcolor
        else:
            r2 = int(abs((r+r1)/2))
            g2 = int(abs((g+g1)/2))
            b2 = int(abs((b+b1)/2))
            if colorchoice == 2:
                return (r2, g2, b2)
            if colorchoice == 1:
                r3 = int(abs((r + r2) / 2))
                g3 = int(abs((g + g2) / 2))
                b3 = int(abs((b + b2) / 2))
                return (r3, g3, b3)
            else:
                r3 = int(abs((r1 + r2) / 2))
                g3 = int(abs((g1 + g2) / 2))
                b3 = int(abs((b1 + b2) / 2))
                return (r3, g3, b3)
        return (r1, g1, b1)

    def rotationGene(self, value):
        # change the number to something along the distribution
        if random.choices([0, 1], [.4, .6]) == [0]:
            return np.random.normal(value, 5)
        # return the same value
        else:
            return value

    def save(self, filename):
        self.collage.save(filename)
