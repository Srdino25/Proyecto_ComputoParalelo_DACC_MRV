import numpy as np


def reconstruir_matriz(resultados, total_imagenes):

    matriz = np.zeros((total_imagenes, 34))
    registrados = np.zeros(total_imagenes, dtype=bool)

    for indice, vector in resultados:

        if not 0 <= indice < total_imagenes:
            raise ValueError("Indice fuera de rango")

        if registrados[indice]:
            raise ValueError(
                f"Imagen duplicada: {indice}"
            )

        vector = np.asarray(vector)

        if vector.shape != (34,):
            raise ValueError("Vector incorrecto")

        if not np.isfinite(vector).all():
            raise ValueError("Vector con valores invalidos")

        matriz[indice] = vector
        registrados[indice] = True

    if not registrados.all():

        faltantes = np.where(~registrados)[0]

        raise ValueError(
            f"Imagenes faltantes: {faltantes}"
        )

    return matriz

if __name__ == "__main__":

    total_imagenes = 8

    # Simulacion de resultados recibidos fuera de orden
    orden_llegada = [4, 5, 0, 1, 6, 7, 2, 3]

    resultados = [
        (indice, np.full(34, indice))
        for indice in orden_llegada
    ]

    print("Orden de llegada:")
    print(orden_llegada)

    matriz = reconstruir_matriz(
        resultados,
        total_imagenes
    )

    print("\nOrden reconstruido:")
    print(matriz[:, 0].astype(int).tolist())

    print("\nDimensiones:", matriz.shape)

    esperado = np.repeat(
        np.arange(total_imagenes)[:, None],
        34,
        axis=1
    )

    assert np.array_equal(matriz, esperado)

    print("Orden correcto: True")
    print("Prueba completada correctamente")