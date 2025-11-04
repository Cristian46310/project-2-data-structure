from Back.utils.DonkeySimulation import DonkeySimulation

if __name__ == "__main__":
    sim = DonkeySimulation()
    # Prueba de calculateDistance entre dos estrellas
    start_star = "Alpha1"
    end_star = "Alpha53"
    # imprime el resultado de calculateDistance para evitar obtener None en la salida
    sim.calculateDistance(start_star, end_star)