import numpy
from structs import *
from ai import *

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder



def findClosestResource(currentPosition, deserialized_map):
    minDistToResource = 10000000
    minDistResourcePosition = 0
    for x in range(deserialized_map):
        for y in range(deserialized_map[x]):
            if deserialized_map[x][y].Content == TileContent.Resource:
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
            if deserialized_map[x][y].Content == TileContent.Lava or deserialized_map[x][y].Content == TileContent.Wall:
                obstacleMap[x][y] = 1
    return obstacleMap

def planMovement(obstacleMap, startPoint, endPoint):
    grid = Grid(matrix=obstacleMap)
    start = grid.node(startPoint.x, startPoint.y)
    end = grid.node(endPoint.x, endPoint.y)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    points = []
    for node in path:
        points.append(Point(node.x, node.y))
    return points

def upgradeInHouse(currentPosition,upgradetypearray):
    if upgradetypearray == 'CarryingCapacity':
        upgrade = UpgradeType.CarryingCapacity
    elif upgradetypearray == 'AttackPower':
        upgrade = UpgradeType.AttackPower
    elif upgradetypearray == 'Defence':
        upgrade = UpgradeType.Defence
    elif upgradetypearray == 'MaximumHealth':
        upgrade = UpgradeType.MaximumHealth
    elif upgradetypearray == 'CollectingSpeed':
        upgrade = UpgradeType.CollectingSpeed

    houseLocation = Player.HouseLocation
    if currentPosition==houseLocation:
        create_upgrade_action(upgrade)




