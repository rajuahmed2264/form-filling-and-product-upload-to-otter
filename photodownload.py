import os
import requests

def download_google_drive_image(file_id, destination_path):
    # Extract the file ID from the given link
    file_id = file_id.split("/")[-2]

    # Google Drive's download link format
    download_link = f"https://drive.google.com/uc?id={file_id}"

    try:
        # Send an HTTP request to get the image
        response = requests.get(download_link)

        # Check if the request was successful
        if response.status_code == 200:
            # Create the "images" folder if it doesn't exist
            if not os.path.exists("images"):
                os.makedirs("images")

            # Save the image in the "images" folder
            image_path = os.path.join("images", destination_path)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print("Image downloaded successfully.")
        else:
            print("Failed to download the image.")
    except Exception as e:
        print("An error occurred:", e)
