#coding:utf-8

import sys
import os
import matplotlib
import cv2

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QTimer
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import maze_generate
import maze_solution
import random
import numpy as np
import time
import copy
import psutil

# set random seed
random.seed(6666)
np.random.seed(6666)

class App(QWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.initUI()
        self.groupIndex1 = 1
        self.groupIndex2 = 1

    # initial UI
    def initUI(self):
        self.setWindowTitle('maze')

        self.setFixedSize(1200, 700)

        self.setMinimumSize(1200, 700)
        self.setMaximumSize(1200, 700)

        self.solutionBtn = QPushButton('maze solution')
        self.generation = QPushButton('maze generation')
        self.generation_btn = QPushButton('loop generation')

        # bind function
        self.solutionBtn.clicked.connect(self.startTimer)
        self.generation.clicked.connect(self.maze_generate)
        self.generation_btn.clicked.connect(self.loop_generation)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.lbl_image = QLabel()
        self.lbl_image.setStyleSheet("QLabel{background-color:rgb(200,101,102);}")
        self.lbl_image.setScaledContents(True)

        self.lbl1 = QRadioButton('Wall follow (left hand)')
        self.lbl2 = QRadioButton('Wall follow (right hand)')
        self.lbl3 = QRadioButton('Recursive')
        self.lbl4 = QRadioButton('A*')
        self.rbr1 = QRadioButton('Prim')
        self.rbr2 = QRadioButton('Randomized DFS         ')
        self.rbr3 = QRadioButton('Sidewinder')

        # input of size
        self.size1Edt = QLineEdit()
        intValidator = QIntValidator()
        intValidator.setRange(0, 1000)
        self.size1Edt.setValidator(intValidator)
        self.size1Edt.setMaximumWidth(100)
        self.size1Edt.setText("5")

        self.size2Edt = QLineEdit()
        self.size2Edt.setValidator(intValidator)
        self.size2Edt.setMaximumWidth(100)
        self.size2Edt.setText("5")

        # input of loop
        self.loopEdt = QLineEdit()
        self.loopEdt.setMaximumWidth(100)
        self.loopEdt.setValidator(QIntValidator(0, 100))
        self.loopEdt.setText("1")
        self.loop_lb = QLabel("loop number:")
        self.size1_lb = QLabel("height:")
        self.size2_lb = QLabel("width:")

        self.resetLeft = QPushButton('reset')
        self.resetLeft.clicked.connect(self.resetLeftGroup)
        self.resetRight = QPushButton('reset')
        self.resetRight.clicked.connect(self.resetRightGroup)

        self.lblPathLength = QLabel("  ")
        self.lblTime = QLabel("               ")
        self.lblSteps = QLabel("  ")
        self.lblMem = QLabel(" ")
        self.lblRoad = QLabel(" ")

        lbl1 = QLabel('Path length:')
        lbl2 = QLabel('Time:')
        lbl3 = QLabel('Steps:')
        lbl4 = QLabel("Dead end:")
        lbl5 = QLabel("Branch:")

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(20)

        grid.addWidget(self.lbl1, 1, 1, 2, 2)
        grid.addWidget(self.lbl2, 2, 1, 2, 2)
        grid.addWidget(self.lbl3, 3, 1, 2, 2)
        grid.addWidget(self.lbl4, 4, 1, 2, 2)


        grid.addWidget(self.rbr1, 1, 18, 2, 2)
        grid.addWidget(self.rbr2, 2, 18, 2, 2)
        grid.addWidget(self.rbr3, 3, 18, 2, 2)
        # grid.addWidget(self.rbr4, 4, 18, 2, 2)



        grid.addWidget(self.size1_lb, 5,18,  1, 1)
        grid.addWidget(self.size1Edt, 5, 18, 2, 2)
        grid.addWidget(self.size2_lb, 6, 18, 1, 1)
        grid.addWidget(self.size2Edt, 6, 18, 2, 2)

        grid.addWidget(self.loop_lb, 9, 18, 1, 1)
        grid.addWidget(self.loopEdt, 9, 18, 2, 2)

        grid.addWidget(self.resetLeft, 20, 1, 2, 2)
        grid.addWidget(self.resetRight, 20, 18, 2, 2)

        grid.addWidget(lbl1, 20, 4, 2, 2)
        grid.addWidget(lbl2, 20, 8, 2, 2)
        grid.addWidget(lbl3, 20, 12, 2, 2)
        grid.addWidget(lbl4, 20, 15, 2, 2)
        grid.addWidget(lbl5, 21, 4, 2, 2)

        grid.addWidget(self.lblPathLength, 20, 6, 2, 2)
        grid.addWidget(self.lblTime, 20, 10, 2, 2)
        grid.addWidget(self.lblSteps, 20, 14, 2, 2)
        grid.addWidget(self.lblMem, 20, 17, 2, 2)
        grid.addWidget(self.lblRoad,21,6,2,2)


        grid.addWidget(self.canvas, 1, 4, 14, 14)

        self.g1 = QButtonGroup(self)
        self.g1.addButton(self.lbl1,1)
        self.g1.addButton(self.lbl2,2)
        self.g1.addButton(self.lbl3,3)
        self.g1.addButton(self.lbl4,4)

        self.g2 = QButtonGroup(self)
        self.g2.addButton(self.rbr1,11)
        self.g2.addButton(self.rbr2,12)
        self.g2.addButton(self.rbr3,13)

        grid.addWidget(self.solutionBtn, 7, 1, 2, 2)
        grid.addWidget(self.generation, 7, 18, 2, 2)
        grid.addWidget(self.generation_btn, 10, 18, 2, 2)


        self.lbl1.setChecked(True)
        self.rbr1.setChecked(True)

        self.g1.buttonClicked[int].connect(self.slot)
        self.g2.buttonClicked[int].connect(self.slot)

        # maze
        self.M = None

    def loop_generation(self):
        if self.M is None:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', 'Please generate maze!')
            msg_box.exec_()
            return
        self.loop_num = int(self.loopEdt.text())
        self.M = maze_generate.generate_loop(self.M,loop_num=self.loop_num)
        # count dead ends
        self.dead_num = maze_generate.get_dead_num(self.M)
        self.lblMem.setText("%d" % maze_generate.get_dead_num(self.M))
        self.lblRoad.setText("%d" % maze_generate.get_road_num(self.M))
        self.image = maze_generate.generate_image(self.M)
        plt.clf()
        plt.xticks([])
        plt.yticks([])
        plt.imshow(self.image, interpolation='none')
        self.canvas.draw()


    def resetLeftGroup(self):
        print("resetLeftGroup")
        self.lbl1.setChecked(True)
        self.groupIndex1 = 1

    def resetRightGroup(self):
        self.rbr1.setChecked(True)
        # self.rbr4.setChecked(False)
        self.groupIndex2 = 1

    def slot(self, id):
        print("id is:", id)
        if id > 9:
            self.groupIndex2 = id - 10
        else:
            self.groupIndex1 = id

    def showTime(self):

        color_num =64

        if self.nowIdx> len(self.path)-1:
            image = self.image
            prev = self.prev
            image[10 * prev[0] + 4,
                  range(max(0, 10 * prev[1] + 5), min(image.shape[1], 10 * prev[1] + 15))] = color_num
            image[10 * prev[0] + 5,
                  range(max(0, 10 * prev[1] + 5), min(image.shape[1], 10 * prev[1] + 15))] = color_num
            plt.clf()
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.image,  interpolation='none')
            self.canvas.draw()
            self.endTimer()
        else:
            prev = self.prev
            item = self.path[self.nowIdx]

            if item in self.path[:self.nowIdx]:
                # invalid path colour
                color_num = 224
            else:
                # final path colour
                color_num = 64

            # calculate direction
            direction = ""
            if item[0] - prev[0] == 1:
                direction = "north"
            elif item[0] - prev[0] == -1:
                direction = "south"
            elif item[1] - prev[1] == 1:
                direction = "right"
            elif item[1] - prev[1] == -1:
                direction = "left"
            # color_num = 128
            i, j = item[0], item[1]
            # print(i, j)
            # (print(direction))
            # print(color_num)
            image = self.image

            if direction == 'right':
                image[10 * i + 4,
                      range(max(0, 10 * prev[1] + 4), min(image.shape[1], 10 * prev[1] + 16))] = color_num
                image[10 * i + 5,
                      range(max(0, 10 * prev[1] + 4), min(image.shape[1], 10 * prev[1] + 16))] = color_num

            elif direction == 'left':
                image[10 * i + 4,
                      range(max(0, 10 * prev[1] - 6), min(image.shape[1], 10 * prev[1] + 6))] = color_num
                image[10 * i + 5,
                      range(max(0, 10 * prev[1] - 6), min(image.shape[1], 10 * prev[1] + 6))] = color_num

            elif direction == 'north':

                image[range(max(0, 10 * prev[0] + 4), min(image.shape[0], 10 * prev[0] + 16)),
                      10 * prev[1] + 4] = color_num
                image[range(max(0, 10 * prev[0] + 4), min(image.shape[0], 10 * prev[0] + 16)),
                      10 * prev[1] + 5] = color_num


            elif direction == 'south':

                image[range(max(0, 10 * prev[0] - 6), min(image.shape[0], 10 * prev[0] + 6)),
                      10 * prev[1] + 4] = color_num
                image[range(max(0, 10 * prev[0] - 6), min(image.shape[0], 10 * prev[0] + 6)),
                      10 * prev[1] + 5] = color_num

            self.prev = item
            self.nowIdx += 1
            plt.clf()
            plt.xticks([])
            plt.yticks([])
            plt.imshow(image, interpolation='none')
            self.canvas.draw()


    def startTimer(self):

        if self.M is None:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', 'Please generate maze!')
            msg_box.exec_()
            return
        self.image = maze_generate.generate_image(self.M)

        self.M_backup = copy.deepcopy(self.M)
        t1 = time.time()

        if self.groupIndex1 == 1:
            self.is_recursive = False
            self.path = maze_solution.wall_follower(self.M,left_hand_rule=True)
            if len(self.path)==0:
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', 'Wall follower can\'t solve this maze!')
                msg_box.exec_()
                return

        elif self.groupIndex1 == 2:
            self.is_recursive = False
            self.path = maze_solution.wall_follower(self.M,left_hand_rule=False)
            if len(self.path)==0:
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', 'Wall follower can\'t solve this maze!')
                msg_box.exec_()
                return

        elif self.groupIndex1 == 3:
            self.is_recursive = True
            self.endTimer()
            self.path = []
            maze_solution.recursive(self.M,(0,0),(self.M.shape[0]-1,self.M.shape[1]-1),self.path)
            self.path.reverse()
        elif self.groupIndex1 == 4:
            self.is_recursive = False
            self.path = maze_solution.A_star(self.M)

        t2 = time.time()
        # print(self.path)

        self.nowIdx = 0
        self.prev = (0,-1)



        if self.is_recursive==False:
            self.timer.start(500)  #
        else:
            self.vis_recursive(self.M,self.path)

        if self.is_recursive == False:
            self.lblSteps.setText(str(len(self.path)))

            s = set(self.path)
            # print(t2-t1)
            self.lblTime.setText("%.5f seconds" % (t2 - t1))
            self.lblPathLength.setText(str(len(s)))

        else:

            total_count = 0
            maze = self.M
            for row_idx in range(maze.shape[0]):
                for col_idx in range(maze.shape[1]):
                    if maze[row_idx, col_idx, 4] == 2 or maze[row_idx, col_idx, 4] == 3:  # 路径
                        total_count+=1


            self.lblSteps.setText(str(total_count))
            s = set(self.path)
            # print(t2-t1)
            self.lblTime.setText("%.5f seconds" % (t2 - t1))
            self.lblPathLength.setText(str(len(s)))
        self.M = copy.deepcopy(self.M_backup)



    def endTimer(self):

        self.timer.stop()  #
        self.path = []
        self.nowIdx = 0

    # maze generation
    def maze_generate(self):
        self.endTimer() #

        # get size
        self.size1 = int(self.size1Edt.text())
        self.size2 = int(self.size2Edt.text())

        # print("maze size1:%d,size2:%d"%(self.size1,self.size2))

        # print('left index:',self.groupIndex1)
        # print('right index:',self.groupIndex2)
        # print(self.rbr4.isChecked())
        # print('left index:', self.groupIndex1)

        if self.groupIndex2 == 1:
            self.M = maze_generate.prim(self.size1, self.size2)

        elif self.groupIndex2 == 2:
            self.M = maze_generate.random_first(self.size1, self.size2)

        elif self.groupIndex2 == 3:
            self.M = maze_generate.sidewinder(self.size1, self.size2)

        # count dead end
        self.dead_num = maze_generate.get_dead_num(self.M)
        self.lblMem.setText("%d" % maze_generate.get_dead_num(self.M))
        self.lblRoad.setText("%d" % maze_generate.get_road_num(self.M))
        # if self.rbr4.isChecked()==True:
        #     self.loop_num = int(self.loopEdt.text())
        #     # print("loop num",self.loop_num)
        #     self.M = maze_generate.generate_loop(self.M,loop_num=self.loop_num)

        self.image = maze_generate.generate_image(self.M)
        plt.clf()
        plt.xticks([])
        plt.yticks([])
        plt.imshow(self.image ,interpolation='none')
        self.canvas.draw()

    # visualization
    def vis_recursive(self, maze, path):
        plt.clf()
        size1, size2 = maze.shape[0], maze.shape[1]
        # The array image is going to be the output image to display
        image = np.zeros((size1 * 10, size2 * 10), dtype=np.uint8)
        # Generate the image for display
        for row in range(0, size1):
            for col in range(0, size2):
                cell_data = maze[row, col]
                for i in range(10 * row + 2, 10 * row + 8):
                    image[i, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[0] == 1:
                    image[range(10 * row + 2, 10 * row + 8), 10 * col] = 255
                    image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 255
                if cell_data[1] == 1:
                    image[10 * row, range(10 * col + 2, 10 * col + 8)] = 255
                    image[10 * row + 1, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[2] == 1:
                    image[range(10 * row + 2, 10 * row + 8), 10 * col + 9] = 255
                    image[range(10 * row + 2, 10 * row + 8), 10 * col + 8] = 255
                if cell_data[3] == 1:
                    image[10 * row + 9, range(10 * col + 2, 10 * col + 8)] = 255
                    image[10 * row + 8, range(10 * col + 2, 10 * col + 8)] = 255

        for item in path:
            i, j = item[0], item[1]
            maze[i, j, 4] = 3

        color_num = 128

        for row_idx in range(maze.shape[0]):
            for col_idx in range(maze.shape[1]):
                if maze[row_idx,col_idx,4] == 2:
                    cv2.circle(image, (10 * col_idx + 5, 10 * row_idx + 5), 1, 128,thickness=1)
                elif maze[row_idx,col_idx,4] == 3:
                    cv2.circle(image, (10 * col_idx + 5, 10 * row_idx + 5), 1, 64,thickness=1)
                    # a = 1
        plt.xticks([])
        plt.yticks([])

        plt.imshow(image, interpolation='none')
        self.canvas.draw()

if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    app.exec()
