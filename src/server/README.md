# Servidor

## Mosquitto

Puedes utilizar el [script de provisionamiento](https://github.com/jojelupipa/smart-plug/blob/master/src/server/script_provisionamiento.sh) para instalar Mosquitto y otras dependencias que harán falta para el funcionamiento del servidor.

## Programa de la API

Este programa ha sido probado y diseñado para Raspberry Pi 3 model B usando Raspbian GNU/Linux.

Son necesarios python3 y pip3 para poder ejecutar el servidor. El script de provisionamiento los habrá instalado si no los tenías.

Puedes obtener las dependencias de Python con pip3:

```pip3 install -r requirements.txt```

Desde este momento puedes lanzar el servidor a mano con:

```python3 app.py [-H HOST_IP] [-p PORT]```

Aunque es recomendable lanzarlo al iniciar el sistema, por ejemplo usando un script en `/init.d/` o utilizar crontab en Raspbian.

Ejemplo:

Añadir a `crontab -e` la línea:

```
@reboot  cd /home/pi/smart-plug && python3 /home/pi/smart-plug/app.py >> /home/pi/smart-plug/log.txt 2>&1 &
```


