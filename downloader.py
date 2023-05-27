import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import threading
import os
from moviepy.editor import VideoFileClip, AudioFileClip

class Downloader(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('YouTube Downloader')
        self.geometry('500x100')

        # Style
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))

        # UI Elements
        self.url_frame = ttk.Frame(self)
        self.url_label = ttk.Label(self.url_frame, text="YouTube URL:")
        self.url_entry = ttk.Entry(self.url_frame, width=50)  # Adjust the width here

        self.option_frame = ttk.Frame(self)
        self.option = tk.StringVar()
        self.radio_mp3 = ttk.Radiobutton(self.option_frame, text='MP3', variable=self.option, value='mp3')
        self.radio_mp4 = ttk.Radiobutton(self.option_frame, text='MP4', variable=self.option, value='mp4')

        self.download_button = ttk.Button(self.option_frame, text="Download", command=self.download)

        # Pack layout
        self.url_frame.pack(padx=10, pady=10, fill="both")
        self.url_label.pack(side=tk.LEFT)
        self.url_entry.pack(side=tk.LEFT)

        self.option_frame.pack(padx=10, pady=10, fill="both")
        self.radio_mp3.pack(side=tk.LEFT)
        self.radio_mp4.pack(side=tk.LEFT)
        self.download_button.pack(side=tk.LEFT)

    def download(self):
        url = self.url_entry.get()
        option = self.option.get()

        if not url or not option:
            messagebox.showerror("Error", "All fields must be filled")
            return

        if option == 'mp4':
            self.thread = threading.Thread(target=self.download_video, args=(url,))
        else:
            self.thread = threading.Thread(target=self.download_audio, args=(url,))

        self.thread.start()

    def download_video(self, url):
        try:
            yt = YouTube(url)
            video = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
            audio = yt.streams.get_audio_only()

            video_file = video.download(filename='video')
            audio_file = audio.download(filename='audio')

            video_clip = VideoFileClip(video_file)
            audio_clip = AudioFileClip(audio_file)

            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile('final.mp4')

            os.remove(video_file)
            os.remove(audio_file)

            messagebox.showinfo("Success", "Download completed")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_audio(self, url):
        try:
            yt = YouTube(url)
            yt = yt.streams.filter(only_audio=True).first()
            out_file = yt.download(filename='audio')
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            messagebox.showinfo("Success", "Download completed")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = Downloader()
    app.mainloop()
