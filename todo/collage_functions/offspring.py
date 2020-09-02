# Given a Collage json file, return a offspring from it 

import glob
import json
import os
import pathlib
import sys
import numpy as np
import importlib

sys.path.append("..") # Adds higher directory to python modules path.

PATH_TO_APPEND = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/"
print("Appending path: " + PATH_TO_APPEND)
sys.path.append(PATH_TO_APPEND)

import random
temp = importlib.import_module("thesis-backend.todo.collage_functions.Collage")
Collage = temp.Collage 

ABS_PATH= PATH_TO_APPEND + "todo/"
PIC_PATH= ABS_PATH + "decades/cat/"

PATH_PRE = ABS_PATH + "static/"
FILE_NAME = None

def setup():
    global colors, pos, offspring, OFFSPRING_JSON

    # load up genes
    with open(PARENT_JSON, 'r') as infile:
        parent_genes = json.load(infile)
    # load the collage 
    parent = Collage(parent_genes)
    
    # create the offspring genes 
    OFFSPRING_JSON = PATH_PRE + FILE_NAME + ".json"
    parent.createOffspring(OFFSPRING_JSON) 
    with open(OFFSPRING_JSON, 'r') as infile:
        genes = json.load(infile)

    # load the offspring 
    offspring = Collage(genes)
    offspring.setup()

def draw():
    offspring.draw()

    fullPath = "{}{}".format(PATH_PRE, FILE_NAME)
    correctName = "{}.png".format(fullPath)
    offspring.save(correctName)

if __name__ == '__main__':
    # get the full paths for the json and png files
    defFileName = "offspring"
    if len(sys.argv) > 2: # first arg is the name of the parent json and second is name of the file ex. "collage11"
        PARENT_JSON = PATH_PRE + sys.argv[1]
        FILE_NAME = sys.argv[2]
    else:
        print("No filename supplied, defaulting to '{}'".format(defFileName))
        FILE_NAME = defFileName

    setup()
    draw()