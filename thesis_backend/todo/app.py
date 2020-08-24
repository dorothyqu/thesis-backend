import sys
import time

from flask import Flask, jsonify, request, url_for
import json
from subprocess import Popen, PIPE
import os
from werkzeug.utils import secure_filename # for securing user-made filenames

# constants for uploading images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = '/Users/dorothyqu/PycharmProjects/thesis/thesis_backend/todo/static/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # todo: test this

# define constants
API_BASE = "http://127.0.0.1:5000/"

# helpful functions
def get_img_urls(year, place, imagePaths):

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

    # get the filenames for the 4 initial images
    fNames = ["{}_{}".format(nextIndex, i) for i in range(4)]
    print("% Creating initial collages:")
    for name in fNames:
        print(" - {}".format(name))

    # launch sub-processes to create collages credit: https://stackoverflow.com/a/636601 (edited a lil)
    print("Launching sub-processes...")
    cmd = [
        '/Users/dorothyqu/PycharmProjects/thesis/venv/bin/python',
        '/Users/dorothyqu/PycharmProjects/thesis/thesis_backend/todo/collage_functions/evolutionary.py'
    ]
    running_procs = [Popen(cmd + [fName], stdout=PIPE, stderr=PIPE) for fName in fNames]

    # wait for them to finish
    print("% Waiting for sub-processes to finish...")
    while running_procs:
        for proc in running_procs:
            retcode = proc.poll()
            if retcode is not None: # process finished
                running_procs.remove(proc)
                break
            else: # no process is done, wait a bit and check again
                time.sleep(.1)
                continue
        # either we ran out of procs or `proc` has finished with return code `retcode`
        if retcode is not None: # a proc actually finished
            if retcode == 0:
                print("% - A collage has been created")
            else:
                print("% - There was an error creating a collage.")
    print("All collages complete.")

    # return image URLs
    imageURLs = [url_for('static', filename="{}.png".format(fName)) for fName in fNames]
    return imageURLs

def allowed_file(filename): # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# secure a filename and optionally override existing files. Returns absolute path
def securedAndVersioned(filename, override=False):
    secured = secure_filename(filename)
    [secureFName, secureExt] = secured.rsplit('.', 1)
    if override: # just return the path
        return os.path.join(app.config['UPLOAD_FOLDER'], secured)
    i = 0
    while True: # loop through until we find a file that doesn't exist
        if i == 0:
            fName = secured
        else:
            fName = "{}_{}.{}".format(secureFName, i, secureExt)
        fullPath = os.path.join(app.config['UPLOAD_FOLDER'], fName)
        if not os.path.exists(fullPath):
            break
        i += 1
    return fullPath


# define routes
@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'

@app.route('/help', methods=["GET"])
def info_view():
    """List of routes for this API."""
    output = {
        'bab': ['hello'],
        'info': 'GET /api/v1',
        'register': 'POST /api/v1/accounts',
        'single profile detail': 'GET /api/v1/accounts/<username>',
        'edit profile': 'PUT /api/v1/accounts/<username>',
        'delete profile': 'DELETE /api/v1/accounts/<username>',
        'login': 'POST /api/v1/accounts/login',
        'logout': 'GET /api/v1/accounts/logout',
        "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
        "create task": 'POST /api/v1/accounts/<username>/tasks',
        "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
        "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
        "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
    }
    return jsonify(output)

# generate an image and return image's URL
@app.route('/collage/req', methods=["POST"])
def get_img():

    year = request.form['year']
    place = request.form['place']
    print("Received collage request w/ year '{}' and place '{}'".format(year, place))

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
            filePath = securedAndVersioned(file.filename, override=False) # append a number for version control
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
        imgURLs = get_img_urls(year, place, accepted_filepaths) # make the initial images
        res = jsonify({
            "img_urls": ["{}{}".format(API_BASE, imgURL) for imgURL in imgURLs]
        })
    res.headers.add('Access-Control-Allow-Origin', '*')  # to fix annoying CORS problem
    return res
