<h1 align="center"> Radio Application </h1>

<div align='center'>
  <img src="https://img.shields.io/badge/python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/TKINTER-013243.svg?style=for-the-badge" alt="numpy">
  <img src="https://img.shields.io/badge/MQTT-660066.svg?style=for-the-badge&logo=mqtt&logoColor=white" alt="python">
</div>
<div align='center' style="margin-top: 20px;">
  <image src="img/transmitter.png" style="height:50px;">
  <image src="img/radio.png" style="height:50px;">
</div>

## Overview

The Radio Application is a Python-based graphical user interface (GUI) designed for streaming and visualizing radio data received through MQTT. It provides features such as dynamic chart display, channel switching, and real-time data updates. The project consists of two main components: the transmitter console and the radio interface.

**Radio integrates the following projects:**

- [VoiceDataGenerator](https://github.com/Dongli99/PY-voice-data-generator)  <image src="img/voice.png" style="width:15%">  
  - Simulating voice data with customizable parameters such as pitch, duration, and noise.

- [Gauge](https://github.com/Dongli99/PY-gui-gauge)  <image src="img/gauge.png" style="width:5%">
  - A customizable graphical representation of a gauge.  

- [DynamicChart](https://github.com/Dongli99/PY-dynamic-chart)  <image src="img/chart.png" style="width:7%">
  - Displaying a dynamic chart with real-time data visualization.

## Requirements

- Python 3.x
- Paho MQTT library

## Configuration

- Modify the util.py file to configure MQTT broker settings, channel details, and color themes.
- Adjust parameters in the files to customize chart settings and transmitter behavior.

## Transmitter Console

The transmitter console simulates the behavior of radio transmitters. It allows users to control the transmission of radio signals through graphical buttons. The console is built using Tkinter and Paho MQTT client libraries.

### Features

- **Transmitter Buttons**: Graphical buttons represent different transmitter channels.
- **Play/Pause Functionality**: Users can toggle the transmission status of each transmitter.

### Usage

- Run the `transmitter.py` script.
- The radio interface GUI will open, displaying the dynamic chart and channel selection buttons.
- Click on the channel buttons to switch between radio channels and view corresponding data on the chart.

<image src="img/transmitter.png" style="width:30%">  

## Radio Interface

The radio interface displays incoming radio data in real-time and allows users to switch between different radio channels. It includes a dynamic chart for visualizing the data and channel selection buttons.

### Features

- **Dynamic Chart**: Real-time visualization of radio data on a dynamic chart.
- **Channel Selection**: Buttons for switching between different radio channels.
- **Automatic Data Refresh**: Data is automatically updated as new information is received.

### Usage

- Run the `radio.py` script.
- The radio interface GUI will open, displaying the dynamic chart and channel selection buttons.
- Click on the channel buttons to switch between radio channels and view corresponding data on the chart.

<image src="img/radio.png" style="width:30%">  
