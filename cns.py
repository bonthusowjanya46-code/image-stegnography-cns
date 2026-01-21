import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
from PIL import Image, ImageTk

engine = pyttsx3.init()

image_path = None
stego_image = None

# ------------------ Functions ------------------

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if image_path:
        show_image(image_path)

def show_image(path):
    img = Image.open(path).resize((200, 200))
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img

def hide_character():
    global stego_image

    if not image_path:
        messagebox.showerror("Error", "Select an image first")
        return

    char = entry.get()
    if len(char) != 1:
        messagebox.showerror("Error", "Enter only ONE character")
        return

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))

    ascii_val = ord(char)
    binary = format(ascii_val, '08b')

    flat = img.flatten()

    for i in range(8):
        flat[i] = (flat[i] & ~1) | int(binary[i])

    stego_image = flat.reshape(img.shape)

    cv2.imwrite("stego_image.png", stego_image)
    show_image("stego_image.png")

    messagebox.showinfo("Success", "Character hidden successfully")

def retrieve_character():
    if stego_image is None:
        messagebox.showerror("Error", "No hidden image found")
        return

    flat = stego_image.flatten()

    binary = ""
    for i in range(8):
        binary += str(flat[i] & 1)

    char = chr(int(binary, 2))
    result_label.config(text=f"Hidden Character: {char}")

    speak(char)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ------------------ GUI ------------------

root = tk.Tk()
root.title("Grayscale Image Steganography")
root.geometry("400x500")

tk.Button(root, text="Select Image", command=select_image).pack(pady=10)

panel = tk.Label(root)
panel.pack()

tk.Label(root, text="Enter One Character to Hide").pack(pady=5)
entry = tk.Entry(root, width=5, font=("Arial", 16))
entry.pack(pady=5)

tk.Button(root, text="Hide Character", command=hide_character).pack(pady=10)
tk.Button(root, text="Retrieve Character", command=retrieve_character).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()