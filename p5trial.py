from p5 import *
from ImageAsset import ImageAsset
from colorpalette import *
import os
import random
import positions
# path="decades/1990/China/"
path="decades/cat/"

files=os.listdir(path)
d=path+random.choice(files)

offset = 0
easing = 0.05
imgMask = None
small = 4
large = 40
img = None

original = (110, 255, 226)
colors = get_palette(original, "COMP")

def setup():
        global img, imgMask, bg, img2, img3, img4, img5
        size(1000,1000)
        pos = positions.get_locations(5, .3)
        print(pos)
        # img = load_image("decades/1970/China/example.jpg")
        img = ImageAsset(path+random.choice(files),  pos[0][0], pos[0][1], (None, 255), None, 1000)
        print("1 done")
        # img2 = ImageAsset(path+random.choice(files),  pos[1][0], pos[1][1], (colors[1], 200), None, 127)
        # print("2 done")
        # img2.mask()
        # img3 = ImageAsset(path+random.choice(files),  pos[2][0], pos[2][1], (None, 100), 'BLUR', 1000)
        # print("3 done")
        # img4 = ImageAsset(path+random.choice(files),  pos[3][0], pos[3][1], (colors[4], 100), None, 1000)
        # # img4.mask()
        # print("4 done")
        # img5 = ImageAsset(path+random.choice(files),  pos[4][0], pos[4][1], (colors[2], 255), None, 1000)
        # print("5 done")
        # img = ImageAsset(path+d,  50, 100, (colors[2], 255), 'blur', 1000)
        # img2 = ImageAsset("output.png",  200, 200, (colors[1], 200), 'invert', 127)
        # img3 = ImageAsset("decades/1970/China/70s-chineselanguage-header.jpg",  200, 100, (None, 100), 'blur', 1000)
        # img4 = ImageAsset("decades/1970/China/unnamed-1.jpg",  0, 500, (colors[4], 100), 'blur', 1000)
        # img5 = ImageAsset("newcrop.png",  500, 500, (colors[2], 255), 'blur', 1000)

def draw():
        global img, offset, easing, imgMask, large, small
        x = 0
        # r, g, b = colors[3]
        # background(r, g, b)
        img.place()
        # img2.place()
        # img3.place()
        # img4.place()
        # img5.place()

        # place colors here
        # for color in colors:
        #         r, g, b = color
        #         fill(r, g, b)
        #         x += 60
        #         circle((x, 60), 60)
        # save("screen.png")

# def dostuff():
        # image(img, (0,0))
        # image(imgMask, (0, height / 2), (img.width / 2, img.height / 2))
        # tint(255, 127)
        # image(imgMask, (0, 0))

if __name__ == '__main__':
        run()