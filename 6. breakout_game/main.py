import tkinter as tk
from ball import Ball
from paddle import Paddle
from bricks import Bricks
from scores import Score

root = tk.Tk()
root.title("Breakout Game")

canvas = tk.Canvas(root, width=750, height=500, bg="black")
canvas.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

restart_btn = tk.Button(
    button_frame,
    text="Restart",
    bg="green",
    fg="white",
    width=12,
    command=lambda: setup_game()
)
restart_btn.pack()

canvas.update()

ball = None
paddle = None
bricks = None
score = None
game_running = False

def setup_game():
    global ball, paddle, bricks, score, game_running
    canvas.delete("all")

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    paddle = Paddle(canvas, canvas_width // 2, canvas_height - 30)
    ball = Ball(canvas, canvas_width // 2, canvas_height // 2)
    bricks = Bricks(canvas)
    score = Score(canvas)
    game_running = True

def game_loop():
    global game_running
    if not game_running:
        return

    game_running = ball.move(paddle, bricks, score)
    paddle.move()

    if game_running:
        root.after(20, game_loop)

setup_game()
game_loop()
root.mainloop()
