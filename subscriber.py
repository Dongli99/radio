import paho.mqtt.client as mqtt
from json import loads
from tkinter import Frame, BOTH, Button, Tk
from threading import Thread
from util import HOST, PORT, CHANNELS, COLORS
from dynamic_chart import DynamicChart


class Radio(Frame):
    """
    A class representing a radio interface.

    Attributes:
        chart_wid (int): The width of the chart.
        data (list): A list containing the radio data.
        buttons (list): A list containing radio button widgets.
        count (int): The count of radio data.
        chart (DynamicChart): An DynamicChart widget for displaying radio data.
        fms (list): A list containing the frequency modulations.
        receiver (Receiver): An Receiver instance for receiving radio signals.
        receiver_thread (Thread): A thread for running the receiver process.
    """

    def __init__(self, chart_wid=100):
        """Initialize the Radio."""
        super().__init__()
        self.chart_wid = chart_wid
        self.data = [[i, 10] for i in range(self.chart_wid)]
        self.buttons = []
        self.count = len(self.data)
        self.initReceiver()
        self.initUI()

    def initReceiver(self):
        """Initialize the radio receiver."""
        self.fms = [i for i in range(4)]
        self.receiver = Receiver()
        self.receiver.client.on_message = self.process
        self.receiver_thread = Thread(target=self.receiver.block, daemon=True)
        self.receiver_thread.start()

    def initUI(self):
        """Initialize the user interface."""
        self.master.title("Radio")
        self.pack(fill=BOTH, expand=1)
        self.chart = DynamicChart(
            box=self.data,
            chart_only=True,
            amplify=5,
            width=self.chart_wid,
            margin=0,
            base=340,
            color_range=self.receiver.theme,
        )
        self.drawLeft()
        self.drawRight()

    def process(self, client, user_data, message):
        """Process incoming radio messages."""
        decoded_msg = message.payload.decode("utf-8")
        message_dict = loads(decoded_msg)
        for _, v in message_dict.items():
            self.data.append([self.count, v])
            self.data.pop(0)
            self.count += 1
        self.update_ui()

    def drawLeft(self):
        """Draw the left section of the radio interface."""
        self.console = Frame(self)
        self.console.place(relx=0.03, rely=0.03, relwidth=0.2, relheight=0.94)
        self.drawBtns(init=True)

    def drawRight(self):
        """Draw the right section of the radio interface."""
        self.chart.place(relx=0.28, rely=0.1, relwidth=0.66, relheight=0.94)
        self.drawChart()

    def drawBtns(self, init=False):
        """Draw the radio buttons."""
        for btn in self.buttons:
            btn.destroy()
        self.buttons = []
        for i, fm in enumerate(self.fms):
            receiving = fm == self.receiver.fm if not init else False
            btn = Button(
                self.console,
                bg="orange" if receiving else "#f0f0f0",
                text=CHANNELS[fm],
                borderwidth=2,
                font=("Helvetica", 18),
                relief="groove" if receiving else "raised",
                fg="white" if receiving else "black",
                command=lambda fm=fm: self.switchFm(fm),
            )
            btn.place(relx=0.03, rely=0.03 + i * 0.23, relwidth=0.8, relheight=0.2)
            self.buttons.append(btn)

    def drawChart(self):
        """Draw the radio chart."""
        self.chart.box = self.data
        self.chart.locs = self.chart.getLocations()
        self.chart.drawChart()

    def switchFm(self, fm):
        """Switch the radio frequency modulation."""
        self.receiver.switch(fm)
        self.drawBtns()

    def update_ui(self):
        """Update the radio user interface."""
        self.chart.box = self.data
        self.chart.col_range = self.receiver.theme
        self.chart.refresh(self.receiver.topic)


class Receiver:
    """
    A class representing a radio signal receiver.

    Attributes:
        fm (int): The frequency modulation index.
        topic (str): The current radio channel topic.
        theme (list): The color theme for the radio chart.
        client (mqtt.Client): An instance of the MQTT client for receiving radio signals.
    """

    def __init__(self, fm=0) -> None:
        """Initialize the radio receiver."""
        self.fm = fm
        self.topic = CHANNELS[self.fm]
        self.theme = COLORS[self.topic]
        self.client = mqtt.Client()
        self.client.connect(HOST, PORT)

    def switch(self, fm):
        """Switch the radio channel."""
        old_topic = CHANNELS[self.fm]
        self.fm = fm
        self.topic = CHANNELS[self.fm]
        self.theme = COLORS[self.topic]
        self.client.unsubscribe(old_topic)
        self.client.subscribe(self.topic)

    def block(self):
        """Start blocking loop to receive radio signals."""
        self.client.loop_forever()


if __name__ == "__main__":
    root = Tk()
    root.geometry("800x500+300+300")
    radio = Radio()
    root.mainloop()
