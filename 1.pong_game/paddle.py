from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.shapesize(5, 1)
        self.penup()
        self.goto(position)

    def move_up(self):
        y = self.ycor() + 30
        if y < 250:
            self.goto(self.xcor(), y)

    def move_down(self):
        y = self.ycor() - 30
        if y > -250:
            self.goto(self.xcor(), y)
