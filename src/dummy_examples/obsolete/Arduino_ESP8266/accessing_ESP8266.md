# Comunicación con el módulo a través de Arduino UNO

1) Seguir el esquema de fritzing de montaje

2) Abrir el monitor serie en Arduino IDE (Ctrl+Shift+M)

Entonces ya se podrán utilizar comandos AT

# Algunos comandos AT

Fuente: https://www.espressif.com/sites/default/files/documentation/4a-esp8266_at_instruction_set_en.pdf


## AT+GMR

Output:

```

AT version:1.2.0.0(Jul  1 2016 20:04:45)

SDK version:1.5.4.1(39cb9a32)

Ai-Thinker Technology Co. Ltd.

Dec  2 2016 14:21:16

```

## AT+CWLAP

Lists available SSIDs.

Output:

```
+CWLAP:(3,"SSID_1",-77,"34:34:11:12:13:14",1,68,0)

+CWLAP:(4,"SSID_2",-48,"61:23:14:13:12:11",1,78,0)

```

## AT+CWJAP="SSID","password"


Output:

```
WIFI CONNECTED

WIFI GOT IP
```

## AT+CIFSR

Returns IP assigned.

Output:

```
 AT+CIFSR


+CIFSR:APIP,"192.168.4.1"

+CIFSR:APMAC,"de:4f:22:0a:cf:1b"

+CIFSR:STAIP,"192.168.1.68"

+CIFSR:STAMAC,"dc:4f:22:0a:cf:1b"
```



## AT+CIPSERVER=1,<port>

Crea una conexión TCP en el puerto indicado con <port>.

La respuesta será el resultado de las conexiones que reciba.

Ej: Si desde el pc ejecutamos `curl <ip>` obtenemos:

```
+IPD,0,76:GET / HTTP/1.1

Host: 192.168.1.68

User-Agent: curl/7.58.0

Accept: */*
```

O con `nc -z <ip> 80`:

```
0,CONNECT

0,CLOSED
```

