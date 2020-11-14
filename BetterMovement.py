from tkinter import *

x = 10
y = 10
width = 100
height = 100
x_vel = 0
y_vel = 0

def move():
    global x_vel
    global y_vel
    if abs(x_vel) + abs(y_vel) > 0:
        canvas1.move(rect, x_vel, y_vel)
    window.after(16, move)

def on_keypress(event):
    print(event.keysym)
    global x_vel
    global y_vel
    if event.keysym == "Left":
        x_vel = -5
    if event.keysym == "Right":
        x_vel = 5
    if event.keysym == "Down":
        y_vel = 5
    if event.keysym == "Up":
        y_vel = -5

def on_keyrelease(event):
    global x_vel
    global y_vel
    print("release", event.keysym, "Xvel", x_vel, "Yvel", y_vel)
    if event.keysym in ["Left", "Right"]:
        x_vel = 0
    else:
        y_vel = 0


window = Tk()
window.geometry("600x600")

#canvas and drawing
canvas1 = Canvas(window, height=600, width=600)
canvas1.grid(row=0, column=0, sticky=W)
coord = [x, y, width, height]
rect = canvas1.create_rectangle(*coord, outline="#fb0", fill="#fb0")

#capturing keyboard inputs and assigning to function
window.bind_all('<KeyPress>', on_keypress)
window.bind_all('<KeyRelease>', on_keyrelease)
move()
window.mainloop()
