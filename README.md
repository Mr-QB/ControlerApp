## Mô tả Dự án: Truyền Tín Hiệu từ Analog Stick qua Socket
### Tổng Quan
Dự án này nhằm phát triển một ứng dụng để truyền tín hiệu từ 2 cần điều khiển analog thông qua một cổng socket tới một ứng dụng Android. Ứng dụng trên máy tính sẽ được phát triển bằng Python với giao diện PyQt, trong khi ứng dụng Android sẽ được phát triển bằng Kotlin.

### Các Thành Phần
#### Ứng dụng Trên Máy Tính (Python + PyQt)
* Ngôn Ngữ: Python
* Source: [Tại đây](PythonApp/main.py)
* Framework GUI: PyQt
* Chức Năng:
    * Đọc tín hiệu từ 2 cần điều khiển analog.
    * Hiển thị trực quan dữ liệu từ 2 cần điều khiển.
    * Thiết lập kết nối socket.
    * Truyền tín hiệu qua cổng socket.
* Triển khai:
    * Cập nhật các thư viện:
    ```pip install PythonApp\requirements.txt```
    * Chạy Python source: ```python3 PythonApp/main.py```
* Demo:

![Demo Python App](https://github.com/Mr-QB/ControlerApp/blob/main/VideoDemo/PythonApp.gif)

#### Ứng dụng Android (Kotlin)
* Source: [Tại đây](AndroidApp\app\src\main\java\com\example\controlerapp\MainActivity.kt)
* Ngôn Ngữ: Kotlin
* Chức Năng:
    * Kết nối tới cổng socket.
    * Nhận tín hiệu từ ứng dụng máy tính.
    * Xử lý và diễn giải các tín hiệu nhận được.
    * Hiển thị các tínJ hiệu nhận được.
* Demo:

![Demo Android App](https://github.com/Mr-QB/ControlerApp/blob/main/VideoDemo/AndroidApp.gif)

