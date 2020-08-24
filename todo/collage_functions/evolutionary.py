import glob
import json
import os
import pathlib
import sys
from p5 import *
# # set to true in production
# IS_PRODUCTION = False

sys.path.append("..") # Adds higher directory to python modules path.
from todo.collage_functions.colorpalette import randomcolor

PATH_TO_APPEND = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/"
print("Appending path: " + PATH_TO_APPEND)
sys.path.append(PATH_TO_APPEND)

import random
from todo.collage_functions.Collage import Collage

ABS_PATH= PATH_TO_APPEND + "todo/"
PIC_PATH= ABS_PATH + "decades/cat/"

PATH_PRE = ABS_PATH + "static/"
FILE_NAME = None

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
    imagenames = glob.glob(PIC_PATH+"*")
    texturenames = glob.glob(ABS_PATH + "textures/*")
    brushnames = glob.glob(ABS_PATH + "brushes/*")

    p = np.random.normal(.5, .1)
    color = randomcolor()
    palette = random.randint(1, 4)

    imageprob = random.random() # do we want tons of pics or not many
    images = [initializeValue(.3) for i in imagenames]

    edits = []
    masks = [initializeValue(.05) for i in imagenames]
    blur = [initializeValue(.05) for i in imagenames]
    rotate = [initializeRotation() for i in imagenames]
    tint = [initializeValue(.05) for i in imagenames]
    textures = [0, 1]
    brushes = [initializeValue(.3) for i in brushnames]

    edits.append(masks)
    edits.append(blur)
    edits.append(rotate)
    edits.append(tint)

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
            "brushnames": brushnames
        }, outfile, indent=2)

def setup():
    global colors, pos, collage
    size(900,1100)

    # save the json
    jsonPath = "{}{}.json".format(PATH_PRE, FILE_NAME)
    initializeGenes(jsonPath)

    # load up genes
    with open(jsonPath, 'r') as infile:
        genes = json.load(infile)

    # actually set up the collage
    collage = Collage(genes)
    collage.setup()

def draw():
    collage.draw()

    fullPath = "{}{}".format(PATH_PRE, FILE_NAME)
    correctName = "{}.png".format(fullPath)
    # saving adds 4 0s for some reason
    save(correctName)

    # so fix it lmao
    os.rename("{}0000.png".format(fullPath), correctName)

    # all done
    exit()

if __name__ == '__main__':
    # get the full paths for the json and png files
    defFileName = "collage"
    if len(sys.argv) > 1: # first arg is the name for the file ex. "collage11"
        FILE_NAME = sys.argv[1]
    else:
        print("No filename supplied, defaulting to '{}'".format(defFileName))
        FILE_NAME = defFileName

    run()
