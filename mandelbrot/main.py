from PIL import Image
import math


def make_image():
    color1 = (0x66, 0x99, 0x99)  # 0の色
#    color2 = (0xff, 0x99, 0x99)  # 1の色
    x_size = 1800
    y_size = 2700  # 出力画像サイズ　今はフルHDの画像を出力します
    center = -1 + 0.3j
    cell = 0.00004
    dotsize = 2  # 一つのセルがドットいくつ分か
    filename = str(center) + " " + str(cell) + "a.png"
    img = Image.new('RGB', (x_size, y_size), color1)
    nx = x_size//dotsize + 1
    ny = y_size//dotsize + 1
    cell_map = [[0 for i in range(ny)] for j in range(nx+2)]

    xcenter = nx/2
    ycenter = ny/2

    for y in range(ny):
        for x in range(nx):
            c = center + (x-xcenter)*cell + 1j * ((y-ycenter) * cell)
            z = 0
            count = 0
            for n in range(400):
                count = count+1
                z = z*z + c
                if abs(z.real) > 3.0 or abs(z.imag) > 3.0:
                    break
            cell_map[x][y] = count

    for i in range(x_size):
        for j in range(y_size):
            num = cell_map[i//dotsize][j//dotsize]
            # num = abs(num-128)*2
            # num = num * num // 100
            # num = - math.log((num+1)) / math.log(400) * 256
            num = (num - 20) * 5
            num = min(max(0, int(num)), 255)
            # num = 0 if num < 50 else 255
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
