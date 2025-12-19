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

## How to use

1. Run the program:
   - Double-click `run.bat`, or
   - Run `python main.py` in the terminal
2. Two folders will be created on your Desktop:
   - `upload_flac_dir` → drop your FLAC files or entire albums here (with subfolders)
   - `result_mp3_dir` → converted MP3 files will appear here with the same structure
3. The program runs in the background and instantly processes any new files
4. All progress and status are shown in the application window

## Requirements

- Python 3.14 or higher
- FFmpeg installed and added to PATH

## Installation

```bash
pip install -r requirements.txt
```

**Note:** The project uses `pydub-ng` (installed automatically via requirements.txt) for compatibility with modern Python versions.

## Launch

```bash
python main.py
```

or simply double-click `run.bat`

---

# Конвертер FLAC → MP3

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

## Как пользоваться

1. Запустите программу:
   - Двойной клик по `run.bat`, или
   - В терминале выполните `python main.py`
2. На рабочем столе создадутся две папки:
   - `upload_flac_dir` → кидайте сюда FLAC-файлы или целые альбомы (с подпапками)
   - `result_mp3_dir` → сюда попадут готовые MP3 с сохранённой структурой
3. Программа работает в фоне и сразу обрабатывает новые файлы
4. Весь процесс и статус отображаются в окне программы

## Требования

- Python 3.14 или новее
- FFmpeg установлен и добавлен в PATH

## Установка зависимостей

```bash
pip install -r requirements.txt
```

**Примечание:** Проект использует `pydub-ng` (устанавливается автоматически) для совместимости с современными версиями Python.

## Запуск

```bash
python main.py
```

или просто дважды кликните по `run.bat`