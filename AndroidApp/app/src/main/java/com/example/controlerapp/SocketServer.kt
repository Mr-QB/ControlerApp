import com.elvishew.xlog.LogLevel
import com.elvishew.xlog.XLog
import org.json.JSONObject
import java.io.BufferedReader
import java.io.DataOutputStream
import java.io.InputStreamReader
import java.io.ObjectOutputStream
import java.io.PrintWriter
import java.net.ServerSocket
import java.net.Socket
import java.net.SocketException

class SocketServer(private val host: String, private val port: Int) {
    private var serverSocket: ServerSocket? = null
    private var isRunning = false
    public var receivedData: String? = null

    //    public var receivedData: String? = null
    init {
        XLog.init(LogLevel.ALL)
        startServer()
    }

    private fun startServer() {
        Thread {
            try {
                serverSocket = ServerSocket(port, 50, java.net.InetAddress.getByName(host))
                println("Server is running on host: $host and port: $port")

                isRunning = true

                while (isRunning) {
                    val clientSocket = serverSocket?.accept()
                    handleClientConnection(clientSocket)
                }
            } catch (e: Exception) {
                XLog.tag("Socket_Server")
                    .e("An error occurred while starting the server: ${e.message}")
            }
        }.start()
    }

    public fun stopServer() {
        isRunning = false
        serverSocket?.close()
    }

    private fun handleClientConnection(clientSocket: Socket?) {
        Thread {
            try {
                // Initialize reader and writer for communication with client
                val reader = BufferedReader(InputStreamReader(clientSocket?.getInputStream()))
                val writer = DataOutputStream(clientSocket?.getOutputStream())

                // Initialize reader and writer for communication with client
                writer.writeUTF("Already connected")
                writer.flush()

                while (true) {

                    receivedData = reader.readLine() // Read data sent by client
                    if (receivedData == null) break // If end of stream is reached, break the loop
                    XLog.tag("Socket_Server").d("Received data: $receivedData")

                    // Send response back to client
                    writer.writeUTF("Message received by server!")
                    writer.flush()
                    XLog.tag("Socket_Server").d("Sent response: Response sent successfully.")
                }
                clientSocket?.close()
            } catch (e: SocketException) { // Handle socket exception
                if (e.message == "Connection reset") {
                    XLog.tag("Socket_Server").e("Connection reset: ${e.message}")
                } else {
                    XLog.tag("Socket_Server").e("SocketException: ${e.message}")
                }
            } catch (e: Exception) { // Handle other exceptions
                XLog.tag("Socket_Server").e("Error handling client connection: ${e.message}")
            }
        }.start()
    }
}

