import sys, os, inspect, traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Back.utils.DonkeySimulation import DonkeySimulation
from Back.Repository.ReadConstellations import ReadConstellations

def print_header(msg):
    print("\n" + "="*10 + " " + msg + " " + "="*10 + "\n")

try:
    sim = DonkeySimulation()
    print_header("Clase y métodos")
    print("Clase:", sim.__class__.__name__)
    print("Métodos públicos (parciales):", [m for m in dir(sim) if not m.startswith('_')][:60])

    # mostrar firma de simulateRoute si existe
    for name in ('simulateRoute','simulate_route','runSimulation','startSimulation','simulate'):
        if hasattr(sim, name):
            func = getattr(sim, name)
            print_header(f"Firma: {name}")
            try:
                print("Signature:", inspect.signature(func))
            except Exception as e:
                print("No se pudo obtener signature:", e)
            try:
                src = inspect.getsource(func)
                print("\n".join(src.splitlines()[:200]))  # primeras 200 líneas
            except Exception as e:
                print("No se pudo leer source:", e)
            break
    else:
        print("No se encontró simulateRoute ni variantes.")

    # cargar constelaciones y listar estrellas
    rc = ReadConstellations()
    data = rc.readJsonConstellations()
    print_header("Constelaciones / Estrellas")
    if not data:
        print("No se pudo leer JSON (readJsonConstellations devolvió None). Ruta usada:", rc.RUTA_DE_CONSTELACIONES)
    else:
        for c in data.get('constellations', []):
            labels = [s.get('label') for s in c.get('starts', []) if s.get('label')]
            print(f"{c.get('name')}: {labels}")

    # seleccionar ejemplos (ajusta si quieres)
    first_const = data.get('constellations', [])[0] if data else None
    start = None
    end = None
    next_star = None
    if first_const:
        stars = [s.get('label') for s in first_const.get('starts', []) if s.get('label')]
        if len(stars) >= 2:
            start, end = stars[0], stars[1]
        elif stars:
            start = stars[0]
    # imprimir intento de llamada
    constellation_name = first_const.get('name') if first_const else "Constelacion del Burro"
    print_header("Intento de llamada directa a simulateRoute / flujo dijkstra")
    print("start:", start, "end:", end, "constellation:", constellation_name)

    try:
        # intentar llamada con varios patrones posicionales
        if hasattr(sim, 'simulateRoute'):
            try:
                print("Llamando sim.simulateRoute(start, end, constellation, None, 'exploration') (posicional)")
                r = sim.simulateRoute(start, end, constellation_name, None, 'exploration')
                print("Resultado simulateRoute:", repr(r))
            except Exception:
                traceback.print_exc()

        # llamar flujo directamente si existe
        if hasattr(sim, 'dijkstra') and sim.dijkstra:
            try:
                print("\nLlamando sim.dijkstra.flujoOptimo(start, end)")
                res = sim.dijkstra.flujoOptimo(start, end)
                print("Resultado flujoOptimo:", repr(res))
            except Exception:
                traceback.print_exc()
    except Exception:
        traceback.print_exc()

except Exception:
    traceback.print_exc()