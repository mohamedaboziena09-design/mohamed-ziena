import sys
from PyQt5.QtWidgets import QApplication
from gui import HRApp


def main():
    app = QApplication(sys.argv)
    win = HRApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
