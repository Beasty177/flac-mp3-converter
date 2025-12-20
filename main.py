import os
import time
from pathlib import Path
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError, ID3, APIC, TIT2, TPE1, TALB, TCON, TRCK

# Desktop folders
desktop = Path(os.path.expanduser("~/Desktop"))
UPLOAD_DIR = desktop / "upload_flac_dir"
RESULT_DIR = desktop / "result_mp3_dir"

class FLACtoMP3Converter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BEASTY FLAC → MP3 Converter")
        self.root.geometry("800x650")
        self.root.configure(bg="#212121")
        self.root.resizable(True, True)

        # Header
        header = tk.Label(self.root, text="FLAC to MP3 320kbps Converter", font=("Arial", 16, "bold"), bg="#212121", fg="#ffffff")
        header.pack(pady=(20, 10))

        status = tk.Label(self.root, text="Auto-scan active", font=("Arial", 12), bg="#212121", fg="#00ff00")
        status.pack(pady=(0, 20))

        # Log area — теперь копируется (Ctrl+C)
        self.log_text = scrolledtext.ScrolledText(
            self.root, font=("Consolas", 10), bg="#000000", fg="#00ff00",
            insertbackground="#00ff00", selectbackground="#333333", selectforeground="#ffffff",
            state='disabled'  # Блокируем редактирование, но выделение работает
        )
        self.log_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Подсказка
        hint = tk.Label(self.root, text="Tip: Highlight text → Ctrl+C to copy log", font=("Arial", 9), bg="#212121", fg="#888888")
        hint.pack(pady=(0, 10))

        # Buttons
        button_frame = tk.Frame(self.root, bg="#212121")
        button_frame.pack(pady=10)

        self.manual_button = tk.Button(
            button_frame, text="Scan and Convert Now", command=self.manual_scan,
            font=("Arial", 12, "bold"), bg="#ff9800", fg="white", width=25, height=2
        )
        self.manual_button.pack(side=tk.LEFT, padx=20)

        self.stop_button = tk.Button(
            button_frame, text="Stop and Exit", command=self.stop,
            font=("Arial", 12, "bold"), bg="#d32f2f", fg="white", width=25, height=2
        )
        self.stop_button.pack(side=tk.LEFT, padx=20)

        self.running = True
        self.processed_files = set()  # Отслеживаем уже обработанные файлы

    def log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, full_message)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
        print(full_message.strip())

    def create_folders(self):
        UPLOAD_DIR.mkdir(exist_ok=True)
        RESULT_DIR.mkdir(exist_ok=True)
        self.log("Folders ready")
        self.log(f"Upload: {UPLOAD_DIR}")
        self.log(f"Output: {RESULT_DIR}")

    def copy_metadata_and_cover(self, flac_path: Path, mp3_path: Path):
        flac_file = FLAC(str(flac_path))
        try:
            mp3_file = ID3(str(mp3_path))
        except ID3NoHeaderError:
            mp3_file = ID3()

        tag_map = {"title": TIT2, "artist": TPE1, "album": TALB, "genre": TCON, "tracknumber": TRCK}
        for flac_key, id3_class in tag_map.items():
            if flac_key in flac_file:
                mp3_file.add(id3_class(encoding=3, text=flac_file[flac_key]))

        if flac_file.pictures:
            pic = flac_file.pictures[0]
            mp3_file.add(APIC(encoding=3, mime=pic.mime, type=3, desc='Cover', data=pic.data))

        mp3_file.save(v2_version=3)

    def convert(self, flac_path: Path):
        if not flac_path.exists() or str(flac_path) in self.processed_files:
            return

        try:
            relative = flac_path.relative_to(UPLOAD_DIR)
        except ValueError:
            relative = Path(flac_path.name)

        mp3_path = RESULT_DIR / relative.with_suffix(".mp3")
        mp3_path.parent.mkdir(parents=True, exist_ok=True)

        self.log(f"Converting: {flac_path.name}")

        try:
            audio = AudioSegment.from_file(str(flac_path), format="flac")
            audio.export(str(mp3_path), format="mp3", bitrate="320k")
            self.copy_metadata_and_cover(flac_path, mp3_path)
            self.log(f"Success: {mp3_path.name}")
            flac_path.unlink()
            self.log(f"Removed: {flac_path.name}")
            self.processed_files.add(str(flac_path))
        except Exception as e:
            self.log(f"Error: {str(e)}")

    def manual_scan(self):
        self.log("Manual scan started")
        flac_files = list(UPLOAD_DIR.rglob("*.flac"))
        if flac_files:
            self.log(f"Found {len(flac_files)} files")
            for p in flac_files:
                if self.running:
                    self.convert(p)
        else:
            self.log("No files found")
        self.log("Manual scan completed")

    def auto_scan(self):
        while self.running:
            time.sleep(10)
            if self.running:
                self.log("Auto-scan running (heartbeat)")
                flac_files = list(UPLOAD_DIR.rglob("*.flac"))
                new_files = [p for p in flac_files if str(p) not in self.processed_files]
                if new_files:
                    self.log(f"Auto-scan found {len(new_files)} new files. Converting...")
                    for p in new_files:
                        if self.running:
                            self.convert(p)
                else:
                    self.log("Auto-scan: no new files")

    def start(self):
        self.create_folders()
        self.manual_scan()  # Начальный скан при запуске
        Thread(target=self.auto_scan, daemon=True).start()

    def stop(self):
        self.running = False
        self.log("Shutting down...")
        self.log("Stopped.")
        self.root.quit()

    def run(self):
        Thread(target=self.start, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

if __name__ == "__main__":
    app = FLACtoMP3Converter()
    app.run()