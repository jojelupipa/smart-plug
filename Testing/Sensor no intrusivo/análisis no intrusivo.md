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

Hay otro concepto importante a tener en cuenta que es la resistencia
de carga. El modelo SCT-013-000 no tiene ninguna resistencia de carga,
lo cual nos permite seleccionar la que nos permita medir con mejor
precisión.

La función de una resistencia de carga es convertir la corriente en un
voltaje limitado que podamos medir con Arduino. Por defecto el SCT-013
mide desde 50mA a 100A, por lo que si queremos usarlo para medir una
corriente de 0.8A~4A se perdería mucha precisión.

Para calcular la resistencia de carga tenemos que conocer la potencia
estimada del dispositivo a medir. **Duda: ¿Significa eso que entonces
estamos condicionados al rango que podemos medir? ¿Es aceptable asumir
que estamos desarrollando un sensor para productos de un rango de
consumo estimado?**

