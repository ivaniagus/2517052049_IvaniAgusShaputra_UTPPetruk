"""validasi.py - pengecekan input dan data KRS."""


class DataTidakValidError(ValueError):
    """Exception buatan sendiri untuk data tidak valid."""


def validasi_angka(teks, nama_field, minimal, maksimal, tipe=float):
    """Ubah teks jadi angka, lalu pastikan ada di rentang minimal..maksimal."""
    try:
        angka = tipe(teks)
    except ValueError:
        raise DataTidakValidError(f"{nama_field} harus berupa angka, bukan '{teks}'.")
    if not minimal <= angka <= maksimal:
        raise DataTidakValidError(f"{nama_field} harus {minimal}-{maksimal}, bukan {angka:g}.")
    return angka


def validasi_nama(nama):
    """Nama tidak boleh kosong dan tidak boleh memuat ';' (pemisah kolom di file)."""
    nama = str(nama).strip()
    if not nama or ";" in nama:
        raise DataTidakValidError("Nama mata kuliah tidak boleh kosong atau memuat ';'.")
    return nama


def validasi_sks(teks):
    return validasi_angka(teks, "SKS", 1, 6, int)


def validasi_semester(teks):
    return validasi_angka(teks, "Semester", 1, 14, int)


def validasi_nilai_angka(teks, nama_field="Nilai"):
    return validasi_angka(teks, nama_field, 0, 100)


def parse_baris(baris):
    """Pecah satu baris file jadi dict, siap dipakai: MataKuliah(**data).

    Format: semester;nama;sks;tugas;uts;uas
    """
    bagian = baris.strip().split(";")
    if len(bagian) < 6:
        raise DataTidakValidError(f"Kolom kurang: butuh minimal 6, ditemukan {len(bagian)}.")

    semester, nama, sks, tugas, uts, uas = bagian[:6]
    data = {"semester": semester, "nama": nama, "sks": sks,
            "tugas": tugas, "uts": uts, "uas": uas}
    for teks in bagian[6:]:                      # sisanya: atribut tambahan kunci=nilai
        kunci, pemisah, nilai = teks.partition("=")
        if not pemisah or kunci.strip() in data:
            raise DataTidakValidError(f"Atribut '{teks}' tidak valid (format: kunci=nilai).")
        data[kunci.strip()] = nilai.strip()
    return data
