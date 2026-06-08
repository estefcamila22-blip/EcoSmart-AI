import logging
import json
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class MQTTService:
    def __init__(self, broker: str = "localhost", port: int = 1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.is_connected = False
        self.callbacks = {}

    async def connect(self):
        try:
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            self.is_connected = True
            logger.info(f"Connected to MQTT broker at {self.broker}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise

    async def disconnect(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
            self.is_connected = False
        except Exception as e:
            logger.error(f"Disconnect error: {e}")

    def publish(self, topic: str, payload: dict, qos: int = 1):
        if self.is_connected:
            self.client.publish(topic, json.dumps(payload), qos=qos)

    def subscribe(self, topic: str, callback):
        self.callbacks[topic] = callback
        self.client.subscribe(topic)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT connection successful")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            if msg.topic in self.callbacks:
                self.callbacks[msg.topic](payload)
        except Exception as e:
            logger.error(f"Message processing error: {e}")