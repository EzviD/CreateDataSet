import pygame as pg
from PIL import Image
import os

from src.preprocess_img import refactor_img
from src.process_img import process_img


class Interface:

    def __init__(self, width=1280, height=720, img=r'\img\1.jpg'):
        self.width = width
        self.height = height

        self.folder = os.getcwd()

        refactor_img(self.folder+img, (int(self.width/2), self.height), to_gray=True)
        self.image = self.folder+img

        self.center = (0, 0)
        self.step = 6

        self.screen_size = self.width, self.height
        self.screen = pg.display.set_mode(self.screen_size)

    def setup_buttons(self):
        half_width = self.width / 2
        half_height = self.height / 2
        horisontal_btn = pg.Rect(half_width + 50, half_height, 25, 25)
        vertical_btn = pg.Rect(half_width + 250, half_height, 25, 25)
        left_incline_btn = pg.Rect(half_width + 50, half_height + 100, 25, 25)
        right_incline_btn = pg.Rect(half_width + 250, half_height + 100, 25, 25)
        empty_btn = pg.Rect(half_width + 50, half_height + 200, 25, 25)

        return half_width, half_height, horisontal_btn, vertical_btn, left_incline_btn, right_incline_btn, empty_btn

    def draw(self, half_width, half_height, horisontal_btn, vertical_btn,
             left_incline_btn, right_incline_btn, empty_btn):

        # button
        pg.draw.rect(self.screen, pg.Color("white"), vertical_btn, 2)
        # rectangle vertical №1
        pg.draw.rect(self.screen, pg.Color("white"), (half_width + 300, half_height - 15, 50, 50), 4)
        pg.draw.line(self.screen, pg.Color("white"), (half_width + 325, half_height - 15), (half_width + 325, half_height + 35))

        #button
        pg.draw.rect(self.screen, pg.Color("white"), horisontal_btn, 2)
        #rectangle horisontal №2
        pg.draw.rect(self.screen, pg.Color("white"), (half_width + 100, half_height - 15, 50, 50), 4)
        pg.draw.line(self.screen, pg.Color("white"), (half_width + 100, half_height + 10), (half_width + 150, half_height + 10))

        #button
        pg.draw.rect(self.screen, pg.Color("white"), right_incline_btn, 2)
        #rectangle left incline №3
        pg.draw.rect(self.screen, pg.Color("white"), (half_width + 100, half_height + 85, 50, 50), 4)
        pg.draw.line(self.screen, pg.Color("white"), (half_width + 100, half_height + 85), (half_width + 150, half_height + 135))

        #button
        pg.draw.rect(self.screen, pg.Color("white"), left_incline_btn, 2)
        #rectangle right incline №4
        pg.draw.rect(self.screen, pg.Color("white"), (half_width + 300, half_height + 85, 50, 50), 4)
        pg.draw.line(self.screen, pg.Color("white"), (half_width + 300, half_height + 135), (half_width + 350, half_height + 85))

        #button
        pg.draw.rect(self.screen, pg.Color("white"), empty_btn, 2)
        #rectangle empty №5
        pg.draw.rect(self.screen, pg.Color("white"), (half_width + 100, half_height + 185, 50, 50), 4)

    def read_data(self):
        temp_x = []
        temp_y = []
        with open("data.txt", "r") as f:
            lines = f.readlines()
            lines_x = lines[0::2]
            lines_y = lines[1::2]
            for l in lines_x:
                temp_x.append(l.split('\n')[0].split())
            for l_y in lines_y:
                temp_y.append(l_y.split('\n')[0])

        return temp_x, temp_y

    def write_file(self, result_x, result_y):
        with open("data.txt", 'w') as f:
            for i in range(len(result_x)):
                for j in range(len(result_x[i])):
                    f.write(f"{result_x[i][j]} ")
                f.write('\n')
                f.write(f"{result_y[i]}\n")

    def start(self):
        pg.init()
        pg.display.set_caption("Data Set")
        self.screen.fill(pg.Color('gray'))
        img = pg.image.load(self.image)
        self.screen.blit(img, (0, 0))

        x, y = 0, 0

        btns = self.setup_buttons()
        self.draw(*btns)
        result_x = []
        result_y = []

        if os.stat(self.folder + r"\data.txt").st_size != 0:
            result_x, result_y = self.read_data()

        running = True
        print(result_x, result_y)
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.write_file(result_x, result_y)
                    running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    img = Image.open(self.folder+r"\img\data\check.jpg")
                    pix = img.load()
                    temp_x = []
                    for i in range(2, len(btns)):
                        if btns[i].collidepoint(mouse_pos):
                            for j in range(self.step):
                                for k in range(self.step):
                                    temp_x.append(pix[k, j])
                            result_y.append(i-1)
                            result_x.append(temp_x)

            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] and x-self.step >= 0:
                x -= self.step
            if keys[pg.K_RIGHT] and x+self.step <= self.width/2:
                x += self.step
            if keys[pg.K_UP] and y-self.step >= 0:
                y -= self.step
            if keys[pg.K_DOWN] and y+self.step <= self.height:
                y += self.step

            process_img(self.screen, self.screen_size, self.image, self.step, x, y, self.folder)

            pg.display.flip()

