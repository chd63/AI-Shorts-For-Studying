# AI Video Generator - Usage Guide

## Running the Application

You can run the AI Video Generator in two different ways:

### 1️⃣ Running with the UI
To launch the graphical user interface (GUI), run:
```bash
python3 UI.py
```
This will open a window where you can:
- Generate videos from uploaded notes (TXT or PPTX).
- Generate videos by entering custom text.
- Choose a background video (random or manually selected).
- Adjust settings like font size and words per screen.

### 2️⃣ Running from the Command Line
To generate videos using the command line, run:
```bash
python3 note_generation.py <notes_file> <key_point> <words_per_screen> [-p]
```
Example:
```bash
python3 note_generation.py notes.txt 5 3
```
- `<notes_file>`: Path to a TXT or PPTX file.
- `<key_point>`: Number of key points to extract and generate videos.
- `<words_per_screen>`: Number of words displayed per screen in the video.
- `-p`: (Optional) Use this flag if the input file is a PowerPoint file.

## API Key Setup
To use **Google Gemini AI**, you must set up an API key.

1. Open `note_generation.py`.
2. Create a `.env` file in the same directory.
3. Add your **Google Gemini API key** in the `.env` file:
```env
API_KEY="your-api-key-here"
```

## Google Script API Requirement
If you are using `google_script` for video generation, you must have a valid API for it to work correctly.

Make sure:
- You have access to the necessary Google API services.
- Your API key and authentication are correctly set up.

## Background Videos Setup
To use background videos, you must create a `background_videos` folder in the project directory. 
- Name your background videos using the format: `background_1.mp4`, `background_2.mp4`, etc.
- The application will randomly select a video or allow you to manually choose one.

---
Now you're ready to create AI-generated videos! 🚀

