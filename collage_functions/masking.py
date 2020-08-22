import os

import cv2
import numpy as np
from PIL import Image
from crfasrnn_pytorch.run_demo import get_labels

def crop(input_file, output_file):
    get_labels(input_file)

    # upload source image, add alpha channel
    src = np.array(Image.open(input_file))
    h, w = src.shape[:2]

    # smooth out the mask
    # uncomment out for smoothing
    #https://stackoverflow.com/questions/41313642/smooth-edges-of-a-segmented-mask
    img = cv2.imread('labels.png', 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    (thresh, binRed) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=3)
    cv2.imwrite("labels.png", opening)

    # reupload mask as a greyscale array, turn into black and white
    mask = np.array(Image.open('../crfasrnn_pytorch/labels.png').convert('L').resize(src.shape[1::-1], Image.BILINEAR))
    mask[mask != 0] = 255 # make everything in the mask that's not black to be white... AKA opaque!

    # add alpha layer
    RGBA = np.dstack((src, mask))

    img = Image.fromarray(RGBA, 'RGBA')
    img.save(output_file)

def blackwhitemask(input_file, output_file):
    # reupload mask as a greyscale array, turn into black and white
    original = cv2.imread(input_file)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    (thresh, blackwhite) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(output_file, blackwhite)

    # read the image
    image_bgr = cv2.imread(output_file)
    # get the image dimensions (height, width and channels)
    h, w, c = image_bgr.shape
    # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
    image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
    # create a mask where white pixels ([255, 255, 255]) are True
    white = np.all(image_bgr == [255, 255, 255], axis=-1)
    # change the values of Alpha to 0 for all the white pixels
    image_bgra[white, -1] = 0
    # save the image
    cv2.imwrite(output_file, image_bgra)
