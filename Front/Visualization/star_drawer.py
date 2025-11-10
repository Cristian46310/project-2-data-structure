import tkinter as tk
import random
import math
class StarDrawer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.scale_factor = 2
        self.star_positions = {}
        self.star_colors = {}
        self.offset_x = 0
        self.offset_y = 0
        self.scale = 1.0
        self.items = []
        
    def set_transform(self, offset_x, offset_y, scale):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale = scale

    def to_screen(self, x, y):
        sx = (x + self.offset_x) * self.scale
        sy = (y + self.offset_y) * self.scale
        return sx, sy

    def draw_star(self, x, y, color, name):
        """Dibuja una estrella individual en coordenadas del mundo (no transformadas)."""
        sx, sy = self.to_screen(x, y)
        size = max(3, int(6 * self.scale))
        oval = self.canvas.create_oval(
            sx - size, sy - size, sx + size, sy + size,
            fill=color, outline='white'
        )
        text = self.canvas.create_text(
            sx, sy - size - 6, text=name, fill='white', font=('Arial', max(8, int(8 * self.scale)))
        )
        self.items.append(oval)
        self.items.append(text)
        return oval, text

    def draw_connection(self, x1, y1, x2, y2, color):
        sx1, sy1 = self.to_screen(x1, y1)
        sx2, sy2 = self.to_screen(x2, y2)
        line = self.canvas.create_line(sx1, sy1, sx2, sy2, fill=color, width=max(1, int(self.scale)))
        self.items.append(line)
        return line

    def clear_canvas(self):
        for it in self.items:
            try:
                self.canvas.delete(it)
            except Exception:
                pass
        self.items = []