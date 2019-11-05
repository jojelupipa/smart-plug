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

Probamos nuestro sensor intrusivo en una bombilla de 11W. 

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
