import numpy as np
import funciones_crochet as fc


def procesar_segmento(rutas, inicio, fin):

    resultados = []

    for indice in range(inicio, fin):

        ruta = rutas[indice]

        vector = np.asarray(
            fc.extraer_caracteristicas(ruta)
        )

        if vector.shape != (34,):
            raise ValueError(
                f"Vector incorrecto en imagen {indice}"
            )

        if not np.isfinite(vector).all():
            raise ValueError(
                f"Valores invalidos en imagen {indice}"
            )

        resultados.append((indice, vector))

    return resultados

if __name__ == "__main__":

    from pathlib import Path

    dataset = (
        Path.cwd()
        / "crochet_dataset"
        / "dataset_crochet"
    )

    extensiones = {
        ".jpg", ".jpeg", ".png",
        ".bmp", ".tif", ".tiff", ".webp"
    }

    rutas = sorted([
        str(archivo)
        for archivo in dataset.rglob("*")
        if archivo.is_file()
        and archivo.suffix.lower() in extensiones
    ])

    assert len(rutas) >= 5, "Dataset no encontrado o insuficiente"

    print("Total de imágenes encontradas:", len(rutas))

    resultados = procesar_segmento(rutas, 0, 5)

    for indice, vector in resultados:

        print(
            f"Imagen {indice} | "
            f"Características: {len(vector)} | "
            f"Valores válidos: {np.isfinite(vector).all()}"
        )

    assert len(resultados) == 5
    assert [i for i, _ in resultados] == list(range(5))

    print("\nPrueba del trabajador completada correctamente")