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

## 4. Distribución manual de imágenes

Se desarrolló el archivo `distribucion_manual.py`, que permite dividir las imágenes mediante el cociente y el residuo de una división entera.

| Procesos propuestos | Distribución | Total asignado |
|---|---|---:|
| 2 | 2650 imágenes por proceso | 5300 |
| 4 | 1325 imágenes por proceso | 5300 |
| 8 | Cuatro procesos con 663 imágenes y cuatro con 662 | 5300 |

Las pruebas confirmaron que no existen imágenes omitidas ni índices duplicados.

## 5. Función trabajadora

Se desarrolló el archivo `trabajador_paralelo.py`.

La función `procesar_segmento` recibe las rutas de las imágenes y los límites del segmento asignado. Utiliza la función de extracción existente para obtener las 18 características LBP y las 16 características GLCM.

Cada resultado conserva el índice original de la imagen y su vector de 34 características.

Se realizó una prueba con cinco imágenes reales, obteniendo vectores completos y valores válidos.

## 6. Reconstrucción de resultados

Se desarrolló el archivo `reconstruccion_resultados.py`.

La función coloca cada vector en la fila correspondiente a su índice original, independientemente del orden de llegada.

Se realizó una prueba con ocho vectores simulados recibidos fuera de orden. La reconstrucción recuperó correctamente el orden original y produjo una matriz de dimensiones (8, 34).

## 7. Validación de equivalencia

Se desarrolló el archivo `validacion_equivalencia.py` para comparar la extracción secuencial con la extracción organizada por segmentos.

Se utilizaron 30 imágenes reales, seleccionando 10 de cada categoría.

| Configuración | Dimensiones | Equivalencia | Diferencia máxima |
|---|---|---|---:|
| 2 segmentos | (30, 34) | True | 0.0 |
| 4 segmentos | (30, 34) | True | 0.0 |
| 8 segmentos | (30, 34) | True | 0.0 |

Todas las pruebas fueron satisfactorias.

## 8. Propuesta de integración

Una vez autorizado el uso de multiprocessing, se propone:

1. Dividir manualmente las rutas mediante dividir_imagenes.
2. Crear individualmente los procesos mediante multiprocessing.Process.
3. Ejecutar procesar_segmento en cada proceso.
4. Recuperar los resultados mediante multiprocessing.Queue.
5. Reconstruir la matriz mediante reconstruir_matriz.
6. Comparar los resultados con la ejecución secuencial.
7. Medir los tiempos, speedup y eficiencia con 2, 4 y 8 procesos.

## 9. Conclusiones

Se diseñaron y validaron los componentes necesarios para la distribución manual, extracción de características y recuperación ordenada de resultados.

Las pruebas demostraron equivalencia numérica entre la extracción secuencial y la segmentada para las 30 imágenes seleccionadas.

El diseño está preparado para su integración. Queda pendiente la autorización del profesor, la creación de procesos independientes y las pruebas de rendimiento paralelo.

No se modificó la celda original de joblib durante esta etapa.