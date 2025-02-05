from google.cloud import texttospeech
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import os
import librosa
import numpy as np

def generate_video(video_path, text, output_video, font_path, video_font_size, words_per_screen):
    """
    Generates a video with text overlay and synthesized speech using Google Cloud Text-to-Speech.

    :param video_path: Path to the input background video.
    :param text: The text to overlay on the video.
    :param output_video: Path to save the final generated video.
    :param font_path: Path to the font file.
    :param video_font_size: Font size for the overlay text.
    :param words_per_screen: Number of words to display on the screen at a time.
    """

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
    speech_file = "speech.mp3"
    with open(speech_file, "wb") as out:
        out.write(response.audio_content)

    if not os.path.exists(speech_file):
        raise FileNotFoundError("Speech file not created successfully.")

    # Load generated speech
    audio = AudioFileClip(speech_file)

    # Load video and sync duration with audio
    video = VideoFileClip(video_path).with_duration(audio.duration)

    # Get video dimensions for dynamic text scaling
    video_width, video_height = video.size  

    # Analyze speech to get accurate durations
    y, sr = librosa.load(speech_file, sr=None)
    total_audio_duration = librosa.get_duration(y=y, sr=sr)

    # Split text into words
    words = text.split()

    # Estimate word durations proportionally
    word_lengths = np.array([len(word) for word in words])
    word_durations = (word_lengths / word_lengths.sum()) * total_audio_duration

    # Group words based on words_per_screen
    grouped_words = []
    grouped_durations = []
    i = 0
    while i < len(words):
        group = " ".join(words[i:i+words_per_screen])
        duration = sum(word_durations[i:i+words_per_screen])
        grouped_words.append(group)
        grouped_durations.append(duration)
        i += words_per_screen

    print("\n📝 **Grouped Words and Durations:**")
    for gw, gd in zip(grouped_words, grouped_durations):
        print(f"   ➤ '{gw}' → {gd:.2f} sec")

    # Function to create text clips
    def create_word_clip(text_chunk, start_time, duration):
        width, height = 1000, 800
        word_clip = TextClip(
            text=text_chunk, 
            font=font_path,
            font_size=video_font_size,  
            color='white',
            stroke_color = 'black',
            stroke_width=3,
            method='caption',
            size=(width, height)
        )
        word_clip = word_clip.with_start(start_time).with_duration(duration)
        return word_clip

    # Create text clips
    word_clips = []
    start_time = -0.4
    for chunk, duration in zip(grouped_words, grouped_durations):
        word_clip = create_word_clip(chunk, start_time, duration)
        word_clips.append(word_clip)
        start_time += duration  # Move start time forward based on actual speech timing

    print("\n✅ **Final Word Clips List:**")
    if not word_clips:
        print("   ❌ No text clips were created. Check text processing logic.")
        return
    for wc in word_clips:
        print(f"   🎥 {wc.text}")

    # Ensure text clips have duration
    text_clips = CompositeVideoClip(word_clips).with_position('center')

    # Combine text and video
    final_video = CompositeVideoClip([video, text_clips])

    # Set final audio
    final_video = final_video.with_audio(audio)

    # Export final video
    final_video.write_videofile(output_video, codec="libx264", fps=24)

    # Cleanup
    os.remove(speech_file)
