import pathlib
import PIL
import cv2
import os
import numpy as np
from PIL import Image
# from flask import
from todo.crfasrnn_pytorch.run_demo import get_labels

PATH_TO_APPEND = str(pathlib.Path(__file__).parent.parent.absolute()) + "/"

def crop(input_file, output_file):
    print("you're masking")
    print(input_file)

    # name of the img to make it RGB
    precrop = os.path.splitext(input_file)[0] + "precrop.png"
    rgba_image = PIL.Image.open(input_file)
    rgb_image = rgba_image.convert('RGB')
    rgb_image.save(precrop)
    get_labels(precrop)

    # upload source image, add alpha channel
    src = np.array(Image.open(precrop))
    h, w = src.shape[:2]

    # smooth out the mask
    # uncomment out for smoothing
    #https://stackoverflow.com/questions/41313642/smooth-edges-of-a-segmented-mask
    img = cv2.imread(PATH_TO_APPEND + 'crfasrnn_pytorch/labels.png', 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    (thresh, binRed) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=3)
    cv2.imwrite(PATH_TO_APPEND + 'crfasrnn_pytorch/labels.png', opening)

    # reupload mask as a greyscale array, turn into black and white
    mask = np.array(Image.open(PATH_TO_APPEND + 'crfasrnn_pytorch/labels.png').convert('L').resize(src.shape[1::-1], Image.BILINEAR))
    mask[mask != 0] = 255 # make everything in the mask that's not black to be white... AKA opaque!

    # add alpha layer
    RGBA = np.dstack((src, mask))

    img = Image.fromarray(RGBA, 'RGBA')
    img.save(output_file)
    
    #now delete precrop 
    os.remove(precrop)

def point(input_file, output_file):
    print("you're pointing")
    print(input_file)

    # smooth out the mask
    # uncomment out for smoothing
    #https://stackoverflow.com/questions/41313642/smooth-edges-of-a-segmented-mask
    img = cv2.imread(input_file, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    (thresh, binRed) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
    cv2.imwrite(output_file, opening)


def blackwhitemask(input_file, output_file):
    print("you're doing black and white stuff")
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
