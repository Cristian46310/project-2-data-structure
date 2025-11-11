import sys
import os
import inspect
import traceback
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Back.utils.DonkeySimulation import DonkeySimulation
from Back.Repository.ReadConstellations import ReadConstellations

class DonkeyVisualizer:
    """Clase que encapsula la simulación del burro y su visualización en el canvas."""
    def __init__(self, canvas, graph_manager):
        self.canvas = canvas
        self.graph_manager = graph_manager
        self.simulation = DonkeySimulation()
        self.reader = ReadConstellations()
        self.current_route = []
        self.current_step = 0
        self.animation_running = False
        self.auto_advance = False  # nuevo: para avanzar automáticamente entre pasos

    def _ensure_simulation_config(self, donkey_config):
        """Asegura que self.simulation.configData esté cargado; intenta métodos internos o config.json."""
        try:
            cfg = getattr(self.simulation, 'configData', None)
            if callable(cfg):
                try:
                    self.simulation.configData()
                except Exception:
                    pass
            if not getattr(self.simulation, 'configData', None):
                if callable(getattr(self.simulation, 'configDonkey', None)):
                    try:
                        sig = inspect.signature(self.simulation.configDonkey)
                        if len(sig.parameters) > 0:
                            try:
                                self.simulation.configDonkey(donkey_config)
                            except Exception:
                                self.simulation.configDonkey()
                        else:
                            self.simulation.configDonkey()
                    except Exception:
                        try:
                            self.simulation.configDonkey()
                        except Exception:
                            pass
            if not getattr(self.simulation, 'configData', None):
                candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Back', 'Data', 'config.json'))
                if os.path.exists(candidate):
                    try:
                        with open(candidate, 'r', encoding='utf-8') as fh:
                            cfg_data = json.load(fh)
                        self.simulation.configData = cfg_data
                    except Exception:
                        pass
        except Exception:
            traceback.print_exc()

    def start_route_simulation(self, start_star, constellation, donkey_config):
        """
        Inicia la simulación adaptando la configuración y llamando a DonkeySimulation.simulateRoute.
        """
        try:
            self._ensure_simulation_config(donkey_config)

            end_star = donkey_config.get('endStar') or donkey_config.get('end')
            next_star = donkey_config.get('nextStarInNewGalaxy') or donkey_config.get('next') or donkey_config.get('nextStar')
            mission = donkey_config.get('mission') or 'exploration'

            if end_star is None:
                print("Error: simulateRoute requiere 'endStar'. Pasa un endStar válido desde la UI.")
                return None

            try:
                result = None
                if hasattr(self.simulation, 'simulateRoute'):
                    result = self.simulation.simulateRoute(start_star, end_star, constellation, next_star, mission)
                else:
                    candidates = [n for n in dir(self.simulation) if 'simulate' in n.lower()]
                    if candidates:
                        func = getattr(self.simulation, candidates[0])
                        sig = inspect.signature(func)
                        params = list(sig.parameters.keys())
                        positional = []
                        for p in params:
                            if p == 'self':
                                continue
                            if p in ('startStar','start_star','start','origin'):
                                positional.append(start_star)
                            elif p in ('endStar','end','dest','destination'):
                                positional.append(end_star)
                            elif p in ('constellation','constellationName','constellation_name','galaxy'):
                                positional.append(constellation)
                            elif p in ('nextStarInNewGalaxy','next','next_star','nextStar'):
                                positional.append(next_star)
                            elif p in ('mission','task'):
                                positional.append(mission)
                            else:
                                positional.append(None)
                        result = func(*positional)
                
                if result and isinstance(result, dict) and 'route' in result:
                    self.current_route = list(result['route'])
                    self.current_step = 0
                    self.auto_advance = True  # activar auto-avance
                    print(f"Ruta detectada con {len(self.current_route)} pasos.")
                    # guardar config para nuevas misiones
                    self.last_donkey_config = donkey_config
                    self.last_constellation = constellation
                else:
                    print("No se pudo identificar 'route' en el resultado. Resultado bruto:")
                    print(result)
                return result
            except Exception as e:
                print("Error llamando a simulateRoute:", e)
                traceback.print_exc()
                return None
        except Exception as e:
            print("Error en start_route_simulation:", e)
            traceback.print_exc()
            return None

    def animate_route(self, step_callback=None):
        """Inicia la animación automática de la ruta."""
        if not self.current_route:
            print("No hay ruta para animar")
            return
        self.animation_running = True
        self.auto_advance = True
        self._animate_step(step_callback)

    def _animate_step(self, step_callback):
        """Anima un paso y continúa automáticamente si auto_advance está activo."""
        if self.current_step >= len(self.current_route) or not self.animation_running:
            self.animation_running = False
            return
        
        current_star = self.current_route[self.current_step]
        self._highlight_star(current_star)
        
        if step_callback:
            step_info = {
                'step': self.current_step + 1,
                'total_steps': len(self.current_route),
                'current_star': current_star,
                'status': 'En progreso'
            }
            step_callback(step_info)
        
        self.current_step += 1
        
        # si auto_advance está activo, continuar automáticamente después de 1 segundo
        if self.auto_advance and self.animation_running:
            self.canvas.after(1000, lambda: self._animate_step(step_callback))

    def continue_animation(self, step_callback=None):
        """Continúa con el siguiente paso (manual)."""
        if not self.animation_running or self.current_step >= len(self.current_route):
            return
        self._animate_step(step_callback)

    def check_route_complete(self, step_callback=None):
        """Verifica si se llegó al destino y genera nueva ruta si es necesario."""
        if self.current_step >= len(self.current_route) and self.animation_running:
            # llegó al destino, activar nueva misión si existe siguiente estrella
            return True
        return False

    def _highlight_star(self, star_name):
        try:
            self.graph_manager.redraw()
            for constellation, layout_data in self.graph_manager.layouts.items():
                for node in layout_data.get('nodes', []):
                    if node.get('label') == star_name:
                        x, y = node.get('x'), node.get('y')
                        sd = self.graph_manager.star_drawer
                        sx = int((x + sd.offset_x) * sd.scale)
                        sy = int((y + sd.offset_y) * sd.scale)
                        marker = self.canvas.create_oval(sx-12, sy-12, sx+12, sy+12, outline='yellow', width=2)
                        # mantener marcador visible más tiempo
                        self.canvas.after(1500, lambda m=marker: self.canvas.delete(m))
                        return
        except Exception as e:
            print(f"Error al resaltar estrella: {e}")
            traceback.print_exc()

    def stop_animation(self):
        self.animation_running = False
        self.auto_advance = False

    def get_simulation_report(self):
        return {
            'total_steps': len(self.current_route),
            'route': self.current_route,
            'current_step': self.current_step
        }