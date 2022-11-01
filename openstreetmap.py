import osmium as osm
import math
import folium
import webbrowser
import os
import sys

#Miguel---------------------------------------------------------------

class Node:
    def __init__(self,type,id,lat,lon):
        self.elem_type=type,
        self.id=id,
        self.latitude = lat
        self.longitude = lon
        self.pos = {"latitude":lat, "longitude":lon}
        self.type = type
        self.f = 0
        self.g = 0
        self.h = 0
        self.visited = False
        self.closed = False
        self.parent = None
        self.neighbors= []

    def get_neighbors(self):
        return self.neighbors

    def __eq__(self, other):
        self.id == other.id

    def __lt__(self, other):
        pass

#Ricardo--------------------------------------------------------------------------------------------------

class Vertex:

  def __init__(self, node_start_ref, node_end_ref, graph, vel=60, oneway=False):

    self.node_start_ref = node_start_ref
    self.node_end_ref = node_end_ref
    self.vel = vel

    currentNode = graph.get_node(node_start_ref)
    currentNode.neighbors.append(node_end_ref)

    if not oneway:
      graph.get_node(node_end_ref).neighbors.append(node_start_ref)

#Ric y Denis-------------------------------------------------------------------------------------------------
      
class Graph(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.nodes = []
        self.ways = []
        self.vertices = []

    def tag_inventory(self, elem, elem_type):
        self.nodes.append(Node(elem_type,elem.id,elem.location.lat,elem.location.lon))

    def tag_way(self, elem, elem_type):
            for i in range(len(elem.nodes) - 1):
                node_start_ref = elem.nodes[i].ref
                node_end_ref = elem.nodes[i+1].ref
                self.vertices.append(Vertex(node_start_ref, node_end_ref, self))
    
    def get_node(self, id):
        for node in self.nodes:
            nodeId = node.id[0]
            if nodeId == id:
                return node
            
    def node(self,n):
        self.tag_inventory(n,"node")
   
    def way(self, w):
        self.tag_way(w, "way")

graph = Graph()

graph.apply_file("Corales_Sur.osm")

def euclid_dist(node_start, node_end):
    return math.sqrt(math.pow(node_start.longitude - node_end.longitude, 2) + math.pow(node_start.latitude - node_end.latitude, 2))


#Prado------------------------------------------------------------

def aStarSearch(start, end):

  openList = [start]

  while len(openList) > 0:

    lowFScoreIndex = 0

    for i in range(len(openList)):
      if openList[i].f < openList[lowFScoreIndex].f:
        lowFScoreIndex = i

    currentNode = openList[lowFScoreIndex]
    
    if currentNode.id == end.id:
      print('success!')
      curr = currentNode
      ret = []
      while curr.parent:
        ret.append(curr)
        curr = curr.parent
      
      return ret[::-1]

    del openList[lowFScoreIndex]
    currentNode.closed = True

    for neighborId in currentNode.neighbors:
      neighbor = graph.get_node(neighborId)

      if neighbor.closed: continue

      gScore = currentNode.g + 1

      gScoreIsBest = False

      if not neighbor.visited:
        gScoreIsBest = True
        neighbor.h = euclid_dist(neighbor, end)
        neighbor.visited = True
        openList.append(neighbor)
        
      elif gScore < neighbor.g:
        gScoreIsBest = True

      if gScoreIsBest:
        neighbor.parent = currentNode
        neighbor.g = gScore
        neighbor.f = neighbor.g + neighbor.h
        neighbor.debug = f"POS: {neighbor.pos} F: {neighbor.f} G: {neighbor.g} H: {neighbor.h}"

  return []

#Denis
def main(inicio, meta):
  mapa =folium.Map(location=[18.4740026,-69.8240954], zoom_start=15)

  start = graph.nodes[inicio]
  end = graph.nodes[meta]
  result = aStarSearch(start, end)
  position = []
  for node in result:
    #El position en este caso debe ser append, ya que se necesita unir la informacion de los nodos para 
    #recorrer la informacion como si fuera una.
    position.append([node.latitude, node.longitude])
    #Es el módulo que nos permite ejecutar paso a paso nuestro código y visualizar
    #qué está ocurriendo en cada momento. Se suele usar normalmente para encontrar 
    #fallos (bugs) en nuestros programas y poder solucionarlos
    print(node.debug)

#Miguel
  folium.PolyLine(position).add_to(mapa)
  folium.Marker(location=[end.latitude, end.longitude], popup="Destino",icon=folium.Icon(color="black")).add_to(mapa)
  mapa.save('mapa.html')











