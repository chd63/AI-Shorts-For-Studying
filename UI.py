import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

# Import your previously defined generate_video function here
from note_generation import generate_video

# Function to browse for a file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PowerPoint files", "*.pptx")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# Function to generate the video
def on_generate_click():
    notes_file = file_entry.get()
    key_point = key_point_entry.get()
    words_per_screen = words_per_screen_entry.get()
    
    # Validate the inputs
    if not os.path.exists(notes_file):
        messagebox.showerror("Error", "Please select a valid notes file.")
        return
    
    if not key_point.isdigit() or int(key_point) <= 0:
        messagebox.showerror("Error", "Key points must be a positive integer.")
        return
    
    if not words_per_screen.isdigit() or int(words_per_screen) <= 0:
        messagebox.showerror("Error", "Words per screen must be a positive integer.")
        return

    key_point = int(key_point)
    words_per_screen = int(words_per_screen)

    # Set other parameters
    script_to_use = "script"
    video_path = video_path_entry.get()
    video_font_size = 20
    font_path = font_path_entry.get()
    output_dir = output_dir_entry.get()

    # Generate video
    try:
        with open(notes_file, 'r', encoding='utf-8') as file:
            notes_text = file.read()
        
        generate_video(notes_text, words_per_screen, key_point, script_to_use, video_path, video_font_size, font_path, output_dir)
        messagebox.showinfo("Success", "Videos have been successfully generated!")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Video Generator")

# Set window size
root.geometry("500x400")

# File selection
file_label = tk.Label(root, text="Notes File:")
file_label.grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Key point input
key_point_label = tk.Label(root, text="Key Points:")
key_point_label.grid(row=1, column=0, padx=10, pady=10)
key_point_entry = tk.Entry(root, width=10)
key_point_entry.grid(row=1, column=1, padx=10, pady=10)

# Words per screen input
words_per_screen_label = tk.Label(root, text="Words Per Screen:")
words_per_screen_label.grid(row=2, column=0, padx=10, pady=10)
words_per_screen_entry = tk.Entry(root, width=10)
words_per_screen_entry.grid(row=2, column=1, padx=10, pady=10)

# Video path input
video_path_label = tk.Label(root, text="Video Path:")
video_path_label.grid(row=3, column=0, padx=10, pady=10)
video_path_entry = tk.Entry(root, width=40)
video_path_entry.grid(row=3, column=1, padx=10, pady=10)

# Font path input
font_path_label = tk.Label(root, text="Font Path:")
font_path_label.grid(row=4, column=0, padx=10, pady=10)
font_path_entry = tk.Entry(root, width=40)
font_path_entry.grid(row=4, column=1, padx=10, pady=10)

# Output directory input
output_dir_label = tk.Label(root, text="Output Directory:")
output_dir_label.grid(row=5, column=0, padx=10, pady=10)
output_dir_entry = tk.Entry(root, width=40)
output_dir_entry.grid(row=5, column=1, padx=10, pady=10)

# Generate button
generate_button = tk.Button(root, text="Generate Videos", command=on_generate_click)
generate_button.grid(row=6, column=0, columnspan=3, padx=10, pady=20)

# Start the GUI
root.mainloop()
