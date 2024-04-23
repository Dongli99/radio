# Author: Dongli Liu
# Description: A class to simulate a transmitter console.

import paho.mqtt.client as mqtt

from queue import Queue
from time import asctime, sleep
from json import dumps
from threading import Thread
from tkinter import Frame, BOTH, Button, Tk

from data_generator import VoiceDataGenerator
from util import HOST, PORT, CHANNELS, METRICS


class Console(Frame):
    """GUI class for managing transmitter buttons."""

    def __init__(self):
        """Initialize Console."""
        super().__init__()
        self.buttons = Queue(maxsize=4)  # Queue for storing buttons
        self.initTransmitters()  # Initialize transmitters
        self.initUI()  # Initialize GUI

    def initTransmitters(self):
        """Initialize transmitters."""
        # Create transmitter objects
        self.transmitters = [Transmitter(bond=i) for i in range(4)]

    def initUI(self):
        """Initialize GUI."""
        self.master.title("Transmitter Console")
        self.pack(fill=BOTH, expand=1)
        self.drawCenter()

    def drawCenter(self):
        """Draw transmitter buttons."""
        self.stage = Frame(self)
        self.stage.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        t = 0
        for i in range(2):
            for j in range(2):
                transmitter = self.transmitters[t]
                btn = self.createTransmitterBtn(self.stage, transmitter)
                btn.place(
                    relx=0.03 + i * 0.5,
                    rely=0.03 + j * 0.5,
                    relwidth=0.45,
                    relheight=0.45,
                )
                self.buttons.put(btn)
                t += 1

    def createTransmitterBtn(self, frame, transmitter):
        """Create a transmitter button."""
        btn = Button(
            frame,
            bg="#f0f0f0" if not transmitter.playing else "orange",
            text=transmitter.topic,
            borderwidth=2,
            font=("Helvetica", 24, "italic"),
            relief="raised" if not transmitter.playing else "groove",
            fg="black" if not transmitter.playing else "white",
        )
        btn.config(command=lambda: self.switchTransmitter(btn, transmitter))
        return btn

    def switchTransmitter(self, btn, transmitter, switch=True):
        """Switch transmitter status."""
        if switch:  # Toggle playing status
            transmitter.playing = not transmitter.playing
        if transmitter.playing:
            btn.config(bg="orange", fg="white", relief="groove")
            if not transmitter.connected:
                transmitter.play()
            else:
                transmitter.restore()  # Restore transmitter
        else:
            btn.config(bg="#f0f0f0", fg="black", relief="raised")
            transmitter.pause()  # Pause transmitter


class Transmitter:
    """Class representing a transmitter."""

    def __init__(
        self,
        bond=0,
        delay=0.3,
    ) -> None:
        """Initialize transmitter."""
        self.bond = bond  # Transmitter bond
        self.topic = CHANNELS[self.bond]  # Transmitter topic
        self.playing = False  # Transmitter playing status
        self.connected = False  # Transmitter connection status
        self.delay = delay  # Transmission delay
        self.cursor = 0  # Cursor position
        self.t = Thread(
            target=self.transmit, args=(), daemon=True
        )  # Transmission thread
        self.data = Queue()  # Data queue
        self.client = mqtt.Client()  # MQTT client
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.tune()  # Tune transmitter parameters

    def play(self):
        """Start transmitter."""
        if not self.connected:
            self.client.connect(HOST, PORT)
            self.connected = True
            self.playing = True
            self.t.start()
        if not self.t.is_alive():
            self.t.start()

    def pause(self):
        """Pause transmitter."""
        self.playing = False

    def restore(self):
        """Restore transmitter."""
        self.playing = True

    def stop(self):
        """Stop transmitter."""
        if self.connected:
            self.connected = False
            self.client.disconnect()

    def tune(self):
        """Set transmitter parameters."""
        self.generator = VoiceDataGenerator(*METRICS[self.bond])

    def process(self):
        """Process data."""
        raw = self.generator.data
        for i in range(raw.shape[0]):
            self.data.put(raw[i, 1])

    def transmit(self):
        """Transmit data."""
        while True:
            if not self.playing:
                continue  # Skip the rest and continue the loop if not playing
            if self.data.empty():
                self.process()
            syllable = {asctime(): self.data.get()}
            payload = dumps(syllable)  # Serialize syllable to JSON
            self.client.publish(topic=self.topic, payload=payload)
            sleep(self.delay)

    def on_publish(self, client, userdata, mid):
        print(f"{self.topic} playing.")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Channel {self.topic} connected to MQTT broker.")
            self.connected = True
        else:
            print(f"Channel {self.topic} failed to connect with code {rc}.")

    def on_disconnect(self, client, userdata, rc):
        print(f"Channel {self.topic} disconnected from MQTT broker.")
        self.connected = False


if __name__ == "__main__":
    root = Tk()
    root.geometry("320x320+300+300")
    Console = Console()
    root.mainloop()
