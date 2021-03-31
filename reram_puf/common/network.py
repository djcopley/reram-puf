######## Client Manager Utilities ########
#
# Authors: Corey Cline
#          Daniel Copley
#
# Date: 03/22/2021
#
# Description:
# A Network interface class for MQTT plug and play communication.
#
#############################################################################
from mqtt_client import MQTTClient

"""Network Class for MQTT Communication between client and server."""


class Network:
    
    def __init__(self, hostname: str, user: str):
        """Constructor method."""
        self.hostname = hostname
        self.user = user
        self.mqtt = MQTTClient(self.hostname, self.user)
        self.unread = self.mqtt.msg_queue

    def close(self, port=1883):
        """Close the network connection."""
        self.mqtt.loop_stop()
        self.mqtt.disconnect()

    def connect(self):
        """Connect to the network interface."""
        self.mqtt.connect(port)
        self.mqtt.loop_start

    def receive(self, user=self.user) -> str:
        """Receive a message and return the string."""
        self.mqtt.subscribe(topic=user)

    def send(self, receiver: str, msg: bytes) -> bool:
        """Send a message, return true if successful."""
        self.mqtt.publish(topic=receiver, msg)
