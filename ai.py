from flask import Flask, request
from structs import *
import json
import numpy

from basicFuncs import *

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

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

    currentPosition = Point(x-offset_x,y-offset_y)
    print("position X= " + str(x) + " Y= " + str(y))
    # get nearest ressource
    #print("BLEHHHHHHH======= " + str(bot.shortestPath == None))
    if bot.shortestPath == None or (currentPosition == player.HouseLocation and bot.ressourcePos != None and deserialized_map[bot.ressourcePos.X][bot.ressourcePos.Y].Content != str(TileContent.Resource)):
        bot.ressourcePos = findClosestResource(currentPosition, deserialized_map)
        print("Resource pos x= " + str(bot.ressourcePos.X) + ", y= " + str(bot.ressourcePos.Y) + "\n")
        bot.shortestPath = planMovement(createObstacleMap(deserialized_map), currentPosition, bot.ressourcePos)

    #Temporary state machine
    #GoToMine State
    if player.CarriedRessources < player.CarryingCapacity and Point().Distance(bot.ressourcePos, currentPosition) > 1:
        bot.pathIndex += 1
        print("Path index is " + str(bot.pathIndex) + "with coords x = " + str(bot.shortestPath[bot.pathIndex].X + offset_x) + ", y = " + str(bot.shortestPath[bot.pathIndex].Y + offset_y) + "\n")
        print("gotomine \n")
        #for i in bot.shortestPath:
        #    print("Path point x = " + str(i.X) + ", y = " + str(i.Y) + "\n")
        return create_move_action(bot.shortestPath[bot.pathIndex] + offset)
    #Mine State
    if player.CarriedRessources < player.CarryingCapacity and Point().Distance(bot.ressourcePos, currentPosition) == 1 and deserialized_map[bot.ressourcePos.X][bot.ressourcePos.Y].Content == TileContent.Resource:
        print("mine \n")
        return create_collect_action(bot.ressourcePos)
    #GoToHouse State
    if (player.CarriedRessources == player.CarryingCapacity or deserialized_map[bot.ressourcePos.X][bot.ressourcePos.Y].Content != TileContent.Resource) and player.HouseLocation != currentPosition:
        bot.pathIndex -= 1
        print("gotohouse \n")
        return create_move_action(bot.shortestPath[bot.pathIndex] + offset)

    return create_move_action(currentPosition)


bot.shortestPath = None
bot.pathIndex = 0
bot.RessourcePos = None

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
