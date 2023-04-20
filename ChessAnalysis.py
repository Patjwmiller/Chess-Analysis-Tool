import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
from PyQt5.QtGui import QPalette, QColor


class ChessAnalyzer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.label = QtWidgets.QLabel("Paste your chess board element:")
        self.textbox = QtWidgets.QTextEdit(self)
        self.button = QtWidgets.QPushButton("Analyze", self)
        self.button.setStyleSheet("QPushButton {"
                           "background-color: rgb(79, 84, 92);"
                           "border-radius: 4px;"
                           "padding: 8px;"
                           "color: rgb(255, 255, 255);"
                           "font-size: 14px;"
                           "font-weight: bold;"
                           "}"
                           "QPushButton:hover {"
                           "background-color: rgb(97, 102, 110);"
                           "}"
                           "QPushButton:pressed {"
                           "background-color: rgb(48, 51, 56);"
                           "}")
        self.label.setStyleSheet("color: #D1D5DB;")
        self.button.clicked.connect(self.get_fen)
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.webview.load(QtCore.QUrl("about:blank"))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        layout.addWidget(self.webview)
        self.setLayout(layout)

        self.setWindowTitle("Chess Analysis Tool")
        self.setGeometry(100, 100, 800, 600)

        # Set window to be topmost
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(54, 57, 63))  # Set the background color
        palette.setColor(QPalette.Button, QColor(79, 84, 92))  # Set the button color
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # Set the button text color
        palette.setColor(QPalette.Base, QColor(35, 39, 42))  # Set the text box background color
        palette.setColor(QPalette.Text, QColor(255, 255, 255))  # Set the text color
        self.setPalette(palette)


    def on_error(self, error):
        QtWidgets.QMessageBox.critical(self, "Error", error)

    def get_fen(self):
        clipboard_text = self.clipboard.text()
        if "chess-board" not in clipboard_text:
            self.on_error("Clipboard does not contain a valid chess board")
            return

        pos = clipboard_text.find("piece")
        board = []
        for i in range(8):
            board.append(['0'] * 8)

        if '<text x="0.75" y="90.75" font-size="2.8" class="coordinate-dark">1</text>' in clipboard_text:
            side = 'w'
        else:
            side = 'b'

        while pos != -1:
            piece = clipboard_text[pos+6:pos+8]
            if not clipboard_text[pos+17].isdigit():
                pos = clipboard_text.find("piece", pos+5)
                continue
            x = int(clipboard_text[pos+16]) - 1
            y = 8 - int(clipboard_text[pos+17])
            board[y][x] = piece
            clipboard_text = clipboard_text[pos+5:]
            pos = clipboard_text.find("piece")

        fen = ''
        for row in board:
            empty_count = 0
            for piece in row:
                if piece == '0':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    if piece[0] == 'b':
                        fen += piece[1]
                    else:
                        fen += piece[1].upper()
            if empty_count > 0:
                fen += str(empty_count)
            fen += '/'
        fen = fen[:-1]

        url = QtCore.QUrl(f"https://lichess.org/analysis/fromPosition/{fen}_{side}")
        self.webview.load(url)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    analyzer = ChessAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())
