import sys
import time

from flask import Flask, jsonify, request, url_for
import json
# from subprocess import Popen, PIPE
import subprocess
import pathlib
import os
from werkzeug.utils import secure_filename # for securing user-made filenames

from todo.search.imagesearch import gather_images

# # set to true in production
# IS_PRODUCTION = False

# constants for uploading images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# UPLOAD_FOLDER = '/Users/dorothyqu/PycharmProjects/thesis/thesis_backend/todo/static/'
print("Computed upload folder: ")
UPLOAD_FOLDER = str(pathlib.Path(__file__).parent.absolute()) + "/static/"

print(UPLOAD_FOLDER)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 104857600 # 50 * 1024 * 1024 * 1024 # todo: test this

# define constants
API_BASE = "https://generativepaintings.com:5001" #"http://127.0.0.1:5000/"

# helpful functions
def get_img_urls(year, place, imagePaths, imgNum, userId): # set imgNum to a number if we're offspringing

    # open json metadata file and figure out where to save
    mdPath = "{}/metadata.json".format(UPLOAD_FOLDER)
    if os.path.exists(mdPath):
        with open(mdPath, "r") as mdFile:
            metadata = json.load(mdFile)
    else:
            metadata = {
                'lastIndex': 0
            }

    # calculate next index
    nextIndex = metadata['lastIndex'] + 1

    # update the metadata
    metadata['lastIndex'] = nextIndex
    with open(mdPath, "w+") as mdFile:
        json.dump(metadata, mdFile)

    # get the filenames for the 4 images
    fNames = ["{}_{}".format(nextIndex, i) for i in range(4)]
    print("% Creating collages:")
    for name in fNames:
        print(" - {}".format(name))

    # launch sub-processes to create collages
    print("Launching sub-processes (for {} images):".format("initial" if not imgNum else "offspring"))
    if not imgNum: # initial images
        cmds = [[
            "/home/dorothy/thesis-backend/backend_env_3.7.9/bin/python",
            "/home/dorothy/thesis-backend/todo/collage_functions/evolutionary.py"
        ] + [fName] + [userId] for fName in fNames]
    else: # offspring images
        # add the image number to records.txt
        records_file = "{}/records.txt".format(UPLOAD_FOLDER)
        records = open(records_file, "a")  # append mode 
        records.write(imgNum[-1]+"\n") 
        records.close() 
   
        cmds = [[
            "/home/dorothy/thesis-backend/backend_env_3.7.9/bin/python",
            "/home/dorothy/thesis-backend/todo/collage_functions/offspring.py"
        ] + ["{}.json".format(imgNum)] + [fName] for fName in fNames[0:3]]

        # last one has randomized genes to test whether people like evolutionary algs 
        cmds.append([
            "/home/dorothy/thesis-backend/backend_env_3.7.9/bin/python",
            "/home/dorothy/thesis-backend/todo/collage_functions/evolutionary.py"
        ] + [fNames[3]] + [userId])

    # execute commands
    print("% Waiting for sub-processes to finish...")
    for cmd in cmds:
        print('----------')
        print(cmd)
        print('----------')
        subprocess.call(cmd)
        print(" - completed a collage")
    print("All collages complete.")

    imageURLs = ["{}/static/{}.png".format(API_BASE, fName) for fName in fNames] # production/dev
    # imageURLs = [url_for('static', filename="{}.png".format(fName)) for fName in fNames] # dev
    return imageURLs


def allowed_file(filename): # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# secure a filename and optionally override existing files. Returns absolute path
def securedAndVersioned(filename, userId, override=False):
    secured = secure_filename(filename)
    [secureFName, secureExt] = secured.rsplit('.', 1)

    UPLOAD_IMG_FOLDER = str(pathlib.Path(__file__).parent.absolute()) + "/images/" + str(userId)
    app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER

    if override: # just return the path
        return os.path.join(app.config['UPLOAD_IMG_FOLDER'], secured)
    i = 0
    while True: # loop through until we find a file that doesn't exist
        if i == 0:
            fName = secured
        else:
            fName = "{}_{}.{}".format(secureFName, i, secureExt)
        fullPath = os.path.join(app.config['UPLOAD_IMG_FOLDER'], fName)
        if not os.path.exists(fullPath):
            break
        i += 1
    return fullPath


# define routes
@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, Dorothy'
    # return 'Hello, world!'

# generate an image and return image's URL
@app.route('/collage/req', methods=["POST"])
def get_img():
    print("Got request")
    year = request.form['year']
    place = request.form['place']
    userId = request.form['userId']
    print("Received collage request w/ year '{}' and place '{}'".format(year, place))
    print("With ID '{}'".format(userId))

    gather_images(year, place, userId)

    errors = [] # aggregate errors
    accepted_filenames = [] # aggregate saved files
    accepted_filepaths = []
    for file in request.files.getlist('file'):
        print("Got file '{}'".format(file.filename))
        if file.filename == '': # empty filename
            errors.append({'filename': 'is empty'})
        elif not allowed_file(file.filename): # extension not allowed # todo: test this
            errors.append({"extension '{}'".format(file.filename): "not allowed"})
        else:
            filePath = securedAndVersioned(file.filename, userId, override=False) # append a number for version control
            file.save(filePath)
            print("Saved '{}' as '{}'".format(file.filename, filePath))
            accepted_filenames.append(file.filename)
            accepted_filepaths.append(filePath)

    if errors: # don't compute a collage if there were errors
        res = jsonify({
            'errors': errors,
            'accepted_files': accepted_filenames
        })
    else:
        print("Paths to all accepted files:")
        print(accepted_filepaths)
        imgURLs = get_img_urls(year, place, accepted_filepaths, None, userId) # make the initial images
        res = jsonify({
            # "img_urls": ["{}{}".format(API_BASE, imgURL) for imgURL in imgURLs]
            "img_urls" : imgURLs
        })
    
    print('Returning the folllowing image URLS:')
    for imgURL in imgURLs:
        print(" - {}".format(imgURL))
    
    res.headers.add('Access-Control-Allow-Origin', '*')  # to fix annoying CORS problem
    return res


# generate an image and return image's URL
@app.route('/collage/offspring', methods=["POST"])
def get_img_two():

    reqJson = json.loads(request.get_data())
    selectedImg = reqJson["selected_img"]
    userId = reqJson["userId"]
    imgNum = selectedImg.rsplit("/", 1)[1].split(".", 1)[0]
    print("Received collage offspring request w/ selected image: {}".format(selectedImg))
    print("So our image number is '{}'".format(imgNum))
    print("And our user ID is '{}'".format(userId))

    imgURLs = get_img_urls(None, None, None, imgNum, userId)
    res = jsonify({
        "img_urls": imgURLs # ["{}{}".format(API_BASE, imgURL) for imgURL in imgURLs]
    })
    print('Returning the folllowing image URLS:')
    for imgURL in imgURLs:
        print(" - {}".format(imgURL))
    res.headers.add('Access-Control-Allow-Origin', '*')  # to fix annoying CORS problem
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 
