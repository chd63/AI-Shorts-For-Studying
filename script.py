from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
import os
import librosa
import numpy as np

# inputs that can be changed
def generate_video(video_path, text, output_video, font_path, video_font_size, words_per_screen):
    """
    Generates a video with text overlay and synthesized speech, accurately timing text appearance with speech.

    :param video_path: Path to the input background video.
    :param text: The text to overlay on the video.
    :param output_video: Path to save the final generated video.
    :param font_path: Path to the font file.
    :param video_font_size: Font size for the overlay text.
    :param words_per_screen: Number of words to display on the screen at a time.
    """

    # Generate speech using gTTS
    speech_file = "speech.mp3"
    tts = gTTS(text, lang="en-uk", slow=False)
    tts.save(speech_file)

    # Ensure the speech file exists before loading
    if not os.path.exists(speech_file):
        raise FileNotFoundError("Speech file not created successfully.")

    # Load generated speech
    audio = AudioFileClip(speech_file)

    # Load video and sync duration with audio
    video = VideoFileClip(video_path).with_duration(audio.duration)


    # Analyze speech to get accurate durations
    y, sr = librosa.load(speech_file, sr=None)  # Load audio file
    total_audio_duration = librosa.get_duration(y=y, sr=sr)  # Get total duration

    # Split text into words
    words = text.split()

    # Estimate word durations proportionally
    word_lengths = np.array([len(word) for word in words])  # Get length of each word
    word_durations = (word_lengths / word_lengths.sum()) * total_audio_duration  # Assign proportional duration

    # Group words based on words_per_screen
    grouped_words = []
    grouped_durations = []
    i = 0
    while i < len(words):
        group = " ".join(words[i:i+words_per_screen])
        duration = sum(word_durations[i:i+words_per_screen])  # Sum durations of grouped words
        grouped_words.append(group)
        grouped_durations.append(duration)
        i += words_per_screen

    print("\n📝 **Grouped Words and Durations:**")
    for gw, gd in zip(grouped_words, grouped_durations):
        print(f"   ➤ '{gw}' → {gd:.2f} sec")

    # Function to create text clips for each word group
    def create_word_clip(text_chunk, start_time, duration, fontSize=video_font_size):
        width, height = 1000, 800
        word_clip = TextClip(
            text=text_chunk,
            font=font_path,
            font_size=fontSize,
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
    start_time = -0.5
    for chunk, duration in zip(grouped_words, grouped_durations):
        #print out word clip
        word_clip = create_word_clip(chunk, start_time, duration)
        word_clips.append(word_clip)
        start_time += duration  # Move start time forward based on actual speech timing

    print("\n✅ **Final Word Clips List:**")
    if not word_clips:
        print("   ❌ No text clips were created. Check text processing logic.")
        return
    for wc in word_clips:
        print(f"   🎥 {wc.text}")

    if not word_clips:
        raise ValueError("❌ No text clips were created, video will have no text.")

    # Combine text clips into one composite
    text_clips = CompositeVideoClip(word_clips).with_position('center')

    # Combine text and video
    final_video = CompositeVideoClip([video, text_clips])

    # Set final audio
    final_video = final_video.with_audio(audio)

    # Export final video
    final_video.write_videofile(output_video, codec="libx264", fps=24)

    # Cleanup
    os.remove(speech_file)