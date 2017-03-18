"""Main init file. File does not need to be edited except for server edits."""

import secure
from utils.generalutils import urlify
from utils.upload import *

import math
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Run server and rate limit.
app = Flask(__name__)
DEBUG = True
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=["10000 per hour"]
)

# Set config vars.
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = secure.DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app, convert_unicode=False)

# Models


class Photo(db.Model):
    """Photo table."""

    id = db.Column(db.BigInteger, primary_key=True)

    uploadedTime = db.Column(db.DateTime, nullable=False)

    caption = db.Column(db.Text(), default="")
    language = db.Column(db.VARCHAR(10), nullable=False)

    views = db.Column(db.Integer, default=0, nullable=False)

    active = db.Column(db.Boolean, default=True, nullable=False)

    fileName = db.Column(db.Text(), nullable=False)

    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    likes = db.Column(db.Integer, default=0, nullable=False)
    dislikes = db.Column(db.Integer, default=0, nullable=False)


# Functions

# Weighting for heuristic. Should add to 1.0
DISTANCE_IMPORTANCE = 0.2
LIKES_IMPORTANCE = 0.45
VIEWS_IMPORTANCE = 0.35

epoch = datetime(1970, 1, 1)


def getDistance(lat1, long1, lat2, long2):
    """Get the distance between two geographic points."""
    # With credit to Salvador Dali on StackOverflow.

    PI_DIV_TWO = 0.017453292519943295
    EARTH_RAD_BY_TWO = 12742

    a = 0.5 - math.cos((lat2 - lat1) * PI_DIV_TWO) / 2 + \
        math.cos(lat1 * PI_DIV_TWO) * \
        math.cos(lat2 * PI_DIV_TWO) * \
        (1 - math.cos((long2 - long1) * PI_DIV_TWO)) / 2

    return EARTH_RAD_BY_TWO * math.asin(math.sqrt(a))


def percentifyList(imageList):
    """Given a list of images, squash all objective values to subjective."""
    # e.g.: [{url, likesHeuristic, distanceInKm, views, ...}]
    #   to: [{url, likesPercentage, distancePercentage, viewsPercentage}, ...]

    likeScoreSum, distanceSum, viewsSum = 0
    for i in imageList:
        likeScoreSum += i['likeScore']
        viewsSum += int(i['views'])
        distanceSum += i['distance']

    for i in imageList:
        i['uph'] = i['likeScore'] / likeScoreSum
        i['viewh'] = 1.0 - (int(i['views']) / viewsSum)
        i['disth'] = i['distance'] / distanceSum

    return imageList


def epoch_seconds(date):
    """Return time distance from date and epoch."""
    td = date - epoch

    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def scoreDiff(ups, downs):
    """Calculate difference between scores."""
    return ups - downs


def weighLikes(ups, downs, date):
    """Weigh likes and return likes score."""
    s = scoreDiff(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)


def addHeuristic(imageList):
    """Add a heuristic key value pair into a list of dicts for images."""
    total = LIKES_IMPORTANCE * int(imageList['uph']) + \
        VIEWS_IMPORTANCE * int(imageList['viewh']) + \
        DISTANCE_IMPORTANCE * int(imageList['disth'])

    imageList['score'] = total

    return imageList


def getTopN(n, userLat, userLon):
    """Get top N images according to our heuristic."""
    result = Photo.query.all()
    imageList = list()

    # Generate distance for everything in the list. Make image list.
    for row in result:
        image = row
        image['distance'] = getDistance(userLat, userLong,
                                        float(row['lat']), float(row['lon']))
        image['likeScore'] = weighLikes(row['likes'], row['dislikes'])
        imageList.append(image)

        # Also, change views += 1.
        row.views += 1
        db.session.commit()

    # Put the image list through all functions until end heuristic is found.
    unsortedImages = addHeuristic(percentifyList(imageList))

    sortedFull = sorted(unsortedImages, key=lambda i: i['heuristic'],
                        reversed=True)

    if len(sortedFull) > n:
        sortedFull = sortedFull[:n]

    return [{'img': i['url'], 'id': i['id']} for i in sortedFull]


# Views

@app.route('/')
def standard():
    """Test page."""
    return "Nothing to see here. Move along.", 403


@app.route('/api/upload', methods=["POST"])
def upload():
    """Upload a file to the host. Return an error if it fails."""
    file = request.files['img']
    capt = request.form['caption']
    lang = request.form['language']
    lat1 = request.form['lat']
    lon1 = request.form['lon']

    # Filename must be nonempty to be valid.
    if file.filename == '':
        return "Forbidden: cannot upload file with no filename."

    # If the file is allowed, continue. If not, return 403.
    if file and allowed_file(file.filename) and checkApiKey(
            str(request.form['apikey']).rstrip()):
        fn = hashFile(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))

        # Upload renamed file to database.
        # newPhoto = Photo(uploadedTime=datetime.utcnow,
        #                  caption=capt.encode('utf-8'),
        #                  language=lang.encode('utf-8'),
        #                  views=0, active=True,
        #                  fileName=fn.encode('utf-8'),
        #                  lat=lat1, lon=lon1,
        #                  likes=0, dislikes=0)

        newPhoto = Photo(uploadedTime=datetime.utcnow,
                         caption="test",
                         language="en-US",
                         views=0, active=True,
                         fileName="test.png",
                         lat=100, lon=-100,
                         likes=0, dislikes=0)

        db.session.add(newPhoto)
        db.session.commit()

        return url_for('uploaded_file', filename=filename)

    return "Forbidden: ensure the file extension is allowed and API key " + \
        "is correct."


@app.route('/api/media/<filename>', methods=["POST"])
def uploadedFile(filename):
    """Show an uploaded file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/photo_list', methods=["POST"])
def sendTopPhotos():
    """From a POST request send n photos in JSON format to the requestee."""
    n = request.form['n']  # number of photos, max.
    apikey = request.form['apikey']
    userLat = request.form['userLat']
    userLon = request.form['userLon']

    try:
        if int(n) < 1:
            raise ValueError
    except ValueError:
        return "Error: n must be an int greater than 0."

    if not checkApiKey(apikey):
        return "Forbidden: API key not in list."

    return getTopN(n, userLat, userLon)


@app.route('/api/upvote/<filename>', methods=["POST"])
def upvote():
    """Apply exactly one upvote for a photo."""
    apikey = request.form['apikey']

    if not checkApiKey(apikey):
        return "Forbidden: API key not in list."

    f = Photo.query.filter_by(fileName=filename).first()
    f.upvotes += 1
    db.session.commit()


@app.route('/api/downvote/<filename>', methods=["POST"])
def downvote(filename):
    """Apply exactly one downvote for a photo."""
    apikey = request.form['apikey']

    if not checkApiKey(apikey):
        return "Forbidden: API key not in list."

    f = Photo.query.filter_by(fileName=filename).first()
    f.downvotes += 1
    db.session.commit()


@app.errorhandler(403)
def fourOhThree(e):
    """Provide standardised string error message as response."""
    return "Access denied. Insufficient permissions for request.", 403


@app.errorhandler(404)
def fourOhFour(e):
    """Provide standardised string error message as response."""
    return "Not found. What you are looking for doesn't exist.", 404


@app.errorhandler(410)
def fourTen(e):
    """Provide standardised string error message as response."""
    return "Not found. The file was here before, but now it's gone.", 410


@app.errorhandler(500)
def fiveHundred(e):
    """Provide standardised string error message as response."""
    return "Internal server error. One of our devs messed up.", 500


db.create_all()
db.session.commit()

# Cron

sched = Celery()


@sched.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Execute every morning at 7:30 a.m."""
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        test.s(),
    )


@sched.task
def deleteOld():
    """Delete all photos older than 24 hours."""
    twentyFourHoursAgo = timedelta(hours=24)

    for i in Photo.query.filter_by(uploadedTime < twentyFourHoursAgo):
        db.session.delete(i)
        db.session.commit()
