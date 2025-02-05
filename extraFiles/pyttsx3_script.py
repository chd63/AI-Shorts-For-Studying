import pyttsx3
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import os
from PIL import ImageFont

# Ensure that fonts are available
try:
    font = ImageFont.truetype("Liberation Sans", 12)
except IOError:
    print("Liberation Sans font is not available.")

# Configuration
video_path = "background.mp4"  # Replace with your selected video file
output_video = "final_video.mp4"
text = "This is an AI-generated explainer video."
text_position = ('center', 'bottom')  # Adjust position as needed
video_font_size = 50

# Split up the words in the text
words = text.split()

# Load video
video = VideoFileClip(video_path)

# Generate speech using pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate (words per minute)
engine.save_to_file(text, 'speech.mp3')
engine.runAndWait()  # Process speech commands

# Load generated speech
audio = AudioFileClip("speech.mp3")

# Ensure video and audio are the same length
video = video.with_duration(audio.duration)

# Create text overlay with the same duration as audio
text_clip = TextClip(text=text, font="/home/dev/.fonts/DejaVuSans.ttf", font_size=video_font_size, color='white', bg_color='black')
text_clip = text_clip.with_position(text_position).with_duration(audio.duration)  # Use audio duration here

# Combine text and video
final_video = CompositeVideoClip([video, text_clip])

# Set final audio
final_video = final_video.with_audio(audio)

# Export final video
final_video.write_videofile(output_video, codec="libx264", fps=24)

# Cleanup
os.remove("speech.mp3")