import paho.mqtt.client as mqtt

from threading import Thread
from json import loads
from tkinter import *

from util import HOST, PORT, CHANNELS


class Radio:
    def __init__(self):
        super().__init__()
        self.t = Thread(target=self.refresh, daemon=True)
        self.initRadio()
        self.initUI()

    def initRadio(self):
        pass

    def initUI(self):
        self.master.title("Radio")
        self.pack(fill=BOTH, expand=1)

    def refresh(self):
        pass


class Channel:
    def __init__(self, fm=0) -> None:
        self.fm = fm
        self.topic = CHANNELS[self.fm]
        self.client = mqtt.Client()
        self.client.on_message = Channel.on_message
        self.client.connect(HOST, PORT)
        self.client.subscribe(self.topic)

    def on_message(client, user_data, message):
        decoded_msg = message.payload.decode("utf-8")
        message_dict = loads(decoded_msg)
        print(message_dict)

    def block(self):
        """Start blocking loop to listen to channel."""
        self.client.loop_forever()


if __name__ == "__main__":
    channel = Channel()
    channel.block()
