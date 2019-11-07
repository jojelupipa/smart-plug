---
title:						# Título
author: Jesús Sánchez de Lechina Tejada		# Nombre del autor
header-includes:      	 	        	# Incluir paquetes en LaTeX
	- \usepackage[spanish]{babel}
toc: true                   			# Índice
numbersections: false       			# Numeración de secciones
fontsize: 11pt              			# Tamaño de fuente
geometry: margin=1in        			# Tamaño de los márgenes
linkcolor: red
---


# Descripción

Probamos nuestro sensor intrusivo (acs712) en una bombilla de 11W. 

# Lecturas

Cuando está apagada, obviamente marca 0 W

Todas las lecturas variaban sistemáticamente entre estos

Irms: 0.093A ,
Potencia: 21.418W
Intensidad: 0.069A ,

Irms: 0.076A ,
Potencia: 17.488W
Intensidad: 0.085A ,

Tras comprobar  que no coincidía con los 11W que teóricamente consumía la bombilla revisé la constante asociada al valor eficaz (1.1 --> 0.707) y entonces producía unos valores más acordes a lo esperado, con pequeñas fluctuaciones


Intensidad: 0.069A ,
Irms: 0.049A ,
Potencia: 11.240W
Intensidad: 0.098A ,
Irms: 0.069A ,
Potencia: 15.895W
Intensidad: 0.069A ,
Irms: 0.049A ,
Potencia: 11.240W
Intensidad: 0.085A ,
Irms: 0.060A ,
Potencia: 13.766W


Pero, tras dejar un tiempo el sensor tomando medidas, aprecié que los valores de estas se habían disparado:

Intensidad: 0.272A ,
Irms: 0.192A ,
Potencia: 44.251W
Intensidad: 0.263A ,
Irms: 0.186A ,
Potencia: 42.800W
Intensidad: 0.285A ,
Irms: 0.201A ,
Potencia: 46.343W
Intensidad: 0.321A ,
Irms: 0.227A ,
Potencia: 52.117W
Intensidad: 0.349A ,
Irms: 0.247A ,
Potencia: 56.758W



Sin haber modificado nada en la instalación los valores tendían a
alterarse por largos períodos de tiempo aunque eventualmente se
estabilizasen por otros períodos de tiempo.

Esto disparó las alarmas respecto a este sensor porque nos
enfrentábamos a un problema no únicamente de eliminación de ruido sino
a un verdadero problema de distinción entre consumo real y
fluctuaciones.

Lo que es peor, tras apagar la bombilla seguía obteniendo lecturas de
20W o más.


# Pasando a ESP32

## Dudas

**Puerto de conexión S - Relé:**

Antes en Arduino utilizábamos el pin 9 para salida digital.

```
// S --> pin 19 (p.ej. vale cualquier pin de entrada/salida)
```

¿Ahora vale cualquier pin de entrada salida? ¿O tiene que ser algún
puerto serial?

**Voltaje de este puerto:** 

Las salidas digitales de arduino operan a 5V, pero las de ESP32
(probado empíricamente en un programa con un LED) muestra una
diferencia de potencial de ~3.35V (335 medido con una escala de 0-20
en corriente continua). 

¿La señal que controla el relé simplemente trabajará con un voltaje
alto-bajo? ¿O afectará que no sean 5V como con arduino? (aunque tras
una medición del voltaje en arduino la diferencia de potencial entre
la tierra y el pin de salida era ~3.84)

## Detalles

* El puerto a utilizar para “escribir al relé”.

* El voltaje de dicho puerto.

* El voltaje que emite el sensor de corriente hacia la lectura
  analógica. Divisor de tensión.


# Fuentes para el diagrama

* Relé: https://github.com/rwaldron/fritzing-components
  (agradecimientos al subreddit r/Arduino)

* ESP32 Devkit: En este hilo https://forum.fritzing.org/t/doit-esp32-devkit-v1/6158/8 este enlace: https://forum.fritzing.org/uploads/default/original/2X/5/52c6aaad54a039b8412a393cc22f929288fa2ac3.fzpz
