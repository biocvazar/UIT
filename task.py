from locale import atof
import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMessageBox
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
from math import *

fig = plt.figure()
ax = fig.add_subplot(111)


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Лабка")
        self.initialize()

        self.btn.clicked.connect(self.plot)

    def initialize(self):
        self.grid = QtGui.QVBoxLayout()

        self.l_a = QtGui.QLabel("Початакова точка межі обчислень {a}")
        self.l_b = QtGui.QLabel("Кінцева точка межі обчислень {b}")
        self.l_y = QtGui.QLabel("Обчислюваний вираз. Після знака {=} . Замість знака [^]\n "
                                "для піднесення в ступінь використовувати [**]")
        self.l_eps = QtGui.QLabel("Точність")
        self.txt_a = QtGui.QLineEdit()
        self.txt_b = QtGui.QLineEdit()
        self.txt_y = QtGui.QLineEdit()
        self.txt_eps = QtGui.QLineEdit()
        self.btn = QtGui.QPushButton("Розрахувати")

        self.grid.addWidget(self.l_a)
        self.grid.addWidget(self.txt_a)
        self.grid.addWidget(self.l_b)
        self.grid.addWidget(self.txt_b)
        self.grid.addWidget(self.l_eps)
        self.grid.addWidget(self.txt_eps)
        self.grid.addWidget(self.l_y)
        self.grid.addWidget(self.txt_y)
        self.grid.addWidget(self.btn)

        self.setLayout(self.grid)


    @pyqtSlot()
    def plot(self):

        try:
            a = atof(self.txt_a.text())
            b = atof(self.txt_b.text())
            y = str(self.txt_y.text())
            print(y, type(y))
            eps = atof(self.txt_eps.text())
        except Exception:
            msg = QMessageBox()
            msg.setText("Некорктно введені дані")
            msg.exec_()
        else:
            points = self.points()


            gs = GoldSeem(a, b, eps, y)
            gs.calc_func()


            x, y = [], []
            for p in points:
                x.append(p[0])
                y.append(p[1])

            x1, y1 = [], []
            for p in gs.list_of_x1:
                x1.append(p[0])
                y1.append(p[1])

            x2, y2 = [], []
            for p in gs.list_of_x2:
                x2.append(p[0])
                y2.append(p[1])

            print("sfjkjbgjgjbjk")
            self.draw(points, gs.X, gs.Y, x1, y1, x2, y2, x, y)
            # self.redraw()

    def points(self):
        try:
            a = atof(self.txt_a.text())
            b = atof(self.txt_b.text())
            ye = str(self.txt_y.text())
            print(ye, type(ye))
            eps = atof(self.txt_eps.text())
        except Exception:
            msg = QMessageBox()
            msg.setText("Некорктно введені дані")
            msg.exec_()
        else:
            p = []
            x = a
            while x <= b:
                y = eval(ye)
                p.append((x, y))
                x += eps
            return p

    def draw(self, points, xm, ym,  xx1, yy1, xx2, yy2, x, y):
        ax.clear()
        x, y = [], []
        for p in points:
            x.append(p[0])
            y.append(p[1])
        ax.plot(x, y, "g-")

        ax.set_xlabel(xlabel=u'x')
        ax.set_ylabel(ylabel=u'y')
        ax.annotate('MAX', xy=(xm, ym), xytext=(xm + 1.2, ym + 1.2),
                    arrowprops=dict(facecolor='black', shrink=0.05),)
        ax.plot(xm, ym, "rs")
        plt.show()


class GoldSeem(object):
    _Fi = 1.618
    X = 0
    Y = 0
    list_of_x1 = []
    list_of_x2 = []

    def __init__(self, a, b, eps, y):
        self.a = a
        self.b = b
        self.eps = eps
        self.y = y

    def x1(self):
        return self.b - (self.b - self.a) / self._Fi

    def x2(self):
        return self.a + (self.b - self.a) / self._Fi

    def calc_func(self):
        func = compile(self.y, "foo.py", "eval")
        x1 = self.x1()
        x2 = self.x2()
        i = 0
        while True and i < 1000:
            try:
                y1 = eval(func, {"x": x1})
                y2 = eval(func, {"x": x2})
            except ZeroDivisionError:
                pass
            self.list_of_x1.append((x1, y1))
            self.list_of_x2.append((x2, y2))
            if y1 <= y2:
                self.a = x1
                x1 = x2
                x2 = self.x2()
            else:
                self.b = x2
                x2 = x1
                x1 = self.x1()
            if abs(self.b - self.a) < self.eps or i == 999:
                self.X = (self.a + self.b) / 2
                self.Y = eval(func, {"x": self.X})
                print("break ", i)
                break
            print(i)
            i += 1


# gs = GoldSeem(-2, 2, 0.1, "1/(x+0.001)+5")
# gs.calc_func()
# print(gs.X, gs.Y)

# # d = Draw(2, 25, 0.2, "-1/x**4")
# # d.draw(d.points())
# #
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # window = QtGui.QWidget()
    my_wind = Window()
    my_wind.show()
    # window.show()
    sys.exit(app.exec_())