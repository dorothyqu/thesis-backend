import pathlib
from google_images_search import GoogleImagesSearch
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api = 'AIzaSyClbHrF30cwcmgnv-POV0YLDkG9O2MSYv0'
cx = '009584431968846876078:joks3ggv695'

PATH_TO_APPEND = str(pathlib.Path(__file__).parent.parent.absolute()) + "/"
keywords_file = "keywords.txt"


# searches 2 images per query
def search_image(query, path, img_id):
    gis = GoogleImagesSearch(api, cx)

    # define search params:
    _search_params = {
        'q': query,
        'num': 3,
    }

    # this will search and download:
    gis.search(search_params=_search_params, path_to_dir=path, custom_image_name=img_id)


# this goes through all the keywords, appends them to the query
# and makes one search per keyword
# 2 images per search?
def keyword_search(query, path):
    file = open(keywords_file)
    keywords = file.read().splitlines()

    # now make one search per word
    img_id = 0
    for kw in keywords:
        print(kw)
        search_image(query + " " + kw, path, str(img_id))
        img_id +=1

# gathers all the images that you need, given the
# year, place ,and the id of the image directory
# makes the directory if it does not exist already
def gather_images(year, place, id):
    img_folder = PATH_TO_APPEND + 'images/' + id
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    query = year + " " + place
    keyword_search(query, img_folder)

# gather_images("1987", "Russia", "4")