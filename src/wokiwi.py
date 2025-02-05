"""
MicroPython IoT Weather Station Example for Wokwi.com

To view the data:

1. Go to http://www.hivemq.com/demos/websocket-client/
2. Click "Connect"
3. Under Subscriptions, click "Add New Topic Subscription"
4. In the Topic field, type "wokwi-weather" then click "Subscribe"

Now click on the DHT22 sensor in the simulation,
change the temperature/humidity, and you should see
the message appear on the MQTT Broker, in the "Messages" pane.

Copyright (C) 2022, Uri Shaked

https://wokwi.com/arduino/projects/322577683855704658
"""

import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# Configurações MQTT
MQTT_CLIENT_ID = "67a395525232ac000835d5a9"
MQTT_BROKER = "mqtt.tago.io"
MQTT_TOPIC = "data"
MQTT_USER = ""
MQTT_PASSWORD = "1bdbd4bc-6550-4868-a9a7-537c22d5406f"

# Configurações Wi-Fi
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# Inicializa o sensor DHT22
sensor = dht.DHT22(Pin(15))

# Função para conectar ao Wi-Fi
def connect_wifi():
    print("Conectando ao Wi-Fi...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    if not sta_if.isconnected():
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 10  # Tempo limite de 10 segundos
        while not sta_if.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1

    if sta_if.isconnected():
        print("\nWi-Fi Conectado! IP:", sta_if.ifconfig()[0])
    else:
        print("\nFalha ao conectar ao Wi-Fi.")

# Função para conectar ao MQTT
def connect_mqtt():
    print("Conectando ao MQTT...")
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
        client.connect()
        print("Conectado ao MQTT!")
        return client
    except Exception as e:
        print("Erro ao conectar ao MQTT:", e)
        return None

# Inicializa conexões
connect_wifi()
mqtt_client = connect_mqtt()

prev_weather = ""

# Loop principal
while True:
    try:
        print("Medindo temperatura e umidade...")
        sensor.measure()
        message = ujson.dumps({
            "temperature": sensor.temperature(),
            "humidity": sensor.humidity(),
        })

        # Evita publicar dados repetidos
        if message != prev_weather:
            print(f"Enviando dados para MQTT ({MQTT_TOPIC}): {message}")
            if mqtt_client:
                mqtt_client.publish(MQTT_TOPIC, message)
            prev_weather = message
        else:
            print("Sem mudanças nos dados.")

    except Exception as e:
        print("Erro durante leitura/publicação:", e)
        mqtt_client = connect_mqtt()  # Tenta reconectar

    time.sleep(5)  # Tempo de espera entre leituras

