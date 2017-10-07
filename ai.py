from flask import Flask, request
from structs import *
import json
#import numpy

from basicFuncs import *

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    bleh = json.dumps(actionContent.__dict__)
    print(bleh)
    return bleh

def create_move_action(target):
    print("Target move x = " + str(target.X) + ", y = " + str(target.Y) + "\n")
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def create_upgrade_action(UpgradeType):
    return create_action("UpgradeAction",UpgradeType)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(20)] for y in range(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map


shortestPath = None
pathIndex = int(0)
resourcePos = None
isFirstMove = True

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), p["Score"],
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    otherPlayers = []

    for players in map_json["OtherPlayers"]:
                player_info = players["Value"]
                p_pos = player_info["Position"]
                player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

                otherPlayers.append(player_info)

    # return decision
    #return create_move_action(Point(0,1))
    offset_x = deserialized_map[0][0].X
    offset_y = deserialized_map[0][0].Y
    offset = Point(offset_x, offset_y)

    global shortestPath
    global resourcePos
    global pathIndex
    global isFirstMove

    currentPosition = Point(x-offset_x,y-offset_y)
    print("position X= " + str(x) + " Y= " + str(y))
    # get nearest ressource
    if shortestPath is None or (currentPosition == player.HouseLocation):
        isFirstMove = True
        print("-------------------------=======================-----------------\n")
        resourcePos = findClosestResource(currentPosition, deserialized_map)
        shortestPath = planMovement(createObstacleMap(deserialized_map), currentPosition, resourcePos)
        print("Resource pos x= " + str(resourcePos.X) + ", y= " + str(resourcePos.Y) + "\n")


    #Temporary state machine
    #GoToMine State
    if player.CarriedRessources < player.CarryingCapacity and Point().Distance(resourcePos, currentPosition) > 1:
        pathIndex += 1
        if pathIndex == 2:
            pathIndex -= 1
        print("Path index is " + str(pathIndex) + " with coords x = " + str(shortestPath[pathIndex].X + offset_x) + ", y = " + str(shortestPath[pathIndex].Y + offset_y) + "\n")
        print("gotomine \n")
        for i in shortestPath:
            print("Path point x = " + str(i.X + offset_x) + ", y = " + str(i.Y + offset_y) + "\n")

        return create_move_action(shortestPath[pathIndex] + offset)
    #Mine State
    if player.CarriedRessources < player.CarryingCapacity and Point().Distance(resourcePos, currentPosition) == 1 and deserialized_map[resourcePos.X][resourcePos.Y].Content == str(TileContent.Resource):
        print("mine \n")
        print("carry: " + str(player.CarriedRessources) + "\n")
        print('\n'.join([''.join(['{:4}'.format(str(item.Content)) for item in row])
                         for row in deserialized_map]))
        return create_collect_action(resourcePos + offset)
    #GoToHouse State
    if (player.CarriedRessources == player.CarryingCapacity or deserialized_map[resourcePos.X][resourcePos.Y].Content != str(TileContent.Resource)) and player.HouseLocation != currentPosition:
        if isFirstMove:
            shortestPath = planMovement(createObstacleMap(deserialized_map), currentPosition, player.HouseLocation - offset)
            isFirstMove = False
        pathIndex += 1
        if pathIndex == 2:
            pathIndex -= 1
        print("gotohouse \n")
        return create_move_action(shortestPath[pathIndex] + offset)

    return create_move_action(currentPosition)




@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
