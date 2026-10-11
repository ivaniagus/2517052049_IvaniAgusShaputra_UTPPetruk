"""main.py - program utama Aplikasi KRS & IPK.  Jalankan: python main.py"""
import unittest

from krs_package import (FILE_DATA, FILE_LAPORAN, DataTidakValidError, MataKuliah, baca_data,
                         buat_file_data, buat_laporan, kelompokkan_per_semester, parse_baris,
                         tambah_data, tulis_laporan, validasi_nama, validasi_nilai_angka,
                         validasi_semester, validasi_sks)
from krs_package import testing

# Data contoh dalam format yang sama dengan isi file data
DATA_CONTOH = """\
1;Pemrograman Terstruktur;3;90;85;90;dosen=Pak Rahman
1;Statistika;3;75;70;72;ruang=GIKL1
1;Pengenalan Organisasi Komputer;3;60;45;40;dosen=Pak Febi;hari=Senin
2;Struktur Data;3;80;78;82;dosen=Bu Dhella
2;Basis Data;3;85;80;90
2;Penggunaan Generative AI;3;70;60;65;ruang=R.103
3;Pemrograman Berorientasi Objek;3;95;90;92;dosen=Pak Agung;ruang=GIKL1B
3;Sistem Operasi;3;80;75;78;dosen=Pak Yoga
3;Jaringan Komputer;3;70;65;72;hari=Rabu
3;Rekayasa Perangkat Lunak;3;50;45;40""".splitlines()

MENU = """
=========== MENU KRS & IPK ===========
 1. Buat file data (+ data contoh)
 2. Tambah mata kuliah
 3. Lihat KRS, IP semester & IPK
 4. Simpan laporan ke file
 5. Jalankan unit test
 0. Keluar
======================================"""


def minta_input(pertanyaan, validator, default=None):
    """Ulangi pertanyaan sampai valid. Enter = nilai default (bila ada)."""
    while True:
        teks = input(pertanyaan).strip()
        if not teks and default is not None:
            return default
        try:
            return validator(teks)
        except DataTidakValidError as err:
            print(f"  Input tidak valid: {err}")


def menu_buat_file():
    if not buat_file_data():
        print("File data sudah ada, tidak ditimpa.")
        return
    print(f"File data baru dibuat: {FILE_DATA}")
    if input("Isi dengan data contoh semester 1-3? (y/n): ").strip().lower() == "y":
        for baris in DATA_CONTOH:
            tambah_data(MataKuliah(**parse_baris(baris)))
        print(f"{len(DATA_CONTOH)} mata kuliah contoh ditambahkan.")


def menu_tambah():
    buat_file_data()                                  # aman: tidak menimpa bila sudah ada
    semester = minta_input("Semester (1-14)      : ", validasi_semester)
    nama = minta_input("Nama mata kuliah    : ", validasi_nama)
    sks = minta_input("SKS (1-6)           : ", validasi_sks)
    tugas = minta_input("Nilai tugas (0-100) : ", lambda t: validasi_nilai_angka(t, "Nilai tugas"))
    uts = minta_input("Nilai UTS (0-100)   : ", lambda t: validasi_nilai_angka(t, "Nilai UTS"))
    uas = minta_input("Nilai UAS (0-100)   : ", lambda t: validasi_nilai_angka(t, "Nilai UAS"))
    atribut = {}
    for kunci in ("dosen", "ruang", "hari"):          # opsional
        isi = input(f"{kunci.capitalize():<10} (boleh kosong): ").strip()
        if isi:
            atribut[kunci] = isi
    matkul = MataKuliah(nama, sks, tugas, uts, uas, semester, **atribut)
    tambah_data(matkul)
    print(f"Tersimpan: {matkul.info_lengkap()} -> nilai {matkul.nilai_akhir():.2f} ({matkul.nilai_huruf()})")


def ambil_laporan():
    """Baca data, tanya semester, kembalikan teks laporan (None bila belum ada data)."""
    daftar_matkul, dilewati = baca_data()
    for pesan in dilewati:
        print(f"  [!] {pesan}")
    daftar_semester = kelompokkan_per_semester(daftar_matkul)
    if not daftar_semester:
        print("Belum ada data. Pakai menu 1 atau 2 dulu.")
        return None
    terakhir = daftar_semester[-1].nomor
    nomor = minta_input(f"Nomor semester [{terakhir}]: ", validasi_semester, default=terakhir)
    return buat_laporan(daftar_semester, nomor)


def menu_lihat():
    laporan = ambil_laporan()
    if laporan:
        print("\n" + laporan)


def menu_simpan():
    laporan = ambil_laporan()
    if laporan:
        tulis_laporan(laporan)
        print("\n" + laporan)
        print(f"\nLaporan disimpan di: {FILE_LAPORAN}")


def menu_test():
    suite = unittest.defaultTestLoader.loadTestsFromModule(testing)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main():
    aksi = {"1": menu_buat_file, "2": menu_tambah, "3": menu_lihat, "4": menu_simpan, "5": menu_test}
    try:
        while True:
            print(MENU)
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "0":
                print("Terima kasih, sampai jumpa!")
                break
            if pilihan in aksi:
                aksi[pilihan]()
            else:
                print("Pilihan tidak dikenal, coba lagi.")
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")


if __name__ == "__main__":
    main()
