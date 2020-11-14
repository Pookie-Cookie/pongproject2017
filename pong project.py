from tkinter import *
from tkinter import ttk


#Creating GUI class
class Gui:
   # initializing variables
   def __init__(self):
       self.root = Tk()
       MenuScreen(self.root)
       self.root.mainloop()


#Creating MenuScreen of the game
class MenuScreen:
   # initializing variables
   def __init__(self, root):
       self.root = root
       self.frame = Frame(self.root, bg="salmon")
       self.title = ttk.Label(self.frame, text="Pong", font=("times new roman", 100))
       self.play_button = ttk.Button(self.frame, text="Start", command=self.play_button)
       self.score_var = StringVar()
       self.score_var.set("No winner yet!")
       self.score = ttk.Label(self.frame, textvariable=self.score_var, font=("courier", 15))
       self.pack()

   # Making a function to pack MenuScreen
   def pack(self):
       self.title.pack()
       self.play_button.pack()
       self.score.pack()
       self.frame.pack()

   # Making a function to unpack MenuScreen
   def unpack(self):
       self.frame.destroy()

   # Making a button to unpack MenuScreen and after that, pack GameScreen.
   def play_button(self):
       self.unpack()
       GameScreen(self.root)

   # Make a function to update the winner
   def score(self, winner):
       if winner:
           self.score_var.set("Player 1 Wins!")
       else:
           self.score_var.set("Player 2 Wins!")


#Creating GameScreen
class GameScreen:
   # initializing variables, including creating canvas and the other components such as ball and paddles
   def __init__(self, root):
       self.root = root
       self.height = 600
       self.width = 800
       self.canvas = Canvas(self.root, height=self.height, width=self.width)
       self.ball = Ball(self.canvas, self.height, self.width)
       self.line = self.canvas.create_line((self.width/2 - 2.5), 0,  (self.width/2 + 2.5), self.height, fill="Black", dash=(5, 5))
       self.frame = ttk.Frame(self.root)
       self.restart_button = ttk.Button(self.frame, text="Restart", command=self.restart)
       self.quit_button = ttk.Button(self.frame, text="Quit", command=self.quit)
       self.paddle1 = Paddle(self.canvas, 50)
       self.paddle2 = Paddle(self.canvas, self.width-75)
       self.pack()
       self.end_game = False
       self.loop = None
       self.player1_winner = None
       self.up = None
       self.ball_collision = False
       self.root.bind_all('<KeyPress>', lambda event: self.on_keypress(self.paddle1, self.paddle2, event))
       self.root.bind_all('<KeyRelease>', lambda event: self.on_keyrelease(self.paddle1, self.paddle2, event))
       self.movement()
       self.root.mainloop()

   # Make a function to combine the movement functions of the paddles and the ball.
   def movement(self):
       if self.paddle1.get_coords()[1] <= 0 and self.up:
           pass
       elif self.paddle1.get_coords()[1] >= self.height-200 and not self.up:
           pass
       else:
           self.paddle1.move()
       if self.paddle2.get_coords()[1] <= 0 and self.up:
           pass
       elif self.paddle2.get_coords()[1] >= self.height-200 and not self.up:
           pass
       else:
           self.paddle2.move()
       # Ending the game when the ball collides with the paddle
       self.ball.ball_move(self.collision())
       self.win_or_lose()
       if self.end_game:
           self.root.after_cancel(self.loop)
           self.unpack()
           MenuScreen.score(MenuScreen(self.root), self.player1_winner)
       else:
           self.loop = self.root.after(16, self.movement)

   # Make a function to move the paddles horizontally
   def on_keypress(self, item1, item2, event):
       if event.keysym == "Down":
           item2.y_vel = 5
           self.up = False
       if event.keysym == "Up":
           item2.y_vel = -5
           self.up = True
       if event.keysym == "w":
           item1.y_vel = -5
           self.up = True
       if event.keysym == "s":
           item1.y_vel = 5
           self.up = False

   # Make a function to end the game when the ball collides with one of the paddle, unpacking and packing MenuScreen
   #  to reset.
   def win_or_lose(self):
       if self.ball.get_ball_coords()[0] > self.width:
           self.end_game = True
           self.player1_winner = True
       elif self.ball.get_ball_coords()[0] < -self.ball.radius * 2:
           self.end_game = True
           self.player1_winner = False
       return self.player1_winner

   # Make a function to stop moving the paddle when the key is released
   def on_keyrelease(self, item1, item2, event):
       item1.y_vel = 0
       item2.y_vel = 0

   # Make a function to quit the program
   def quit(self):
       exit()

   # Make a function to quit the game and restart the game
   def restart(self):
       self.root.after_cancel(self.loop)
       self.unpack()
       MenuScreen(self.root)

   # Make a function to pack GameScreen class
   def pack(self):
       self.restart_button.pack()
       self.quit_button.pack()
       self.canvas.pack()
       self.frame.pack()

   # Make a function to destroy the GameScreen class
   def unpack(self):
       self.canvas.destroy()
       self.frame.destroy()

   # Make a function to check whether the ball collides with one of the paddle
   def collision(self):
       if self.ball.ball in self.paddle1.overlap() or self.ball.ball in self.paddle2.overlap():
           self.ball_collision = True
       else:
           self.ball_collision = False
       return self.ball_collision


# Create a class to create a ball in the game
class Ball:
   # initializing variables
   def __init__(self, canvas, height, width):
       self.x_vel = 5
       self.y_vel = 5
       self.x = 200
       self.y = 200
       self.height = height
       self.width = width
       self.radius = 15
       self.canvas = canvas
       self.ball = canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y + self.radius)

   # return the co-ordinates of the ball
   def get_ball_coords(self):
       return int(self.canvas.coords(self.ball)[0]), int(self.canvas.coords(self.ball)[1])

   # Make a function to make the ball moving
   # Change the direction of the ball when the ball collides with the wall or one of the paddles
   def ball_move(self, ball_collide):
       # check if ball collides with paddle
       if ball_collide:
           # if the ball collides with the paddle, change its direction to the opposite direction
           self.x_vel *= -1
       # if the ball doesn't collide with the paddle, keep moving the ball
       else:
           x_cord, y_cord = self.get_ball_coords()
           if y_cord <= 0:
               self.y_vel = 5
           elif y_cord >= self.height-15:
               self.y_vel = -5
       if abs(self.x_vel) + abs(self.y_vel) > 0:
           self.canvas.move(self.ball, self.x_vel, self.y_vel)


# def __init__(self, parent, x, y, width, height, x_vel, y_vel, fill, outline):
class Paddle:
   # initializing variables
   def __init__(self, parent, x):
       self.x = x
       self.y = 200
       self.y_vel = 0
       self.x_vel = 0
       self.canvas = parent
       height = 100
       width = 20
       self.paddle = parent.create_rectangle(x, self.y, x + width, self.y + height, fill="Blue")
       self.get_coords()

   # move the paddle by y velocity, up.
   def move(self):
       if abs(self.y_vel) > 0:
           self.canvas.move(self.paddle, self.x_vel, self.y_vel)

   # return the co-ordinates of the paddle
   def get_coords(self):
       return self.canvas.coords(self.paddle)

   # return what overlaps with the paddle
   def overlap(self):
       return self.canvas.find_overlapping(*self.get_coords())


Gui()

