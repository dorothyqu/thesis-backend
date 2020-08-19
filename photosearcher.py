from google_images_download import google_images_download
import random

# search for an image of a keyword randomly picked from the given filename
def get_random_image(filename):
    with open(filename) as file:
        titles = file.readlines()

    keywords = random.choice(titles)
    # SHOULD I add the file name to the search but take out the txt???
    image_search(keywords)

def image_search(keywords):
    response = google_images_download.googleimagesdownload()
    # played around with parameters to give the "best" aesthetic & recognizable image
    arguments = {"keywords": keywords, "limit": 1, "size": "medium", "type":"photo"}
    paths = response.download(arguments)
    print(paths)

# image_search("The Avengers: United They Stand")
get_random_image('decades/1980/Russia/Soviet Cuisine')