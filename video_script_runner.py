import importlib
import os
import random

def get_random_video(directory):
    """
    Selects a random video file from the given directory.
    
    :param directory: Path to the folder containing background videos.
    :return: Path to the randomly selected video file.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Error: The directory '{directory}' does not exist.")

    # List all files in the directory
    video_files = [f for f in os.listdir(directory) if f.endswith((".mp4", ".mov", ".avi", ".mkv"))]

    if not video_files:
        raise FileNotFoundError("Error: No video files found in the 'background_videos' directory.")

    # Randomly select a video file
    selected_video = random.choice(video_files)
    return os.path.join(directory, selected_video)

def run_video_script(script_name, video_path, text, output_path, font_path, video_font_size, words_per_screen):
    """
    Dynamically imports the selected script and runs the generate_video function.

    :param script_name: Name of the script module (without `.py`).
    :param video_path: Path to the input video.
    :param text: Text to overlay on the video.
    :param output_path: Path to save the output video.
    """
    try:
        # Dynamically import the selected script
        script_module = importlib.import_module(script_name)
        
        # Call the generate_video function
        if hasattr(script_module, 'generate_video'):
            script_module.generate_video(video_path, text, output_path, font_path, video_font_size, words_per_screen)
        else:
            print(f"Error: {script_name}.py does not contain 'generate_video' function.")
    except ModuleNotFoundError:
        print(f"Error: {script_name}.py not found.")

# Example usage
if __name__ == "__main__":

    #uncomment if you want to have the choice at runtime
    #script_to_use = input("Enter script name (script/google_script): ").strip()  # Choose which script to run

    #default values
    script_to_use = "google_script" # use script if you want to have the gtts API and google_script if you want the google one
    video_path = "./background_videos/background_1.mp4"
    text = "Chris you are such a sussy baka muah. Come here and kiss me."
    output_path = "final_output.mp4"
    video_font_size = 20
    font_path="/home/dev/.fonts/DejaVuSans.ttf"
    #option to change number of words on screen at a time
    words_per_screen = 3

    run_video_script(script_to_use, video_path, text, output_path, font_path, video_font_size, words_per_screen)