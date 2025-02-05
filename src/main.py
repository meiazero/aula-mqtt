from fastapi import FastAPI, HTTPException
import paho.mqtt.client as mqtt

app = FastAPI()

topics = set()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code: {rc}")

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")

# MQTT setup
def setup_mqtt(broker="localhost", port=1883):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(broker, port, keepalive=60)
    mqtt_client.loop_start()
    return mqtt_client

# Initialize MQTT client
mqtt_client = setup_mqtt()

@app.post("/topics")
def create_topic(topic_name: str):
    if topic_name in topics:
        raise HTTPException(status_code=400, detail="Topic already exists")
    topics.add(topic_name)
    mqtt_client.subscribe(topic_name)
    return {"message": f"Topic '{topic_name}' created successfully"}

@app.get("/topics")
def list_topics():
    return {"registered_topics": list(topics)}

@app.post("/topics/{topic_name}")
def publish_topic_message(topic_name: str, message: str):
    if topic_name not in topics:
        raise HTTPException(status_code=404, detail="Topic not found")
    mqtt_client.publish(topic_name, message)
    return {"message": f"Message published to topic '{topic_name}'"}
