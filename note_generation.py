import google.generativeai as genai
from dotenv import load_dotenv
import video_script_runner
import sys
import json
import re
import os

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

    :param file_path: Path to the notes file.
    :return: Content of the file as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)  # Exit the program if the file is missing

def get_integer_input(arg_value):
    """
    Validates and converts a command-line argument to an integer.

    :param arg_value: The argument to convert.
    :return: The converted integer value.
    """
    try:
        return int(arg_value)
    except ValueError:
        print(f"❌ Error: '{arg_value}' is not a valid number.")
        sys.exit(1)  # Exit if the user input is not a number

# Check if enough arguments were provided
if len(sys.argv) < 3:
    print("❌ Error: Please provide a notes file and a number.")
    print("Usage: python3 main.py <notes_file> <words_per_screen>")
    sys.exit(1)

# Read parameters from command-line
notes_file = sys.argv[1]       # First argument: notes file path
words_per_screen = get_integer_input(sys.argv[2])  # Second argument: number input
notes_text = read_notes_file(notes_file)

request_string = f"""
Please extract {words_per_screen} key ideas from the following text. 
Each idea should be concise, under 100 words. 
Format the output as a **valid Python list of strings**.

Return only the JSON output without any additional text.

Text:
{notes_text}
"""

# uncomment for debug
#print(request_string)


# create a text 


# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate text
response = model.generate_content(request_string)

# Print response
#uncomment for debug
#print(response.text)

response_text = response.text.strip()
response_text = re.sub(r"^```(?:json)?\n", "", response_text)
response_text = re.sub(r"\n```$", "", response_text)


#uncomment for debug
#print("\n🚀 **Raw Gemini Response After Cleaning:**")
#print(response_text)  # Debug print to verify cleaned response


# ✅ Safely convert the cleaned response into a Python list
try:
    extracted_list = json.loads(response_text)  # Convert cleaned response into Python list
    if not isinstance(extracted_list, list):
        raise ValueError("Response is not a valid JSON list.")
except (json.JSONDecodeError, ValueError) as e:
    print(f"❌ Error parsing response into list: {e}")
    extracted_list = [response_text]  # Fallback to raw response if parsing fails


# uncomment for debug
# Print extracted key points
#print("\n📌 Extracted Key Points:")
#for idx, item in enumerate(extracted_list, start=1):
#    print(f"{idx}. {item}")


# TODO: parse through and get user input worth of text to be used to create videos

# call the video script runner

# Define parameters
script_to_use = "script"
video_path = "./background_videos/background_1.mp4"
video_font_size = 20
font_path = "/home/dev/.fonts/DejaVuSans.ttf"
words_per_screen = 3
output_dir = "./generated_videos/"

# Loop through the extracted key points and create a video for each
for idx, key_point in enumerate(extracted_list, start=1):
    output_path = f"{output_dir}output_{idx}.mp4"  # Generate a unique output path for each key point
    print(f"\n🎬 Creating video for key point {idx}: {key_point}")

    # Call the video creation function with each key point
    video_script_runner.run_video_script(
        script_to_use, video_path, key_point, output_path, font_path, video_font_size, words_per_screen
    )
    print(f"✅ Video {output_path} created successfully.")


# Call the function from the imported module
#video_script_runner.run_video_script(script_to_use, video_path, text, output_path, font_path, video_font_size, words_per_screen)