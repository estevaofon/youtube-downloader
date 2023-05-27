## :space_invader: About

This code is a Python script for a YouTube downloader application. It uses the tkinter package to create a user interface with a text entry field for entering a YouTube video URL and radio buttons for selecting video or audio downloads. It also uses the pytube and moviepy packages for downloading and processing the videos. The script runs as a Tkinter application and starts by initializing the UI elements. When the user clicks the download button, the download function retrieves the URL and download option, checks whether both fields are filled, and creates a new thread to start the download process. The download function then passes the URL to the appropriate YouTube download function, either download_video or download_audio, based on the user's selected option. Finally, upon successful completion of a download, an alert box informs the user that the download is completed.

## :wrench: Requirements

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```
## :runner:  Usage

To run the code in the terminal, you would need to save the code in a file, such as downloader.py, and then run it using the command:

python downloader.py

## :raising_hand: Contribution

All contributions are welcome! Please open an issue or submit a pull request.

