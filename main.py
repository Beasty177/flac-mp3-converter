import os
import time
from pathlib import Path
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError, ID3, APIC, TIT2, TPE1, TALB, TCON, TRCK
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Desktop folders
desktop = Path(os.path.expanduser("~/Desktop"))
UPLOAD_DIR = desktop / "upload_flac_dir"
RESULT_DIR = desktop / "result_mp3_dir"

class FLACtoMP3Converter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FLAC → MP3 320kbps Converter")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        # Log area
        self.log_text = scrolledtext.ScrolledText(
            self.root, state='disabled', font=("Consolas", 10), bg="black", fg="#00ff00"
        )
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Stop button
        self.stop_button = tk.Button(
            self.root, text="Stop and Exit", command=self.stop, bg="#ff4444", fg="white", font=("Arial", 10, "bold")
        )
        self.stop_button.pack(pady=8)

        self.observer = None
        self.running = True

    def log(self, message: str):
        def _insert():
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        self.root.after(0, _insert)

    def create_folders(self):
        UPLOAD_DIR.mkdir(exist_ok=True)
        RESULT_DIR.mkdir(exist_ok=True)
        self.log(f"Folders ready:")
        self.log(f"  Upload: {UPLOAD_DIR}")
        self.log(f"  Result: {RESULT_DIR}")

    def copy_metadata_and_cover(self, flac_path: Path, mp3_path: Path):
        flac_file = FLAC(str(flac_path))
        try:
            mp3_file = ID3(str(mp3_path))
        except ID3NoHeaderError:
            mp3_file = ID3()

        tag_map = {
            "title": TIT2,
            "artist": TPE1,
            "album": TALB,
            "genre": TCON,
            "tracknumber": TRCK,
        }
        for flac_key, id3_class in tag_map.items():
            if flac_key in flac_file:
                mp3_file.add(id3_class(encoding=3, text=flac_file[flac_key]))

        if flac_file.pictures:
            pic = flac_file.pictures[0]
            mp3_file.add(APIC(encoding=3, mime=pic.mime, type=3, desc='Cover', data=pic.data))

        mp3_file.save(v2_version=3)

    def convert(self, flac_path: Path):
        try:
            relative = flac_path.relative_to(UPLOAD_DIR)
        except ValueError:
            relative = Path(flac_path.name)

        mp3_path = RESULT_DIR / relative.with_suffix(".mp3")
        mp3_path.parent.mkdir(parents=True, exist_ok=True)

        self.log(f"Converting: {flac_path.name}")

        audio = AudioSegment.from_file(str(flac_path), format="flac")
        audio.export(str(mp3_path), format="mp3", bitrate="320k")

        self.copy_metadata_and_cover(flac_path, mp3_path)
        self.log(f"Done: {mp3_path.name}")

        flac_path.unlink()
        self.log(f"Original FLAC deleted: {flac_path.name}")

    def process_existing_files(self):
        flac_files = list(UPLOAD_DIR.rglob("*.flac"))
        if flac_files:
            self.log(f"Found {len(flac_files)} existing FLAC files — converting...")
            for path in flac_files:
                if self.running:
                    self.convert(path)
        else:
            self.log("Upload folder is empty — waiting for new files...")

    def start_monitoring(self):
        class Handler(FileSystemEventHandler):
            def on_created(self, event):
                if event.is_directory:
                    return
                path = Path(event.src_path)
                if path.suffix.lower() == ".flac":
                    time.sleep(1)  # Wait for file to finish copying
                    if path.exists() and self.running:
                        self.convert(path)

            def on_moved(self, event):
                if event.is_directory:
                    return
                path = Path(event.dest_path)
                if path.suffix.lower() == ".flac" and UPLOAD_DIR in path.parents:
                    time.sleep(1)
                    if path.exists() and self.running:
                        self.convert(path)

        self.create_folders()
        self.process_existing_files()

        self.observer = Observer()
        self.observer.schedule(Handler(), str(UPLOAD_DIR), recursive=True)
        self.observer.start()
        self.log("Monitoring started — drop FLAC files into 'upload_flac_dir'!")

    def stop(self):
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.log("Converter stopped.")
        self.root.quit