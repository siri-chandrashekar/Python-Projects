import customtkinter as ctk


def reset_timer(event=None):
    global timer, time_left

    if timer:
        app.after_cancel(timer)

    time_left = 5
    countdown()


def delete_text():
    textbox.delete("1.0", "end")
    timer_label.configure(text="Deleted!", text_color="#ff4444")


def countdown():
    global time_left, timer
    timer_label.configure(text=f"{time_left}")

    if time_left <= 2:
        timer_label.configure(text_color="red")
        timer_label.configure(font=("Arial", 25, "bold"))
    else:
        timer_label.configure(text_color="#00ff88")
        timer_label.configure(font=("Arial", 25))

    if time_left > 0:
        time_left -= 1
        timer = app.after(1000, countdown)
    else:
        delete_text()


ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Dangerous Writing App")
app.geometry("800x600")

time_left = 5
timer = None

# Title
title = ctk.CTkLabel(
    app,
    text="The Dangerous Writing App",
    font=("Arial", 28, "bold"),
    text_color="#00ff88",
)
title.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(
    app,
    text="Keep typing... or everything will disappear.",
    font=("Arial", 20),
)
subtitle.pack(pady=(0, 10))

# Timer
timer_label = ctk.CTkLabel(app, text="5", font=("Arial", 20))
timer_label.pack()

textbox = ctk.CTkTextbox(app, width=1000, height=500)
textbox.pack(pady=20)
textbox.bind("<Key>", reset_timer)

reset_timer()

app.mainloop()
