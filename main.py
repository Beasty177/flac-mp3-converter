import os
import shutil
from pathlib import Path
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError, ID3, APIC, TIT2, TPE1, TALB, TCON, TRCK
from mutagen.mp4 import MP4Cover

# Пути к папкам на рабочем столе
desktop = Path(os.path.expanduser("~/Desktop"))
UPLOAD_DIR = desktop / "upload_flac_dir"
RESULT_DIR = desktop / "result_mp3_dir"

def create_folders():
    """Создаёт папки на рабочем столе, если их нет"""
    UPLOAD_DIR.mkdir(exist_ok=True)
    RESULT_DIR.mkdir(exist_ok=True)
    print(f"Папки созданы/проверены:\n  Загрузка: {UPLOAD_DIR}\n  Результат: {RESULT_DIR}")

def copy_metadata_and_cover(flac_path: Path, mp3_path: Path):
    """Копирует метаданные и обложку из FLAC в MP3"""
    flac_file = FLAC(str(flac_path))
    
    try:
        mp3_file = ID3(str(mp3_path))
    except ID3NoHeaderError:
        mp3_file = ID3()
    
    # Копируем основные тэги
    mapping = {
        "title": TIT2,
        "artist": TPE1,
        "album": TALB,
        "genre": TCON,
        "tracknumber": TRCK,
    }
    
    for flac_tag, id3_class in mapping.items():
        if flac_tag in flac_file:
            mp3_file.add(id3_class(encoding=3, text=flac_file[flac_tag]))
    
    # Копируем обложку, если есть
    if flac_file.pictures:
        picture = flac_file.pictures[0]
        mp3_file.add(APIC(
            encoding=3,
            mime=picture.mime,
            type=3,  # Cover (front)
            desc='Cover',
            data=picture.data
        ))
    
    mp3_file.save(v2_version=3)  # ID3v2.3 для лучшей совместимости

def convert_flac_to_mp3(flac_path: Path, relative_path: Path):
    """Конвертирует один FLAC в MP3 с сохранением структуры"""
    # Путь в папке результата (сохраняем структуру)
    mp3_path = RESULT_DIR / relative_path.with_suffix(".mp3")
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Конвертируем: {flac_path.name}")
    
    # Конвертация через pydub + ffmpeg
    audio = AudioSegment.from_file(str(flac_path), format="flac")
    audio.export(str(mp3_path), format="mp3", bitrate="320k")
    
    # Копируем метаданные и обложку
    copy_metadata_and_cover(flac_path, mp3_path)
    
    print(f"Готово: {mp3_path}")
    
    # Удаляем исходный FLAC (оставляем папки!)
    flac_path.unlink()
    print(f"Исходный FLAC удалён: {flac_path}")

def test_single_file():
    """Тест: найди любой FLAC в upload и конвертируй (для проверки)"""
    create_folders()
    flac_files = list(UPLOAD_DIR.rglob("*.flac"))
    if not flac_files:
        print("Для теста кинь любой .flac файл (или папку с ними) в папку upload_flac_dir на рабочем столе")
        return
    
    for flac_path in flac_files:
        # Относительный путь от upload_dir для сохранения структуры
        try:
            relative = flac_path.relative_to(UPLOAD_DIR)
        except ValueError:
            relative = flac_path.name
        convert_flac_to_mp3(flac_path, relative)

if __name__ == "__main__":
    print("=== Тест конвертации одного/нескольких файлов ===")
    test_single_file()
    print("\nТест завершён. Если всё ок — в следующей версии добавим мониторинг в фоне.")