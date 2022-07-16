from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5 import uic
import sys
import requests


# Method to call API and get the information
# Returns the information in JSON form
def call_api(city_name):
    # Generate API key at https://openweathermap.org/api
    API_KEY = "---"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    request_url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(request_url)

    return response


# Main application method
def main():
    app = QApplication(sys.argv)
    UIWindow = UI()
    sys.exit(app.exec_())


# Class that contains the window information, components and methods
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Loading window from .ui file
        uic.loadUi("MainWindow.ui", self)
        self.show()

        # Importing the components from .ui file
        self.main_label = self.findChild(QLabel, "mainTitle")
        self.description = self.findChild(QLabel, "description")
        self.line_edit = self.findChild(QLineEdit, "lineEdit")
        self.button = self.findChild(QPushButton, "pushButton")
        self.button2 = self.findChild(QPushButton, "pushButton_2")
        self.main_layout = self.findChild(QVBoxLayout, "layout")
        self.background_label.setStyleSheet('background-image: url(Background.png);')

        # Defining the logic after button presses
        self.button.clicked.connect(self.change_to_weather)
        self.button2.clicked.connect(self.change_to_main)
        self.button2.hide()

    # Method used to change the window to the weather information mode
    # (appears after inserting the correct name of the city and confirming it with button press)
    def change_to_weather(self):
        city_name = self.line_edit.text()
        response = call_api(city_name)

        if response.status_code == 200:
            data = response.json()
            self.main_label.setText(data['name'])
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(12)
            self.description.setFont(font)
            self.description.setText(
                f"Temperature: {round(data['main']['temp'])}°C\nPressure: {data['main']['pressure']} hPa\n"
                f"Wind: {data['wind']['speed']} m/s\n")
            self.line_edit.hide()
            self.button.hide()
            self.button2.show()
        else:
            self.change_to_error()

    # Changing the window the main mode        
    def change_to_main(self):
        self.main_label.setText("WeatherApp")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.description.setFont(font)
        self.description.setText("Insert the name of the city:")
        self.button2.hide()
        self.line_edit.clear()
        self.line_edit.show()
        self.button.show()

    # Changing the window to the error mode
    # (appears after inserting the incorrect city name and confirming it with button press)
    def change_to_error(self):
        self.main_label.setText("Error!")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        self.description.setFont(font)
        self.description.setText("")
        self.line_edit.hide()
        self.button.hide()
        self.button2.show()


# Calling the main method
if __name__ == '__main__':
    main()
