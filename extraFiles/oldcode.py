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
