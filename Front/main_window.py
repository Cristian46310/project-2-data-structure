import tkinter as tk
from tkinter import ttk
import sys
import os

# ...existing code...
# asegurarse que el path relativo permita importar el backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Back.Repository.ReadConstellations import ReadConstellations
from Front.Visualization.graph_manager import GraphManager

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("NASA Data Structure Visualizer")
        self.root.geometry("900x700")
        self.graph_manager = None

        # transform para pan/zoom (coordenadas del mundo)
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.scale = 1.0
        self._drag_start = None

        # CONFIGURACIÓN DE LA REJILLA PRINCIPAL
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

        # PANEL LATERAL IZQUIERDO (Control)
        self.control_panel = ttk.Frame(self.root, width=200, relief=tk.SUNKEN, padding=10)
        self.control_panel.grid(row=0, column=0, sticky="ns")
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
        ttk.Label(self.control_panel, text="Control Panel", font=("Arial", 12, "bold")).pack(pady=5)
        ttk.Button(self.control_panel, text="Cargar Constelaciones", command=self.load_constellations).pack(pady=10)
        ttk.Button(self.control_panel, text="Iniciar Simulación", command=self.start_visualization).pack(pady=10)

    def create_map_canvas(self):
        ttk.Label(self.map_visualization, text="Mapa de Constelaciones", font=("Arial", 12, "bold")).pack(pady=5)

        # contenedor para canvas + scrollbars
        canvas_frame = ttk.Frame(self.map_visualization)
        canvas_frame.pack(expand=True, fill="both")

        # canvas
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

        # graph manager para dibujo y layout
        self.graph_manager = GraphManager(self.canvas)

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

    def load_constellations(self):
        print("Cargando archivo JSON de constelaciones...")
        reader = ReadConstellations()
        constellations = self.graph_manager.draw_constellations(reader)

        # aplicar transform actual al drawer y redibujar
        self.graph_manager.star_drawer.set_transform(self.offset_x, self.offset_y, self.scale)
        self.graph_manager.redraw()

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

    def start_visualization(self):
        self.status_label.config(text="Simulación en curso...")
        print("Visualización iniciada.")

    # ---- handlers de pan/zoom y resize ----
    def _on_mouse_down(self, event):
        self._drag_start = (event.x, event.y)

    def _on_mouse_drag(self, event):
        if not self._drag_start:
            return
        # desplazar en coordenadas del mundo (tener en cuenta escala)
        dx = (event.x - self._drag_start[0]) / self.scale
        dy = (event.y - self._drag_start[1]) / self.scale
        self._drag_start = (event.x, event.y)
        self.offset_x += dx
        self.offset_y += dy
        # actualizar transform y redraw
        self.graph_manager.star_drawer.set_transform(self.offset_x, self.offset_y, self.scale)
        self.graph_manager.redraw()

    def _on_mouse_wheel(self, event):
        # Zoom centrado en cursor
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

        # ajustar offset para que el punto bajo el cursor permanezca fijo
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
        # actualizar tamaño en graph_manager para mejores layouts si es necesario
        try:
            self.graph_manager.width = max(100, event.width)
            self.graph_manager.height = max(100, event.height)
            # actualizar scrollregion para coincidir con tamaño virtual
            self.canvas.configure(scrollregion=(0, 0, self.graph_manager.width, self.graph_manager.height))
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()