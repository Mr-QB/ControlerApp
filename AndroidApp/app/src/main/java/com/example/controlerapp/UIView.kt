import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.view.View
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.elvishew.xlog.XLog
import org.json.JSONArray

class UIView(context: Context) : View(context) {
    private val socketServer = SocketServer("192.168.1.6", 12345)
    private val paint = Paint()

    data class Data(val values: List<Double?>)

    var centerFirstCirclePositionX: Float = 0f
    var centerFirstCirclePositionY: Float = 0f
    var firstRadius: Float = 0f
//    private var pointX: Float = 0f
//    private var pointY: Float = 0f

    var axesData by mutableStateOf(Data(listOf(0.0, 1.0, 3.0, 4.0, 5.0, 6.0)))


    init {
        paint.style = Paint.Style.FILL

        updatePositionPoint()
    }

    private fun updatePositionPoint() {
        // Function to get axis values from received data
        fun extractAxesValues(data: String): UIView.Data {
            try {
                // Convert JSON data to JSON array
                val jsonArray = JSONArray(data)
                val axes = mutableListOf<Double>()
                for (i in 0 until jsonArray.length()) {
                    axes.add(jsonArray.getDouble(i))
                }
                return UIView.Data(axes) // Returns data with extracted axis values
            } catch (e: Exception) {
                e.printStackTrace()
            }
            return UIView.Data(listOf(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        }

        val threadUpdatePositionPoint = Thread {
            while (true) { // Infinite loop to update data from socket port
                val newData = socketServer.receivedData // Get new data from port port
                if (newData != null) { // Check if there is new data
                    axesData = extractAxesValues(newData)
                    postInvalidate() // Redraw CircleView
                    XLog.tag("UIView").d(axesData)
                }
            }
        }
        threadUpdatePositionPoint.start()
    }

    private val linePaint = Paint().apply {
        color = Color.rgb(255, 255, 255)
        strokeWidth = 1f // Width of diameter
    }

    private fun drawCircle(
        canvas: Canvas,
        centerX: Float,
        centerY: Float,
        radius: Float,
        axesX: Float,
        axesY: Float,
        circleColor: Int
    ) {
        centerFirstCirclePositionX = centerX
        centerFirstCirclePositionY = centerY
        firstRadius = radius

        paint.color = circleColor // Set the color of the circle

        canvas.drawCircle(centerX, centerY, radius, paint)

        canvas.drawLine(
            centerX - radius,
            centerY,
            centerX + radius,
            centerY,
            linePaint
        ) // Draw the vertical diameter

        canvas.drawLine(
            centerX,
            centerY - radius,
            centerX,
            centerY + radius,
            linePaint
        ) // Draw the horizontal diameter

        // Calculate the coordinates of the point based on the data from axesData and draw a circle at that point
        val pointX = centerX + radius * axesX
        val pointY = centerY + radius * axesY
        paint.color = Color.BLUE
        canvas.drawCircle(pointX, pointY, 10f, paint)

        // Draw a line from the center of the circle to the computed point
        paint.color = Color.BLACK
        canvas.drawLine(centerX, centerY, pointX, pointY, paint)
    }

    fun drawColumnChart(
        canvas: Canvas,
        value: Float,
        xPosition: Float,
        yPosition: Float,
        chartName: String
    ) {
        val barWidth = 20f
        val barHeight = 200f * Math.abs(value) / 2

        // Draw center divider
        paint.color = Color.BLACK
        canvas.drawLine(
            xPosition - barWidth / 2,
            yPosition,
            xPosition + barWidth / 2,
            yPosition,
            paint
        )

        // Draw bar above center divider if value is positive, otherwise draw below
        if (value >= 0) {
            paint.color = Color.argb(127, 0, 0, 255) // Blue color for positive value
            canvas.drawRect(
                xPosition - barWidth / 2,
                yPosition - barHeight,
                xPosition + barWidth / 2,
                yPosition,
                paint
            )
        } else {
            paint.color = Color.argb(127, 0, 255, 0) // Green color for negative value
            canvas.drawRect(
                xPosition - barWidth / 2,
                yPosition,
                xPosition + barWidth / 2,
                yPosition + barHeight,
                paint
            )
        }

        // Set font for chart name
        val font = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        paint.typeface = font
        paint.textSize = 20f

        // Draw chart name
        val textWidth = paint.measureText(chartName)
        if (value < 0) {
            canvas.drawText(
                chartName,
                xPosition - barWidth / 2 - textWidth / 1.5f,
                yPosition + barHeight + 15,
                paint
            )
        } else {
            canvas.drawText(
                chartName,
                xPosition - barWidth / 2 - textWidth / 1.5f,
                yPosition - barHeight,
                paint
            )
        }
    }

    fun drawSquare(
        canvas: Canvas,
        squarePosition: Pair<Float, Float>,
        squareSize: Pair<Float, Float>,
        squareText: String,
        squareIntensity: Float
    ) {
        val (x, y) = squarePosition
        val (w, h) = squareSize

        // Calculate color based on intensity
        val gray = 255 - (255 * squareIntensity).toInt()
        val color = Color.rgb(gray, gray, gray)
        paint.color = color

        // Draw square
        canvas.drawRect(x, y, x + w, y + h, paint)

        // Draw border
        paint.color = Color.rgb(98, 192, 133)
        paint.strokeWidth = 2f
        paint.style = Paint.Style.STROKE
        canvas.drawRect(x, y, x + w, y + h, paint)

        // Set up text
        paint.color = Color.rgb(98, 192, 133) // Set text color
        paint.textSize = 24f // Set text size
        paint.textAlign = Paint.Align.CENTER // Set text alignment to center
        paint.style = Paint.Style.FILL

        // Calculate text position
        val textX = x + w / 2
        val textY = y + h / 2 - (paint.descent() + paint.ascent()) / 2 // Adjust text baseline

        // Draw text
        canvas.drawText(squareText, textX, textY, paint)
    }


    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        val circleRadius = Math.min(width, height) / 4f


        drawSquare( // Draw the first square - L1
            canvas,
            Pair(width * 1 / 7f, height * 1 / 7f),
            Pair(100f, 60f),
            "L1",
            (axesData.values.getOrNull(6)?.toFloat() ?: 0f)
        )
        drawSquare( // Draw the second square - L2
            canvas,
            Pair(width * 2 / 7f, height * 1 / 7f),
            Pair(100f, 60f),
            "L2",
            (axesData.values.getOrNull(4)?.toFloat() ?: 0f)
        )
        drawSquare( // Draw the third square - R1
            canvas,
            Pair(width * 5 / 7f, height * 1 / 7f),
            Pair(100f, 60f),
            "L1",
            (axesData.values.getOrNull(7)?.toFloat() ?: 0f)
        )
        drawSquare( // Draw the fourth square - R2
            canvas,
            Pair(width * 6 / 7f, height * 1 / 7f),
            Pair(100f, 60f),
            "L2",
            (axesData.values.getOrNull(5)?.toFloat() ?: 0f)
        )


        val firstCircleColor = Color.argb(127, 255, 0, 0)
        drawCircle(
            canvas,
            width / 4f,
            height / 2f,
            circleRadius,
            (axesData.values.getOrNull(0)?.toFloat() ?: 0f),
            (axesData.values.getOrNull(1)?.toFloat() ?: 0f),
            firstCircleColor
        )

        val secondCircleColor = Color.argb(127, 0, 0, 255)
        drawCircle(
            canvas,
            width * 3 / 4f,
            height / 2f,
            circleRadius,
            (axesData.values.getOrNull(2)?.toFloat() ?: 0f),
            (axesData.values.getOrNull(3)?.toFloat() ?: 0f),
            secondCircleColor
        )

        val chart1Value = (axesData.values.getOrNull(0)?.toFloat() ?: 0f)
        val chart2Value = (axesData.values.getOrNull(1)?.toFloat() ?: 0f)
        val chart3Value = (axesData.values.getOrNull(2)?.toFloat() ?: 0f)
        val chart4Value = (axesData.values.getOrNull(3)?.toFloat() ?: 0f)
        val gap = 100  // Gap distance between columns
        drawColumnChart(
            canvas,
            chart1Value,
            width / 2f - gap * 1.5f,
            height / 2f,
            "Axes 0"
        )
        drawColumnChart(
            canvas,
            chart2Value,
            width / 2f - gap / 2f,
            height / 2f,
            "Axes 1"
        )
        drawColumnChart(
            canvas,
            chart3Value,
            width / 2f + gap / 2f,
            height / 2f,
            "Axes 2"
        )
        drawColumnChart(
            canvas,
            chart4Value,
            width / 2f + gap * 1.5f,
            height / 2f,
            "Axes 3"
        )
    }
}