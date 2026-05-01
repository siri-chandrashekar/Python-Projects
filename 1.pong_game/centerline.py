from turtle import Turtle


class Centerline(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.pencolor("white")
        self.penup()
        self.goto(0, 290)
        self.setheading(270)
        self.pendown()
        for _ in range(15):
            self.forward(20)
            self.penup()
            self.forward(20)
            self.pendown()
