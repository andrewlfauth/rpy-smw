from download import download_hack, get_hack_url_by_title
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
import sys

def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load('main.qml')

    sys.exit(app.exec())

main()