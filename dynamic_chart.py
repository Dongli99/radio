import random
import time
import numpy as np

from threading import Thread
from tkinter import *

from data_generator import VoiceDataGenerator


class DynamicChart(Frame):
    """
    A class representing a dynamic chart widget.

    Attributes:
        GENERATOR (VoiceDataGenerator): An instance of VoiceDataGenerator used for data generation.
        DATA (list): A list containing the generated data.
        width (int): The width of the chart.
        c_data (CircularList): An instance of CircularList containing the circular data.
        margin (int): The margin around the chart.
        amplify (int): The amplification factor for the chart for better appearance.
        box (list): A list containing the current data box.
        locs (list): A list containing the locations of the chart elements.
        col_range (list): A list containing the range of colors for the chart bars.
        thread (Thread): A Thread object for running the chart update loop.
    """

    GENERATOR = VoiceDataGenerator(duration=1000, gender="M")
    DATA = GENERATOR.data.tolist()

    def __init__(
        self,
        data=DATA,
        chart_only=False,
        width=20,
        margin=30,
        amplify=32,
        frequency=0.4,
        box=None,
        base=340,
        color_range=[[255, 113, 205], [87, 85, 254]],
    ):
        """Initialize the DynamicChart."""
        super().__init__()
        self.width = width
        self.chart_only = chart_only
        self.c_data = self.CircularList(data)
        self.margin = margin
        self.amplify = amplify
        self.frequency = frequency
        self.base = base
        self.box = box if self.chart_only else self.c_data.roll(self.width)
        self.locs = self.getLocations()
        self.col_range = color_range
        self.initUI()

    def initUI(self):
        """Initialize the user interface of the chart."""
        self.pack(fill=BOTH, expand=1)
        self.thread = Thread(target=self.refresh, daemon=True)
        if not self.chart_only:
            self.master.title("Dynamic Chart")
            self.drawTop()
        self.drawChart()

    def drawTop(self):
        """Draw the top section of the chart."""

        def handleLucky():
            # randomize color
            self.col_range[0] = generateRandomColor()
            self.col_range[1] = generateRandomColor()

        frame = Frame(self)
        frame.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.08)
        go_btn = Button(frame, text="Go", command=self.thread.start)
        go_btn.place(relx=0.38, rely=0.1, relwidth=0.12, relheight=0.8)
        luck_btn = Button(frame, text="Lucky", command=handleLucky)
        luck_btn.place(relx=0.52, rely=0.1, relwidth=0.12, relheight=0.8)

    def drawChart(self, topic=None):
        """Draw the main chart area."""
        frame = Frame(self)
        if not self.chart_only:
            frame.place(relx=0.03, rely=0.15, relwidth=0.94, relheight=0.86)
        else:
            frame.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.94)
        self.canvas = Canvas(frame)
        self.canvas.pack(fill=BOTH, expand=1)
        self.drawBars()
        if not self.chart_only:
            self.drawLine()
        self.drawInfo(self.locs[-1][-1], topic=topic)

    def refresh(self, topic=None):
        """Refresh the chart."""
        if self.chart_only is not True:
            while True:
                time.sleep(self.frequency)
                self.canvas.delete("bars")
                self.box = self.c_data.roll(self.width)
                self.locs = self.getLocations()
                self.drawBars()
                self.drawLine()
                self.drawInfo(self.locs[-1][-1])
        else:
            self.canvas.delete("all")
            self.locs = self.getLocations()
            self.drawBars()
            self.drawInfo(self.locs[-1][-1], topic=topic)
            # self.drawLine()

    def drawBars(self):
        """Draw the bars on the chart."""

        def getColor(pitch):
            # generate a color corresponding to the pitch
            rgb = [
                a + (b - a) * pitch / 255
                for a, b in zip(self.col_range[0], self.col_range[1])
            ]
            return hexColor(rgb)

        rec_wid = self.amplify * 0.8
        for loc in self.locs:
            self.canvas.create_rectangle(
                loc[0] - rec_wid / 2,
                loc[1],
                loc[0] + rec_wid / 2,
                self.base + 20,
                fill=getColor(loc[1]),
                outline="",
                tags="bars",
            )

    def drawLine(self):
        """Draw the line on the chart."""
        self.canvas.create_line(self.locs, width=2, smooth=True)

    def drawInfo(self, pitch, topic):
        """
        Draw the information text on the chart.

        Args:
            pitch (int): The pitch value.
        """
        if not self.chart_only:
            msg = (
                "The "
                + ("man " if DynamicChart.GENERATOR.gender == "M" else "woman ")
                + (
                    "is talking. Pitch: "
                    if self.base - pitch > 60
                    else "is in silence. Noise: "
                )
                + str(self.base - pitch)
            )
        else:
            topic = topic.capitalize() if topic is not None else "No Channel"
            msg = f" {topic} is playing..."
        self.canvas.create_text(self.margin / 2, self.base + 30, text=msg, anchor=W)

    def getLocations(self):
        """Calculate the locations of the chart elements."""
        locations = []
        offset = self.box[0][0]
        for i in range(self.width):
            x = (self.box[i][0] - offset) * self.amplify + self.margin
            y = self.base - round(self.box[i][1])
            locations.append([x, y])
        return locations

    class CircularList:
        """
        A class representing a circular list.

        Attributes:
            l (list): The list data.
            c (int): The current index cursor.
            n (int): The length of the list.
        """

        def __init__(self, data):
            """
            Initialize the CircularList.

            Args:
                data (list): The initial list data.
            """
            if isinstance(data, list):
                self.l = data
            else:
                raise ValueError("l must be a list.")
            self.c = 0
            self.n = len(self.l)

        def walk(self):
            """Move the cursor and return the element."""
            e = self.l[self.c]
            self.c += 1
            if self.c == self.n - 1:
                self.c = 0
            return e

        def roll(self, wid):
            """
            Roll the circular list to generate a box of data.

            Args:
                wid (int): The width of the box.

            Returns:
                list: A list containing the box of data.
            """
            tmp = self.c  # current cursor
            es = [self.walk() for _ in range(wid)]  # create a list in width
            self.c = tmp  # reset cursor to previous and walk to next
            self.walk()
            return es


def hexColor(rgb):
    """
    Convert an RGB color to hexadecimal format.

    Args:
        rgb (list): List containing the RGB values.

    Returns:
        str: Hexadecimal representation of the RGB color.
    """
    red = max(0, min(int(rgb[0]), 255))
    green = max(0, min(int(rgb[1]), 255))
    blue = max(0, min(int(rgb[2]), 255))
    return "#{:02x}{:02x}{:02x}".format(red, green, blue)


def generateRandomColor():
    """Generate a random RGB color."""
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return [red, green, blue]


if __name__ == "__main__":
    data = [[i, 0] for i in range(100)]
    root = Tk()
    root.geometry("720x450+300+300")
    chart = DynamicChart()
    root.mainloop()
