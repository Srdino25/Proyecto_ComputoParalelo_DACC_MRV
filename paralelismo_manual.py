import multiprocessing as mp
import os
import time
import numpy as np

from queue import Empty
from pathlib import Path

from distribucion_manual import dividir_imagenes
from trabajador_paralelo import procesar_segmento
from reconstruccion_resultados import reconstruir_matriz


def trabajador(id_proceso, rutas, inicio, fin, cola):

    try:

        print(
            f"Proceso {id_proceso} | "
            f"PID: {os.getpid()} | "
            f"Imagenes asignadas: {fin - inicio}",
            flush=True
        )

        resultados = procesar_segmento(
            rutas, inicio, fin
        )

        cola.put((id_proceso, resultados, None))

    except Exception as error:

        cola.put((id_proceso, [], str(error)))


def ejecutar_paralelo(rutas, num_procesos):

    if not rutas:
        raise ValueError("No hay imagenes para procesar")

    inicio_tiempo = time.perf_counter()

    segmentos = dividir_imagenes(
        len(rutas),
        num_procesos
    )

    contexto = mp.get_context("spawn")
    cola = contexto.Queue()

    procesos = []
    resultados = []

    try:

        # Crear los procesos manualmente
        for i, (inicio, fin) in enumerate(segmentos):

            proceso = contexto.Process(
                target=trabajador,
                args=(
                    i + 1,
                    rutas,
                    inicio,
                    fin,
                    cola
                )
            )

            procesos.append(proceso)

        # Iniciar todos los procesos
        for proceso in procesos:
            proceso.start()

        # Recuperar los resultados
        for _ in procesos:

            try:

                id_proceso, datos, error = cola.get(
                    timeout=300
                )

            except Empty:

                raise RuntimeError(
                    "No se recibieron todos los resultados"
                )

            if error is not None:

                raise RuntimeError(
                    f"Error en proceso {id_proceso}: {error}"
                )

            resultados.extend(datos)

            print(
                f"Resultados recibidos del proceso "
                f"{id_proceso}: {len(datos)} imagenes"
            )

        # Esperar la finalizacion
        for proceso in procesos:

            proceso.join(timeout=30)

            if proceso.exitcode != 0:

                raise RuntimeError(
                    f"Error o bloqueo en PID {proceso.pid}"
                )

        # Reconstruir en el orden original
        matriz = reconstruir_matriz(
            resultados,
            len(rutas)
        )

        tiempo = time.perf_counter() - inicio_tiempo

        return matriz, tiempo

    finally:

        for proceso in procesos:

            if proceso.is_alive():
                proceso.terminate()

            if proceso.pid is not None:
                proceso.join()

        cola.close()
        cola.join_thread()


if __name__ == "__main__":

    dataset = (
        Path.cwd()
        / "crochet_dataset"
        / "dataset_crochet"
    )

    extensiones = {
        ".jpg", ".jpeg", ".png",
        ".bmp", ".tif", ".tiff", ".webp"
    }

    categorias = [
        "medio_punto_alto",
        "punto_alto",
        "punto_bajo"
    ]

    rutas = []

    # Seleccionar 10 imagenes de cada categoria
    for categoria in categorias:

        imagenes = sorted([
            str(archivo)
            for archivo in (dataset / categoria).rglob("*")
            if archivo.is_file()
            and archivo.suffix.lower() in extensiones
        ])

        assert len(imagenes) >= 10

        rutas.extend(imagenes[:10])

    print("Total de imagenes:", len(rutas))

    # Primera prueba con dos procesos
    matriz, tiempo = ejecutar_paralelo(rutas, 2)

    print("\nRESULTADOS FINALES")
    print("-" * 45)
    print("Dimensiones:", matriz.shape)
    print("Valores validos:", np.isfinite(matriz).all())
    print(f"Tiempo de ejecucion: {tiempo:.4f} segundos")

    assert matriz.shape == (30, 34)
    assert np.isfinite(matriz).all()

    print("Extraccion paralela completada correctamente")