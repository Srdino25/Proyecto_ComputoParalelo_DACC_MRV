def dividir_imagenes(total_imagenes, num_procesos):

    if num_procesos <= 0 or total_imagenes < 0:
        raise ValueError("Cantidad de imágenes o procesos inválida")

    base = total_imagenes // num_procesos
    residuo = total_imagenes % num_procesos

    segmentos = []
    inicio = 0

    for proceso in range(num_procesos):

        cantidad = base

        if proceso < residuo:
            cantidad += 1

        fin = inicio + cantidad

        segmentos.append((inicio, fin))

        inicio = fin

    return segmentos


if __name__ == "__main__":

    total_imagenes = 5300

    for num_procesos in [2, 4, 8]:

        print(f"\nDistribución con {num_procesos} procesos")
        print("-" * 45)

        segmentos = dividir_imagenes(
            total_imagenes,
            num_procesos
        )

        for i, (inicio, fin) in enumerate(segmentos):

            print(
                f"Proceso {i + 1}: "
                f"imágenes {inicio} a {fin - 1} "
                f"| Total: {fin - inicio}"
            )

        total_asignado = sum(
            fin - inicio for inicio, fin in segmentos
        )

        indices = [
            indice
            for inicio, fin in segmentos
            for indice in range(inicio, fin)
        ]

        assert indices == list(range(total_imagenes))

        print(f"Total asignado: {total_asignado}")
        print("Distribución correcta: True")