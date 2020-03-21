from tkinter import *
from PIL import Image
import os
import math

BUTTON_WIDTH = 5

class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.setUI()
        self.brush_size = 2
        self.color = "black"
        self.branch_angle = 0
        self.branch_size = 1
        self.branch_points = [(1, 0), (1, -20), (-1, -20), (-1, 0)]
        self.branch_center = (0, -10)
        self.leaf_angle = 0
        self.leaf_size = 1
        self.leaf_points = [(0, 0), (5, -5), (5, -15), (0, -20), (-5, -15), (-5, -5)]
        self.leaf_center = (0, -20)

    def setUI(self):
        self.parent.title("Генеалогическое древо")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(24, weight=1)
        self.rowconfigure(3, weight=1)

        self.canv = Canvas(self, bg="white")
        self.canv.grid(row=3, column=0, columnspan=25,
                       padx=5, pady=5,
                       sticky=E + W + S + N)
        self.canv.bind("<B1-Motion>", self.draw)

        # Лейбл для веток
        branch_lab = Label(self, text="Ветки:")
        branch_lab.grid(row=0, column=0, padx=6)

        # Ветка
        btn_branch = Button(self, text="Ветка", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.draw_branch))
        btn_branch.grid(row=0, column=1)

        # Лейбл угла наклона ветки
        angle_lab = Label(self, text="Угол:")
        angle_lab.grid(row=0, column=2, padx=6)

        # Кнопки, задающие разный угол наклона ветки
        btn__30 = Button(self, text="-30", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_angle(-30)))
        btn__30.grid(row=0, column=3)

        btn__10 = Button(self, text="-10", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_angle(-10)))
        btn__10.grid(row=0, column=4)

        btn__5 = Button(self, text="-5", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_angle(-5)))
        btn__5.grid(row=0, column=5)

        btn_5 = Button(self, text="5", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_angle(5)))
        btn_5.grid(row=0, column=6)

        btn_10 = Button(self, text="10", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_angle(10)))
        btn_10.grid(row=0, column=7)

        btn_30 = Button(self, text="30", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_angle(30)))
        btn_30.grid(row=0, column=8)

        # Лейбл размера ветки
        branch_size_lab = Label(self, text="Размер:")
        branch_size_lab.grid(row=0, column=9, padx=6)

        # Ветки разного размера
        btn_2 = Button(self, text="Увеличить в 2 раза", width=15, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_size(2)))
        btn_2.grid(row=0, column=10)

        btn_3 = Button(self, text="Увеличить в 3 раза", width=15, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_size(3)))
        btn_3.grid(row=0, column=11)

        btn_5 = Button(self, text="Увеличить в 5 раз", width=15, command=lambda: self.canv.bind("<B1-Motion>", self.set_branch_size(5)))
        btn_5.grid(row=0, column=12)

        btn_reset_branch = Button(self, text="Сбросить", width=15, command=self.reset_branch)
        btn_reset_branch.grid(row=0, column=13)

        # Лейбл для листьев
        leaf_lab = Label(self, text="Листья:")
        leaf_lab.grid(row=1, column=0, padx=6)

        # Кнопка для листьев
        leaf_btn = Button(self, text="Лист", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.draw_leaf))
        leaf_btn.grid(row=1, column=1)

        # Лейбл угла поворота листьев
        leaf_angle_lab = Label(self, text="Угол:")
        leaf_angle_lab.grid(row=1, column=2, padx=6)

        # Угол поворота листьев
        btn_leaf__30 = Button(self, text="-30", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_angle(-30)))
        btn_leaf__30.grid(row=1, column=3)

        btn_leaf__10 = Button(self, text="-10", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_angle(-10)))
        btn_leaf__10.grid(row=1, column=4)

        btn_leaf__5 = Button(self, text="-5", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_angle(-5)))
        btn_leaf__5.grid(row=1, column=5)

        btn_leaf_5 = Button(self, text="5", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_angle(5)))
        btn_leaf_5.grid(row=1, column=6)

        btn_leaf_10 = Button(self, text="10", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_angle(10)))
        btn_leaf_10.grid(row=1, column=7)

        btn_leaf_30 = Button(self, text="30", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_angle(30)))
        btn_leaf_30.grid(row=1, column=8)

        # Лейбл размера листьев
        leaf_size_lab = Label(self, text="Размер:")
        leaf_size_lab.grid(row=1, column=9)

        # Задаем разные размеры листа
        btn_leaf_2 = Button(self, text="Увеличить в 2 раза", width=15, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_size(2)))
        btn_leaf_2.grid(row=1, column=10)

        btn_leaf_3 = Button(self, text="Увеличить в 3 раза", width=15, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_size(3)))
        btn_leaf_3.grid(row=1, column=11)

        btn_leaf_5 = Button(self, text="Увеличить в 5 раз", width=15, command=lambda: self.canv.bind("<B1-Motion>", self.set_leaf_size(5)))
        btn_leaf_5.grid(row=1, column=12)

        # Сброс
        btn_reset_leaf = Button(self, text="Сбросить", width=15, command=self.reset_leaf)
        btn_reset_leaf.grid(row=1, column=13)

        # Определяем кисть
        lab = Label(self, text="Кисть:")
        lab.grid(row=2, column=0, padx=6)

        brush_btn = Button(self, text="Кисть", width=BUTTON_WIDTH, command=lambda: self.canv.bind("<B1-Motion>", self.draw))
        brush_btn.grid(row=2, column=1)

        # Цвет
        color_lab = Label(self, text="Цвет:")
        color_lab.grid(row=2, column=2, padx=6)

        brown_btn = Button(self, text="Коричневый", width=8, command=lambda: self.set_color("brown"))
        brown_btn.grid(row=2, column=3)

        green_btn = Button(self, text="Зеленый", width=7, command=lambda: self.set_color("green"))
        green_btn.grid(row=2, column=4)

        black_btn = Button(self, text="Черный", width=7, command=lambda: self.set_color("black"))
        black_btn.grid(row=2, column=5)

        white_btn = Button(self, text="Белый", width=7, command=lambda: self.set_color("white"))
        white_btn.grid(row=2, column=6)

        # Размер кисти
        size_lab = Label(self, text="Размер кисти:")
        size_lab.grid(row=2, column=7, padx=6)

        one_btn = Button(self, text="1", width=BUTTON_WIDTH, command=lambda: self.set_brush_size(1))
        one_btn.grid(row=2, column=8)

        two_btn = Button(self, text="2", width=BUTTON_WIDTH, command=lambda: self.set_brush_size(2))
        two_btn.grid(row=2, column=9)

        five_btn = Button(self, text="5", width=BUTTON_WIDTH, command=lambda: self.set_brush_size(5))
        five_btn.grid(row=2, column=10)

        ten_btn = Button(self, text="10", width=BUTTON_WIDTH, command=lambda: self.set_brush_size(10))
        ten_btn.grid(row=2, column=11)

        twenty_btn = Button(self, text="20", width=BUTTON_WIDTH, command=lambda: self.set_brush_size(20))
        twenty_btn.grid(row=2, column=12)

        clear_btn = Button(self, text="Очистить все", width=15, command=lambda: self.canv.delete("all"))
        clear_btn.config(bg="red")
        clear_btn.grid(row=2, column=13, sticky=W)

        save_btn = Button(self, text="Сохранить", width=15, command=self.save_as_png)
        save_btn.config(bg="red")
        save_btn.grid(row=2, column=14)


    def draw(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill=self.color, outline=self.color)

    def set_color(self, new_color):
        self.color = new_color

    def set_brush_size(self, new_size):
        self.brush_size = new_size

    def save_as_png(self,fileName='image'):
        self.canv.postscript(file = fileName + '.eps')
        img = Image.open(fileName + '.eps')
        img.save(fileName + '.png', 'png')
        os.remove(fileName + '.eps')

    def reset_branch(self):
        self.branch_points = [(1, 0), (1, -20), (-1, -20), (-1, 0)]
        self.branch_size = 1
        self.branch_angle = 0
        self.branch_center = (0, -10)

    def draw_branch(self, event):
        points = []
        for x, y in self.branch_points:
            points.append((event.x + x, event.y + y))
        self.canv.create_polygon(points, outline='black', fill='brown', width=1)

    def set_branch_size(self, size):
        resized = resize(self.branch_points, size)
        center = (self.branch_center[0] * size, self.branch_center[1] * size)
        self.branch_center = center
        self.branch_size = size
        self.branch_points = resized

    def set_branch_angle(self, angle):
        rotated = rotate(self.branch_points, angle, self.branch_center)
        self.branch_angle = angle
        self.branch_points = rotated

    def reset_leaf(self):
        self.leaf_points = [(0, 0), (5, -5), (5, -15), (0, -20), (-5, -15), (-5, -5)]
        self.leaf_center = (0, -20)
        self.leaf_size = 1
        self.leaf_angle = 0

    def draw_leaf(self, event):
        points = []
        for x, y in self.leaf_points:
            points.append((event.x + x, event.y + y))
        self.canv.create_polygon(points, outline='black', fill='green', width=1)

    def set_leaf_size(self, size):
        resized = resize(self.leaf_points, size)
        center = (self.leaf_center[0] * size, self.leaf_center[1] * size)
        self.leaf_center = center
        self.leaf_size = size
        self.leaf_points = resized

    def set_leaf_angle(self, angle):
        rotated = rotate(self.leaf_points, angle, self.leaf_center)
        self.leaf_angle = angle
        self.leaf_points = rotated

def resize(points, k):
    new_points = []
    for x, y in points:
        new_points.append((x * k, y * k))
    return new_points

def rotate(points, angle, center):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center
    new_points = []
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    return new_points


def main():
    root = Tk()
    root.geometry("1920x1080+300+300")
    app = Paint(root)
    root.mainloop()


if __name__ == "__main__":
    main()