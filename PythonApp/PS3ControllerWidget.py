import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
import pygame
from DataSocket import *
import threading


class PS3ControllerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.initPS3Controller()

        self.host = "192.168.1.6"
        self.port = 12345

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle('PS3 Controller')
        self.center()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(25)  # Update every 50 milliseconds

        self.axes = [0.0, 0.0, 0.0, 0.0]
        self.radius = 100

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screenGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initPS3Controller(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print("No joystick detected.")
            return
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def drawColumnChart(self, painter, value, x_position, y_position, chart_name):
        bar_width = 10
        bar_height = (self.radius) * abs(value) / 2

        # Draw center divider
        painter.setPen(Qt.black)
        painter.drawLine(x_position - bar_width / 2, y_position, x_position + bar_width / 2, y_position)

        # Draw bar above center divider if value is positive, otherwise draw below
        if value >= 0:
            painter.setBrush(QColor(0, 0, 255, 127))  # Blue color for positive value
            painter.drawRect(x_position - bar_width / 2, -bar_height, bar_width, bar_height)
        else:
            painter.setBrush(QColor(0, 255, 0, 127))  # Green color for negative value
            painter.drawRect(x_position - bar_width / 2, 0, bar_width, bar_height)

        # Set font for chart name
        font = QFont("Arial", 9)  # Example: Arial, 12px, Bold
        painter.setFont(font)

        
        if value < 0:
            painter.drawText(x_position - bar_width / 2 - 11, bar_height, 35, 10, Qt.AlignCenter, chart_name)
        else:
            painter.drawText(x_position - bar_width / 2 - 11, -bar_height - 15, 35, 10, Qt.AlignCenter, chart_name)

    def drawCircle(self, painter, circle_position, circle_color, point_position):
        # Draw circle
        painter.translate(circle_position[0], circle_position[1])
        painter.setPen(Qt.NoPen)
        painter.setBrush(circle_color)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

        # Draw the first diameter
        painter.setPen(QColor(255, 255, 255))  # Color of the first diameter
        painter.drawLine(-self.radius, 0, self.radius, 0)
        # Draw the second diameter
        painter.setPen(QColor(255, 255, 255))  # Color of the second diameter
        painter.drawLine(0, -self.radius, 0, self.radius)

        # Draw point
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.blue)
        painter.drawEllipse(point_position[0] - 5, point_position[1] - 5, 10, 10)

        # Draw line from circle center to point
        painter.setPen(QPen(QColor(56, 56, 56)))
        painter.drawLine(point_position[0], point_position[1], 0, 0)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Update position based on Axes
        self.axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]

        # Send the data stored in self.axes to the connected client through the data socket.
        self.sentDataToSocket(self.axes)

        # Draw first circle
        circle_position = (self.width() / 4, self.height() / 2)
        circle_color = QColor(255, 0, 0, 127)
        point_position = [self.radius * self.axes[0], self.radius * self.axes[1]]
        self.drawCircle(painter, circle_position, circle_color, point_position)

        x_position = circle_position[0]  # Set initial x position of the column chart
        gap = 40  # Gap distance between columns
        self.drawColumnChart(painter, self.axes[0], x_position - gap * 1.5, 0, "Axes 0")
        self.drawColumnChart(painter, self.axes[1], x_position - gap / 2, 0, "Axes 1")
        self.drawColumnChart(painter, self.axes[2], x_position + gap / 2, 0, "Axes 2")
        self.drawColumnChart(painter, self.axes[3], x_position + gap * 1.5, 0, "Axes 3")

        # Draw second circle
        circle_position = (self.width() / 2, 0)
        circle_color = QColor(0, 0, 255, 127)
        point_position = (self.radius * self.axes[2], self.radius * self.axes[3])
        self.drawCircle(painter, circle_position, circle_color, point_position)

    def sentDataToSocket(self, data):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
            client_socket.connect((self.host, self.port))  # Connect to the server
            data_str = json.dumps(data)  # Convert to json
            client_socket.sendall(data_str.encode())  # Send data
            # # Receive response (if any)
            # try:
            #     response = client_socket.recv(1024)
            #     print(f"Received response from server: {response.decode()}")
            # except socket.timeout:
            #     print("Timeout occurred while receiving response from server.")
            client_socket.close()  # Close the connection
        except Exception as e:
            print(f"An error occurred while sending data: {e}")