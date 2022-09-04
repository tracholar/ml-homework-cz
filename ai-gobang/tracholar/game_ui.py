# coding:utf-8
import pygame
from pygame.locals import *
import numpy as np

CIRCLE_RADIUS = 14
CIRCLE_PADDING = 4
CIRCLE_DISTANCE = CIRCLE_RADIUS * 2 + CIRCLE_PADDING
CIRCLE_NUM = 13
PADDING = 10
SCREEN_WIDTH = CIRCLE_DISTANCE * (CIRCLE_NUM - 1) + CIRCLE_RADIUS * 2 + PADDING * 2
SCREEN_HEIGHT = SCREEN_WIDTH

class BoardUI(object):
    def __init__(self, size=15):

        pygame.init()

        CIRCLE_RADIUS = 14
        CIRCLE_PADDING = 4
        CIRCLE_DISTANCE = CIRCLE_RADIUS * 2 + CIRCLE_PADDING
        CIRCLE_NUM = size
        PADDING = 10
        SCREEN_WIDTH = CIRCLE_DISTANCE * (CIRCLE_NUM - 1) + CIRCLE_RADIUS * 2 + PADDING * 2
        SCREEN_HEIGHT = SCREEN_WIDTH

        print(SCREEN_HEIGHT, SCREEN_WIDTH)
        self.screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])

        self.board = np.zeros((CIRCLE_NUM, CIRCLE_NUM), dtype=int)

    def draw_board(self):
        self.screen.fill((255,255,255))
        for i in range(CIRCLE_NUM):
            x = PADDING + CIRCLE_RADIUS + i * CIRCLE_DISTANCE
            y1 = PADDING + CIRCLE_RADIUS
            y2 = PADDING + CIRCLE_RADIUS + CIRCLE_DISTANCE * (CIRCLE_NUM - 1)

            pygame.draw.line(self.screen, (0,0,0), (x, y1), (x, y2))
            pygame.draw.line(self.screen, (0,0,0), (y1, x), (y2, x))

        for i in range(CIRCLE_NUM):
            for j in range(CIRCLE_NUM):
                z = self.board[i, j]
                if z == 0:
                    continue
                x = PADDING + CIRCLE_RADIUS + i * CIRCLE_DISTANCE
                y = PADDING + CIRCLE_RADIUS + j * CIRCLE_DISTANCE


                if z == 1:
                    c = (0, 0, 0)
                elif z == 2:
                    c = (255, 255, 255)
                else:
                    c = (128, 128, 128)

                pygame.draw.circle(self.screen, c, (x, y), CIRCLE_RADIUS)
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), CIRCLE_RADIUS, width=1)

    def run(self):
        running = True
        self.draw_board()
        pygame.display.flip()
        role = 1
        while running:
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    running = False

                if evt.type == MOUSEBUTTONUP:
                    print(evt)
                    x, y = evt.pos
                    xi = int(round(float(x - PADDING - CIRCLE_RADIUS)/CIRCLE_DISTANCE))
                    yi = int(round(float(y - PADDING - CIRCLE_RADIUS)/CIRCLE_DISTANCE))

                    if self.board[xi, yi] != 0:
                        continue
                    self.board[xi, yi] = role
                    role = 3 - role

                    self.draw_board()

                    pygame.display.flip()

    def quit(self):
        pygame.quit()

if __name__ == '__main__':
    b = BoardUI()
    b.run()
    b.quit()