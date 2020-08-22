from PIL import Image, ImageDraw
import pygame as pg


def scale_img(path, folder, cnvs = r"\img\cnvs.jpg"):
    img = Image.open(path)
    canvas = Image.open(folder+cnvs)
    width, height = canvas.size
    dr = ImageDraw.Draw(canvas)
    pix = img.load()

    step = int(width/6)
    left, upper, right, lower = 0, 0, step, step
    i, j = 0, 0
    while lower <= height:
        while right <= width:

            for k in range(left, right):
                for l in range(upper, lower):
                    dr.point((k, l), (pix[j, i], pix[j, i], pix[j, i]))

            j += 1

            right += step
            left += step

        i += 1
        j = 0

        left, right = 0, step
        upper += step
        lower += step

    canvas.save(folder+r"\img\scaled_img.jpg")


def process_img(screen, sizes, image, step, x, y, folder, path=r"\img\data\check.jpg"):
    im = Image.open(image)
    im.crop((x, y, x+step, y+step)).save(folder+path)
    pg.draw.rect(screen, pg.Color("yellow"), (x, y, step, step), 1)
    scale_img(folder+path, folder)
    scaled_im = pg.image.load(folder+r"\img\scaled_img.jpg")
    screen.blit(scaled_im, (sizes[0]/2 + 200, 25))

