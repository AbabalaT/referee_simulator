from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
import sys
import cv2

points = []
key4send = 0
location = [0, 0]

map_img = cv2.imread('map.png')
cv2.cvtColor(map_img, cv2.COLOR_BGR2RGB, map_img)
map_height, map_width, map_bytesPerComponent = map_img.shape

def getPos(event):
    x = event.pos().x()
    y = event.pos().y()
    if event.buttons() == Qt.LeftButton:
        global location
        location = [x, y]
    elif event.buttons() == Qt.RightButton:
        points.append([x, y])
    ui.refresh_img()

def SendRoute():
    global points

    print('发送哨兵路径！')
    ui.refresh_img()

class Ui(object):
    def refresh_img(self):
        image = map_img.copy()
        if location != [0, 0]:
            cv2.rectangle(image, (location[0] - 8, location[1] - 8), (location[0] + 8, location[1] + 8), (0, 255, 0),
                          -1)
        if len(points) > 0:
            for [px, py] in points:
                cv2.circle(image, (px, py), 8, (255, 125, 0), -1)
            if len(points) > 1:
                for i in range(1, len(points)):
                    cv2.line(image, tuple(points[i - 1]), tuple(points[i]), (255, 125, 0), 3)
        map_QImg = QImage(image.data, map_width, map_height, 3 * map_width, QImage.Format_RGB888)
        map_pixmap = QPixmap.fromImage(map_QImg)
        self.image.setPixmap(map_pixmap)

    def ClearRoute(self):
        global points
        points = []
        print('清除哨兵路径！')
        ui.refresh_img()

    def DeletePoint(self):
        if len(points) > 0:
            points.pop()
        ui.refresh_img()

    def SendLocation(self):
        print('发送 按键+坐标！')

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.key1 = QtWidgets.QPushButton(self.centralwidget)
        self.key1.setGeometry(QtCore.QRect(950, 0, 100, 60))
        self.key1.setObjectName("key1")
        self.key1.clicked.connect(self.ClearRoute)
        self.key2 = QtWidgets.QPushButton(self.centralwidget)
        self.key2.setGeometry(QtCore.QRect(950, 75, 100, 60))
        self.key2.setObjectName("key2")
        self.key2.clicked.connect(self.DeletePoint)
        self.key3 = QtWidgets.QPushButton(self.centralwidget)
        self.key3.setGeometry(QtCore.QRect(950, 150, 100, 60))
        self.key3.setObjectName("key3")
        self.key3.clicked.connect(SendRoute)
        self.key4 = QtWidgets.QPushButton(self.centralwidget)
        self.key4.setGeometry(QtCore.QRect(925, 290, 150, 60))
        self.key4.setObjectName("key4")
        self.key4.clicked.connect(self.SendLocation)

        self.preview = QtWidgets.QLabel(self.centralwidget)
        self.preview.setGeometry(QtCore.QRect(900, 220, 200, 60))
        self.preview.setLayoutDirection(Qt.LeftToRight)
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setObjectName("preview")

        self.note = QtWidgets.QLabel(self.centralwidget)
        self.note.setGeometry(QtCore.QRect(10, 480, 800, 50))
        self.note.setObjectName("note")

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(0, 0, 865, 468))
        self.image.setObjectName("image")
        self.image.mousePressEvent = getPos
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1045, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.key1, self.key2)
        MainWindow.setTabOrder(self.key2, self.key3)
        MainWindow.setTabOrder(self.key3, self.key4)
        MainWindow.setTabOrder(self.key4, self.key1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "云台手GUI"))
        self.key3.setText(_translate("MainWindow", "发送哨兵路径"))
        self.key1.setText(_translate("MainWindow", "清除哨兵路径"))
        self.preview.setText(_translate("MainWindow", '按键预览：' + '无'))
        self.key4.setText(_translate("MainWindow", "发送 按键+坐标"))
        self.note.setText(_translate("MainWindow", "左键：选取坐标点    右键：添加哨兵路径点"))
        self.key2.setText(_translate("MainWindow", "删除最后一点"))


class MainWindow(QMainWindow, Ui):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # 初始化父类属性
        self.setupUi(self)

    def keyPressEvent(self, QKeyEvent):
        if Qt.Key_A <= QKeyEvent.key() <= Qt.Key_Z:
            key4send = QKeyEvent.key()
            note1 = ''
            if key4send == Qt.Key_A:
                note1 = '（攻打）'
            elif key4send == Qt.Key_B:
                note1 = '（防守）'
            elif key4send == Qt.Key_C:
                note1 = '（待命）'
            elif key4send == Qt.Key_D:
                note1 = '（修正定位）'
            elif key4send == Qt.Key_E:
                note1 = '（开陀螺）'
            elif key4send == Qt.Key_F:
                note1 = '（关陀螺）'
            elif key4send == Qt.Key_G:
                note1 = '（开游走）'
            elif key4send == Qt.Key_H:
                note1 = '（关游走）'
            ui.preview.setText('按键预览：' + chr(key4send) + note1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ui.refresh_img()
    sys.exit(app.exec_())
