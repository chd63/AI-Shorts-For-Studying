from upload_video import upload_video  # Import the upload_video function

def main():
    # Specify the video details
    file_path = "final_output.mp4"  # Path to your video file
    title = "My YouTube Video"  # Video title
    description = "This is a test video uploaded via API"  # Video description
    tags = ["test", "upload", "api"]  # Tags for the video
    category_id = "22"  # YouTube category (default is "People & Blogs")
    privacy_status = "private"  # Privacy status ("public", "unlisted", or "private")
    is_short = False  # Whether the video is a YouTube Short or not

    # Call the upload function
    upload_video(file_path, title, description, tags, category_id, privacy_status, is_short)

if __name__ == "__main__":
    main()