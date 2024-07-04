import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp as youtube_dl
import os
from moviepy.editor import *

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OGDownloaderV2")
        self.root.geometry("800x400")
        self.root.configure(bg="#f0f0f0")

        self.title_label = tk.Label(self.root, text="OGDownloaderV2", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20)

        self.url_label = tk.Label(self.root, text="Video URL'si (YouTube veya TikTok):", font=("Helvetica", 14), bg="#f0f0f0")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=60, font=("Helvetica", 14))
        self.url_entry.pack(pady=5)

        self.platform_var = tk.StringVar(value="YouTube")
        self.youtube_radio = tk.Radiobutton(self.root, text="YouTube", variable=self.platform_var, value="YouTube", font=("Helvetica", 12), bg="#f0f0f0")
        self.youtube_radio.pack(pady=5)
        self.tiktok_radio = tk.Radiobutton(self.root, text="TikTok", variable=self.platform_var, value="TikTok", font=("Helvetica", 12), bg="#f0f0f0")
        self.tiktok_radio.pack(pady=5)

        self.resolution_label = tk.Label(self.root, text="Çözünürlük (sadece YouTube için):", font=("Helvetica", 14), bg="#f0f0f0")
        self.resolution_label.pack(pady=5)
        self.resolution_combobox = ttk.Combobox(self.root, values=["144p", "360p", "720p", "1080p", "Highest"], font=("Helvetica", 12))
        self.resolution_combobox.set("Highest")
        self.resolution_combobox.pack(pady=5)

        self.format_label = tk.Label(self.root, text="Format:", font=("Helvetica", 14), bg="#f0f0f0")
        self.format_label.pack(pady=5)
        self.format_combobox = ttk.Combobox(self.root, values=["mp4", "mp3"], font=("Helvetica", 12))
        self.format_combobox.set("mp4")
        self.format_combobox.pack(pady=5)

        self.download_button = tk.Button(self.root, text="İndir", font=("Helvetica", 14, "bold"), command=self.download_video, bg="#4CAF50", fg="white")
        self.download_button.pack(pady=20)

        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f0f0f0")
        self.status_label.pack(pady=10)

    def download_video(self):
        url = self.url_entry.get()
        platform = self.platform_var.get()
        resolution = self.resolution_combobox.get()
        file_format = self.format_combobox.get()

        if not url:
            messagebox.showerror("Hata", "Lütfen bir video linki giriniz.")
            return

        download_path = filedialog.askdirectory()
        if not download_path:
            messagebox.showerror("Hata", "Lütfen bir indirme dizini seçiniz.")
            return

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }

        if file_format == "mp3":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            if resolution != "Highest":
                ydl_opts['format'] = f'bestvideo[height<={resolution[:-1]}]+bestaudio/best'

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                self.status_label.config(text="İndiriliyor, lütfen bekleyin...")
                ydl.download([url])
            self.status_label.config(text="İndirme tamamlandı!")
            messagebox.showinfo("Başarılı", "Video başarıyla indirildi!")
        except Exception as e:
            self.status_label.config(text="")
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

root = tk.Tk()
app = YouTubeDownloaderApp(root)
root.mainloop()
