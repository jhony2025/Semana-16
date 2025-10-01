## Creado por 
Nombre: Johnny Vera 

estudianrte de la universidad Estatal Amazónica (UEA)

Asignatura: Sistemas Operativos 

Semestre. Segundo semestre 

## Proyecto: Simulación de Fragmentación Externa en la Asignación de Memoria
# Descripción

Este proyecto implementa en Python una simulación de la fragmentación externa, un problema clásico en la gestión de memoria de los sistemas operativos.

El código utiliza un modelo de memoria dividido en bloques fijos que los procesos solicitan de manera dinámica y contigua.
A medida que los procesos piden y liberan memoria, los bloques libres quedan dispersos, provocando que aun existiendo memoria libre suficiente en total, algunas solicitudes de mayor tamaño no puedan ser satisfechas.

 ## Funcionamiento del código

La memoria se representa como una lista de bloques ("." = libre, "#" = ocupado).

Los procesos piden un número aleatorio de bloques (entre 2 y 6).

La asignación se realiza con el algoritmo first-fit (primer hueco contiguo disponible).

Los procesos liberan memoria tras un tiempo de ejecución simulado.

## El sistema detecta:

Fallo por falta total de memoria → cuando no hay suficientes bloques libres.

Fallo por fragmentación externa → cuando sí hay memoria libre total, pero no contigua.

Se muestran:

El estado de la memoria después de cada operación.

Los huecos libres (posición y tamaño).

Un resumen final con estadísticas de fragmentación.

## ¿Qué es la fragmentación externa?

La fragmentación externa ocurre cuando la memoria libre se encuentra dividida en pequeños huecos dispersos.
Aunque la suma total de huecos libres sea suficiente, no pueden atenderse peticiones grandes que requieren espacio contiguo.

## Ejemplo simplificado:

Memoria:  [###..##..###..##....]
Libre:    8 bloques en total
Hueco máx: 2 bloques
Petición: 6 bloques → Falla por fragmentación externa

## Ventajas y Desventajas
# Ventajas

Modelo más sencillo de implementar (segmentación contigua).

Acceso directo y rápido a los bloques (menos traducciones de direcciones).

Útil en sistemas embebidos o con memoria pequeña y estática.

## Desventajas

Fragmentación externa → desperdicio de memoria aunque esté libre.

Necesidad de realizar compactación periódica (costosa en tiempo).

Dificultad para escalar en sistemas grandes o multitarea intensiva.

## Estrategias para Mitigar la Fragmentación

Basado en la clase 16 de memoria y segmentación:

# Compactación

Mover procesos en memoria para reagrupar huecos libres en un bloque grande.

Problema: consume mucho tiempo de CPU y afecta al rendimiento.

## Buddy System

## Divide la memoria en bloques de tamaños potencias de 2.

Reduce la fragmentación externa, aunque introduce algo de fragmentación interna.

Paginación (Linux, Windows, Android)

La memoria se divide en páginas de tamaño fijo.

Evita la fragmentación externa porque no se requieren bloques contiguos.

Introduce fragmentación interna (última página no siempre se llena).

Permite usar algoritmos de reemplazo y listas de páginas activas/inactivas.

## Relación con Sistemas Operativos Reales

# Linux

Usa paginación multinivel y segmentación lógica.

Minimiza fragmentación externa con páginas grandes y esquemas de reemplazo (NRU, segunda oportunidad).

Windows

Gestiona memoria con páginas y regiones críticas por procesador.

Evita fragmentación externa mediante la virtualización de direcciones.

Android

Basado en Linux, mantiene aplicaciones cargadas para optimizar consumo de energía.

Controla la memoria mediante eventos y listas de páginas activas/inactivas.

## Ejecución del código

Clonar el repositorio o copiar el archivo.

Ejecutar con Python 3:

python simulacion_fragmentacion.py


Observar cómo los procesos piden, liberan y cómo surgen los fallos por fragmentación externa.

## Ejemplo de salida
A3 pide 6 bloques de memoria...
## A3 no pudo asignar 6 bloques. ⚠️ Fallo por fragmentación externa.

## Estado actual de la memoria:
###..##..###..##....
Huecos libres: [(3,4,2),(7,8,2),(13,14,2),(18,19,2)]

## Resumen final:
Fallos por fragmentación externa: 7
Fallos por falta total de memoria: 3
