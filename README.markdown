# FLAC → MP3 Converter

A simple Windows background tool that automatically converts FLAC files to high-quality MP3 (320 kbps) while preserving:

- All metadata (artist, album, title, track number, genre)
- Album cover art
- Full folder structure

Perfect for converting entire music libraries without manual work.

## Features

- Background monitoring of the upload folder (using watchdog)
- Real-time log in a GUI window (Tkinter)
- Automatic conversion of new and existing FLAC files
- Deletes original FLAC files after successful conversion (keeps empty folders)
- Full support for nested folders and album structures


## Quick Start (Executable)

Download the latest ready-to-use version:

[Download BFMC.exe (Windows)](https://github.com/Beasty177/flac-mp3-converter/releases/latest/download/BFMC.exe)

- Double-click to run
- No Python or additional software needed
- Works on Windows 10/11

## How to use

1. Run the program:
   - Launch the application, or
   - Double-click `run.bat`, or
   - Run `python main.py` in the terminal
2. Two folders will be created on your Desktop:
   - `upload_flac_dir` → drop your FLAC files or entire albums here (with subfolders)
   - `result_mp3_dir` → converted MP3 files will appear here with the same structure
3. Files are processed automatically (auto-scan enabled by default) or manually
4. All progress and status are shown in the application window

## Requirements

- Python 3.14 or higher
- FFmpeg installed and added to PATH

## Installation

```bash
pip install -r requirements.txt
```

**Note:** The project uses `pydub-ng` (installed automatically via requirements.txt) for compatibility with modern Python versions.

## Launch (sourse)

```bash
python main.py
```

or simply double-click `run.bat`

---

# Конвертер BFMC — Beasty FLAC to MP3 Converter 

Простая программа для Windows, которая автоматически конвертирует FLAC-файлы в высококачественный MP3 (320 kbps) с полным сохранением:

- Всех метаданных (артист, альбом, название трека, номер трека, жанр)
- Обложки альбома
- Полной структуры папок

Идеально подходит для конвертации всей музыкальной коллекции без ручной работы.

## Возможности

- Фоновый мониторинг папки загрузки (на базе watchdog)
- Окно с логом в реальном времени (Tkinter)
- Автоматическая конвертация новых и уже существующих FLAC-файлов
- Удаление исходных FLAC после успешной конвертации (пустые папки остаются)
- Полная поддержка вложенных папок и структуры альбомов

## Быстрый запуск (готовый файл)

Скачайте последнюю версию:

[Скачать BFMC.exe (Windows)](https://github.com/Beasty177/flac-mp3-converter/releases/latest/download/BFMC.exe)

- Дважды кликните для запуска
- Не требуется Python и дополнительное ПО
- Работает на Windows 10/11

## Как пользоваться

1. Запустите программу:
   - Запустите приложение, или
   - Двойной клик по `run.bat`, или
   - В терминале выполните `python main.py`
2. На рабочем столе создадутся две папки:
   - `upload_flac_dir` → кидайте сюда FLAC-файлы или целые альбомы (с подпапками)
   - `result_mp3_dir` → сюда попадут готовые MP3 с сохранённой структурой
3. Файлы обрабатываются автоматически (авто-скан включён по умолчанию) или вручную
4. Весь процесс и статус отображаются в окне программы

## Требования

- Python 3.14 или новее
- FFmpeg установлен и добавлен в PATH

## Установка зависимостей

```bash
pip install -r requirements.txt
```

**Примечание:** Проект использует `pydub-ng` (устанавливается автоматически) для совместимости с современными версиями Python.

## Запуск (из исходников)

```bash
python main.py
```

или просто дважды кликните по `run.bat`