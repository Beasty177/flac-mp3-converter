import os
import time
from pathlib import Path
from threading import Thread
import tkinter as tk
import subprocess

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
        self.root.geometry("400x650")
        self.root.configure(bg="#212121")
        self.root.resizable(True, True)

        # Header
        header = tk.Label(self.root, text="FLAC → MP3 Converter", font=("Arial", 14, "bold"), bg="#212121", fg="#ffffff")
        header.pack(pady=(15, 10))

        # Log area — текст копируется
        log_frame = tk.Frame(self.root)
        log_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(
            log_frame, font=("Consolas", 9), bg="#000000", fg="#00ff00",
            insertbackground="#00ff00", selectbackground="#004400", selectforeground="#ffffff",
            wrap=tk.WORD
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)



        # Controls frame
        controls_frame = tk.Frame(self.root, bg="#212121")
        controls_frame.pack(pady=10, fill=tk.X)

        # Auto-scan toggle
        self.auto_scan_var = tk.BooleanVar(value=True)
        self.auto_scan_check = tk.Checkbutton(
            controls_frame, text="Auto-scan", variable=self.auto_scan_var,
            command=self.toggle_auto_scan, font=("Arial", 10), bg="#212121", fg="#ffffff",
            selectcolor="#333333", activebackground="#212121"
        )
        self.auto_scan_check.pack(anchor=tk.W, padx=30)

        # Open folders buttons — зелёные, по центру
        open_frame = tk.Frame(self.root, bg="#212121")
        open_frame.pack(pady=5)

        self.open_upload_btn = tk.Button(
            open_frame, text="Open Upload Folder", command=self.open_upload_folder,
            font=("Arial", 9, "bold"), bg="#4caf50", fg="white", width=20
        )
        self.open_upload_btn.pack(side=tk.LEFT, padx=10)

        self.open_result_btn = tk.Button(
            open_frame, text="Open Result Folder", command=self.open_result_folder,
            font=("Arial", 9, "bold"), bg="#4caf50", fg="white", width=20
        )
        self.open_result_btn.pack(side=tk.LEFT, padx=10)

        # Manual scan button
        self.manual_button = tk.Button(
            self.root, text="Scan and Convert Now", command=self.manual_scan,
            font=("Arial", 10, "bold"), bg="#ff9800", fg="white", width=40, height=2
        )
        self.manual_button.pack(pady=15)

        self.running = True
        self.auto_scan_active = True
        self.processed_files = set()

    def log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, full_message)
        self.log_text.see(tk.END)
        self.log_text.config(state='normal')  # Оставляем normal для копирования

    def create_folders(self):
        UPLOAD_DIR.mkdir(exist_ok=True)
        RESULT_DIR.mkdir(exist_ok=True)
        self.log("Folders initialized")
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
        str_path = str(flac_path)
        if not flac_path.exists() or str_path in self.processed_files:
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
            self.processed_files.add(str_path)
        except Exception as e:
            self.log(f"Error: {str(e)}")

    def manual_scan(self):
        self.log("Manual scan started")
        flac_files = [p for p in UPLOAD_DIR.rglob("*.flac") if str(p) not in self.processed_files]
        if flac_files:
            self.log(f"Found {len(flac_files)} new files")
            for p in flac_files:
                if self.running:
                    self.convert(p)
        else:
            self.log("No new files")
        self.log("Manual scan completed")

    def toggle_auto_scan(self):
        if self.auto_scan_var.get():
            self.auto_scan_active = True
            self.log("Auto-scan enabled")
        else:
            self.auto_scan_active = False
            self.log("Auto-scan disabled — manual only")

    def auto_scan_loop(self):
        while self.running:
            time.sleep(10)
            if self.running and self.auto_scan_active:
                flac_files = [p for p in UPLOAD_DIR.rglob("*.flac") if str(p) not in self.processed_files]
                if flac_files:
                    self.log(f"Auto-scan: {len(flac_files)} new files")
                    for p in flac_files:
                        if self.running:
                            self.convert(p)

    def open_upload_folder(self):
        subprocess.Popen(f'explorer "{UPLOAD_DIR}"')

    def open_result_folder(self):
        subprocess.Popen(f'explorer "{RESULT_DIR}"')

    def start(self):
        self.create_folders()
        self.manual_scan()
        self.log("Auto-scan enabled (default)")
        Thread(target=self.auto_scan_loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.log("Shutting down...")
        self.log("Application stopped.")
        self.root.quit()

    def run(self):
        Thread(target=self.start, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.stop)  # Закрытие крестиком останавливает всё
        self.root.mainloop()

if __name__ == "__main__":
    app = FLACtoMP3Converter()
    app.run()