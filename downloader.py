import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import threading
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import itertools
from pathvalidate import sanitize_filename


class Downloader(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('YouTube Downloader')
        self.geometry('500x150')

        # UI Elements
        self.url_frame = ttk.Frame(self)
        self.url_label = ttk.Label(self.url_frame, text="YouTube URL:")
        self.url_entry = ttk.Entry(self.url_frame, width=50)

        self.option_frame = ttk.Frame(self)
        self.option = tk.StringVar()
        self.radio_mp3 = ttk.Radiobutton(self.option_frame, text='MP3', variable=self.option, value='mp3')
        self.radio_mp4 = ttk.Radiobutton(self.option_frame, text='MP4', variable=self.option, value='mp4')

        self.download_button = ttk.Button(self.option_frame, text="Download", command=self.download)

        self.loading_label = ttk.Label(self.option_frame, text="")

        # Progressbar: initially hidden
        self.progress = ttk.Progressbar(self, length=400, mode='determinate')

        # Pack layout
        self.url_frame.pack(padx=10, pady=20, fill="both")
        self.url_label.pack(side=tk.LEFT)
        self.url_entry.pack(side=tk.LEFT)

        self.option_frame.pack(padx=10, pady=5, fill="both")
        self.radio_mp3.pack(side=tk.LEFT)
        self.radio_mp4.pack(side=tk.LEFT)
        self.download_button.pack(side=tk.LEFT)
        self.loading_label.pack(side=tk.LEFT)

    def progress_func(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress['value'] = percentage
        self.update_idletasks()

    def download(self):
        url = self.url_entry.get()
        option = self.option.get()

        if not url or not option:
            messagebox.showerror("Error", "All fields must be filled")
            return

        self.progress['value'] = 0

        # Repack progress bar when download starts
        self.progress.pack(pady=10)

        if option == 'mp4':
            self.thread = threading.Thread(target=self.download_video, args=(url,))
        else:
            self.thread = threading.Thread(target=self.download_audio, args=(url,))

        self.thread.start()

    def download_video(self, url):
        try:
            yt = YouTube(url)
            yt.register_on_progress_callback(self.progress_func)
            video = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
            audio = yt.streams.get_audio_only()

            video_file = video.download(filename='video')
            audio_file = audio.download(filename='audio')

            video_clip = VideoFileClip(video_file)
            audio_clip = AudioFileClip(audio_file)

            final_clip = video_clip.set_audio(audio_clip)

            loading_text = 'Merging Video and Audio...'
            loading_animation = itertools.cycle(['|', '/', '-', '\\'])

            def animate_loading():
                self.loading_label.config(text=loading_text + next(loading_animation))
                if not self.thread.is_alive():
                    self.download_button.config(state='normal')
                    self.loading_label.config(text='')
                else:
                    self.after(200, animate_loading)

            self.url_entry.config(state='disabled')
            self.download_button.config(state='disabled')
            self.loading_label.pack(side=tk.LEFT)
            self.loading_label.config(text=loading_text + next(loading_animation))
            self.after(200, animate_loading)

            final_clip.write_videofile(sanitize_filename(yt.title + '.mp4'))

            os.remove(video_file)
            os.remove(audio_file)

            messagebox.showinfo("Success", "Video Completed")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.url_entry.config(state='normal')
            self.download_button.config(state='normal')
            self.loading_label.config(text='')
            self.progress.pack_forget()  # Unpack progress bar when download is done

    def download_audio(self, url):
        try:
            yt = YouTube(url)
            yt.register_on_progress_callback(self.progress_func)
            yt = yt.streams.filter(only_audio=True).first()
            out_file = yt.download(filename='audio')
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

            loading_text = 'Downloading...'
            loading_animation = itertools.cycle(['|', '/', '-', '\\'])

            def animate_loading():
                self.loading_label.config(text=loading_text + next(loading_animation))
                if not self.thread.is_alive():
                    self.download_button.config(state='normal')
                    self.loading_label.config(text='')
                else:
                    self.after(200, animate_loading)

            self.url_entry.config(state='disabled')
            self.download_button.config(state='disabled')
            self.loading_label.pack(side=tk.LEFT)
            self.loading_label.config(text=loading_text + next(loading_animation))
            self.after(200, animate_loading)

            messagebox.showinfo("Success", "Download completed")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.url_entry.config(state='normal')
            self.download_button.config(state='normal')
            self.loading_label.config(text='')
            self.progress.pack_forget()  # Unpack progress bar in case of an error


if __name__ == "__main__":
    app = Downloader()
    app.mainloop()