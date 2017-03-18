"""Get tables from the database and apply heuristic to get list of photos."""

import math
from datetime import datetime, timedelta

from models import Photo, db

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


def getTopN(conn, imageList, n, userLat, userLong):
    """Get top N images according to our heuristic."""
    result = Photo.query.filter_by(active=True).all()
    imageList = list()

    # Generate distance for everything in the list. Make image list.
    for row in result:
        image = row
        image['distance'] = getDistance(userLat, userLong,
                                        float(row['lat']), float(row['lon']))
        image['likeScore'] = weighLikes(row['likes'], row['dislikes'])
        imageList.append(image)

    # Put the image list through all functions until end heuristic is found.
    unsortedImages = addHeuristic(percentifyList(imageList))

    sortedFull = sorted(unsortedImages, key=lambda i: i['heuristic'],
                        reversed=True)

    if len(sortedFull) > n:
        sortedFull = sortedFull[:n]

    return [{'img': i['url'], 'id': i['id']} for i in sortedFull]
