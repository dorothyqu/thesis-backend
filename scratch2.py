# import fiona
# import shapely.geometry as geometry
# input_shapefile = 'concave_demo_points.shp'
# shapefile = fiona.open(input_shapefile)
# points = [geometry.shape(point['geometry'])
#           for point in shapefile]
import json

from Collage import Collage

fName = "/Users/dorothyqu/PycharmProjects/thesis/flask/todo/static/{}".format("collage.json")
# load up genes
with open(fName, 'r') as infile:
    genes = json.load(infile)

# actually set up the collage
collage = Collage(genes)
print(collage.createOffspring())