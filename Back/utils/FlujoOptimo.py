from Back.Controller.ControllerConstellations import ControllerConstellations as Constellations

class dijkstra:
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
    



