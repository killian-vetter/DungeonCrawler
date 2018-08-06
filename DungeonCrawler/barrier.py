from tkinter import *

class Barrier (object):
    #takes 2 points along with the width and height of canvas
    def __init__(self, x1, y1, x2, y2, w, h):
        self.point1 = (x1, y1)
        self.point2 = (x2, y2)
        self.nodes = []
        #makes nodes for if enemies need to go around a barrier
        if self.point1[0] == self.point2[0]:
            a = min(self.point1[1], self.point2[1]) - 50
            b = max(self.point1[1], self.point2[1]) + 50
            if 0 <= a <= h:
                self.nodes.append((self.point1[0], a))
            if 0 <= b <= h:
                self.nodes.append((self.point1[0], b))
        elif line[1][1] == line[1][1]:
            a = min(self.point1[0], self.point2[0]) - 50
            b = max(self.point1[0], self.point2[0]) + 50
            if 0 <= a <= w:
                self.nodes.append((a, self.point1[1]))
            if 0 <= b <= w:
                self.nodes.append((b, self.point1[1]))
        #else invalid barrier

    def draw (self, canvas):
        canvas.create_line(self.point1[0], self.point1[1], self.point2[0], self.point2[1], width = 10)