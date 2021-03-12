import sorting
import time
import os
import numpy as np
import sys
import pygame as pg
from pygame.locals import *


class Vis(object):
    def __init__(self):
        self.sorted = False
        self.arr = np.random.randint(400, size=100)
        self.vis_arr = []
        self.alg = 0
        pg.init()
        pg.display.set_caption('Sorting Visualization')
        self.display = pg.display.set_mode((1024, 512))
        self.buttons = [pg.Rect(50, 450, 200, 50), pg.Rect(300, 450, 200, 50), pg.Rect(550, 450, 200, 50),
                        pg.Rect(800, 450, 200, 50)]
        self.options = ['Quick Sort', 'Insertion Sort', 'Bubble Sort', 'Merge Sort']
        self.font = pg.font.SysFont('Arial', 20)
        self.bg = [255, 255, 255]
        self.display.fill(self.bg)
        for o, b in zip(self.options, self.buttons):
            pg.draw.rect(self.display, [255, 0, 0], b)
            print(b[0])
            self.display.blit(self.font.render(o, True, (0, 0, 0)), (b[0] + 50, b[1] + 15))

        pg.display.update()

    def check_events(self):  # Check if the pg window was quit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                for b in self.buttons:
                    if b.collidepoint(mouse_pos):
                        # prints current location of mouse
                        print('button was pressed at {0}'.format(mouse_pos))
                        ret = self.sorting_screen(b)
                        if ret == -1:
                            return -1

    def update_array(self):
        self.display.fill(self.bg)
        loc = 15
        for a in self.arr:
            self.vis_arr.append(pg.Rect(loc, 50, 5, a))
            loc += 10
        for a in self.vis_arr:
            pg.draw.rect(self.display, [255, 0, 0], a)
        pg.display.update()
        self.vis_arr.clear()

    def mergeSort(self, arr):
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        self.mergeSort(L)
        self.mergeSort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            self.update_array()

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            self.update_array()

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            self.update_array()

    def partition(self, low, high):
        i = (low - 1)  # index of smaller element
        pivot = self.arr[high]  # pivot

        for j in range(low, high):
            if self.arr[j] <= pivot:
                i = i + 1
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
                self.update_array()

        self.arr[i + 1], self.arr[high] = self.arr[high], self.arr[i + 1]
        self.update_array()
        return i + 1

    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(self.arr, low, high)
            self.quickSort(self.arr, low, pi - 1)
            self.quickSort(self.arr, pi + 1, high)

    def sort(self):
        if self.alg == 0:  # Quick Sort
            self.quick_sort(0, 399)
        elif self.alg == 1:  # Insertion Sort
            for i in range(1, len(self.arr)):
                key = self.arr[i]
                j = i - 1
                while j >= 0 and key < self.arr[j]:
                    self.arr[j + 1] = self.arr[j]
                    j -= 1
                    self.update_array()
                self.arr[j + 1] = key
                self.update_array()
        elif self.alg == 2:  # Bubble Sort
            n = len(self.arr)
            for i in range(n - 1):
                for j in range(0, n - i - 1):
                    if self.arr[j] > self.arr[j + 1]:
                        self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                        self.update_array()
        elif self.alg == 3:
            self.mergeSort(self.arr)

    def sorting_screen(self, button):
        if button[0] != 412:
            self.update_array()
            start = pg.Rect(412, 480, 200, 30)
            self.buttons.append(start)
            pg.draw.rect(self.display, [255, 0, 0], start)
            self.display.blit(self.font.render('Start', True, (0, 0, 0)), (490, 485))

            if button[0] == 50:
                self.display.blit(self.font.render(self.options[0], True, (0, 0, 0)), (475, 20))
                pg.display.update()
            elif button[0] == 300:
                self.alg = 1
                self.display.blit(self.font.render(self.options[1], True, (0, 0, 0)), (450, 20))
                pg.display.update()
            elif button[0] == 550:
                self.alg = 2
                self.display.blit(self.font.render(self.options[2], True, (0, 0, 0)), (475, 20))
                pg.display.update()
            elif button[0] == 800:
                self.alg = 3
                self.display.blit(self.font.render(self.options[3], True, (0, 0, 0)), (475, 20))
                pg.display.update()
        else:
            # start button was pressed, will have to start the selected algorithm
            if not self.sorted:
                time.sleep(.5)
                self.sort()
                pg.draw.rect(self.display, [255, 0, 0], self.buttons[-1])
                # self.display.blit(self.font.render('Back', True, (0, 0, 0)), (490, 485))
                # pg.display.update()
                self.sorted = True
            else:
                return -1


# need a main call here eventually
def running():
    disp = Vis()
    while True:
        ret = disp.check_events()
        if ret == -1:
            break

while 1:
    running()
