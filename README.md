# smart-plug
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

Este repositorio contiene todo lo relativo a mi Proyecto de Fin de Grado del Grado en Ingeniería Informática en la Universidad de Granada: **Diseño y construcción de un sistema para adquisición y análisis del consumo energético en el hogar.**

En este se describe el proceso de diseño y construcción del sistema, la arquitectura desde el enchufe hasta la interfaz de usuario, así como se recopila el código usado para su funcionamiento. Un sistema que recoge datos relativos al consumo eléctrico mediante sensores en un enchufe y se comunica por MQTT con un broker MQTT ([Mosquitto](https://mosquitto.org/)) y finalmente se presenta en una app de escritorio desde la cual se puede controlar el gasto energético y manipular los enchufes.

Indice
======
* [src - Código del proyecto](#src)
  * [Módulo Hardware](#módulo-hardware)
    * [¿Cómo usarlo?](#cómo-usarlo)
	* [¿Necesito exactamente este enchufe para usar el sistema?](#necesito-exactamente-este-enchufe-para-poder-usar-el-sistema)
  * [Módulo Servidor](#módulo-servidor)
  * [Módulo Cliente](#módulo-cliente)
    * [¿Puedo utilizar mi propia app?](#puedo-utilizar-mi-propia-app)
* [Documentación](#documentación)

## src

Colección del código relativo al proyecto en cada uno de sus apartados.

### Módulo Hardware

* Submódulo hardware: Construcción de enchufe. Gestión del relé y de las lecturas, comunicación con el broker.

#### **¿Cómo usarlo?**

Si se dispone de un enchufe como el descrito en [la documentación](https://github.com/jojelupipa/smart-plug/blob/master/documentacion/memoria.pdf) se puede conectar directamente a la corriente para comenzar a usarlo. Si se desea modificar el comportamiento del [programa del microcontrolador](https://github.com/jojelupipa/smart-plug/blob/master/src/esp32_module/esp32_module.ino) puede usarse algún editor como [Arduino IDE](https://www.arduino.cc/en/Main/Software) para simplificar las tareas de conexión con este módulo.

#### ¿Necesito exactamente este enchufe para poder usar el sistema?

¡Para nada! Utilizar el mismo enchufe solo simplifica las cosas. Puedes usar tu propio enchufe o cualquier tipo de interfaz que se comunique por MQTT con el broker, simplemente ha de publicar en un tema correspondiente y, si se desea disponer de las funcionalidades de control, tener algún tipo de relé para controlar tu enchufe.

### Módulo servidor

* Submódulo servidor: Gestión del broker. Gestión de la base de datos

### Módulo cliente

* Submódulo cliente: App para gestionar el enchufe, comunicarse con el broker, consultar y visualizar lecturas.

#### ¿Puedo utilizar mi propia app?

Por supuesto, el servidor dispone de una API para proporcionar toda la información de consumo. Siéntete libre para crear una app nueva o adaptarla a tus necesidades.

## documentación

En [esta sección](https://github.com/jojelupipa/smart-plug/tree/master/documentacion) se recoge toda la memoria y documentación del proyecto.

