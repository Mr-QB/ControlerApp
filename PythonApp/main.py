from PS3ControllerWidget import *
def main():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ps3Widget = PS3ControllerWidget()
    mainWindow.setCentralWidget(ps3Widget)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()