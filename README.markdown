# FLAC → MP3 Converter

A simple Windows background tool that automatically converts FLAC files to high-quality MP3 (320 kbps) while preserving:
- All metadata (artist, album, title, track number, genre)
- Album cover art
- Full folder structure

Perfect for converting entire music libraries.

## How to use
1. Run the program (`python main.py` or double-click `run.bat`)
2. Two folders will appear on your Desktop:
   - `upload_flac_dir` — drop your FLAC files or albums here
   - `result_mp3_dir` — converted MP3 files will appear here
3. The program runs in the background and processes new files automatically
4. Real-time status is shown in the window

## Requirements
- Python 3.14+
- FFmpeg installed and added to PATH

## Installation
```bash
pip install -r requirements.txt

Note: The project uses pydub-ng (installed automatically) for compatibility with modern Python versions.

## Launch
Just run:
Bashpython main.py
or double-click run.bat