import tkinter as tk
from tkinter import Menu
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk, ImageOps


class SubWindow:
    def __init__(self, image, root):
        self.cropped_image_window = tk.Toplevel(root)
        self.cropped_image_window.geometry("300x150")
        self.image_original = image
        self.image_on_screen = self.image_original
        self.num_of_colors = 256
        self.resolution = 128
        self.should_equalize_image = False

        self.cropped_image_menu = Menu(self.cropped_image_window)
        self.cropped_image_window.config(menu=self.cropped_image_menu)

        self.resolution_submenu = Menu(self.cropped_image_menu, tearoff=0)
        self.cropped_image_menu.add_cascade(label='Resolução', menu=self.resolution_submenu)
        self.resolution_submenu.add_command(label='128 x 128', command=lambda: self.change_resolution(128))
        self.resolution_submenu.add_command(label='64 x 64', command=lambda: self.change_resolution(64))
        self.resolution_submenu.add_command(label='32 x 32', command=lambda: self.change_resolution(32))
        self.resolution_submenu.add_command(label='16 x 16', command=lambda: self.change_resolution(16))
        self.resolution_submenu.add_command(label='8 x 8', command=lambda: self.change_resolution(8))
        self.resolution_submenu.add_command(label='4 x 4', command=lambda: self.change_resolution(4))
        self.resolution_submenu.add_command(label='2 x 2', command=lambda: self.change_resolution(2))

        self.quantize_submenu = Menu(self.cropped_image_menu, tearoff=0)
        self.cropped_image_menu.add_cascade(label='Quantização', menu=self.quantize_submenu)
        self.quantize_submenu.add_command(label='256', command=lambda: self.change_quantize(256))
        self.quantize_submenu.add_command(label='32', command=lambda: self.change_quantize(32))
        self.quantize_submenu.add_command(label='16', command=lambda: self.change_quantize(16))
        self.quantize_submenu.add_command(label='8', command=lambda: self.change_quantize(8))
        self.quantize_submenu.add_command(label='4', command=lambda: self.change_quantize(4))
        self.quantize_submenu.add_command(label='2', command=lambda: self.change_quantize(2))

        self.cropped_image_menu.add_command(label='Equalizar', command= self.equalize_image)

        self.cropped_image_menu.add_command(label='Reset', command=self.reset)
        self.canvas = tk.Canvas(self.cropped_image_window, width=128, height=128)

        self.photo_image = ImageTk.PhotoImage(self.image_on_screen)
        self.image_canvas = self.canvas.create_image(0, 0, image=self.photo_image, anchor='nw')
        self.canvas.pack()
        self.cropped_image_window.mainloop()

    def change_quantize(self, colors):
        self.num_of_colors = colors
        self.re_draw()

    def change_resolution(self, resolution):
        self.resolution = resolution
        self.re_draw()

    def equalize_image(self):
        self.should_equalize_image = True
        self.re_draw()

    def re_draw(self):
        self.image_on_screen = self.image_original.quantize(colors=self.num_of_colors)
        self.image_on_screen = self.image_on_screen.resize((self.resolution, self.resolution))
        self.image_on_screen = self.image_on_screen.resize((128, 128))

        if self.should_equalize_image:
            self.image_on_screen = ImageOps.equalize(self.image_on_screen)

        self.photo_image = ImageTk.PhotoImage(self.image_on_screen)
        self.image_canvas = self.canvas.create_image(0, 0, image=self.photo_image, anchor='nw')

    def reset(self):
        self.num_of_colors = 256
        self.resolution = 128
        self.should_equalize_image = False
        self.re_draw()




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
        self.selection_enabled = False
        self.selection_rect = None

        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)
        submenu = Menu(self.menu, tearoff=0)

        self.menu.add_command(label='Abrir Imagem', command=self.open_image)
        self.menu.add_command(label='Zoom In', command=self.zoom_in)
        self.menu.add_command(label='Zoom Out', command=self.zoom_out)
        self.menu.add_command(label='Reset Zoom', command=self.reset_zoom)
        self.menu.add_command(label="Selecionar Área", command=self.selection_area)

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

        # self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.window.mainloop()

    def selection_area(self):
        self.selection_enabled = not self.selection_enabled

    def on_mousewheel(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        if not self.selection_enabled:
            self.scale = self.scale * 1.2
            self.re_draw()

    def zoom_out(self):
        if not self.selection_enabled:
            self.scale = self.scale / 1.2
            self.re_draw()

    def reset_zoom(self):
        if not self.selection_enabled:
            self.scale = 1
            self.re_draw()

    def re_draw(self):
        width, height = self.image_original.size
        new_width = int(width * self.scale)
        new_height = int(height * self.scale)
        if new_width > 5000 or new_height > 5000 or new_width <= 0 or new_height <= 0:
            return
        self.image_on_screen = self.image_original.resize((new_width, new_height))
        self.photo_image = ImageTk.PhotoImage(self.image_on_screen)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor='nw')

    def open_cropped_image_window(self, image):
        SubWindow(image, self.window)

    def on_click(self, event):
        self.canvas.scan_mark(event.x, event.y)

        if self.selection_enabled:
            if self.selection_rect is not None:
                self.canvas.delete(self.selection_rect)

            x1, y1, x3, y3 = self.draw_selection_rectangle(event)

            cropped_image = self.image_on_screen.crop((x1, y1, x3, y3))

            self.open_cropped_image_window(cropped_image)

    def draw_selection_rectangle(self, event):
        x_center, y_center = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        x1, y1 = x_center - 64, y_center - 64
        x3, y3 = x_center + 64, y_center + 64
        self.selection_rect = self.canvas.create_rectangle(x1, y1, x3, y3, dash=(4, 1), outline="blue")

        return event.x - 64, event.y - 64, event.x + 64, event.y + 64

    def on_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def open_image(self):
        self.filepath = askopenfilename(
            filetypes=[("Image Files", "*.png *.tif")]
        )
        if self.filepath == '':
            return
        self.image_original = (Image.open(self.filepath)).convert("L")
        self.image_on_screen = self.image_original
        self.photo_image = ImageTk.PhotoImage(self.image_on_screen)
        self.image_canvas = self.canvas.create_image(0, 0, image=self.photo_image, anchor='nw')
        width, height = self.image_on_screen.size  # Get dimensions
        self.window.geometry(f"{width}x{height}")
        self.canvas.config(width=width, height=height)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # TODO infito


def main():
    MainWindow()


main()
