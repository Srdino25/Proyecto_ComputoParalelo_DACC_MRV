# Reconocimiento paralelo de tipos de punto de crochet

Proyecto de análisis de texturas mediante LBP y GLCM,
clasificación con SVM y Random Forest, y comparación
de extracción secuencial y paralela de características.

## Dataset

El archivo de imágenes se aloja en Google Drive debido a su tamaño:

[Descargar dataset](https://drive.google.com/file/d/1VFIiJyw321f7i6QoNwe5LHzM47KshPkd/view?usp=drive_link)

Las imágenes están organizadas por tipo de punto:

- Punto bajo.
- Medio punto alto.
- Punto alto.

Se incluyen tejidos de diferentes colores, pero la organización
y las etiquetas corresponden al tipo de punto, no al color.

## Preparación de las imágenes

Montserrat Reyes participó en la preparación del dataset:
elaboró tejidos, tomó fotografías de muestras con diferentes
colores y colaboró en la organización de las imágenes
en carpetas por tipo de punto.

## Ubicación de los datos

1. Descargar y descomprimir el ZIP de Google Drive.
2. Localizar la carpeta dataset_crochet dentro del contenido extraído.
3. Colocarla en la misma carpeta que proyecto_crochet.ipynb.
4. Conservar los nombres de las subcarpetas y las imágenes:
   el notebook utiliza las rutas registradas en procedencia.csv.

El archivo procedencia.csv contiene información de las imágenes;
no sustituye a los archivos de imagen.
