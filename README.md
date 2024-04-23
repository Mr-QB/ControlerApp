## Project Description: Signal Transmission from Analog Stick via Socket
### Overview
This project aims to develop an application to transmit signals from 2 analog control sticks through a socket port to an Android application. The computer application will be developed using Python with PyQt interface, while the Android application will be developed using Kotlin.

### Components
#### Computer Application (Python + PyQt)
* Language: Python
* Source: [Here](PythonApp/main.py)
* GUI Framework: PyQt
* Features:
    * Read signals from 2 analog control sticks.
    * Visually display data from 2 analog control sticks.
    * Establish socket connection.
    * Transmit signals through the socket port.
* Deployment:
    * Update libraries:
    ```pip install -r PythonApp\requirements.txt```
    * Run Python source: ```python3 PythonApp/main.py```
* Demo:

![Demo Python App](https://github.com/Mr-QB/ControlerApp/blob/main/VideoDemo/PythonApp.gif)

#### Android Application (Kotlin)
* Source: [Here](AndroidApp\app\src\main\java\com\example\controlerapp\MainActivity.kt)
* Language: Kotlin
* Features:
    * Connect to the socket port.
    * Receive signals from the computer application.
    * Process and interpret received signals.
    * Display received signals.
* Demo:

![Demo Android App](https://github.com/Mr-QB/ControlerApp/blob/main/VideoDemo/AndroidApp.gif)
