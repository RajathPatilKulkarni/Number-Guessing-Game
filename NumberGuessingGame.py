import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QRect, QEasingCurve
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QPropertyAnimation


class NumberGuessingGame(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.target_number = random.randint(1, 100)
        self.attempts = 0

    def initUI(self):
        self.setWindowTitle('Number Guessing Game')
        self.resize(400, 300)  # Set the window size to 400x300 pixels

        # Set dark background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.ColorRole.WindowText, QColor(30, 30, 30))  # Darker background
        self.setPalette(palette)

        self.layout = QVBoxLayout()

        # Styling the label
        self.label = QLabel('Guess a number between 1 and 100', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text in the label
        self.label.setFont(QFont('Arial', 18))  # Set font size to 18
        self.label.setStyleSheet("QLabel { color: #FFFFFF; }")  # White text color
        self.layout.addWidget(self.label)

        # Styling the input
        self.input = QLineEdit(self)
        self.input.setFont(QFont('Arial', 14))
        self.input.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.2); color: #FFFFFF; border: 2px solid #FFD700; border-radius: 10px; padding: 5px;")
        self.layout.addWidget(self.input)

        # Styling the button
        self.button = QPushButton('Submit Guess', self)
        self.button.setFont(QFont('Arial', 16))  # Increase font size for larger button text
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #4A148C; /* Darker purple */
                color: #FFD700; /* Gold */
                border-radius: 20px;
                border: 2px solid #FFD700;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #6A0DAD; /* Purple */
                color: #FFD700; /* Gold */
            }
        """)
        self.button.clicked.connect(self.check_guess)
        self.layout.addWidget(self.button)

        # Add attempt counter
        self.attempt_label = QLabel('Attempts: 0', self)
        self.attempt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.attempt_label.setFont(QFont('Arial', 14))
        self.attempt_label.setStyleSheet("QLabel { color: #FFFFFF; }")
        self.layout.addWidget(self.attempt_label)

        self.setLayout(self.layout)

    def check_guess(self):
        guess = self.input.text()

        if not guess.isdigit():
            QMessageBox.warning(self, 'Error', 'Please enter a valid number')
            return

        guess = int(guess)
        self.attempts += 1
        self.attempt_label.setText(f'Attempts: {self.attempts}')

        if guess < self.target_number:
            self.feedback_animation('Too low! Try again.', 'red')
        elif guess > self.target_number:
            self.feedback_animation('Too high! Try again.', 'red')
        else:
            self.feedback_animation(f'Correct! You guessed it in {self.attempts} attempts.', 'green')
            self.reset_game()

    def feedback_animation(self, message, color):
        self.label.setText(message)
        self.label.setStyleSheet(f"QLabel {{ color: {color}; }}")
        animation = QPropertyAnimation(self.label, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(self.label.x(), self.label.y(), self.label.width(), self.label.height()))
        animation.setEndValue(QRect(self.label.x(), self.label.y() - 10, self.label.width(), self.label.height()))
        animation.setLoopCount(3)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        animation.start()

    def reset_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.input.clear()
        self.attempt_label.setText('Attempts: 0')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = NumberGuessingGame()
    game.show()
    sys.exit(app.exec())
