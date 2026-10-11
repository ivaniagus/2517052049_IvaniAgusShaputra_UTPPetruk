"""fileio.py - baca/tulis/tambah file. Mode: 'x' buat | 'a' tambah | 'r' baca | 'w' tulis."""
import os

from .processing import MataKuliah
from .validasi import parse_baris

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_DATA = os.path.join(BASE_DIR, "data_krs.txt")
FILE_LAPORAN = os.path.join(BASE_DIR, "laporan_krs.txt")


def buat_file_data(path=FILE_DATA):
    """Mode 'x': buat file baru. Return False bila file sudah ada (data lama aman)."""
    try:
        with open(path, "x", encoding="utf-8") as file:
            file.write("# semester;nama;sks;tugas;uts;uas;atribut(kunci=nilai)\n")
        return True
    except FileExistsError:
        return False


def tambah_data(matkul, path=FILE_DATA):
    """Mode 'a': tambah satu mata kuliah di akhir file."""
    with open(path, "a", encoding="utf-8") as file:
        file.write(matkul.ke_baris() + "\n")


def baca_data(path=FILE_DATA):
    """Mode 'r': return (daftar MataKuliah, daftar pesan baris yang dilewati)."""
    daftar_matkul, dilewati = [], []
    try:
        with open(path, "r", encoding="utf-8-sig") as file:
            for nomor, baris in enumerate(file, start=1):
                if not baris.strip() or baris.startswith("#"):
                    continue
                try:
                    daftar_matkul.append(MataKuliah(**parse_baris(baris)))
                except ValueError as err:                     # baris rusak dilewati saja
                    dilewati.append(f"Baris {nomor} dilewati: {err}")
    except FileNotFoundError:
        print("File data belum ada. Buat dulu lewat menu 1.")
    return daftar_matkul, dilewati


def tulis_laporan(teks, path=FILE_LAPORAN):
    """Mode 'w': tulis laporan (isi lama ditimpa)."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(teks + "\n")
