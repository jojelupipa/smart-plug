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

Queremos probar de manera análoga al ACS712. Pero para este no tenemos
un código de prueba como para el anterior. Así que vamos a
documentarnos primero como en el artículo
https://programarfacil.com/blog/arduino-blog/sct-013-consumo-electrico-arduino/

Aquí encontramos un detalle importante: _“El sensor SCT-013 nos dará
una resolución de 2 decimales por lo tanto, si queremos calibrar bien
este sensor debemos utilizar un aparato que consuma más de 20W”_.
