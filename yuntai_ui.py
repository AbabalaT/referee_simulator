from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

class Ui(object):
    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if event.buttons() == QtCore.Qt.LeftButton:
            print(x, y, '左键')
        elif event.buttons() == QtCore.Qt.RightButton:
            print(x, y, '右键')

    def SendRoute(self):
        print('发送哨兵路径！')

    def ClearRoute(self):
        print('清除哨兵路径！')

    def DeletePoint(self):
        print('删除路径点！')

    def SendLocation(self):
        print('发送 按键+坐标！')

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.key1 = QtWidgets.QPushButton(self.centralwidget)
        self.key1.setGeometry(QtCore.QRect(900, 0, 100, 60))
        self.key1.setObjectName("key1")
        self.key1.clicked.connect(self.ClearRoute)
        self.key2 = QtWidgets.QPushButton(self.centralwidget)
        self.key2.setGeometry(QtCore.QRect(900, 75, 100, 60))
        self.key2.setObjectName("key2")
        self.key2.clicked.connect(self.DeletePoint)
        self.key3 = QtWidgets.QPushButton(self.centralwidget)
        self.key3.setGeometry(QtCore.QRect(900, 150, 100, 60))
        self.key3.setObjectName("key3")
        self.key3.clicked.connect(self.SendRoute)
        self.key4 = QtWidgets.QPushButton(self.centralwidget)
        self.key4.setGeometry(QtCore.QRect(880, 290, 150, 60))
        self.key4.setObjectName("key4")
        self.key4.clicked.connect(self.SendLocation)

        self.preview = QtWidgets.QLabel(self.centralwidget)
        self.preview.setGeometry(QtCore.QRect(870, 220, 150, 60))
        self.preview.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.preview.setAlignment(QtCore.Qt.AlignCenter)
        self.preview.setObjectName("preview")

        self.note = QtWidgets.QLabel(self.centralwidget)
        self.note.setGeometry(QtCore.QRect(10, 480, 800, 50))
        self.note.setObjectName("note")

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(0, 0, 865, 468))
        self.image.setObjectName("image")
        self.image.mousePressEvent = self.getPos
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

        # self.key1.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.key2.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.key3.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.key4.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.image.setFocusPolicy(QtCore.Qt.NoFocus)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "云台手GUI"))
        self.key3.setText(_translate("MainWindow", "发送哨兵路径"))
        self.key1.setText(_translate("MainWindow", "清除哨兵路径"))
        self.preview.setText(_translate("MainWindow", "按键预览:无"))
        self.key4.setText(_translate("MainWindow", "发送 按键+坐标"))
        self.note.setText(_translate("MainWindow", "左键：选取坐标点    右键：添加哨兵路径点"))
        self.key2.setText(_translate("MainWindow", "删除最后一点"))

class MainWindow(QMainWindow, Ui):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # 初始化父类属性
        self.setupUi(self)

    def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
        if QKeyEvent.key() == Qt.Key_C:  # 判断是否按下了A键
            # key()  是普通键
            print('按下了C键')

if __name__=="__main__":
    import sys, cv2
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    map_img = cv2.imread('map.png')
    cv2.cvtColor(map_img, cv2.COLOR_BGR2RGB, map_img)
    map_height, map_width, map_bytesPerComponent = map_img.shape
    map_QImg = QImage(map_img.data, map_width, map_height, 3 * map_width, QImage.Format_RGB888)
    map_pixmap = QPixmap.fromImage(map_QImg)
    ui.image.setPixmap(map_pixmap)

    sys.exit(app.exec_())
