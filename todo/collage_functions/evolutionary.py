import glob
import json
import os
import pathlib
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageFile

sys.path.append("..") # Adds higher directory to python modules path.
from todo.collage_functions.colorpalette import randomcolor

PATH_TO_APPEND = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/"
print("Appending path: " + PATH_TO_APPEND)
sys.path.append(PATH_TO_APPEND)

import random
from todo.collage_functions.Collage import Collage

ABS_PATH= PATH_TO_APPEND + "todo/"
PIC_PATH= ABS_PATH + "images/" 

PATH_PRE = ABS_PATH + "static/"
FILE_NAME = None
USER_ID = None

# input: probability that it will be a 1
def initializeValue(p):
    # 0 = don't change, 1 = change
    if random.choices([0, 1], [1 - p, p]) == [1]:
        return 1
    else:
        return 0

def initializeRotation():
    # change the number to something along the distribution
    if random.choices([0, 1], [.4, .6]) == [0]:
        return np.random.normal(0, 5)
    # return the same value
    else:
        return 0

# initialize genes for a parent collage
def initializeGenes(fName):
    # GENE TIME
    # set up the paths
    imagenames = glob.glob(PIC_PATH+str(USER_ID)+"/*")
    imagenames = [f for f in imagenames if os.path.isfile(f)]
    # try to open the image with PIL - if it doesn't open, remove it from the list 
    for image in imagenames: 
        # try opening image in PIL
        try:
            Image.open(image)
        # if it doesn't open, remove it from the imagenames list
        except: 
            imagenames.remove(image)
            os.remove(image)

    texturenames = glob.glob(ABS_PATH + "textures/*")
    texturenames = [f for f in texturenames if os.path.isfile(f)]
    brushnames = glob.glob(ABS_PATH + "brushes/*")
    brushnames = [f for f in brushnames if os.path.isfile(f)]

    p = np.random.normal(.5, .1)
    color = randomcolor()
    palette = random.randint(1, 4)

    imageprob = random.random() # do we want tons of pics or not many
    images = [initializeValue(.3) for i in imagenames]

    edits = []
    masks = [initializeValue(.03) for i in imagenames]
    blur = [initializeValue(.05) for i in imagenames]
    rotate = [initializeRotation() for i in imagenames]
    tint = [initializeValue(.1) for i in imagenames]
    point = [initializeValue(.1) for i in imagenames]
    textures = [initializeValue(.05) for i in texturenames]
    backgrounds = [initializeValue(.1) for i in texturenames]
    brushes = [initializeValue(.05) for i in brushnames]

    edits.append(masks)
    edits.append(blur)
    edits.append(rotate)
    edits.append(tint)
    edits.append(point)

    # saveies genes
    with open(fName, 'w+') as outfile:
        json.dump({
            "imagenames": imagenames,
            "p": p,
            "color": color,
            "palette": palette,
            "images": images,
            "edits": edits,
            "textures": textures,
            "texturenames": texturenames,
            "brushes": brushes,
            "brushnames": brushnames, 
            "backgrounds" : backgrounds
        }, outfile, indent=2)

def setup():
    global colors, pos, collage

    # save the json
    jsonPath = "{}{}.json".format(PATH_PRE, FILE_NAME)
    initializeGenes(jsonPath)

    # load up genes
    with open(jsonPath, 'r') as infile:
        genes = json.load(infile)

    # actually set up the collage
    collage = Collage(genes)
    collage.setup()
    collage.renameFiles()
    collage.saveGenes(jsonPath)


def draw():
    collage.draw()

    fullPath = "{}{}".format(PATH_PRE, FILE_NAME)
    correctName = "{}.png".format(fullPath)
    collage.save(correctName)

if __name__ == '__main__':
    # get the full paths for the json and png files
    defFileName = "collage"
    if len(sys.argv) > 1: # first arg is the name for the file ex. "collage11"
        FILE_NAME = sys.argv[1]
        USER_ID = sys.argv[2]
    else:
        print("No filename supplied, defaulting to '{}'".format(defFileName))
        FILE_NAME = defFileName
        USER_ID = 0

    setup()
    draw()
