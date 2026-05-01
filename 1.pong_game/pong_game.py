import time
from turtle import Screen

from ball import Ball
from centerline import Centerline
from paddle import Paddle
from scoreboard import Scoreboard

RIGHT_PADDLE_POSITION = (350, 0)
LEFT_PADDLE_POSITION = (-350, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    screen = Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.bgcolor("black")
    screen.title("My Pong Game")
    screen.listen()
    screen.tracer(0)

    right_paddle = Paddle(RIGHT_PADDLE_POSITION)
    left_paddle = Paddle(LEFT_PADDLE_POSITION)

    screen.onkey(right_paddle.move_up, "Up")
    screen.onkey(right_paddle.move_down, "Down")
    screen.onkey(left_paddle.move_up, "w")
    screen.onkey(left_paddle.move_down, "s")

    ball = Ball()
    scoreboard = Scoreboard()
    Centerline()

    game_is_on = True
    while game_is_on:
        screen.update()
        time.sleep(ball.speedball)
        ball.move()

        if ball.ycor() > 280 or ball.ycor() < -280:
            ball.bounce_y()

        if (
            ball.distance(right_paddle) < 50 and ball.xcor() > 320
        ) or (
            ball.distance(left_paddle) < 50 and ball.xcor() < -320
        ):
            ball.bounce_x()

        if ball.xcor() > 400:
            scoreboard.left_scores()
            ball.reset_position()

        if ball.xcor() < -400:
            scoreboard.right_scores()
            ball.reset_position()

    screen.exitonclick()


if __name__ == "__main__":
    main()
