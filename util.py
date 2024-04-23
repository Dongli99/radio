HOST = "localhost"
PORT = 1883
CHANNELS = ["news", "talk", "story", "sport"]
METRICS = [  # representing the parameters for creating data generators
    [200, "M", 20, -20, -10],
    [300, "F", 50, 0, 0],
    [1000, "F", 10, -25, -10],
    [500, "M", 100, 20, 10],
]
COLORS = {
    "news": [[255, 113, 205], [87, 85, 254]],
    "talk": [[100, 200, 50], [200, 100, 50]],
    "story": [[50, 150, 200], [200, 150, 50]],
    "sport": [[200, 50, 50], [50, 200, 50]],
}
