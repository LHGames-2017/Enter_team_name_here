import numpy
from structs import *

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def findClosestResource(currentPosition, deserialized_map):
    minDistToResource = 10000000
    minDistResourcePosition = 0
    for x in range(0,len(deserialized_map)):
        for y in range(0, len(deserialized_map[0])):
            if deserialized_map[x][y].Content == TileContent.Resource:
                resPosition = Point(x, y)
                currentDistance = Point().Distance(currentPosition, resPosition)
                if currentDistance < minDistToResource:
                    minDistToResource = currentDistance
                    minDistResourcePosition = resPosition
    return minDistResourcePosition


# TODO: Add obstacle being other players
def createObstacleMap(deserialized_map):
    obstacleMap = [[0 for col in range(0, len(deserialized_map[0]))] for row in range(0,len(deserialized_map))]
    for x in range(0,len(deserialized_map)):
        for y in range(0, len(deserialized_map[0])):
            if deserialized_map[x][y].Content != TileContent.Empty :
                obstacleMap[x][y] = 1
    #print('\n'.join([''.join(['{:4}'.format(item) for item in row])
    #                 for row in obstacleMap]))
    return obstacleMap

def planMovement(obstacleMap, startPoint, endPoint):
    obstacleMap[endPoint.X][endPoint.Y] = 1
    grid = Grid(matrix=obstacleMap)
    print("Position x = " + str(startPoint.X) + ", y = " + str(startPoint.Y) + "\n")
    start = grid.node(startPoint.X, startPoint.Y)
    end = grid.node(endPoint.X, endPoint.Y)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    points = []
    for node in path:
        points.append(Point(node.x, node.y))
    return points

#def upgradeInHouse(currentPosition,upgradetypearray):
#    if upgradetypearray == 'CarryingCapacity':
#        upgrade = UpgradeType.CarryingCapacity
#    elif upgradetypearray == 'AttackPower':
#        upgrade = UpgradeType.AttackPower
#    elif upgradetypearray == 'Defence':
#        upgrade = UpgradeType.Defence
#    elif upgradetypearray == 'MaximumHealth':
#        upgrade = UpgradeType.MaximumHealth
#    elif upgradetypearray == 'CollectingSpeed':
#        upgrade = UpgradeType.CollectingSpeed
#
#    houseLocation = Player.HouseLocation
#    if currentPosition==houseLocation:
#        create_upgrade_action(upgrade)




