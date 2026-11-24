import multiprocessing as mp
import os
import time

from distribucion_manual import dividir_imagenes


def trabajador(id_proceso, inicio, fin):

    print(
        f"Proceso {id_proceso} | "
        f"PID: {os.getpid()} | "
        f"Imagenes: {inicio} a {fin - 1} | "
        f"Total: {fin - inicio}",
        flush=True
    )

    # Simular trabajo durante dos segundos
    time.sleep(2)

    print(
        f"Proceso {id_proceso} finalizado",
        flush=True
    )


def ejecutar_procesos(total_imagenes, num_procesos):

    segmentos = dividir_imagenes(
        total_imagenes,
        num_procesos
    )

    procesos = []

    inicio_tiempo = time.perf_counter()

    # Crear individualmente los procesos
    for i, (inicio, fin) in enumerate(segmentos):

        proceso = mp.Process(
            target=trabajador,
            args=(i + 1, inicio, fin)
        )

        procesos.append(proceso)

    # Iniciar todos los procesos
    for proceso in procesos:
        proceso.start()

    # Esperar a que todos terminen
    for proceso in procesos:
        proceso.join()

    # Comprobar que finalizaron correctamente
    for proceso in procesos:
        if proceso.exitcode != 0:
            raise RuntimeError(
                f"Error en proceso {proceso.pid}"
            )

    tiempo = time.perf_counter() - inicio_tiempo

    print(f"\nTiempo total: {tiempo:.4f} segundos")


if __name__ == "__main__":

    for num_procesos in [2, 4, 8]:

        print(f"\nPrueba con {num_procesos} procesos")
        print("-" * 50)

        ejecutar_procesos(5300, num_procesos)