# Given a Collage json file, return a offspring from it 

import glob
import json
import os
import pathlib
import sys
import numpy as np

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

def setup(collage_json):
    global colors, pos, collage

    # load up genes
    with open(collage_json, 'r') as infile:
        genes = json.load(infile)
    # load the collage 
    collage = Collage(genes)
    
    # create the offspring genes 
    # returns the name of the json file 
    offspring_json = collage.createOffspring() 
    with open(offspring_json, 'r') as infile:
        genes = json.load(infile)
    # load the offspring 
    offspring = Collage(genes)
    offspring.setup()

def draw():
    offspring.draw()

    fullPath = "{}{}".format(PATH_PRE, FILE_NAME)
    correctName = "{}.png".format(fullPath)
    # saving adds 4 0s for some reason
    offspring.save(correctName)

if __name__ == '__main__':
    # get the full paths for the json and png files
    defFileName = "collage"
    if len(sys.argv) > 1: # first arg is the name for the file ex. "collage11"
        FILE_NAME = sys.argv[1]
    else:
        print("No filename supplied, defaulting to '{}'".format(defFileName))
        FILE_NAME = defFileName

    setup()
    draw()
