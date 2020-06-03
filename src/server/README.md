Este programa ha sido probado y diseñado para Raspberry Pi 3 model B usando Raspbian GNU/Linux.

Puede ser necesario instalar python3 y pip3 para poder ejecutar el servidor. Puedes instalarlo en Raspbian con apt:

```sudo apt-get install python3 python3-pip```

Una vez hecho esto puedes obtener las dependencias con pip3:

```pip3 install -r requirements.txt```

Desde este momento puedes lanzar el servidor a mano con:

```python3 app.py [-H HOST_IP] [-p PORT]```

Aunque es recomendable lanzarlo al iniciar el sistema, por ejemplo usando un script en `/init.d/` o utilizar crontab en Raspbian.

Ejemplo:

Añadir a `crontab -e` la línea:

```
@reboot  cd /home/pi/smart-plug && python3 /home/pi/smart-plug/app.py >> /home/pi/smart-plug/log.txt 2>&1 &
```

