from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
import os
import librosa
import numpy as np

# inputs that can be changed
def generate_video(video_path, text, output_video, font_path, video_font_size, words_per_screen):

    # Configuration
    #video_path = "background.mp4"  # Replace with your selected video file
    #output_video = "final_video.mp4"
    #text = "This is an AI-generated explainer video."
    #text_position = ('center', 'center')  # Adjust position as needed
    #video_font_size = 30
    #duration = 10  # Duration of text appearance

    # Split up the words in the text
    words = text.split()

    # grouped into chunks based on words_per_screen
    grouped_words = [" ".join(words[i:i+words_per_screen]) for i in range(0, len(words), words_per_screen)]

    # Load video
    video = VideoFileClip(video_path)


    # Generate speech using gTTS
    tts = gTTS(text, lang="en-uk", slow=False)
    tts.save("speech.mp3")

    # Load generated speech
    audio = AudioFileClip("speech.mp3")

    # Ensure video and audio are the same length
    video = video.with_duration(audio.duration)

    # Function to create text clips for each word
    def create_word_clip(word, start_time, fontSize=video_font_size):

        width, height = 1000, 800
        word_clip = TextClip(text=word,  # Use 'text' as a keyword argument
                            font=font_path,  # Font path
                            font_size=fontSize, 
                            color='white',
                            method='caption',
                            size=(width, height))  
        word_clip = word_clip.with_start(start_time).with_duration(audio.duration / len(words) )  # Show each word over the duration of the audio
        return word_clip

    # Create individual word clips
    word_clips = []
    start_time = -0.6
    chunk_duration = audio.duration / len(grouped_words)
    for chunk  in grouped_words:
        word_clip = create_word_clip(chunk, start_time)
        word_clips.append(word_clip)
        start_time += chunk_duration  # Adjust timing for word chunks

    # Combine word clips into one composite
    text_clips = CompositeVideoClip(word_clips)

    final_text = text_clips.with_position('center')

    # Combine text and video
    final_video = CompositeVideoClip([video, final_text])

    # Set final audio
    final_video = final_video.with_audio(audio)

    # Export final video
    final_video.write_videofile(output_video, codec="libx264", fps=24)

    # Cleanup
    os.remove("speech.mp3")



# gooogle code 
from google.cloud import texttospeech
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import os
from PIL import ImageFont

def generate_video(video_path, text, output_video, font_path, video_font_size):

    # Configuration
    #video_path = "background.mp4"  # Replace with your selected video file
    #output_video = "final_video.mp4"
    #text = "This is an AI-generated explainer video."
    #text_position = ('center', 'bottom')  # Adjust position as needed
    #video_font_size = 50
    #duration = 10  # Duration of text appearance

    # Split up the words in the text
    words = text.split()

    # Load video
    video = VideoFileClip(video_path)

    # Initialize Google Cloud TTS client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Set voice parameters (language, gender)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Set audio parameters (encoding, type)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Generate speech
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save the audio to a file
    with open("speech.mp3", "wb") as out:
        out.write(response.audio_content)

    # Load generated speech
    audio = AudioFileClip("speech.mp3")

    # Ensure video and audio are the same length
    video = video.with_duration(audio.duration)

    # Function to create text clips for each word
    def create_word_clip(word, start_time, fontSize=video_font_size):
        width, height = 1000, 800
        word_clip = TextClip(text=word,  # Use 'text' as a keyword argument
                            font=font_path,  # Font path
                            font_size=fontSize, 
                            color='white',
                            method='caption',
                            size=(width, height))  
        word_clip = word_clip.with_position('center').with_start(start_time).with_duration(audio.duration / len(words))  # Show each word over the duration of the audio
        return word_clip

    # Create individual word clips
    word_clips = []
    start_time = -0.4  # Start at the beginning of the audio
    for word in words:
        word_clip = create_word_clip(word, start_time)
        word_clips.append(word_clip)
        start_time += audio.duration / len(words)  # Increment start time for each word

    # Combine word clips into one composite
    text_clips = CompositeVideoClip(word_clips)

    final_text = text_clips.with_position('center')

    # Combine text and video
    final_video = CompositeVideoClip([video, final_text])

    # Set final audio
    final_video = final_video.with_audio(audio)

    # Export final video
    final_video.write_videofile(output_video, codec="libx264", fps=24)

    # Cleanup
    os.remove("speech.mp3")



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

