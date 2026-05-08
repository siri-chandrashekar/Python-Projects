
class Ball:
    def __init__(self, canvas, x, y):
        self.canvas = canvas

        # Create ball
        self.id = canvas.create_oval(x-10, y-10, x+10, y+10, fill="white")

        # Movement direction
        self.x_velocity = 3
        self.y_velocity = -3

    def move(self, paddle, bricks, score):
        self.canvas.move(self.id, self.x_velocity, self.y_velocity)

        pos = self.canvas.coords(self.id)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Left & Right wall bounce
        if pos[0] <= 0 or pos[2] >= canvas_width:
            self.x_velocity = -self.x_velocity

        # Top wall bounce
        if pos[1] <= 0:
            self.y_velocity = -self.y_velocity
        
        # Paddle collision
        if self.hit_paddle(pos, paddle) and self.y_velocity > 0:
            self.y_velocity = -self.y_velocity
        
        # Brick collision
        self.hit_brick(pos, bricks, score)

        if len(bricks.bricks) == 0:
            self.canvas.create_text(
                canvas_width / 2,
                canvas_height / 2,
                text="YOU WIN!",
                fill="lime",
                font=("Arial", 24)
            )
            return False

        # Bottom (game over)
        if pos[3] >= canvas_height:
            self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 2,
            text="GAME OVER",
            fill="red",
            font=("Arial", 24)
        )
            return False  # stop game
        return True

    def hit_paddle(self, pos, paddle):
        paddle_pos = self.canvas.coords(paddle.id)

        # Check overlap
        if (
            pos[2] >= paddle_pos[0] and   # ball right >= paddle left
            pos[0] <= paddle_pos[2] and   # ball left <= paddle right
            pos[3] >= paddle_pos[1] and   # ball bottom >= paddle top
            pos[1] <= paddle_pos[3]       # ball top <= paddle bottom
        ):
            return True
        return False
    

    def hit_brick(self, pos, bricks, score):
        for brick in bricks.bricks:
            brick_pos = self.canvas.coords(brick)

            # Check overlap
            if (
                pos[2] >= brick_pos[0] and
                pos[0] <= brick_pos[2] and
                pos[3] >= brick_pos[1] and
                pos[1] <= brick_pos[3]
            ):
                # Remove brick
                self.canvas.delete(brick)
                bricks.bricks.remove(brick)

                score.update()

                # Bounce
                self.y_velocity = -self.y_velocity

                self.increase_speed()

                break

    def increase_speed(self):
        if self.x_velocity > 0:
            self.x_velocity += 0.2
        else:
            self.x_velocity -= 0.2

        if self.y_velocity > 0:
            self.y_velocity += 0.2
        else:
            self.y_velocity -= 0.2
