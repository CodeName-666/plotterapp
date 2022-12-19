import sys
import random
from PyQt5 import QtCore, QtWidgets, QtQml

# Create the application object
app = QtWidgets.QApplication(sys.argv)

# Create the QML engine
engine = QtQml.QQmlApplicationEngine()

# Load the main QML file
engine.load("KiCodegen_qmlChart.qml")

# Function to update the chart with new data
def update_chart():
    # Generate some random data
    x = random.randint(0, 10)
    y = random.randint(0, 10)

    # Get the chart object from the QML engine
    chart = engine.rootObjects()

    # Add the new data to the chart
    chart.append({"x": x, "y": y})

# Create a timer to periodically update the chart
timer = QtCore.QTimer()

# Connect the timer's timeout signal to the update_chart function
timer.timeout.connect(update_chart)

# Start the timer with a 1 second interval
timer.start(1000)

# Run the application
app.exec_()
