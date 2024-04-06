import paho.mqtt.client as mqtt

from queue import Queue
from time import asctime, sleep
from json import dumps
from threading import Thread
from tkinter import *

from data_generator import VoiceDataGenerator
from util import HOST, PORT, CHANNELS, METRICS


class Console(Frame):
    def __init__(self):
        super().__init__()
        self.t = Thread(target=self.refreshDisplay, daemon=True)
        self.initTransmitters()
        self.initUI()

    def initTransmitters(self):
        self.transmitters = [Transmitter(bond=i) for i in range(4)]
        for t in self.transmitters:
            print(t.topic)

    def initUI(self):
        self.master.title("Transmitter Console")
        self.pack(fill=BOTH, expand=1)
        self.drawDisplay()
        self.drawCenter()
        self.drawBottom()

    def drawDisplay(self):
        pass

    def drawCenter(self):
        pass

    def drawBottom(self):
        pass

    def refreshDisplay(self):
        pass


class Transmitter:

    def __init__(
        self,
        bond=0,
        delay=1,
    ) -> None:
        self.bond = bond
        self.topic = CHANNELS[self.bond]
        self.playing = False
        self.connected = False
        self.delay = delay
        self.cursor = 0
        self.t = Thread(target=self.transmit, daemon=True)
        self.data = Queue()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.tune()

    def play(self):
        if not self.connected:
            self.client.connect(HOST, PORT)
            self.connected = True
            self.playing = True
            self.t.start()
        if not self.t.is_alive():
            self.t.start()

    def pause(self):
        self.playing = False

    def stop(self):
        if self.connected:
            self.connected = False
            self.client.disconnect()

    def tune(self):
        self.generator = VoiceDataGenerator(*METRICS[self.bond])

    def process(self):
        raw = self.generator.data
        for i in range(raw.shape[0]):
            self.data.put(raw[i, 1])

    def transmit(self):
        while True:
            if not self.playing:
                break  # Exit the loop if playing is False
            if self.data.empty():
                self.process()
            syllable = {asctime(): self.data.get()}
            payload = dumps(syllable)
            self.client.publish(topic=self.topic, payload=payload)
            sleep(self.delay)

    def on_publish(self, client, userdata, mid):
        print("Syllable sent.")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Channel {self.name} connected to MQTT broker.")
            self.connected = True
        else:
            print(f"Channel {self.name} failed to connect with result code {rc}.")

    def on_disconnect(self, client, userdata, rc):
        print(f"Channel {self.name} disconnected from MQTT broker.")
        self.connected = False


if __name__ == "__main__":
    root = Tk()
    root.geometry("720x450+300+300")
    Console = Console()
    root.mainloop()
