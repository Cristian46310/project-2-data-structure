from Back.Controller.ControllerConstellations import ControllerConstellations as Constellations

class dijkstra:
    """
    dijkstra class: Builds a weighted graph from constellation data and computes shortest paths.
    This class depends on an external Constellations controller instance (self.controller) to fetch
    constellation data and to resolve star identifiers into star names. It constructs an in-memory,
    directed weighted graph of star-to-star links (ignoring links marked as blocked) and implements
    Dijkstra's algorithm to compute the shortest path (minimum total distance) between two stars.
    Attributes
    ----------
    controller : Constellations
        A controller object used to fetch constellation JSON data and to map star IDs to star names.
    Methods
    -------
    flujoOptimo(Start, end)
        Build a graph from constellation data and compute the shortest path between the stars named
        Start and end. Returns None if no data is available or if the destination is unreachable.
        Parameters:
            Start (str): The name of the starting star node.
            end (str): The name of the destination star node.
        Returns:
            dict or None: If a path exists, returns a dict with keys:
                - 'distance' (float): Total distance of the shortest path.
                - 'path' (list of str): Ordered list of star names from Start to end inclusive.
            Returns None if constellation data is missing or if end is unreachable.
    methodDijkstra(graph, start, end)
        Run Dijkstra's shortest-path algorithm on an explicit adjacency representation of a graph.
        The graph is expected to be a dict mapping node names to dicts of neighbor: weight pairs.
        Parameters:
            graph (dict): { node_name: { neighbor_name: weight, ... }, ... }
            start (str): Name of the start node (must be present in graph).
            end (str): Name of the end node (must be present in graph).
        Behavior:
            - Uses a simple O(V^2) implementation (selects the unvisited node with minimal current
              tentative distance by linear search).
            - Maintains `distances` (tentative shortest distances) and `previous` (to reconstruct path).
            - If the end node is unreachable, returns None.
        Returns:
            dict or None: On success, returns {'distance': total_distance, 'path': [start, ..., end]}.
            Returns None if `end` is unreachable (distance is infinite).
    """
    def __init__(self):
        self.controller = Constellations()
    #Metodo para crear el grafo a partir de los datos de las constelaciones    
    def flujoOptimo(self, Start, end):
        data = self.controller.fetchJsonConstellations()
        if data is None:
            print("No data available")
            return None
        else:
            graph = {}
            for constellation in data.get('constellations', []):
                for star in constellation.get('starts', []):
                    starName = star.get('label')
                    if starName not in graph:
                        graph[starName] = {}
                    for link in star.get('linkedTo', []):
                        if link.get('blocked', False):
                            continue  
                        linkedStarId = link.get('starId')
                        distance = link.get('distance')
                        linkedStarName = self.controller.fetchStarNameById(linkedStarId)
                        if linkedStarName:
                            graph[starName][linkedStarName] = distance
            return self.methodDijkstra(graph,Start,end)
    
    #Metodo Dijkstra busca el flujo optimo entre dos nodos
    def methodDijkstra(self,graph,start,end):  #start y end son los nombres de las estrellas
        infity = float('inf') #variable que representa infinito
        distances={node: infity for node in graph} #compresion de diccionario
        previous={node: None for node in graph}
        visitados=set() #set() crea un conjunto vacio
        distances[start]=0 
        while len(visitados)<len(graph):
            current=None
            minDistance=infity
            for node in graph:
                if node not in visitados and distances[node]<minDistance:
                    minDistance=distances[node]
                    current=node
            if current is None:
                break
            visitados.add(current)
            #for clave:valor in grafo[posicionActual].items(): items=lista de las tuplas que tiene el diccionario ejemplo: (nodo,distance)
            for neighbor, weight in graph[current].items():
                if neighbor not in visitados:
                    newDistance=distances[current]+weight
                    if newDistance<distances[neighbor]:
                        distances[neighbor]=newDistance
                        previous[neighbor]=current

        path=[]
        current=end
        while current is not None:
            path.append(current)
            current=previous[current]
        path.reverse()
        if distances[end]==infity:
            return None
        return {'distance': distances[end], 'path': path}
    



