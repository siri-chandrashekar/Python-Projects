import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

file_path = None

def upload_photo():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if file_path:
        status_var.set("Image selected successfully.")
        upload_btn.config(text="Change Image")
        watermark_btn.state(["!disabled"])
    else:
        status_var.set("No image selected.")

def reset_form():
    global file_path
    file_path = None
    watermark_var.set("")
    upload_btn.config(text="Upload Image")
    watermark_btn.state(["disabled"])
    status_var.set("Ready.")

def add_watermark():
    global file_path
    if not file_path:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    watermark_text = watermark_var.get().strip()
    if not watermark_text:
        messagebox.showerror("Error", "Enter watermark text!")
        return

    try:
        image = Image.open(file_path).convert("RGBA")

        txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        try:
            font = ImageFont.truetype("arial.ttf", 42)
        except:
            font = ImageFont.load_default()

        left, top, right, bottom = draw.textbbox((0, 0), watermark_text, font=font)
        text_w = right - left
        text_h = bottom - top

        width, height = image.size
        x = width - text_w - 24
        y = height - text_h - 24

        if x < 10:
            x = 10
        if y < 10:
            y = 10

        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 140))

        watermarked = Image.alpha_composite(image, txt_layer)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )

        if save_path:
            watermarked.convert("RGB").save(save_path)
            status_var.set("Watermarked image saved successfully.")
            messagebox.showinfo("Success", "Watermarked image saved!")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_var.set("Something went wrong.")

root = tk.Tk()
root.title("WaterMarkly.photos")
root.geometry("760x480")
root.configure(bg="#f4f7fb")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background="#f4f7fb")
style.configure("Card.TFrame", background="white")
style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background="#f4f7fb", foreground="#1f2937")
style.configure("Sub.TLabel", font=("Segoe UI", 10), background="#f4f7fb", foreground="#6b7280")
style.configure("TLabel", background="#f4f7fb", foreground="#1f2937", font=("Segoe UI", 10))
style.configure("Status.TLabel", font=("Segoe UI", 9), background="#f4f7fb", foreground="#4b5563")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
style.configure("Accent.TButton", background="#2563eb", foreground="white")
style.map("Accent.TButton", background=[("active", "#1d4ed8"), ("disabled", "#93c5fd")])

main = ttk.Frame(root, padding=24)
main.pack(fill="both", expand=True)

card = ttk.Frame(main, style="Card.TFrame", padding=24)
card.pack(fill="both", expand=True)

title = ttk.Label(card, text="WaterMarkly.photos", style="Title.TLabel")
title.grid(row=0, column=0, sticky="w")

subtitle = ttk.Label(
    card,
    text="Upload an image, enter your watermark text, and save a protected version in seconds.",
    style="Sub.TLabel"
)
subtitle.grid(row=1, column=0, sticky="w", pady=(6, 18))

image_label = ttk.Label(card, text="Selected image")
image_label.grid(row=2, column=0, sticky="w", pady=(0, 6))

upload_btn = ttk.Button(card, text="Upload Image", command=upload_photo, style="Accent.TButton")
upload_btn.grid(row=3, column=0, sticky="ew", pady=(0, 16))

watermark_label = ttk.Label(card, text="Watermark text")
watermark_label.grid(row=4, column=0, sticky="w", pady=(0, 6))

watermark_var = tk.StringVar()
watermark_entry = ttk.Entry(card, textvariable=watermark_var, width=40)
watermark_entry.grid(row=5, column=0, sticky="ew", pady=(0, 16))

button_frame = ttk.Frame(card)
button_frame.grid(row=6, column=0, sticky="ew")

watermark_btn = ttk.Button(button_frame, text="Add Watermark", command=add_watermark, style="Accent.TButton")
watermark_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

reset_btn = ttk.Button(button_frame, text="Clear", command=reset_form)
reset_btn.pack(side="left", expand=True, fill="x", padx=(8, 0))

watermark_btn.state(["disabled"])

status_var = tk.StringVar(value="Ready.")
status = ttk.Label(card, textvariable=status_var, style="Status.TLabel")
status.grid(row=7, column=0, sticky="w", pady=(18, 0))

card.grid_columnconfigure(0, weight=1)

root.mainloop()