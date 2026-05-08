class Bricks:
    def __init__(self, canvas):
        self.canvas = canvas
        self.bricks = []

        self.create_bricks()

    def create_bricks(self):
        rows = 6
        cols = 10

        brick_width = 60
        brick_height = 20
        padding = 10

        start_x = 30
        start_y = 30

        for row in range(rows):
            for col in range(cols):
                x1 = start_x + col * (brick_width + padding)
                y1 = start_y + row * (brick_height + padding)
                x2 = x1 + brick_width
                y2 = y1 + brick_height

                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="blue"
                )

                self.bricks.append(brick)