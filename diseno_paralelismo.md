# Diseño de procesamiento paralelo manual

**Responsable:** Montserrat Reyes  
**Proyecto:** Reconocimiento paralelo de tipos de punto de crochet  
**Rama:** monse-desarrollo

## 1. Objetivo

Sustituir el procesamiento paralelo basado en joblib por una implementación que permita controlar manualmente la creación de procesos, la distribución de imágenes y la recuperación de resultados.

## 2. Herramientas propuestas

Se propone utilizar las siguientes herramientas de la biblioteca multiprocessing de Python:

- Process: creación individual de procesos.
- Queue: comunicación entre procesos y recuperación de resultados.
- start(): inicio de cada proceso.
- join(): espera de la finalización de cada proceso.

La distribución de las imágenes se realizará manualmente, sin utilizar joblib, n_jobs ni Pool.map.

## 3. Estado inicial

El dataset contiene 5300 imágenes distribuidas en tres categorías:

| Categoría | Imágenes |
|---|---:|
| Medio punto alto | 3120 |
| Punto alto | 1160 |
| Punto bajo | 1020 |
| Total | 5300 |

Cada imagen genera un vector de 34 características, compuesto por 18 características LBP y 16 características GLCM.

La propuesta se encuentra en fase de diseño, pendiente de confirmar que el profesor permita el uso de multiprocessing. Por el momento, no se modificará la implementación original del notebook.