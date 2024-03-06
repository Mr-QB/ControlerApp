import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsTextItem
from PyQt5.QtCore import Qt, QTimer, QRectF, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
import pygame
from DataSocket import *
import threading


class PaintThread(QThread):
    paintEventSignal = pyqtSignal()
    def run(self):
        while True:
            self.paintEventSignal.emit()
            self.msleep(30)  # Delay for 30 milliseconds

class PS3ControllerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.initPS3Controller()

        self.host = "192.168.1.6"
        self.port = 12345

        self.axes = [0.0, 0.0, 0.0, 0.0]
        self.bumperButtonStates = [0.0, 0.0]

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle('PS3 Controller')
        self.center()

        # Create an instance of the PaintThread
        self.paintThread = PaintThread()
        self.paintThread.paintEventSignal.connect(self.updateEvent)

        # Start the thread
        self.paintThread.start()

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

    def updateEventJoystick(self):
        self.axes = [self.joystick.get_axis(i) for i in
                     range(self.joystick.get_numaxes())]  # Update the status of joystick axes
        self.bumperButtonStates[0] = self.joystick.get_button(4)  # Status of Left Bumper
        self.bumperButtonStates[1] = self.joystick.get_button(5)  # Status of Right Bumper

    def drawSquare(self, painter, square_position, square_size, square_text, square_intensity):
        x, y = square_position
        w, h = square_size

        # Calculate color based on lightness
        gray = 255 - int(255 * square_intensity)
        color = QColor(gray, gray, gray)
        painter.setBrush(color)
        painter.drawRect(x, y, w, h)

        # Draw text inside the square
        text_font = QFont("Arial", 12)
        text_width = painter.fontMetrics().boundingRect(square_text).width() * 2  # Measure the size of the text
        text_height = painter.fontMetrics().boundingRect(square_text).height() * 2
        text_x = x + (w - text_width) / 2  # Calculate the position to center the text
        text_y = y + (h - text_height) / 2
        painter.setFont(text_font)
        painter.setPen(QColor(98, 192, 133))  # Set text color based on background intensity
        painter.drawText(text_x, text_y, text_width, text_height, Qt.AlignCenter, square_text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Update position based on Axes & button status
        self.updateEventJoystick()

        # Send the data stored in self.axes to the connected client through the data socket.
        self.sentDataToSocket(self.axes + self.bumperButtonStates)
        self.print_thread_count() # Check thread

        self.drawSquare(painter, (self.width() * 1 / 7, self.height() * 2 / 8), (60, 30), "L1",
                        self.bumperButtonStates[0])  # Draw the first square - L1
        self.drawSquare(painter, (self.width() * 2 / 7, self.height() * 2 / 8), (60, 30), "L2",
                        self.axes[4])  # Draw the second square - L2
        self.drawSquare(painter, (self.width() * 4.7 / 7, self.height() * 2 / 8), (60, 30), "R1",
                        self.bumperButtonStates[1])  # Draw the third square - R1
        self.drawSquare(painter, (self.width() * 5.5 / 7, self.height() * 2 / 8), (60, 30), "R2",
                        self.axes[5])  # Draw the fourth square - R2

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

        # self.drawSquare(painter, square_position, square_size, square_text, square_intensity)

    def print_thread_count(self):
        thread_count = threading.active_count()
        print(f"Current number of threads: {thread_count}")

    def sentDataToSocket(self, data):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
                client_socket.connect((self.host, self.port))  # Connect to the server
                data_str = json.dumps(data)  # Convert to json
                client_socket.sendall(data_str.encode())  # Send data
                client_socket.close()  # Close the connection
            except Exception as e:
                print(f"An error occurred while sending data: {e}")

    def updateEvent(self):
        self.update()