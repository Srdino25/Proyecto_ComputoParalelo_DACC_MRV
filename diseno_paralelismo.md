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

## 10. Autorización e integración del procesamiento paralelo

Se confirmó con el profesor que está permitido utilizar multiprocessing.

Se implementó el procesamiento paralelo mediante la creación y gestión individual de procesos, sin utilizar joblib, n_jobs ni Pool.

La implementación se encuentra en el archivo `paralelismo_manual.py`.

El procedimiento consiste en:

1. Dividir manualmente la lista de imágenes.
2. Crear procesos independientes mediante multiprocessing.Process.
3. Iniciar todos los procesos mediante start().
4. Ejecutar la extracción LBP y GLCM en cada segmento.
5. Enviar los resultados mediante multiprocessing.Queue.
6. Recuperar los resultados antes de esperar la finalización de los procesos.
7. Reconstruir la matriz utilizando los índices originales.

## 11. Validación de la creación de procesos

Se realizó una prueba inicial utilizando trabajo simulado para comprobar la creación y ejecución concurrente de procesos.

| Procesos | Tiempo (s) |
|---:|---:|
| 2 | 2.1236 |
| 4 | 2.0140 |
| 8 | 2.0219 |

Los procesos finalizaron correctamente y presentaron identificadores PID independientes.

Estos tiempos corresponden únicamente a una prueba de funcionamiento y no representan el rendimiento real de la extracción de características.

## 12. Validación del procesamiento paralelo real

Se desarrolló el archivo `validacion_paralela_real.py` para comparar el procesamiento secuencial con la implementación mediante multiprocessing.

Se seleccionaron 30 imágenes reales, 10 de cada categoría, obteniendo los siguientes resultados:

| Procesos | Tiempo (s) | Speedup | Eficiencia (%) |
|---:|---:|---:|---:|
| Secuencial | 1.7250 | 1.0000 | 100.00 |
| 2 | 1.5398 | 1.1203 | 56.01 |
| 4 | 1.2320 | 1.4001 | 35.00 |
| 8 | 1.3521 | 1.2758 | 15.95 |

## 13. Equivalencia numérica

| Procesos | Dimensiones | Valores válidos | Equivalencia | Diferencia máxima |
|---:|---|---|---|---:|
| 2 | (30, 34) | True | True | 0.0 |
| 4 | (30, 34) | True | True | 0.0 |
| 8 | (30, 34) | True | True | 0.0 |

Todas las configuraciones produjeron resultados idénticos al procesamiento secuencial para las imágenes evaluadas.

La reconstrucción mediante índices permitió conservar el orden original, independientemente del orden de llegada de los resultados.

## 14. Análisis preliminar

La configuración de cuatro procesos obtuvo el menor tiempo de ejecución, con un speedup de 1.4001 y una reducción aproximada del 28.58 % respecto al método secuencial.

El incremento a ocho procesos no produjo una mejora adicional. Este comportamiento puede relacionarse con el costo de creación de procesos, comunicación y gestión de resultados.

Las mediciones son preliminares debido al tamaño reducido de la muestra y a que se realizó una ejecución por configuración. Queda pendiente evaluar el rendimiento utilizando las 5300 imágenes del dataset y múltiples repeticiones.

## 15. Integración con el proyecto principal

La función ejecutar_paralelo del archivo paralelismo_manual.py recibe la lista de rutas y la cantidad de procesos, y devuelve la matriz de características y el tiempo de ejecución.

Su integración permitirá sustituir el procesamiento basado en joblib sin modificar las funciones originales de extracción LBP y GLCM.

El notebook principal permanece sin modificaciones durante esta etapa.

## 16. Estado final de la implementación

- Distribución manual: completada.
- Creación de procesos independientes: completada.
- Comunicación entre procesos: completada.
- Extracción paralela real: completada.
- Reconstrucción ordenada: completada.
- Validación numérica preliminar: completada.
- Mediciones definitivas con el dataset completo: pendientes.
- Integración en el notebook principal: pendiente.