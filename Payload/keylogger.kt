import java.awt.event.KeyEvent
import java.awt.event.KeyListener
import javax.swing.JFrame
import javax.swing.JTextArea

class KeyLogger : JFrame(), KeyListener {
    private val textArea = JTextArea()

    init {
        title = "Keylogger"
        setSize(400, 400)
        defaultCloseOperation = EXIT_ON_CLOSE
        add(textArea)
        addKeyListener(this)
        isVisible = true
    }

    override fun keyTyped(e: KeyEvent) {
        textArea.append(e.keyChar.toString())
    }

    override fun keyPressed(e: KeyEvent) {
        // No action needed
    }

    override fun keyReleased(e: KeyEvent) {
        // No action needed
    }
}

fun main() {
    KeyLogger()
}
