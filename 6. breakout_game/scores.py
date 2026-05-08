class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0

        # Display text on top
        self.text = canvas.create_text(
            50, 15,
            text=f"Score: {self.score}",
            fill="white",
            font=("Arial", 14)
        )

    def update(self):
        self.score += 1
        self.canvas.itemconfig(self.text, text=f"Score: {self.score}")