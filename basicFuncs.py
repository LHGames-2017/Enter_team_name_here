import numpy



def findClosestResource(currentPosition, deserialized_map):
    minDistToResource = 10000000
    minDistResourcePosition = 0
    for x in range(deserialized_map):
        for y in range(deserialized_map[x]):
            if deserialized_map[x][y].Content == Resource:
                resPosition = Point(x, y)
                currentDistance = Point.Distance(currentPosition, resPosition)
                if currentDistance < minDistToResource:
                    minDistToResource = currentDistance
                    minDistResourcePosition = resPosition
    return minDistResourcePosition


# TODO: Add obstacle being other players
def createObstacleMap(deserialized_map):
    obstacleMap = numpy.zeros(len(deserialized_map), len(deserialized_map[0]))
    for x in range(deserialized_map):
        for y in range(deserialized_map[x]):
            if deserialized_map[x][y].Content == Lava or deserialized_map[x][y].Content == Wall:
                obstacleMap[x][y] = 1
    return obstacleMap

