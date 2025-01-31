import json
from src.logger import print
from src.variables import *
from src.settings import *
from src.helpers import *
from src.mainUI import *
import sys

class Item:
    Uid = 0
    Type = ""

class Node:
    Uid = 0
    X = 0
    Z = 0
    Rotation = 0
    ForwardItem = None
    BackwardItem = None
    
nodes = []
optimizedNodes = {}
nodeFileName = variables.PATH + "/plugins/Map/GameData/nodes.json"

def LoadNodes():
    global nodes
    global optimizedNodes
    
    loading = LoadingWindow("Parsing Nodes...", grab=False, progress=0, totalProgress=0)
    
    jsonData = json.load(open(nodeFileName))
    
    count = 0
    for node in jsonData:
        nodeObj = Node()
        nodeObj.Uid = node["Uid"]
        nodeObj.X = node["X"]
        nodeObj.Z = node["Z"]
        nodeObj.Rotation = node["Rotation"]
        try:
            nodeObj.ForwardItem = Item()
            nodeObj.ForwardItem.Uid = node["ForwardItem"]["Uid"]
            nodeObj.ForwardItem.Type = node["ForwardItem"]["Type"]
        except:
            nodeObj.ForwardItem = None
            
        try:
            nodeObj.BackwardItem = Item()
            nodeObj.BackwardItem.Uid = node["BackwardItem"]["Uid"]
            nodeObj.BackwardItem.Type = node["BackwardItem"]["Type"]
        except:
            nodeObj.BackwardItem = None
        
        nodes.append(nodeObj)
        count += 1
        
        if count % 1000 == 0:
            sys.stdout.write(f"\rLoaded {count} nodes.\r")
            LoadingWindow.update(loading, progress=count/len(jsonData) * 100)
    
    sys.stdout.write(f"Loaded {count} nodes.\nOptimizing array...\n")      
    
    # Populate the optimized nodes dict by getting the first 3 numbers of the node Uid
    loading.update(text="Optimizing array...", progress=False)
    for node in nodes:
        firstTwo = str(node.Uid)[:3]
        if firstTwo not in optimizedNodes:
            optimizedNodes[firstTwo] = []
        
        optimizedNodes[firstTwo].append(node)
    
    loading.destroy()
    print(f"Node parsing done!")
    
def GetNodeByUid(uid):
    
    if uid == 0:
        return None
    if uid == None:
        return None
    
    firstThree = str(uid)[:3]
    if firstThree in optimizedNodes:
        for node in optimizedNodes[firstThree]:
            if node.Uid == uid:
                return node
    else:
        for node in nodes:
            if node.Uid == uid:
                return node
        
    return None