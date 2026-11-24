import numpy as np
import time
from pathlib import Path

import funciones_crochet as fc
from paralelismo_manual import ejecutar_paralelo


def obtener_rutas():

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

    for categoria in categorias:

        imagenes = sorted([
            str(archivo)
            for archivo in (dataset / categoria).rglob("*")
            if archivo.is_file()
            and archivo.suffix.lower() in extensiones
        ])

        assert len(imagenes) >= 10

        rutas.extend(imagenes)

    return rutas


if __name__ == "__main__":

    rutas = obtener_rutas()

    print("Imagenes seleccionadas:", len(rutas))

    # Extraccion secuencial de referencia
    inicio = time.perf_counter()

    matriz_secuencial = np.array([
        fc.extraer_caracteristicas(ruta)
        for ruta in rutas
    ])

    tiempo_secuencial = time.perf_counter() - inicio

    assert matriz_secuencial.shape == (len(rutas), 34)
    assert np.isfinite(matriz_secuencial).all()

    print("\nPROCESAMIENTO SECUENCIAL")
    print("-" * 50)
    print("Dimensiones:", matriz_secuencial.shape)
    print(f"Tiempo: {tiempo_secuencial:.4f} segundos")

    resumen = []

    # Extraccion paralela real
    for num_procesos in [2, 4, 8]:

        print(f"\nPRUEBA CON {num_procesos} PROCESOS")
        print("-" * 50)

        matriz_paralela, tiempo_paralelo = ejecutar_paralelo(
            rutas,
            num_procesos
        )

        mismas_dimensiones = (
            matriz_secuencial.shape
            == matriz_paralela.shape
        )

        assert mismas_dimensiones

        valores_validos = np.isfinite(
            matriz_paralela
        ).all()

        equivalentes = np.allclose(
            matriz_secuencial,
            matriz_paralela,
            rtol=1e-7,
            atol=1e-9
        )

        diferencia = np.max(np.abs(
            matriz_secuencial - matriz_paralela
        ))

        speedup = tiempo_secuencial / tiempo_paralelo
        eficiencia = speedup / num_procesos * 100

        print("\nRESULTADOS")
        print("Dimensiones:", matriz_paralela.shape)
        print("Mismas dimensiones:", mismas_dimensiones)
        print("Valores validos:", valores_validos)
        print("Resultados equivalentes:", equivalentes)
        print("Diferencia maxima:", diferencia)

        print(f"Tiempo: {tiempo_paralelo:.4f} segundos")
        print(f"Speedup: {speedup:.4f}")
        print(f"Eficiencia: {eficiencia:.2f}%")

        assert valores_validos
        assert equivalentes

        resumen.append((
            num_procesos,
            tiempo_paralelo,
            speedup,
            eficiencia
        ))

    print("\nRESUMEN GENERAL")
    print("-" * 65)

    print(
        f"{'Procesos':<12}"
        f"{'Tiempo (s)':<15}"
        f"{'Speedup':<15}"
        f"{'Eficiencia (%)':<15}"
    )

    for procesos, tiempo, speedup, eficiencia in resumen:

        print(
            f"{procesos:<12}"
            f"{tiempo:<15.4f}"
            f"{speedup:<15.4f}"
            f"{eficiencia:<15.2f}"
        )

    print("\nTodas las pruebas fueron satisfactorias")