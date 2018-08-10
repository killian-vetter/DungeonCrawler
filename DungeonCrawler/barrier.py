from tkinter import *

class Barrier (object):
    #takes 2 points along with the width and height of canvas
    def __init__(self, x1, y1, x2, y2, w, h):
        self.CW = w
        self.CH = h
        self.nodes = []
        #makes nodes for if enemies need to go around a barrier
        if x1 == x2:
            if y1>y2:
                self.point1 = (x2, y2)
                self.point2 = (x1, y1)
            else:
                self.point1 = (x1, y1)
                self.point2 = (x2, y2)
            a = self.point1[1] - 100
            b = self.point2[1] + 100
            if 0 <= a <= h:
                self.nodes.append((self.point1[0], a))
            if 0 <= b <= h:
                self.nodes.append((self.point1[0], b))
        else:
            if x1>x2:
                self.point1 = (x2, y2)
                self.point2 = (x1, y1)
            else:
                self.point1 = (x1, y1)
                self.point2 = (x2, y2)
            a = self.point1[0] - 100
            b = self.point2[0] + 100
            if 0 <= a <= w:
                self.nodes.append((a, self.point1[1]))
            if 0 <= b <= w:
                self.nodes.append((b, self.point1[1]))

    def __repr__(self):
        return "Barrier %d %d %d %d" % (self.point1[0], self.point1[1], self.point2[0], self.point2[1])

    def points(self):
        return (self.point1, self.point2)

    #shift the bottom or right most point to (x,y) and keeps dimensions
    def shift(self, x, y):
        self.point1 = (self.point1[0]-self.point2[0]+x, self.point1[1]-self.point2[1]+y)
        self.point2 = (x,y)
        self.nodes = []
        if self.point1[0] == self.point2[0]:
            a = self.point1[1] - 100
            b = self.point2[1] + 100
            if 0 <= a <= self.CH:
                self.nodes.append((self.point1[0], a))
            if 0 <= b <= self.CH:
                self.nodes.append((self.point1[0], b))
        if self.point1[1] == self.point2[1]:
            a = self.point1[0] - 100
            b = self.point2[0] + 100
            if 0 <= a <= self.CW:
                self.nodes.append((a, self.point1[1]))
            if 0 <= b <= self.CW:
                self.nodes.append((b, self.point1[1]))

    def draw (self, canvas):
        canvas.create_line(self.point1[0], self.point1[1], self.point2[0], self.point2[1], 
                           width = 10, fill = "white")

    def drawOther(self, canvas):
        canvas.create_line(self.point1[0], self.point1[1], self.point2[0], self.point2[1], 
                           width = 10, fill = "black")

    def copy(self):
        return Barrier ()