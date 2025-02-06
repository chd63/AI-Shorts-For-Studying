import tkinter as tk
from tkinter import filedialog, messagebox, Text, StringVar, OptionMenu
import os
import random
from note_generation import generate_video, read_notes_file, extract_text_from_pptx, extract_text_from_pdf  # Import updated PDF extraction
from video_script_runner import run_video_script

BACKGROUND_VIDEOS_DIR = "./background_videos/"

def get_random_video():
    """Returns a random video file from the background_videos directory."""
    if not os.path.exists(BACKGROUND_VIDEOS_DIR):
        raise FileNotFoundError(f"Error: The directory '{BACKGROUND_VIDEOS_DIR}' does not exist.")

    video_files = [f for f in os.listdir(BACKGROUND_VIDEOS_DIR) if f.endswith((".mp4", ".mov", ".avi", ".mkv"))]

    if not video_files:
        raise FileNotFoundError("Error: No video files found in the 'background_videos' directory.")

    return os.path.join(BACKGROUND_VIDEOS_DIR, random.choice(video_files))


class VideoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Video Generator - Main Menu")
        self.root.geometry("400x350")

        # Main Menu Buttons
        tk.Label(root, text="Welcome to AI Video Generator", font=("Arial", 14)).pack(pady=20)
        tk.Button(root, text="Generate Video from Notes", command=self.open_notes_page, width=30).pack(pady=10)
        tk.Button(root, text="Generate Video from Text", command=self.open_text_page, width=30).pack(pady=10)
        tk.Button(root, text="Exit", command=root.quit, width=30, fg="red").pack(pady=10)

    def open_notes_page(self):
        self.clear_window()
        NotesPage(self.root, self)

    def open_text_page(self):
        self.clear_window()
        TextPage(self.root, self)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class NotesPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.root.title("Generate Video from Notes")
        self.root.geometry("800x400")

        # File Selection
        tk.Label(root, text="Upload Notes File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=5)

        # Key Points Input
        tk.Label(root, text="Key Points (Videos to Generate):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.key_point_entry = tk.Entry(root, width=10)
        self.key_point_entry.grid(row=2, column=1, padx=10, pady=5)

        # Words Per Screen Input
        tk.Label(root, text="Words Per Screen:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.words_per_screen_entry = tk.Entry(root, width=10)
        self.words_per_screen_entry.insert(0, "3")
        self.words_per_screen_entry.grid(row=3, column=1, padx=10, pady=5)

        # Font Size Input
        tk.Label(root, text="Font Size:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.font_size_entry = tk.Entry(root, width=10)
        self.font_size_entry.insert(0, "20") 
        self.font_size_entry.grid(row=4, column=1, padx=10, pady=5)

        # Generate Button
        tk.Button(root, text="Generate Videos", command=self.generate_videos).grid(row=5, column=0, columnspan=3, pady=20)

        # Back Button
        tk.Button(root, text="Back to Main Menu", command=self.go_back, fg="blue").grid(row=6, column=0, columnspan=3, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PowerPoint Files", "*.pptx"), ("PDF Files", "*.pdf")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def generate_videos(self):
        notes_file = self.file_entry.get()
        key_point = self.key_point_entry.get()  # This is a string from the entry field, no issue here.
        words_per_screen = self.words_per_screen_entry.get()  # This is also a string.
        font_size = self.font_size_entry.get()  # String.

        # Convert necessary fields to integers
        try:
            key_point = int(key_point)  # Convert key_point to an integer
        except ValueError:
            messagebox.showerror("Error", "Key Points must be an integer.")
            return

        try:
            words_per_screen = int(words_per_screen)  # Convert words_per_screen to an integer
        except ValueError:
            messagebox.showerror("Error", "Words Per Screen must be an integer.")
            return

        try:
            font_size = int(font_size)  # Convert font_size to an integer
        except ValueError:
            messagebox.showerror("Error", "Font Size must be an integer.")
            return

        # Determine the text extraction method based on file type
        if notes_file.endswith(".txt"):
            notes_text = read_notes_file(notes_file)
        elif notes_file.endswith(".pptx"):
            notes_text = extract_text_from_pptx(notes_file)
        elif notes_file.endswith(".pdf"):
            notes_text = extract_text_from_pdf(notes_file)  # PDF handling
        else:
            messagebox.showerror("Error", "Unsupported file type")
            return

        # Select a random background video
        video_path = get_random_video()

        script_to_use = "script"
        font_path = "/home/dev/.fonts/DejaVuSans.ttf"
        output_dir = "./generated_videos/"

        try:
            generate_video(notes_text, words_per_screen, key_point, script_to_use, font_size, font_path, output_dir)
            messagebox.showinfo("Success", "Videos have been successfully generated!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def go_back(self):
        self.main_app.clear_window()
        VideoGeneratorApp(self.root)



class TextPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.root.title("Generate Video from Text")
        self.root.geometry("500x400") 

        # Text Input
        tk.Label(root, text="Enter Text for Video:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.text_input = Text(root, width=50, height=5)
        self.text_input.grid(row=0, column=1, padx=10, pady=5)

        # Background Video Selection
        tk.Label(root, text="Choose Background Video:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.video_var = StringVar(root)
        self.video_var.set("Random")

        video_files = ["Random"] + [f for f in os.listdir(BACKGROUND_VIDEOS_DIR) if f.endswith((".mp4", ".mov", ".avi", ".mkv"))]
        self.video_dropdown = OptionMenu(root, self.video_var, *video_files)
        self.video_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Words Per Screen Input
        tk.Label(root, text="Words Per Screen:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.words_per_screen_entry = tk.Entry(root, width=10)
        self.words_per_screen_entry.insert(0, "3") 
        self.words_per_screen_entry.grid(row=2, column=1, padx=10, pady=5)

        # Font Size Input
        tk.Label(root, text="Font Size:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.font_size_entry = tk.Entry(root, width=10)
        self.font_size_entry.insert(0, "20")
        self.font_size_entry.grid(row=3, column=1, padx=10, pady=5)

        # Generate Button
        tk.Button(root, text="Generate Video", command=self.generate_video).grid(row=4, column=0, columnspan=2, pady=20)

        # Back Button
        tk.Button(root, text="Back to Main Menu", command=self.go_back, fg="blue").grid(row=5, column=0, columnspan=2, pady=10)

    def generate_video(self):
        text = self.text_input.get("1.0", tk.END).strip()
        video_path = get_random_video() if self.video_var.get() == "Random" else os.path.join(BACKGROUND_VIDEOS_DIR, self.video_var.get())

        run_video_script("script", video_path, text, "final_output.mp4", "/home/dev/.fonts/DejaVuSans.ttf", int(self.font_size_entry.get()), int(self.words_per_screen_entry.get()))

    def go_back(self):
        self.main_app.clear_window()
        VideoGeneratorApp(self.root)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGeneratorApp(root)
    root.mainloop()
