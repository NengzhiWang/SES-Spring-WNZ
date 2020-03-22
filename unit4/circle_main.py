# -*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import time


class Circle:
    def __init__(self, radius=0, center_x=0, center_y=0):
        self.r = radius
        self.x = center_x
        self.y = center_y

    def ListUp(self, cl):
        cl.append(self)
        return True

    def PointJudge(self, cl):
        if cl is not []:
            for c in cl:
                if np.linalg.norm([self.x - c.x, self.y - c.y]) <= c.r:
                    return False
            return True
        else:
            return True

    def distance(self, c2):
        d = ((self.x - c2.x)**2 + (self.y - c2.y)**2)**0.5
        return d


#迭代中的重要函数，可计算出可取半径的值
def MinDistance(ptx, pty, cl):
    distance = []
    for c in cl:
        if np.linalg.norm([ptx - c.x, pty - c.y]) <= c.r:
            return -1000
        elif np.max(np.abs([ptx, pty])) >= 1:
            return -1000
        distance.append(np.linalg.norm([ptx - c.x, pty - c.y]) - c.r)
    distance.append(1 - np.max(np.abs([ptx, pty])))
    return np.min(distance)


#将该函数送入优化器中进行优化
def PointOptimize(arg):
    cl = arg
    md = lambda x: 1 - MinDistance(x[0], x[1], cl)
    return md


def RSquare(cl):
    total = 0
    for c in cl:
        total += c.r**2
    print("Total r square is {}.".format(total))
    return total


def Print(cl):
    for i in range(len(cl)):
        print("The {} circle's x is {}, y is {}, r is {}.".format(
            i + 1, cl[i].x, cl[i].y, cl[i].r))


def MaxAreaCircles(m, plot=False):
    cl = []
    for i in range(m):
        if (i + 1) % 4 == 0:  #在第一象限生成
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            c1 = Circle(None, x, y)
            while not c1.PointJudge(cl):
                c1.x = random.uniform(0, 1)
                c1.y = random.uniform(0, 1)
        elif (i + 1) % 4 == 1:  #在第二象限生成
            x = random.uniform(-1, 0)
            y = random.uniform(0, 1)
            c1 = Circle(None, x, y)
            while not c1.PointJudge(cl):
                c1.x = random.uniform(-1, 0)
                c1.y = random.uniform(0, 1)
        elif (i + 1) % 4 == 2:  #在第三象限生成
            x = random.uniform(-1, 0)
            y = random.uniform(-1, 0)
            c1 = Circle(None, x, y)
            while not c1.PointJudge(cl):
                c1.x = random.uniform(-1, 0)
                c1.y = random.uniform(-1, 0)
        elif (i + 1) % 4 == 3:  #在第四象限生成
            x = random.uniform(0, 1)
            y = random.uniform(-1, 0)
            c1 = Circle(None, x, y)
            while not c1.PointJudge(cl):
                c1.x = random.uniform(0, 1)
                c1.y = random.uniform(-1, 0)
        #使用优化器进行圆心坐标的优化
        MaxRadius = minimize(PointOptimize(cl), (c1.x, c1.y), method='SLSQP')
        c1.r = MinDistance(float(MaxRadius.x[0]), float(MaxRadius.x[1]), cl)
        c1.x = float(MaxRadius.x[0])
        c1.y = float(MaxRadius.x[1])
        c1.ListUp(cl)
    #绘制整个图案
    if plot is True:
        plt.figure(figsize=(7, 7))
        theta = np.linspace(0, 2 * np.pi, 50)
        for c in cl:
            plt.plot(c.x + c.r * np.cos(theta), c.y + c.r * np.sin(theta), 'b')
        plt.axes().set_aspect('equal')
        plt.xlim([-1, 1])
        plt.ylim([-1, 1])
        plt.show()
    return cl


if __name__ == "__main__":
    time_start = time.time()
    m = 10
    circle_list = MaxAreaCircles(m, True)
    RSquare(circle_list)
    Print(circle_list)
    time_end = time.time()
    print('totally cost', time_end - time_start)
