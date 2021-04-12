import tkinter as tk
from tkinter import Menu
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk


class MainWindow:
    def __init__(self):
        # Screen
        self.window = tk.Tk()
        self.window.eval('tk::PlaceWindow . center')
        self.window.geometry("800x800")
        self.window.title("Trabalho PI")
        self.filepath = ""
        self.image_original = None
        self.photo_image = None
        self.scale = 1

        # image_original = Image.open("image.png")
        # test = ImageTk.PhotoImage(image_low)
        #
        # label1 = tk.Label(image=test)
        # label1.image = test
        #
        # # Position image
        # label1.place(x=0, y=0)

        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)
        submenu = Menu(self.menu, tearoff=0)

        self.menu.add_command(label='Abrir Imagem', command=self.open_image)
        self.menu.add_command(label='Zoom In', command=self.zoom_in)
        self.menu.add_command(label='Zoom Out', command=self.zoom_out)
        self.menu.add_command(label='Reset Zoom', command=self.reset_zoom)

        self.menu.add_cascade(label='Transformações', menu=submenu)
        submenu.add_command(label='Translação', )
        submenu.add_command(label='Rotação', )
        submenu.add_command(label='Escala', )
        submenu.add_command(label='Reflexão X')
        submenu.add_command(label='Reflexão Y', )
        submenu.add_command(label='Reflexão XY', )

        lines_menu = Menu(self.window, tearoff=0)
        self.menu.add_cascade(label='Retas', menu=lines_menu)
        lines_menu.add_command(label='DDA', )
        lines_menu.add_command(label='Bresenham', )

        self.canvas = tk.Canvas(self.window, width=800, height=800, bg='black')
        self.canvas.pack()

        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<Button-1>', self.click)
        self.window.mainloop()

    def zoom_in(self):
        self.scale = self.scale * 1.2
        self.re_draw()

    def zoom_out(self):
        self.scale = self.scale / 1.2
        self.re_draw()

    def reset_zoom(self):
        self.scale = 1
        self.re_draw()

    def re_draw(self):
        width, height = self.image_original.size
        new_width = int(width * self.scale)
        new_height = int(height * self.scale)
        if new_width > 5000 or new_height > 5000 or new_width <= 0 or new_height <= 0:
            return

        self.photo_image = ImageTk.PhotoImage(self.image_original.resize((new_width, new_height)))
        self.canvas.create_image(0, 0, image=self.photo_image, anchor='center')

    def click(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def open_image(self):
        self.filepath = askopenfilename(
            filetypes=[("Image Files", "*.png *.tif")]
        )
        if self.filepath == '':
            return
        self.image_original = Image.open(self.filepath)
        self.photo_image = ImageTk.PhotoImage(self.image_original)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor='center')
        # self.canvas.configure(scrollregion=self.canvas.bbox("all")) #TODO infito


def main():
    MainWindow()


main()
