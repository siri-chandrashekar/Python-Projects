import tkinter as tk
import random

SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing speed improves with consistent practice every day.",
    "Python makes it easy to build powerful applications.",
    "Focus on accuracy first, then increase your speed."
]

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x500")
        self.root.configure(bg="#f5f7fb")

        self.sample_text = tk.StringVar(value=random.choice(SAMPLE_TEXTS))
        self.time_left = 60
        self.timer_running = False
        self.after_id = None

        tk.Label(root, text="Typing Speed Test", font=("Arial", 20, "bold"), bg="#f5f7fb").pack(pady=(15, 5))
        tk.Label(root, text="Type the text below as quickly and accurately as you can.", font=("Arial", 11), bg="#f5f7fb").pack()

        self.timer_label = tk.Label(root, text="Time: 60", font=("Arial", 14, "bold"), fg="blue", bg="#f5f7fb")
        self.timer_label.pack(pady=10)

        tk.Label(
            root,
            textvariable=self.sample_text,
            font=("Arial", 12),
            wraplength=700,
            justify="left",
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        ).pack(padx=20, pady=10, fill="x")

        self.text_input = tk.Text(root, height=6, width=70, font=("Arial", 12), bd=2, relief="groove")
        self.text_input.pack(padx=20, pady=10)

        self.status_label = tk.Label(root, text="Start typing to begin.", font=("Arial", 11), bg="#f5f7fb")
        self.status_label.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f5f7fb")
        self.result_label.pack(pady=5)

        button_frame = tk.Frame(root, bg="#f5f7fb")
        button_frame.pack(pady=15)

        self.check_button = tk.Button(button_frame, text="Check Speed",font=("Arial", 11, "bold"), bg="lightblue", fg="white", width=14, command=self.calculate_speed)
        self.check_button.grid(row=0, column=0, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reset", bg="red", fg="white", font=("Arial", 11, "bold"), width=14, command=self.reset_test)
        self.reset_button.grid(row=0, column=1, padx=10)

        self.check_button.config(state="disabled")

        self.text_input.bind("<KeyPress>", self.start_timer)

    def start_timer(self, event=None):
        if not self.timer_running:
            self.timer_running = True
            self.countdown()

    def countdown(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.after_id = self.root.after(1000, self.countdown)
        else:
            self.timer_label.config(text="Time: 0")
            self.text_input.config(state="disabled")
            self.check_button.config(state="normal")
            self.status_label.config(text="Time is up. Click Check Speed.")

    def calculate_speed(self):
        typed_text = self.text_input.get("1.0", tk.END).strip()
        original_text = self.sample_text.get()

        words_typed = len(typed_text.split())
        correct_chars = sum(
            1 for i, c in enumerate(typed_text)
            if i < len(original_text) and c == original_text[i]
        )
        accuracy = round((correct_chars / len(original_text)) * 100) if original_text else 0

        self.result_label.config(text=f"WPM: {words_typed} | Accuracy: {accuracy}%")

    def reset_test(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)

        self.time_left = 60
        self.timer_running = False
        self.sample_text.set(random.choice(SAMPLE_TEXTS))
        self.timer_label.config(text="Time: 60")
        self.text_input.config(state="normal")
        self.text_input.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.status_label.config(text="Start typing to begin.")
        self.check_button.config(state="disabled")

root = tk.Tk()
app = TypingSpeedApp(root)
root.mainloop()