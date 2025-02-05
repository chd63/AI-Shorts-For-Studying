import google.generativeai as genai
from dotenv import load_dotenv
from pptx import Presentation
import video_script_runner
import sys
import json
import re
import os
import argparse

# Load environment variables
load_dotenv()
api_key_1 = os.getenv("API_KEY")
if not api_key_1:
    raise ValueError("API_KEY not found. Check your .env file.")

# Set your API key
genai.configure(api_key=api_key_1)

# Function to read notes from a file
def read_notes_file(file_path):
    """
    Reads the content of a notes file and returns it as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)  # Exit the program if the file is missing

# Extract text from PowerPoint file
def extract_text_from_pptx(file_path):
    try:
        prs = Presentation(file_path)
        content = []
        for slide in prs.slides:
            slide_text = []
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slide_text.append(shape.text)
            content.append("\n".join(slide_text))
        return "\n\n".join(content)
    except Exception as e:
        print(f"Error processing PowerPoint file: {e}")
        sys.exit(1)

# Function to generate video based on input parameters
def generate_video(notes_text, words_per_screen, key_point, script_to_use, video_path, video_font_size, font_path, output_dir):
    """
    Generate videos based on the extracted text and key points.
    """
    # Request to extract key ideas from AI
    request_string = f"""
    Please extract {key_point} key ideas from the following text. 
    Each idea should be concise, less than 100 words. 
    Format the output as a **valid Python list of strings**.

    Return only the JSON output without any additional text.

    Text:
    {notes_text}
    """

    # Initialize the model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate text
    response = model.generate_content(request_string)

    response_text = response.text.strip()
    #print("Raw response tex:",response.text)
    # Clean the response text

    response_text = re.sub(r"^```(?:json)?\n", "", response_text)
    response_text = re.sub(r"\n```$", "", response_text)

    # Safely convert the cleaned response into a Python list
    try:
        extracted_list = json.loads(response_text)  # Convert cleaned response into Python list
        if not isinstance(extracted_list, list):
            raise ValueError("Response is not a valid JSON list.")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ Error parsing response into list: {e}")
        extracted_list = [response_text]  # Fallback to raw response if parsing fails

    # Loop through the extracted key points and create a video for each
    for idx, key_point in enumerate(extracted_list, start=1):
        output_path = f"{output_dir}output_{idx}.mp4"  # Generate a unique output path for each key point
        print(f"\n🎬 Creating video for key point {idx}: {key_point}")

        # Call the video creation function with each key point
        video_script_runner.run_video_script(
            script_to_use, video_path, key_point, output_path, font_path, video_font_size, words_per_screen
        )
        print(f"✅ Video {output_path} created successfully.")

# Command line interface (CLI)
def main():
    parser = argparse.ArgumentParser(description="Process notes from a text file or PowerPoint and generate videos.")
    parser.add_argument("notes_file", help="Path to the notes file (TXT or PPTX)")
    parser.add_argument("key_point", type=int, help="Number of key points to extract and generate videos")
    parser.add_argument("words_per_screen", type=int, help="Number of words to display per screen in the video")
    parser.add_argument("-p", "--powerpoint", action="store_true", help="Use PowerPoint file instead of a text file")
    
    args = parser.parse_args()

    if args.powerpoint:
        notes_text = extract_text_from_pptx(args.notes_file)
    else:
        notes_text = read_notes_file(args.notes_file)

    # Set parameters (these can be adjusted by the user)
    script_to_use = "script"
    video_path = "./background_videos/background_1.mp4"
    video_font_size = 20
    font_path = "/home/dev/.fonts/DejaVuSans.ttf"
    output_dir = "./generated_videos/"

    # Generate the video
    generate_video(notes_text, args.words_per_screen, args.key_point, script_to_use, video_path, video_font_size, font_path, output_dir)

if __name__ == "__main__":
    main()
