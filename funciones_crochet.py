import numpy as np
from PIL import Image
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops


def preprocesar_imagen(ruta):
    with Image.open(ruta) as imagen:
        return np.array(imagen.convert("L"), dtype=np.uint8)


def extraer_lbp(imagen):
    puntos = 16
    lbp = local_binary_pattern(imagen, puntos, 2, method="uniform")
    hist, _ = np.histogram(
        lbp.ravel(),
        bins=np.arange(puntos + 3),
        density=True
    )
    return hist


def extraer_glcm(imagen):
    glcm = graycomatrix(
        imagen,
        distances=[1],
        angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4],
        levels=256,
        symmetric=True,
        normed=True
    )
    return np.concatenate([
        graycoprops(glcm, propiedad).ravel()
        for propiedad in [
            "contrast", "homogeneity", "energy", "correlation"
        ]
    ])


def extraer_caracteristicas(ruta):
    imagen = preprocesar_imagen(ruta)
    return np.concatenate([
        extraer_lbp(imagen),
        extraer_glcm(imagen)
    ])
