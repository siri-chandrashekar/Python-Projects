class Paddle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas

        # Create paddle (rectangle)
        self.id = canvas.create_rectangle(x-50, y-10, x+50, y+10, fill="white")

        # Movement speed
        self.x_velocity = 0

        # Key press (start moving)
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

        # Key release (stop moving)
        self.canvas.bind_all("<KeyRelease-Left>", self.stop)
        self.canvas.bind_all("<KeyRelease-Right>", self.stop)

    def move_left(self, event):
        self.x_velocity = -5

    def move_right(self, event):
        self.x_velocity = 5
    
    def stop(self, event):
        self.x_velocity = 0

    def move(self):
        self.canvas.move(self.id, self.x_velocity, 0)

        pos = self.canvas.coords(self.id)
        canvas_width = self.canvas.winfo_width()

        # Stop at left wall
        if pos[0] <= 0:
            self.x_velocity = 0
            self.canvas.move(self.id, -pos[0], 0)

        # Stop at right wall
        if pos[2] >= canvas_width:
            self.x_velocity = 0
            self.canvas.move(self.id, canvas_width - pos[2], 0)