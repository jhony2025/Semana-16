import random
import time

# Simulación de memoria con bloques fijos (simula la memoria física)
class Memoria:
    def __init__(self, tamanio):
        self.tamanio = tamanio
        self.memoria = [None] * tamanio  # Lista que representa los bloques de memoria
        self.fallos_fragmentacion = 0
        self.fallos_totales = 0

    # Método para intentar asignar memoria
    def asignar(self, proceso, tamanio_requerido):
        for i in range(self.tamanio - tamanio_requerido + 1):
            # Buscar un bloque contiguo libre
            if all(self.memoria[i + j] is None for j in range(tamanio_requerido)):
                # Asignar el bloque de memoria
                for j in range(tamanio_requerido):
                    self.memoria[i + j] = proceso
                print(f"✅ {proceso} asignó {tamanio_requerido} bloques de memoria.")
                return True

        # Si llega aquí → no encontró hueco contiguo
        libres_totales = self.memoria.count(None)
        if libres_totales >= tamanio_requerido:
            print(f"❌ {proceso} no pudo asignar {tamanio_requerido} bloques. "
                  f"⚠️ Fallo por fragmentación externa.")
            self.fallos_fragmentacion += 1
        else:
            print(f"❌ {proceso} no pudo asignar {tamanio_requerido} bloques. "
                  f"❌ No hay suficiente memoria total.")
            self.fallos_totales += 1
        return False

    # Método para liberar memoria
    def liberar(self, proceso):
        liberado = False
        for i in range(self.tamanio):
            if self.memoria[i] == proceso:
                self.memoria[i] = None
                liberado = True
        if liberado:
            print(f"🔓 {proceso} ha liberado su memoria.")

    # Método para mostrar el estado de la memoria
    def mostrar_memoria(self):
        print("\n📊 Estado actual de la memoria:")
        print("".join(["." if x is None else "#" for x in self.memoria]))
        self.mostrar_huecos()

    # Mostrar huecos libres (para visualizar fragmentación)
    def mostrar_huecos(self):
        huecos = []
        i = 0
        while i < self.tamanio:
            if self.memoria[i] is None:
                inicio = i
                while i < self.tamanio and self.memoria[i] is None:
                    i += 1
                fin = i - 1
                huecos.append((inicio, fin, fin - inicio + 1))
            else:
                i += 1
        print("Huecos libres:", huecos if huecos else "Ninguno")


# Simulación de un proceso que pide memoria y luego la libera
def proceso(nombre, memoria):
    tamanio_requerido = random.randint(2, 6)  # Cantidad aleatoria de bloques
    print(f"\n{name} pide {tamanio_requerido} bloques de memoria...")
    if memoria.asignar(nombre, tamanio_requerido):
        time.sleep(0.2)  # El proceso realiza una tarea
        memoria.liberar(nombre)  # Liberamos la memoria
    time.sleep(0.2)


# Función para simular la gestión de memoria
def gestionar_memoria():
    memoria = Memoria(20)  # Memoria de 20 bloques
    procesos = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for i in range(12):  # Lanzamos varias solicitudes
        proceso_nombre = random.choice(procesos) + str(i)
        proceso(proceso_nombre, memoria)
        memoria.mostrar_memoria()

    print("\n📌 Resumen final:")
    print(f"Fallos por fragmentación externa: {memoria.fallos_fragmentacion}")
    print(f"Fallos por falta total de memoria: {memoria.fallos_totales}")


# Ejecución de la simulación
if __name__ == "__main__":
    gestionar_memoria()
