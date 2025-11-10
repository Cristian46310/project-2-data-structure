import random
import math
from .star_drawer import StarDrawer

class GraphManager:
    def __init__(self, canvas):
        self.star_drawer = StarDrawer(canvas)
        self.constellation_colors = {}
        self.layouts = {}
        self.width = 600
        self.height = 500
        self.margin = 40

    def generate_random_color(self):
        """Genera un color aleatorio en formato hexadecimal"""
        return f'#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}'

    def draw_constellations(self, reader):
        """Dibuja todas las constelaciones"""
        try:
            self.star_drawer.clear_canvas()
            constellations = reader.allConstellations()
            
            if not constellations:
                print("No se encontraron constelaciones")
                return []

            # Asignar colores a cada constelación
            for constellation in constellations:
                self.constellation_colors[constellation] = self.generate_random_color()

            # Encontrar estrellas compartidas
            shared_stars = self._find_shared_stars(reader, constellations)
            
            # Dibujar cada constelación
            for constellation in constellations:
                self._draw_constellation(reader, constellation, shared_stars)
                
            return constellations
        except Exception as e:
            print(f"Error al dibujar constelaciones: {e}")
            return []

    def _get_constellation_stars(self, reader, constellation_name):
        """Obtiene los datos completos de las estrellas de una constelación"""
        json_data = reader.readJsonConstellations()
        if json_data:
            for const in json_data['constellations']:
                if const['name'] == constellation_name:
                    return const['starts']
        return []

    def _find_shared_stars(self, reader, constellations):
        """Encuentra estrellas que pertenecen a múltiples constelaciones"""
        try:
            star_count = {}
            for constellation in constellations:
                stars = self._get_constellation_stars(reader, constellation)
                for star in stars:
                    if 'label' in star:
                        star_count[star['label']] = star_count.get(star['label'], 0) + 1
            
            return {star for star, count in star_count.items() if count > 1}
        except Exception as e:
            print(f"Error al buscar estrellas compartidas: {e}")
            return set()

    def _draw_constellation(self, reader, constellation, shared_stars):
        """Dibuja una constelación individual"""
        try:
            stars = self._get_constellation_stars(reader, constellation)
            if not stars:
                return

            color = self.constellation_colors[constellation]
            
            # Asignar coordenada x basada en el índice
            x_spacing = 550 // (len(stars) + 1)
            
            # Dibujar estrellas y sus conexiones
            for i, star in enumerate(stars, 1):
                if 'label' not in star or 'coordenates' not in star:
                    continue
                    
                # Calcular posición x basada en el índice
                x = i * x_spacing
                # Usar la coordenada y del JSON
                y = star['coordenates'].get('y', 250)  # valor por defecto 250 si no hay y
                
                # Dibujar la estrella
                star_color = 'red' if star['label'] in shared_stars else color
                self.star_drawer.draw_star(x, y, star_color, star['label'])
                
                # Dibujar conexiones
                if 'linkedTo' in star and star['linkedTo']:
                    for link in star['linkedTo']:
                        # Encontrar la estrella conectada
                        target_star = next((s for s in stars if s['id'] == link['starId']), None)
                        if target_star and 'coordenates' in target_star:
                            target_x = stars.index(target_star) * x_spacing
                            target_y = target_star['coordenates'].get('y', 250)
                            self.star_drawer.draw_connection(x, y, target_x, target_y, color)

        except Exception as e:
            print(f"Error al dibujar constelación {constellation}: {e}")
            raise  # Para ver el error completo
    
    def draw_constellations(self, reader):
        """Calcula layout y dibuja todas las constelaciones (y guarda layout para redraw)."""
        try:
            self.star_drawer.clear_canvas()
            constellations = reader.allConstellations()
            if not constellations:
                print("No se encontraron constelaciones")
                return []

            for constellation in constellations:
                self.constellation_colors[constellation] = self.generate_random_color()

            shared_stars = self._find_shared_stars(reader, constellations)

            # calcular layout por constelación y dibujar
            self.layouts = {}
            for constellation in constellations:
                stars = self._get_constellation_stars(reader, constellation)
                nodes, edges = self._compute_layout(stars)
                self.layouts[constellation] = {'nodes': nodes, 'edges': edges, 'shared': shared_stars}
                self._draw_layout(constellation)
            return constellations
        except Exception as e:
            print(f"Error al dibujar constelaciones: {e}")
            return []

    def _compute_layout(self, stars):
        """Small force-directed layout. Retorna nodes y edges.
           nodes: list de dict {id,label,x,y}
           edges: list de (id_source, id_target)
        """
        # crear nodos iniciales
        nodes = []
        id_to_node = {}
        n = len(stars) if stars else 1
        spacing_x = max(80, (self.width - 2*self.margin) // max(1, n))
        for i, s in enumerate(stars):
            # si JSON tiene coordenadas y.x usar como inicial
            init_x = self.margin + i * spacing_x + random.uniform(-20, 20)
            init_y = self.margin + (s.get('coordenates', {}).get('y', self.height//2)) + random.uniform(-30, 30)
            node = {'id': s.get('id'), 'label': s.get('label'), 'x': init_x, 'y': init_y}
            nodes.append(node)
            id_to_node[s.get('id')] = node

        # edges
        edges = []
        for s in stars:
            for link in s.get('linkedTo', []):
                src = s.get('id')
                dst = link.get('starId')
                if src is not None and dst is not None:
                    edges.append((src, dst))

        # force-directed iterations (repulsion + attraction)
        K = math.sqrt((self.width * self.height) / max(1, len(nodes)))
        iterations = 80
        for _ in range(iterations):
            # repulsive forces
            disp = {node['id']: [0.0, 0.0] for node in nodes}
            for i, v in enumerate(nodes):
                for j, u in enumerate(nodes):
                    if v['id'] == u['id']:
                        continue
                    dx = v['x'] - u['x']
                    dy = v['y'] - u['y']
                    dist = math.hypot(dx, dy) + 0.01
                    force = (K*K) / dist
                    disp[v['id']][0] += (dx / dist) * force
                    disp[v['id']][1] += (dy / dist) * force
            # attractive forces (edges)
            for (a, b) in edges:
                na = id_to_node.get(a)
                nb = id_to_node.get(b)
                if not na or not nb:
                    continue
                dx = na['x'] - nb['x']
                dy = na['y'] - nb['y']
                dist = math.hypot(dx, dy) + 0.01
                force = (dist*dist) / K
                disp[na['id']][0] -= (dx / dist) * force
                disp[na['id']][1] -= (dy / dist) * force
                disp[nb['id']][0] += (dx / dist) * force
                disp[nb['id']][1] += (dy / dist) * force
            # apply displacements with limit
            for node in nodes:
                dx, dy = disp[node['id']]
                max_disp = 10.0
                dlen = math.hypot(dx, dy)
                if dlen > 0:
                    node['x'] += (dx / dlen) * min(max_disp, dlen)
                    node['y'] += (dy / dlen) * min(max_disp, dlen)
                # keep in bounds
                node['x'] = min(max(self.margin, node['x']), self.width - self.margin)
                node['y'] = min(max(self.margin, node['y']), self.height - self.margin)
        return nodes, edges

    def _draw_layout(self, constellation):
        data = self.layouts.get(constellation)
        if not data:
            return
        nodes = data['nodes']
        edges = data['edges']
        color = self.constellation_colors.get(constellation, '#ffffff')
        shared = data.get('shared', set())

        # map id -> node
        id_map = {n['id']: n for n in nodes}
        # dibujar aristas
        for a, b in edges:
            na = id_map.get(a); nb = id_map.get(b)
            if na and nb:
                self.star_drawer.draw_connection(na['x'], na['y'], nb['x'], nb['y'], color)
        # dibujar nodos
        for n in nodes:
            c = 'red' if n['label'] in shared else color
            self.star_drawer.draw_star(n['x'], n['y'], c, n['label'])

    def redraw(self):
        """Redibuja usando layouts guardados (útil cuando se pan/zoom)."""
        self.star_drawer.clear_canvas()
        for constellation in self.layouts:
            self._draw_layout(constellation)