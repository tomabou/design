from PIL import Image
import sys
import numpy as np
import random


def make_image():
    color1 = (0x66, 0x99, 0x99)  # 0の色
    color2 = (0xff, 0x99, 0x99)  # 1の色
    x = 1920
    y = 1080  # 出力画像サイズ　今はフルHDの画像を出力します
    center = -1 + 0.291j
    cell = 0.00003
    dotsize = 1  # 一つのセルがドットいくつ分か
    filename = str(center) + " " + str(cell) + "a.png"
    img = Image.new('RGB', (x, y), color1)
    nx = x//dotsize + 1
    ny = y//dotsize + 1
    cell_map = [[0 for i in range(ny)] for j in range(nx+2)]

    xcenter = x/2
    ycenter = y/2

    for y in range(ny):
        for x in range(nx):
            c = center + (x-xcenter)*cell + 1j * ((y-ycenter) * cell)
            z = 0
            count = 0
            for n in range(400):
                count = count+1
                z = z*z + c
                if z.real > 3.0 or z.imag > 3.0 or z.real < -3.0 or z.imag < -3.0:
                    break
            cell_map[x][y] = count

    for i in range(x):
        for j in range(y):
            num = cell_map[i//dotsize][j//dotsize]
            num = abs(num-128)*2
#            if num<100:
#                color = (0xff - num * 256 //100, 0xff,0xff)
#            elif num<200:
#                color = (0, 0xff-(num-100)*256//100,0xff)
#            else:
#                color = (0,0,0xff - (num-200)*256//100)
            color = (num, num, num)
            img.putpixel((i, j), color)

    img.save(filename)
    return img


if __name__ == "__main__":
    #    argv = sys.argv
    #    if len(argv)==1:
    #        rule = 30
    #    else:
    #         rule = int(argv[1])
    #    if len(argv)<=2:
    #        mode = "simple"
    #    else:
    #        mode = argv[2]

    img = make_image()
    img.show()
