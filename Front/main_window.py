import tkinter as tk
from tkinter import ttk
import sys
import os
import json

# asegurarse que el path relativo permita importar el backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Back.Repository.ReadConstellations import ReadConstellations
from Front.Visualization.graph_manager import GraphManager
from Front.Visualization.donkey_visualizer import DonkeyVisualizer

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("NASA Data Structure Visualizer")
        self.root.geometry("1000x750")
        self.graph_manager = None
        self.donkey_visualizer = None
        
        # transform para pan/zoom (coordenadas del mundo)
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.scale = 1.0
        self._drag_start = None
        
        # configuración de misión actual
        self.current_mission_config = None
        self.simulation_running = False

        # nueva cola de misiones y referencias UI
        self.mission_queue = []
        self.mission_listbox = None
        self.stats_labels = {}
        self._stats_updater_id = None

        # CONFIGURACIÓN DE LA REJILLA PRINCIPAL
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

        # PANEL LATERAL IZQUIERDO (Control) - MÁS ANCHO
        self.control_panel = ttk.Frame(self.root, width=250, relief=tk.SUNKEN, padding=10)
        self.control_panel.grid(row=0, column=0, sticky="nsew")
        self.control_panel.grid_propagate(False)
        self.create_control_panel()

        # PANEL CENTRAL (Mapa)
        self.map_visualization = ttk.Frame(self.root, relief=tk.SUNKEN)
        self.map_visualization.grid(row=0, column=1, sticky="nsew")
        self.create_map_canvas()

        # PANEL INFERIOR (Monitoreo)
        self.monitoring_panel = ttk.Frame(self.root, height=100, relief=tk.SUNKEN, padding=10)
        self.monitoring_panel.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.create_monitoring_panel()

    def create_control_panel(self):
        # Crear un scrollable frame para el panel de control
        canvas = tk.Canvas(self.control_panel, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.control_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Contenido del panel de control
        ttk.Label(scrollable_frame, text="Control Panel", font=("Arial", 12, "bold")).pack(pady=5)
        ttk.Button(scrollable_frame, text="Cargar Constelaciones", command=self.load_constellations).pack(pady=6, fill="x", padx=5)

        # Frame para configuración del burro
        donkey_frame = ttk.LabelFrame(scrollable_frame, text="Configurar Burro", padding=8)
        donkey_frame.pack(pady=8, fill="x", padx=5)

        ttk.Label(donkey_frame, text="Estado de Salud:").pack(anchor="w")
        self.health_var = tk.StringVar(value="excelente")
        ttk.Combobox(donkey_frame, textvariable=self.health_var,
                     values=["excelente", "buena", "mala", "moribundo"]).pack(fill="x", pady=2)

        ttk.Label(donkey_frame, text="Edad:").pack(anchor="w")
        self.age_var = tk.IntVar(value=5)
        ttk.Spinbox(donkey_frame, from_=1, to=50, textvariable=self.age_var).pack(fill="x", pady=2)

        ttk.Label(donkey_frame, text="Energía (%):").pack(anchor="w")
        self.energy_var = tk.IntVar(value=100)
        ttk.Spinbox(donkey_frame, from_=1, to=100, textvariable=self.energy_var).pack(fill="x", pady=2)

        ttk.Label(donkey_frame, text="Pasto (kg):").pack(anchor="w")
        self.grass_var = tk.IntVar(value=50)
        ttk.Spinbox(donkey_frame, from_=0, to=500, textvariable=self.grass_var).pack(fill="x", pady=2)

        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=6)

        # Entradas de ruta necesarias por DonkeySimulation
        route_frame = ttk.LabelFrame(scrollable_frame, text="Ruta / Misión", padding=8)
        route_frame.pack(pady=6, fill="x", padx=5)

        ttk.Label(route_frame, text="Estrella Inicial:").pack(anchor="w")
        self.start_star_var = tk.StringVar(value="")
        self.start_star_cb = ttk.Combobox(route_frame, textvariable=self.start_star_var, values=[])
        self.start_star_cb.pack(fill="x", pady=2)

        ttk.Label(route_frame, text="Estrella Destino (endStar):").pack(anchor="w")
        self.end_star_var = tk.StringVar(value="")
        self.end_star_cb = ttk.Combobox(route_frame, textvariable=self.end_star_var, values=[])
        self.end_star_cb.pack(fill="x", pady=2)

        ttk.Label(route_frame, text="Siguiente Estrella (nextStar):").pack(anchor="w")
        self.next_star_var = tk.StringVar(value="")
        self.next_star_cb = ttk.Combobox(route_frame, textvariable=self.next_star_var, values=[])
        self.next_star_cb.pack(fill="x", pady=2)

        ttk.Label(route_frame, text="Misión:").pack(anchor="w")
        self.mission_var = tk.StringVar(value="exploration")
        ttk.Combobox(route_frame, textvariable=self.mission_var,
                     values=["exploration", "rescue", "delivery", "survey"]).pack(fill="x", pady=2)

        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=6)

        # FRAME DE BOTONES - BIEN VISIBLE
        button_frame = ttk.LabelFrame(scrollable_frame, text="Controles", padding=8)
        button_frame.pack(pady=10, fill="x", padx=5)

        self.start_button = ttk.Button(button_frame, text="▶ Iniciar Simulación",
                   command=self.start_visualization)
        self.start_button.pack(pady=6, fill="x")

        self.continue_button = ttk.Button(button_frame, text="⏭ Continuar Siguiente Misión",
                   command=self.continue_next_mission_handler, state="disabled")
        self.continue_button.pack(pady=6, fill="x")

        self.stop_button = ttk.Button(button_frame, text="⏹ Terminar Simulación",
                   command=self.stop_visualization, state="disabled")
        self.stop_button.pack(pady=6, fill="x")
        
        # BOTÓN: Guardar configuración en tiempo real
        ttk.Button(button_frame, text="💾 Guardar Ahora", command=self.update_burro_config).pack(pady=6, fill="x")

        # CONTROLES DE COLA DE MISIONES
        queue_frame = ttk.LabelFrame(scrollable_frame, text="Cola de Misiones (n recorridos)", padding=8)
        queue_frame.pack(pady=8, fill="x", padx=5)

        self.mission_listbox = tk.Listbox(queue_frame, height=6)
        self.mission_listbox.pack(fill="both", pady=4, padx=2)

        q_buttons = ttk.Frame(queue_frame)
        q_buttons.pack(fill="x", pady=2)
        ttk.Button(q_buttons, text="➕ Agregar a Cola", command=self.add_mission_to_queue).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(q_buttons, text="▶ Iniciar Secuencia", command=self.start_mission_sequence).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(q_buttons, text="🧹 Limpiar Cola", command=lambda: (self.mission_queue.clear(), self.update_mission_listbox())).pack(side="left", expand=True, fill="x", padx=2)

    def create_map_canvas(self):
        ttk.Label(self.map_visualization, text="Mapa de Constelaciones", font=("Arial", 12, "bold")).pack(pady=5)

        # contenedor para canvas + scrollbars
        canvas_frame = ttk.Frame(self.map_visualization)
        canvas_frame.pack(expand=True, fill="both")

        # canvas (crear antes de instanciar GraphManager/DonkeyVisualizer)
        self.canvas = tk.Canvas(canvas_frame, bg="black", width=600, height=500)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # scrollbars
        vbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        hbar = ttk.Scrollbar(canvas_frame, orient='horizontal', command=self.canvas.xview)
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        # permitir que canvas_frame expanda el canvas
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        # graph manager y visualizador ahora que self.canvas existe
        self.graph_manager = GraphManager(self.canvas)
        self.donkey_visualizer = DonkeyVisualizer(self.canvas, self.graph_manager)

        # Bindings para pan (arrastrar) y zoom (rueda)
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)   # Windows / Mac
        self.canvas.bind("<Button-4>", self._on_mouse_wheel)     # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mouse_wheel)     # Linux scroll down

        # Cuando cambie el tamaño del canvas, recomputar tamaño en graph_manager
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def create_monitoring_panel(self):
        ttk.Label(self.monitoring_panel, text="Panel de Monitoreo", font=("Arial", 12, "bold")).pack(pady=5)
        self.status_label = ttk.Label(self.monitoring_panel, text="Estado: Listo", font=("Arial", 10))
        self.status_label.pack()

        # Panel de estadísticas en tiempo real
        stats_frame = ttk.Frame(self.monitoring_panel)
        stats_frame.pack(pady=6, fill="x")
        labels = {
            'health': 'Salud',
            'age': 'Edad',
            'energy': 'Energía',
            'grass': 'Pasto',
            'current_star': 'Estrella Actual',
            'missions_left': 'Misiones en Cola'
        }
        for key, txt in labels.items():
            lbl = ttk.Label(stats_frame, text=f"{txt}: --")
            lbl.pack(anchor="w")
            self.stats_labels[key] = lbl

    def load_constellations(self):
        print("Cargando archivo JSON de constelaciones...")
        reader = ReadConstellations()
        constellations = self.graph_manager.draw_constellations(reader)

        # obtener lista de labels desde el reader (si devuelve raw data)
        try:
            data = reader.readJsonConstellations()
            labels = []
            if data and isinstance(data, dict):
                for c in data.get('constellations', []):
                    for s in c.get('starts', []):
                        lbl = s.get('label')
                        if lbl:
                            labels.append(lbl)
            # popular los menús con los labels extraídos
            self.populate_star_menus(labels)
        except Exception as e:
            print("Error extrayendo estrellas del JSON:", e)

        # aplicar transform actual al drawer y redibujar
        try:
            self.graph_manager.star_drawer.set_transform(self.offset_x, self.offset_y, self.scale)
            self.graph_manager.redraw()
        except Exception:
            pass

        # actualizar scrollregion para permitir scroll con scrollbars
        try:
            w = max(200, int(self.graph_manager.width))
            h = max(200, int(self.graph_manager.height))
            self.canvas.configure(scrollregion=(0, 0, w, h))
        except Exception:
            pass

        if constellations:
            self.status_label.config(text=f"Constelaciones cargadas: {', '.join(constellations)}")
        else:
            self.status_label.config(text="No se pudieron cargar las constelaciones.")

    def populate_star_menus(self, star_labels):
        """Rellena los Combobox de inicio/fin/next con la lista de etiquetas de estrellas."""
        try:
            if not star_labels:
                star_labels = []
            # eliminar duplicados y ordenar para mejor UX
            unique = sorted(dict.fromkeys(star_labels))
            self.start_star_cb['values'] = unique
            self.end_star_cb['values'] = unique
            self.next_star_cb['values'] = unique
            # preset a la primera estrella si están vacíos
            if unique:
                if not self.start_star_var.get():
                    self.start_star_var.set(unique[0])
                if not self.end_star_var.get():
                    self.end_star_var.set(unique[-1])
        except Exception as e:
            print("Error al popular menús de estrellas:", e)

    def update_burro_config(self):
        """Actualiza el archivo config.json con los parámetros del burro."""
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Back', 'Data', 'config.json'))
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

            # Actualizar valores del burro
            config['burroEnergiaIcial'] = self.energy_var.get()
            config['estadoSalud'] = self.health_var.get()
            config['pasto'] = self.grass_var.get()
            config['startAge'] = self.age_var.get()

            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(config, file, indent=4)

            print("✓ Config.json actualizado correctamente.")
            # refrescar estadísticas visibles tras guardar
            self.refresh_stats_from_config()
        except Exception as e:
            print("✗ Error al actualizar Config.json:", e)

    # NUEVO: Agregar misión a la cola desde los campos actuales
    def add_mission_to_queue(self):
        start_star = self.start_star_var.get().strip()
        end_star = self.end_star_var.get().strip() or None
        mission = self.mission_var.get().strip() or "exploration"

        if not start_star or not end_star:
            self.status_label.config(text="Error: la misión requiere estrella inicio y fin")
            return

        entry = {'start': start_star, 'end': end_star, 'mission': mission}
        self.mission_queue.append(entry)
        self.update_mission_listbox()
        self.status_label.config(text=f"Misión agregada: {start_star} → {end_star}")

    # NUEVO: Actualizar Listbox de cola
    def update_mission_listbox(self):
        if self.mission_listbox is None:
            return
        self.mission_listbox.delete(0, tk.END)
        for i, m in enumerate(self.mission_queue, start=1):
            self.mission_listbox.insert(tk.END, f"{i}. {m['start']} → {m['end']} ({m['mission']})")
        # actualizar contador de misiones restantes en stats
        if 'missions_left' in self.stats_labels:
            self.stats_labels['missions_left'].config(text=f"Misiones en Cola: {len(self.mission_queue)}")

    # NUEVO: Iniciar secuencia completa (usa la cola). La primera ejecución respeta la configuración inicial guardada.
    def start_mission_sequence(self):
        if not self.mission_queue:
            self.status_label.config(text="Cola vacía. Agrega misiones primero.")
            return

        # Si no hay simulación en curso, arrancar la primera
        if not self.simulation_running and self.mission_queue:
            next_m = self.mission_queue.pop(0)
            self.update_mission_listbox()
            self._begin_mission(next_m['start'], next_m['end'], None, next_m['mission'], use_config_write=True)
        else:
            self.status_label.config(text="Simulación ya en curso.")

    # REFACTORIZACIÓN: Inicio de misión común (usado por start_visualization y secuencias)
    def _begin_mission(self, start_star, end_star, next_star, mission, use_config_write=False):
        try:
            if use_config_write:
                self.update_burro_config()

            donkey_config = {
                'health': self.health_var.get(),
                'age': self.age_var.get(),
                'energy': self.energy_var.get(),
                'grass': self.grass_var.get(),
                'endStar': end_star,
                'end': end_star,
                'nextStarInNewGalaxy': next_star,
                'next': next_star,
                'mission': mission
            }

            self.status_label.config(text="Iniciando simulación...")
            print(f"\n🚀 INICIANDO SIMULACIÓN: {start_star} → {end_star}")

            constellation_name = "Constelacion del Burro"
            result = self.donkey_visualizer.start_route_simulation(start_star, constellation_name, donkey_config)

            if result is None:
                self.status_label.config(text="Error: No se generó ruta válida")
                return

            if getattr(self.donkey_visualizer, 'current_route', None):
                # ESTADO DE SIMULACIÓN ACTIVA
                self.simulation_running = True
                self.start_button.config(state="disabled")
                self.continue_button.config(state="normal")
                self.stop_button.config(state="normal")
                
                # Guardar config para siguientes misiones (solo meta)
                self.current_mission_config = {
                    'start_star': start_star,
                    'end_star': end_star,
                    'next_star': next_star,
                    'mission': mission,
                    'constellation': constellation_name,
                    'health': self.health_var.get(),
                    'age': self.age_var.get(),
                    'energy': self.energy_var.get(),
                    'grass': self.grass_var.get()
                }
                
                # lanzar actualización periódica de stats
                self._start_periodic_stats()

                # Animar automáticamente hasta destino (se pausa al llegar)
                self.donkey_visualizer.animate_route(step_callback=self._on_simulation_step)
                self.status_label.config(text="Simulación en curso... Presiona 'Continuar' para siguiente misión o 'Terminar' para detener")
            else:
                self.status_label.config(text="No se detectó ruta válida")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            print("Error en _begin_mission:", e)

    # MODIFICAR start_visualization para usar _begin_mission y escribir config inicial
    def start_visualization(self):
        """Inicia una NUEVA simulación desde el principio."""
        try:
            start_star = self.start_star_var.get().strip()
            end_star = self.end_star_var.get().strip() or None
            next_star = self.next_star_var.get().strip() or None
            mission = self.mission_var.get().strip() or "exploration"

            if not start_star:
                self.status_label.config(text="Error: selecciona una estrella inicial")
                return

            # Para el inicio completo, escribir los valores iniciales del burro
            self._begin_mission(start_star, end_star, next_star, mission, use_config_write=True)
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            print("Error en start_visualization:", e)

    # MODIFICAR continue_next_mission_handler para priorizar la cola
    def continue_next_mission_handler(self):
        """Continúa a la siguiente misión asignada o toma de la cola si existe."""
        if not self.current_mission_config and not self.mission_queue:
            self.status_label.config(text="No hay misión anterior ni cola para continuar")
            return

        # Si hay cola, tomar siguiente misión de la cola
        if self.mission_queue:
            next_m = self.mission_queue.pop(0)
            self.update_mission_listbox()
            print(f"\n📍 INICIANDO SIGUIENTE EN COLA: {next_m['start']} → {next_m['end']}")
            self._begin_mission(next_m['start'], next_m['end'], None, next_m['mission'], use_config_write=False)
            return

        # Si no hay cola, seguir el flujo anterior (next_star dentro de current_mission_config)
        config = self.current_mission_config
        if not config:
            self.status_label.config(text="No hay misión anterior para continuar")
            return
        
        new_start = config['end_star']
        new_end = config['next_star']
        
        if not new_end:
            self.status_label.config(text="No hay siguiente estrella asignada. Simulación completada.")
            self.stop_visualization()
            return
        
        # Nueva configuración para siguiente misión
        new_config = {
            'health': config.get('health', 'excelente'),
            'age': config.get('age', 5),
            'energy': config.get('energy', 100),
            'grass': config.get('grass', 50),
            'endStar': new_end,
            'end': new_end,
            'nextStarInNewGalaxy': None,
            'next': None,
            'mission': config.get('mission', 'exploration')
        }
        
        print(f"\n📍 SIGUIENTE MISIÓN: {new_start} → {new_end}")
        result = self.donkey_visualizer.start_route_simulation(new_start, config['constellation'], new_config)
        
        if result and getattr(self.donkey_visualizer, 'current_route', None):
            # Actualizar config para próxima misión
            self.current_mission_config.update({
                'start_star': new_start,
                'end_star': new_end,
                'next_star': None
            })
            # Animar hasta destino
            self.donkey_visualizer.animate_route(step_callback=self._on_simulation_step)
            self.status_label.config(text=f"Misión en curso: {new_start} → {new_end}")
        else:
            self.status_label.config(text="Error al generar ruta para siguiente misión")
            self.stop_visualization()

    def stop_visualization(self):
        """Termina completamente la simulación."""
        self.donkey_visualizer.stop_animation()
        self.simulation_running = False
        
        # Actualizar config.json UNA ÚLTIMA VEZ
        self.update_burro_config()
        
        # Resetear botones
        self.start_button.config(state="normal")
        self.continue_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        
        # detener actualización de stats periódica
        self._stop_periodic_stats()

        self.status_label.config(text="Simulación terminada. Presiona 'Iniciar Simulación' para comenzar nueva simulación")
        print("\n❌ SIMULACIÓN TERMINADA\n")
        
    def _on_simulation_step(self, step_info):
        """Callback en cada paso de la simulación."""
        step = step_info.get('step', 0)
        total = step_info.get('total_steps', 0)
        current_star = step_info.get('current_star', '?')
        status = step_info.get('status', 'En progreso')
        
        # Actualizar interfaz
        self.status_label.config(
            text=f"Paso {step}/{total} - Estrella: {current_star} - Estado: {status}"
        )
        
        # actualizar estadísticas en pantalla (lee config.json para reflejar estado real)
        self.refresh_stats_from_config()

        # Si llegó al destino (último paso)
        if step == total and status != 'Muerto':
            self._on_route_complete(current_star)
        
        # Si el burro muere
        if status == 'Muerto':
            self.donkey_visualizer.stop_animation()
            self.update_burro_config()
            self.start_button.config(state="normal")
            self.continue_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            self.simulation_running = False
            self._stop_periodic_stats()
            self.status_label.config(text=f"💀 El burro ha muerto en {current_star}")

    # MODIFICAR _on_route_complete para arrancar automáticamente siguiente misión en cola si existe
    def _on_route_complete(self, arrived_star):
        """Se ejecuta cuando llega al destino."""
        if not self.simulation_running:
            return
        
        # PAUSAR la simulación - detener animación actual
        self.donkey_visualizer.stop_animation()
        
        # Si existe una misión en la cola, iniciar automáticamente la siguiente
        if self.mission_queue:
            next_m = self.mission_queue.pop(0)
            self.update_mission_listbox()
            self.status_label.config(text=f"✅ Llegó a {arrived_star}. Iniciando siguiente misión en cola: {next_m['start']} → {next_m['end']}")
            print(f"\n✅ LLEGÓ A {arrived_star} - INICIANDO SIGUIENTE EN COLA")
            # arrancar sin sobrescribir estado del burro (use_config_write=False)
            self._begin_mission(next_m['start'], next_m['end'], None, next_m['mission'], use_config_write=False)
            return

        # Si no hay cola, esperar acción del usuario
        self.status_label.config(
            text=f"✅ Llegó a {arrived_star}. Presiona 'Continuar' para seguir o 'Terminar' para detener"
        )
        print(f"\n✅ LLEGÓ A {arrived_star}")
            
    # NUEVO: refrescar estadísticas leyendo config.json
    def refresh_stats_from_config(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Back', 'Data', 'config.json'))
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                conf = json.load(f)
         # map keys defensivamente
            energy = conf.get('burroEnergiaActual', conf.get('burroEnergiaIcial', self.energy_var.get()))
            grass = conf.get('pasto', self.grass_var.get())
            age = conf.get('startAge', self.age_var.get())
            health = conf.get('estadoSalud', self.health_var.get())
            current_star = conf.get('currentStar', '?')
            
            if 'energy' in self.stats_labels:
                self.stats_labels['energy'].config(text=f"Energía: {energy}")
            if 'grass' in self.stats_labels:
                self.stats_labels['grass'].config(text=f"Pasto: {grass}")
            if 'age' in self.stats_labels:
                self.stats_labels['age'].config(text=f"Edad: {age}")
            if 'health' in self.stats_labels:
                self.stats_labels['health'].config(text=f"Salud: {health}")
            if 'current_star' in self.stats_labels:
                self.stats_labels['current_star'].config(text=f"Estrella Actual: {current_star}")
            if 'missions_left' in self.stats_labels:
                self.stats_labels['missions_left'].config(text=f"Misiones en Cola: {len(self.mission_queue)}")
        except Exception:
            # silencioso si no existe/config malformado
            pass

    # NUEVOS: control de actualización periódica de stats mientras la simulación corre
    def _start_periodic_stats(self):
        self._stop_periodic_stats()
        def _upd():
            self.refresh_stats_from_config()
            self._stats_updater_id = self.root.after(1000, _upd)
        _upd()

    def _stop_periodic_stats(self):
        if self._stats_updater_id:
            try:
                self.root.after_cancel(self._stats_updater_id)
            except Exception:
                pass
            self._stats_updater_id = None


    def _on_mouse_down(self, event):
        self._drag_start = (event.x, event.y)

    def _on_mouse_drag(self, event):
        if not self._drag_start:
            return
        dx = (event.x - self._drag_start[0]) / self.scale
        dy = (event.y - self._drag_start[1]) / self.scale
        self._drag_start = (event.x, event.y)
        self.offset_x += dx
        self.offset_y += dy
        self.graph_manager.star_drawer.set_transform(self.offset_x, self.offset_y, self.scale)
        self.graph_manager.redraw()

    def _on_mouse_wheel(self, event):
        try:
            if hasattr(event, 'delta'):
                factor = 1.0 + (event.delta / 1200.0)
            else:
                factor = 1.1 if event.num == 4 else 0.9
        except Exception:
            factor = 1.0

        old_scale = self.scale
        self.scale *= factor
        self.scale = max(0.2, min(4.0, self.scale))

        mx, my = event.x, event.y
        wx_before = mx / old_scale - self.offset_x
        wy_before = my / old_scale - self.offset_y
        wx_after = mx / self.scale - self.offset_x
        wy_after = my / self.scale - self.offset_y
        self.offset_x += (wx_before - wx_after)
        self.offset_y += (wy_before - wy_after)

        self.graph_manager.star_drawer.set_transform(self.offset_x, self.offset_y, self.scale)
        self.graph_manager.redraw()

    def _on_canvas_configure(self, event):
        try:
            self.graph_manager.width = max(100, event.width)
            self.graph_manager.height = max(100, event.height)
            self.canvas.configure(scrollregion=(0, 0, self.graph_manager.width, self.graph_manager.height))
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()