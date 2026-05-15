import turtle
import random
import time

window = turtle.Screen()
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("The Real Python Space Invaders")
window.tracer(0)

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
CANNON_STEP = 10
GUTTER = 0.05 * window.window_width()
LASER_LENGTH = 20
LASER_SPEED = 10
ALIEN_SPAWN_INTERVAL = 1.2  # Seconds
MAX_ALIENS = 7
INITIAL_ALIEN_SPEED = 1
ALIEN_SPEED = INITIAL_ALIEN_SPEED
game_running = True
lasers = []
aliens = []

score = 0
game_over_turtle = None
restart_button = None
restart_bounds = None

score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.color("white")
score_writer.goto(0, TOP - 40)
score_writer.write(f"Score: {score}", align="center", font=("Arial", 16, "bold"))


def update_score():
    score_writer.clear()
    score_writer.write(f"Score: {score}", align="center", font=("Arial", 16, "bold"))


def show_restart_button():
    global restart_button, restart_bounds
    if restart_button is not None:
        return

    restart_button = turtle.Turtle()
    restart_button.hideturtle()
    restart_button.penup()
    restart_button.goto(0, -30)
    restart_button.shape("square")
    restart_button.shapesize(stretch_wid=1.2, stretch_len=4.2)
    restart_button.fillcolor("black")
    restart_button.pencolor("white")
    restart_button.showturtle()
    restart_button.onclick(restart_game)
    # Backup hitbox via screen click in case turtle onclick misses.
    half_width = 42
    half_height = 12
    restart_bounds = (-half_width, -30 - half_height, half_width, -30 + half_height)

    label = turtle.Turtle()
    label.hideturtle()
    label.penup()
    label.color("white")
    label.goto(0, -40)
    label.write("RESTART", align="center", font=("Arial", 12, "bold"))
    restart_button.label = label


def hide_restart_button():
    global restart_button, restart_bounds
    if restart_button is None:
        return

    restart_button.hideturtle()
    restart_button.onclick(None)
    restart_button.label.clear()
    restart_button.label.hideturtle()
    restart_button = None
    restart_bounds = None


def handle_screen_click(x, y):
    if game_running or restart_bounds is None:
        return
    left, bottom, right, top = restart_bounds
    if left <= x <= right and bottom <= y <= top:
        restart_game()


def reset_player_position():
    base.setposition(0, FLOOR_LEVEL)
    cannon.setposition(0, FLOOR_LEVEL + 20)


def clear_projectiles_and_aliens():
    for laser in lasers:
        laser.clear()
        laser.hideturtle()
    lasers.clear()

    for alien in aliens:
        alien.hideturtle()
    aliens.clear()


def restart_game(x=None, y=None):
    global game_running, score, ALIEN_SPEED, game_over_turtle

    hide_restart_button()
    clear_projectiles_and_aliens()
    reset_player_position()

    score = 0
    ALIEN_SPEED = INITIAL_ALIEN_SPEED
    update_score()

    if game_over_turtle is not None:
        game_over_turtle.clear()
        game_over_turtle.hideturtle()
        game_over_turtle = None

    game_running = True
    window.update()
    game_loop()


def game_over():
    global game_running, game_over_turtle
    game_running = False
    game_over_turtle = turtle.Turtle()
    game_over_turtle.hideturtle()
    game_over_turtle.color("red")
    game_over_turtle.penup()
    game_over_turtle.goto(0, 20)
    game_over_turtle.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
    show_restart_button()


def draw_turtles():
    # base
    base.penup()
    base.shape("square")
    base.shapesize(1, 3)
    base.color("white")
    base.setposition(0, FLOOR_LEVEL)

    # cannon
    cannon.penup()
    cannon.color("white")
    cannon.shape("triangle")
    cannon.shapesize(1, 2)
    cannon.setheading(90)
    cannon.setposition(0, FLOOR_LEVEL + 20)


def move_left():
    new_base = base.xcor() - CANNON_STEP
    new_cann = cannon.xcor() - CANNON_STEP
    if new_base >= LEFT + GUTTER or new_cann >= LEFT + GUTTER:
        base.setx(new_base)
        cannon.setx(new_cann)
    window.update()


def move_right():
    new_base = base.xcor() + CANNON_STEP
    new_cann = cannon.xcor() + CANNON_STEP
    if new_base <= RIGHT - GUTTER or new_cann <= RIGHT - GUTTER:
        base.setx(new_base)
        cannon.setx(new_cann)
    window.update()


def shoot_lasers():
    if not game_running:
        return

    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    # Prepare to draw the laser
    laser.pendown()
    laser.pensize(5)
    laser.forward(10)  # small visible line

    lasers.append(laser)
    window.update()


def move_laser(laser):
    laser.clear()  # erase old laser
    laser.penup()
    laser.sety(laser.ycor() + LASER_SPEED)

    laser.pendown()
    laser.forward(LASER_LENGTH)


def is_collision(t1, t2):
    return t1.distance(t2) < 20


def game_loop():
    if not game_running:
        return

    for laser in lasers[:]:
        move_laser(laser)

        # Remove if out of bounds
        if laser.ycor() > TOP:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)
            continue

        # detect collision
        for alien in aliens[:]:
            if is_collision(alien, laser):
                # Remove both
                laser.clear()
                laser.hideturtle()
                if laser in lasers:
                    lasers.remove(laser)

                alien.hideturtle()
                aliens.remove(alien)

                # score
                global score, ALIEN_SPEED
                score += 10
                update_score()
                # increase difficulty every 50 points
                if score % 50 == 0:
                    ALIEN_SPEED += 0.2

                break  # stop checking this laser

    # Move aliens
    for alien in aliens[:]:
        alien.sety(alien.ycor() - ALIEN_SPEED)

        # game over
        if alien.ycor() < FLOOR_LEVEL:
            game_over()
            return

        if alien.ycor() < BOTTOM:
            alien.hideturtle()
            aliens.remove(alien)

    window.update()
    window.ontimer(game_loop, 30)


def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(
        random.randint(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)


def spawn_aliens():
    if game_running and len(aliens) < MAX_ALIENS:
        create_alien()

    # random delay (in milliseconds)
    delay = random.randint(500, 2000)
    window.ontimer(spawn_aliens, delay)


base = turtle.Turtle()
cannon = turtle.Turtle()

draw_turtles()
window.update()

window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(shoot_lasers, "space")
window.onkeypress(turtle.bye, "q")
window.onkeypress(restart_game, "r")
window.onclick(handle_screen_click)
window.listen()

game_loop()
spawn_aliens()

turtle.done()
