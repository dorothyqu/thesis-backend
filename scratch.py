# import the necessary packages
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pylab as pl
import shapely.geometry as geometry
import warnings
import sys
from descartes import PolygonPatch
import alphashape

from PIL import Image

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

def get_edges(imagePath):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)
	# apply Canny edge detection using a wide threshold, tight
	# threshold, and automatically determined threshold
	tight = cv2.Canny(blurred, 225, 250)
	# auto = auto_canny(blurred)
	# show the images
	# cv2.imshow("Edges", tight)

	# split image into four
	height, width = tight.shape[:2]
	# quad1 = tight[0: int(height/4), 0: int(width/4)]
	quad1 = tight[0: int(height/2), 0: int(width/2)]
	cv2.imshow("half", quad1)

	# turn all white pixels into points
	np_quad1 = np.array(quad1)

	indices = np.where(np_quad1 == [255])
	return indices[1], indices[0][::-1]

x, y = get_edges("dog.jpg")
#
# z = np.polyfit(x, y, 3)
# p = np.poly1d(z)
# p(10)
# with warnings.catch_warnings():
#     warnings.simplefilter('ignore', np.RankWarning)
#     p30 = np.poly1d(np.polyfit(x, y, 30))
# p30(4.5)
#
# xp = np.linspace(500, 0)
# _ = plt.plot(x, y, '.', xp, p(xp), '-', xp, p30(xp), '--')
# plt.show()


def give_me_a_line_like_excel(x, y):
	coefs = np.polyfit(x, y, deg=30)
	p_obj = np.poly1d(coefs)  # this is a convenience class
	return p_obj

# p_obj = give_me_a_line_like_excel(x, y)
# x_line = np.linspace(min(x), max(x), 100)  # make new xvalues
# y_line = p_obj(x_line)
#
# plt.plot(x, y, 'o')
# plt.plot(x_line, y_line, 'r--')
# plt.show()
points = tuple(zip(x, y))
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
alpha_shape = alphashape.alphashape(points, 3.5)
fig, ax = plt.subplots()
ax.scatter(*zip(*points))
ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()