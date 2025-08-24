from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import ctypes
from ctypes import windll, byref, sizeof, c_int, c_uint

class BlurInputDialog(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.result = None  # Store input or None on cancel

        # Frameless, always-on-top, translucent
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(300, 70)

        # Rounded corners using a mask
        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, 300, 70, 30, 30)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)  # Padding

        self.input = QtWidgets.QLineEdit(self)
        self.input.setPlaceholderText("Folder Name ")
        self.input.setFont(QtGui.QFont("Arial", 24))
        self.input.setStyleSheet("QLineEdit { padding-left: 10px; padding-right: 10px; }")
        layout.addWidget(self.input)

        self.input.returnPressed.connect(self.on_enter)

        # Enable Windows blur effect (uncomment next line if you want blur)
        # self.enable_blur()

    def showEvent(self, event): # type: ignore
        # Guarantee focus when shown
        self.activateWindow()
        self.raise_()
        self.input.setFocus()
        super().showEvent(event)

    def enable_blur(self):
        # Windows-specific blur behind effect (Windows 10/11)
        try:
            hwnd = self.winId().__int__()

            class ACCENTPOLICY(ctypes.Structure):
                _fields_ = [("AccentState", c_int),
                            ("AccentFlags", c_int),
                            ("GradientColor", c_uint),
                            ("AnimationId", c_int)]

            accent = ACCENTPOLICY()
            accent.AccentState = 3  # ACCENT_ENABLE_BLURBEHIND
            accent.GradientColor = 0x00ffffff  # Transparent white

            class WINCOMPATTRDATA(ctypes.Structure):
                _fields_ = [("Attribute", c_int),
                            ("Data", ctypes.POINTER(ACCENTPOLICY)),
                            ("SizeOfData", c_int)]

            data = WINCOMPATTRDATA()
            data.Attribute = 19  # WCA_ACCENT_POLICY
            data.Data = byref(accent)
            data.SizeOfData = sizeof(accent)

            windll.user32.SetWindowCompositionAttribute(hwnd, byref(data))
        except Exception as e:
            print("Blur not supported:", e)

    def keyPressEvent(self, event):  # type: ignore
        # ESC cancels and closes
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.result = None
            self.close()
        else:
            super().keyPressEvent(event)

    def on_enter(self):
        self.result = self.input.text()
        self.close()

def get_input():
    app = QtWidgets.QApplication(sys.argv)
    dialog = BlurInputDialog()
    dialog.show()
    app.exec()
    return dialog.result

if __name__ == "__main__":
    result = get_input()
    print(result)
