"""Get tables from the database and apply heuristic to get list of photos."""

import math

# Weighting for heuristic. Should add to 1.0
DISTANCE_IMPORTANCE = 0.2
LIKES_IMPORTANCE = 0.45
VIEWS_IMPORTANCE = 0.35


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


def weighLikes(likes, dislikes):
    """Create a score that fairly derives from likes and dislikes."""
    pass


def addHeuristic(imageList):
    """Add a heuristic key value pair into a list of dicts for images."""
    total = LIKES_IMPORTANCE * int(imageList['uph']) + \
        VIEWS_IMPORTANCE * int(imageList['viewh']) + \
        DISTANCE_IMPORTANCE * int(imageList['disth'])

    imageList['score'] = total

    return imageList


def getTopN(conn, imageList, n, userLat, userLong):
    """Get top N images according to our heuristic."""
    result = conn.execute("SELECT * FROM Images WHERE Active == TRUE")
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

    return sorted(unsortedImages, key=lambda i: i['heuristic'],
                  reversed=True)[:n]
