# create a color palette given root color and whether it's monochromatic, analogous,
# complementary, split complementary, triadic, and tetradic
import random

from p5 import *

# returns a list of colors
# color is RGB tuple
# schemes: MONO, ANA, COMP, SPLCOMP, TRI, TETR
def get_palette(color, scheme):
    colors = []
    golden = 1.618
    r, g, b = color
    if scheme == 1:
        colors.append((min(255, int(r * golden * golden)), min(255, int(g * golden * golden)),min(255, int(b * golden * golden))))
        colors.append((min(255, int(r * golden)), min(255, int(g * golden)), min(255, int(b * golden))))
        colors.append(color)
        colors.append((int(r/golden), int(g/golden), int(b/golden)))
        colors.append((int(r / golden/golden), int(g / golden/golden), int(b / golden/golden)))

    if scheme == 2:
        colors.append((min(255, int(r * golden * golden)*.9), min(255, int(g * golden * golden*.95)),min(255, int(b * golden * golden*golden))))
        colors.append((min(255, int(r * golden*1.1)), min(255, int(g * golden*.75)), min(255, int(b * golden*.7))))
        colors.append(color)
        colors.append((int(r*1.1/golden), int(g*1.2/golden), int(b*1.2*golden*golden)))
        colors.append((int(r/golden/golden/golden/golden), int(g/golden/golden), b))

    if scheme == 3:
        colors.append((min(255, int(g * golden*1.2)), min(255, int(g * golden*golden*.8)),min(255, int(r*golden))))
        colors.append((min(255, int(b*golden*golden)), min(255, int(g*.95)), min(255, int(r*1.1/golden))))
        colors.append(color)
        colors.append((int(r/golden), int(g/golden), int(b/golden)))
        colors.append((int(r / golden/golden), int(g / golden/golden), int(b / golden/golden)))

    else:
        colors.append((min(255, int(b * golden*golden)), min(255, int(g/golden)),min(255, int(r/golden))))
        colors.append((min(255, int(r/1.1)), min(255, int(b*golden)), min(255, int(g*1.1/golden))))
        colors.append(color)
        colors.append((int(180*(b/255)), int(180*(g/255)), min(255, int(180*(r*10/255)))))
        colors.append((int(100*(r/255)), int(120*(g/255)), int(b*golden*golden*golden)))

    return colors

def randomcolor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def setup():
    size(500, 500)

def draw():
    no_stroke()
    original = (252, 115, 7)
    colors = get_palette(original, "MONO")
    x = 0
    for color in colors:
        r, g, b = color
        fill(r, g, b)
        x+= 60
        circle((x, 60), 60)

    x = 0
    colors = get_palette(original, "ANA")
    for color in colors:
        r, g, b = color
        fill(r, g, b)
        x+= 60
        circle((x, 120), 60)

    x = 0
    colors = get_palette(original, "COMP")
    for color in colors:
        r, g, b = color
        fill(r, g, b)
        x+= 60
        circle((x, 180), 60)

    x = 0
    colors = get_palette(original, "SPLCOMP")
    for color in colors:
        r, g, b = color
        fill(r, g, b)
        x+= 60
        circle((x, 240), 60)

if __name__ == '__main__':
     run()