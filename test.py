import customtkinter
from CTkMessagebox import CTkMessagebox
from CTkMenuBar import *
from customtkinter import filedialog
from PIL import Image
from pinterest import Pinterest
from pypdl import Downloader
import threading
import os
import configparser
from urllib.parse import urlparse
import time
import webbrowser

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("PintDown")
        self.geometry('700x250')

        # Create frame
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.menu = CTkTitleMenu(self)
        self.file = self.menu.add_cascade("File", hover_color="#b60000")
        self.about = self.menu.add_cascade("About", hover_color="#b60000", command=self.about)
        self.download_folder = CustomDropdownMenu(widget=self.file)
        self.download_folder.add_option(option="Download Folder", command=self.ask_directory)
        self.dl = Downloader()
        self.resizable(False, False)

        self.label = customtkinter.CTkLabel(self.frame, text="PinDown", font=("Helvetica", 30))
        self.label.pack(pady=10)

        self.link_enty = customtkinter.CTkEntry(self.frame, width=550, height=40, corner_radius=15)
        self.link_enty.pack(pady=10, padx=30)

        self.frame_progress = customtkinter.CTkFrame(self.frame, width=550, height=30, bg_color="transparent", fg_color="transparent")
        self.frame_progress.pack(pady=10)

        self.download_btn = customtkinter.CTkButton(self.frame, text="Download", corner_radius=12, fg_color="#b60000", hover_color="white", text_color="Black", font=("Helvetica", 14), command=lambda: threading.Thread(target=self.download).start())
        self.download_btn.pack(pady=10)

    def about(self):
        msg = CTkMessagebox(title="About", message="Made by Y3script.\nFor More info Contact Me via social Media.", option_2="Visit")
        if msg.get() == "Visit":
            webbrowser.open("https://bio.link/y3script")

    def download(self):
        while not os.path.exists("config.ini"):
            self.ask_directory()
        if self.link_enty.get() != "":
            config = configparser.ConfigParser()
            config.read("config.ini")
            try:
                download_path = config.get('Download_Path', 'path')
            except configparser.NoOptionError:
                CTkMessagebox(title="Error", message="Download path not set in config file.")
                return

            pin = Pinterest(self.link_enty.get())
            self.download_btn.configure(state="disabled")
            media_link = pin.get_media_Link()
            if media_link and media_link.get("success"):
                media_link = media_link['link']
                threading.Thread(target=self.progress_dl).start()
                url_parse = urlparse(media_link)
                self.dl.start(media_link, multithread=True, display=False, file_path=os.path.join(download_path, os.path.basename(url_parse.path)))

    def ask_directory(self):
        path = filedialog.askdirectory()
        config = configparser.ConfigParser()
        config["Download_Path"] = {"path": path}
        with open("config.ini", "w", encoding="utf-8") as configfile:
            config.write(configfile)

    def progress_dl(self):
        self.progress = customtkinter.CTkProgressBar(self.frame_progress, progress_color="#b60000", width=550)
        self.progress.pack(pady=10)
        while self.dl.progress < 100:
            self.progress.set(int(self.dl.progress) / 100)
        self.progress.set(1)
        time.sleep(2)
        self.progress.destroy()
        CTkMessagebox(title="success", message="File downloaded successfully", icon="check")
        self.download_btn.configure(state="normal")


app = App()
app.mainloop()
