from pygame.math import Vector2 as Vec
from os import system, environ
from random import choice, randint
import sys
import time
from getch import getch

W = 10
H = 20

FIGURES = [
        [1, 2, 3, 5], # T
        [1, 3, 4, 5], # L
        [0, 2, 4, 6], # I
        [0, 1, 2, 3], # X
        [1, 2, 3, 5]] # Z

COLORS = ["@", "P", "Q", "X"]
EMPTY_COLOR = "."

def spawn_figure():
    n = randint(0, len(FIGURES)-1)
    a = [Vec() for _ in range(4)]
    for i in range(4):
        a[i].x = FIGURES[n][i] % 2 + W // 2
        a[i].y = FIGURES[n][i] // 2 + 1
    return a

def rotate_figure(a):
    center = a[1]
    for i in range(4):
        a[i] = (a[i]-center).rotate(90)
        a[i] += center
    """
    center = a[1]
    for i in range(4):
        norm = a[i] - center
        a[i].x = -norm.y 
        a[i].y = norm.x
        a[i] += center
    """

def clear_frame(frame):
    h = len(frame)
    w = len(frame[0])
    for i in range(h):
        for j in range(w):
            frame[i][j] = EMPTY_COLOR

def check_line(field):
    for i in range(H - 1, 0, -1):
        if all(field[i]):
            for j in range(i, 0, -1):
                if not any(field[j]):
                    return True
                field[j] = field[j - 1]
    return False

def get_time_in_ms():
    return int(round(time.time() * 1000))

def check_collision(a):
    for i in range(4):
        x = int(a[i].x)
        y = int(a[i].y)
        if x < 0 or x > W-1 or y > H-1:
            return True
        if field[y][x] is not None:
            return True
    return False



n = 1
color = choice(COLORS)
a = spawn_figure()
b = a[:]

dx = 0
dy = 1

timer = 0
prev_time = 0
frame_time_ms = 0
delay = 300

frame = [[EMPTY_COLOR for _ in range(W)] for _ in range(H)]
field = [[None for _ in range(W)] for _ in range(H)]

score = 0

is_running = True
while is_running:

    prev_time = get_time_in_ms()

    # input
    c = getch()
    if c == "a":
        dx = -1
    elif c == "d":
        dx = 1
    elif c == "w":
        rotate_figure(a)
    elif c == "s":
        delay = 600
    #print(c)

    # processing

    # horizontal movement

    for i in range(4):
        a[i].x += dx
    if not check_collision(a):
        for i in range(4):
            b[i] = a[i]
            

    # vertical movement
    timer += frame_time_ms
    if timer > delay:
        for i in range(4):
            a[i].y += dy
        timer = 0

        if not check_collision(a):
            for i in range(4):
                b[i] = a[i]
        else:
            for i in range(4):
                x = int(b[i].x)
                y = int(b[i].y)
                print(x,y)
                field[y-1][x] = color
            color = choice(COLORS)
            a = spawn_figure()
            
    if check_line(field):
        score += 100

    # graphics
    # draw field
    for j in range(H):
        for i in range(W):
            if field[j][i] is not None:
                frame[j][i] = field[j][i]

    # draw falling figure
    for i in range(4):
        x = int(a[i].x) 
        y = int(a[i].y)
        try:
            frame[y-1][x] = color
        except IndexError:
            print(x, y)

    # print final frame
    system("clear")
    print(f"Score: {score}")
    for row in frame:
        print("".join(row))
    clear_frame(frame)

    frame_time_ms = get_time_in_ms() - prev_time
    dx = 0
    delay = 300
    #print(frame_time_ms)
    #print("Press <Ctrl-C> to quit...>")

