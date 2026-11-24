import numpy as np
from pathlib import Path
import funciones_crochet as fc

from distribucion_manual import dividir_imagenes
from trabajador_paralelo import procesar_segmento
from reconstruccion_resultados import reconstruir_matriz


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

    # Seleccionar 10 imágenes de cada categoría
    for categoria in categorias:

        imagenes = sorted([
            str(archivo)
            for archivo in (dataset / categoria).rglob("*")
            if archivo.is_file()
            and archivo.suffix.lower() in extensiones
        ])

        assert len(imagenes) >= 10

        rutas.extend(imagenes[:10])

    total = len(rutas)

    print("Imagenes seleccionadas:", total)

    # Extraccion secuencial de referencia
    matriz_secuencial = np.array([
        fc.extraer_caracteristicas(ruta)
        for ruta in rutas
    ])

    print("Matriz secuencial:", matriz_secuencial.shape)

    assert matriz_secuencial.shape == (total, 34)
    assert np.isfinite(matriz_secuencial).all()

    # Validar el diseño con 2, 4 y 8 segmentos
    for num_procesos in [2, 4, 8]:

        print(f"\nConfiguracion: {num_procesos} segmentos")
        print("-" * 45)

        segmentos = dividir_imagenes(
            total,
            num_procesos
        )

        resultados = []

        # Simular la llegada de segmentos fuera de orden
        for inicio, fin in reversed(segmentos):

            resultados.extend(
                procesar_segmento(rutas, inicio, fin)
            )

        matriz_segmentada = reconstruir_matriz(
            resultados,
            total
        )

        mismas_dimensiones = (
            matriz_secuencial.shape
            == matriz_segmentada.shape
        )

        valores_validos = np.isfinite(
            matriz_segmentada
        ).all()

        equivalentes = np.allclose(
            matriz_secuencial,
            matriz_segmentada,
            rtol=1e-7,
            atol=1e-9
        )

        diferencia = np.max(np.abs(
            matriz_secuencial - matriz_segmentada
        ))

        print("Dimensiones:", matriz_segmentada.shape)
        print("Mismas dimensiones:", mismas_dimensiones)
        print("Valores validos:", valores_validos)
        print("Resultados equivalentes:", equivalentes)
        print("Diferencia maxima:", diferencia)

        assert mismas_dimensiones
        assert valores_validos
        assert equivalentes

    print("\nTodas las pruebas fueron satisfactorias")