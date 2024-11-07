from random import random, choice
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from tkinter import ttk
from PIL import ImageTk, Image
import os
import time, threading


WINDOW_HEIGHT = 900
WINDOW_WIDTH = 820
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

# Setup the window
window = tk.Tk()
window.title("Image Slideshow")
window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
window.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

#global variables used throughout the program
filename = ''
path = ''
file_list = []
get_random_img = False

def browse_files():
    global filename, path
    if len(path) == 0:
        path = Path.cwd()
        filename = filedialog.askopenfilename(initialdir=f'{path}', title='Select a File',
                    filetypes=(('all files', '*.*'), ('Text files', '*.txt*'), ('jpeg', '*.jpg*')))
        path = os.path.split(filename)[0]
        load_images()
        load_image_from_file()


def load_images():
    global file_list, path
    for path, subdirs, files in os.walk(path):
        for filename in files:
            f = os.path.join(path, filename)
            file_list.append(f)

def load_image_from_file():
    global canvas

    if len(filename) == 0: return

    img = open_image()
    img = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_container, image=img)
    canvas.imgref = img

def open_image():
    loaded_image = Image.open(filename)
    # Resize the image
    canvas_width = CANVAS_WIDTH
    canvas_height = CANVAS_HEIGHT
    image_width = loaded_image.width
    image_height = loaded_image.height
    if image_height < image_width:
        proportion = canvas_height / image_width
    else:
        proportion = canvas_height / image_height
    image_width = int(image_width * proportion)
    image_height = int(image_height * proportion)
    img = loaded_image.resize((image_width, image_height))

    return img

timer_length = 3
def time_adjust(value):
    global timer_length
    timer_length = int(value)

slide_show_status = False
def start_slideshow():
    global slide_show_status
    slide_show_status = True
    auto_forward()

def end_slideshow():
    global slide_show_status
    slide_show_status = False

def auto_forward():
    next_image_num(1)
    if slide_show_status:
        threading.Timer(timer_length, auto_forward).start()

def next_image_num(direction: int):
    global image_num, get_random_img
    image_num += direction

    if image_num > 0:
        image_num = len(file_list) - 1
    elif image_num > len(file_list) - 1:
        image_num = 0
    next_image()

def next_image():
    global image_container, canvas, image_num, pic_label, get_random_img

    if get_random_img:
        image_num = choice(range(len(file_list)))
    load = Image.open(file_list[image_num])

    #filename = file_list[image_num]
    pic_label.config(text=file_list[image_num])

    #load_image_from_file()
    canvas_width = CANVAS_WIDTH
    canvas_height = CANVAS_HEIGHT
    image_width = load.width
    image_height = load.height
    if image_height < image_width:
        proportion = canvas_width / image_width
    else:
        proportion = canvas_height / image_height
    image_width = int(image_width * proportion)
    image_height = int(image_height * proportion)
    img = load.resize((image_width, image_height))
    img = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_container, image=img)
    canvas.imgref = img


random_checked = tk.BooleanVar()
def flag_random():
    global random_checked, get_random_img
    get_random_img = random_checked.get()

def build_compontents():
    global image_num, pic_label, canvas, image_container

    #Menu
    menu = tk.Menu(window)
    window.config(menu=menu)

    file_menu = tk.Menu(menu)
    menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Open', command=browse_files)

    #Build a canvas for the image
    canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=CANVAS_HEIGHT,
                       highlightcolor='blue', highlightbackground='blue',
                       highlightthickness=5)
    image_container = canvas.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
    canvas.grid(row=0, column=0, columnspan=6)
    image_num = -1

    #Label for the file name of the image
    pic_label = tk.Label(text='The name of the image')
    pic_label.grid(row=1, column=0, columnspan=6)

    #Allow the user to display slides in order or randomly
    random_check_box = tk.Checkbutton(text='Random', variable=random_checked,
                                      onvalue=True, offvalue=False,
                                      command=flag_random)

    random_check_box.grid(row=2, column=0)
    prev_button = tk.Button(text='Prev', command=lambda: next_image_num(-1))
    prev_button.grid(row=2, column=1)
    next_button = tk.Button(text='Next', command=lambda: next_image_num(1))
    next_button.grid(row=2, column=2)
    slide_show_start_button = tk.Button(command=start_slideshow,
                                        text='Start Slideshow')
    slide_show_start_button.grid(row=3, column=3)
    slide_show_end_button = tk.Button(command=end_slideshow,
                                      text='Stop Slideshow')
    slide_show_end_button.grid(row=2, column=4)
    slide_show_timer_adjust = tk.Scale(from_=1, to=10, command=time_adjust,
                                       orient=tk.HORIZONTAL, width=10,
                                       length=150, sliderlength=10,
                                       tickinterval=1)
    slide_show_timer_adjust.set(3)
    slide_show_timer_adjust.grid(row=2, column=5)

#build all the componetns
build_compontents()


# keep window open
window.mainloop()

