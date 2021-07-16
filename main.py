from PIL import Image
import sys
import random
import numpy as np


def make_image(rule, mode="simple", p=0.5):
    color1 = (0x66, 0x99, 0x99)  # 0の色
    color2 = (0xff, 0x99, 0x99)  # 1の色
    color2 = (0, 0, 0)  # 0の色
    color1 = (0xff, 0xff, 0xff)  # 1の色
    colors = [
        (0xff, 0xff, 0xff),
        (0xaa, 0xaa, 0xaa),
        (0x55, 0x55, 0x55),
        (0x00, 0x00, 0x00),
    ]
    x = 1800
    y = 2500  # 出力画像サイズ　今はフルHDの画像を出力します
    x = 2518
    y = 2991  # 出力画像サイズ　今はフルHDの画像を出力します
    dotsize = 7  # 一つのセルがドットいくつ分か
    drawsize = 7
    filename = "rule"+str(rule)+"_"+str(x)+"x"+str(y) + \
        "_"+str(dotsize)+"_"+mode+".png"
    img = Image.new('RGB', (x, y), color1)

    rule_list = list()
    for i in range(8):
        rule_list.append(rule % 2)
        rule = rule // 2

    print(rule_list)

    nx = x//dotsize + 1
    ny = y//dotsize + 1
    cell_map = [[0 for i in range(ny)] for j in range(nx+2)]
    if mode == "simple":
        for i in range(int(p)):
            cell_map[nx//(2)+i][0] = 1
    elif mode == "random":
        for i in range(nx):
            cell_map[i][0] = 1 if random.random() < p else 0
    elif mode == "sense":
        for i in range(nx):
            if random.random() < p:
                cell_map[i][0] = 1
                i += 1
                while random.random() < 0.3 and i < nx:
                    cell_map[i][0] = 1
                    i += 1

    cell_map[nx][0] = cell_map[0][0]
    cell_map[nx+1][0] = cell_map[1][0]

    for j in range(ny-1):
        for i in range(nx):
            num = 4*cell_map[i][j] + 2 * cell_map[i+1][j]+cell_map[i+2][j]
            cell_map[i+1][j+1] = rule_list[num]

        cell_map[0][j+1] = cell_map[nx][j+1]
        cell_map[nx+1][j+1] = cell_map[1][j+1]

    pixelMap = np.ndarray((x, y), dtype=int)
    for i in range(nx):
        for j in range(ny):
            if cell_map[i][j] == 0:
                continue
            for dx in range(drawsize):
                for dy in range(drawsize):
                    xtmp = i*dotsize + dx
                    ytmp = j*dotsize + dy
                    if xtmp < x and ytmp < y:
                        pixelMap[xtmp][ytmp] += 1

    for i in range(x):
        for j in range(y):
            colorID = min(len(colors)-1, pixelMap[i][j])
            if pixelMap[i][j] > 0:
                img.putpixel((i, j), colors[3])

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
