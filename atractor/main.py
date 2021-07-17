from PIL import Image, ImageDraw
import sys
import random
import numpy as np
import math
from typing import Tuple, List

k = 0.1
B = 12.0


def f1(x: float, y: float, t: float) -> Tuple[float, float]:
    return y, -k*y - x * x * x + B * math.cos(t)


def runge_kutta(x: float, y: float,
                t: float, dt: float) -> Tuple[float, float, float]:
    dx1, dy1 = f1(x, y, t)
    dx2, dy2 = f1(x + dx1 * dt / 2, y + dy1 * dt/2, t + dt/2)
    dx3, dy3 = f1(x + dx2 * dt / 2, y + dy2 * dt/2, t + dt/2)
    dx4, dy4 = f1(x + dx3 * dt, y + dy3 * dt, t + dt)
    nx = x + (dx1 + 2*dx2 + 2*dx3 + dx4) * dt / 6
    ny = y + (dy1 + 2*dy2 + 2*dy3 + dy4) * dt / 6
    return nx, ny, t + dt


def run_scheme(T, dt) -> List[Tuple[float, float]]:
    t = 0.0
    x = 0
    y = 3
    ret = []
    while True:
        ret.append((x, y))
        x, y, t = runge_kutta(x, y, t, dt)
        if t > T:
            break
    return ret


def make_image(rule, mode="simple", p=0.5):
    color1 = (0, 0, 0)  # 0の色
    color2 = (255, 255, 255)  # 1の色
    x_size = 2518
    y_size = 2991
    x_center = 0.0
    y_center = 0.0
    x_range = 20.0
    circle_size: int = 5
    dt = 0.001
    filename = "rule"+str(rule)+"_"+str(x_size)+"x"+str(y_size) + \
        "_"+mode+".png"
    img: Image = Image.new('RGB', (x_size, y_size), color1)
    draw = ImageDraw.Draw(img)

    data = run_scheme(1000, dt)
    for (a, b) in data:
        circle_center_x = (a-x_center) * x_size / x_range
        circle_center_y = (b-y_center) * x_size / x_range
        circle_center_x = int(circle_center_x) + x_size//2
        circle_center_y = int(circle_center_y) + y_size//2
        xy = (
            circle_center_x-circle_size, circle_center_y-circle_size,
            circle_center_x+circle_size, circle_center_y+circle_size
        )
        draw.ellipse(xy, fill=color2)

    img.save(filename)
    return img


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        rule = 30
    else:
        rule = int(argv[1])
    if len(argv) <= 2:
        mode = "simple"
    else:
        mode = argv[2]

    if len(argv) > 3:
        p = float(argv[3])
    else:
        p = 0.5

    img = make_image(rule, mode, p)
    img.show()
