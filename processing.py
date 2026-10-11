"""processing.py - class dan perhitungan KRS (IP semester & IPK)."""
from .validasi import (validasi_nama, validasi_nilai_angka, validasi_semester, validasi_sks)

BOBOT_KOMPONEN = {"tugas": 0.3, "uts": 0.3, "uas": 0.4}
BATAS_HURUF = ((85, "A"), (70, "B"), (55, "C"), (40, "D"))   # di bawah 40 = E
BOBOT_HURUF = {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0}
BOBOT_LULUS_MIN = 2                                          # lulus bila minimal C


def total_sks_diambil(*sks):
    """Jumlahkan sejumlah SKS sekaligus (*args)."""
    return sum(sks)


class MataKuliah:
    def __init__(self, nama, sks, tugas, uts, uas, semester=1, **atribut):
        # **atribut menampung data tambahan, mis. dosen="Pak Budi", ruang="R.201"
        self.nama = validasi_nama(nama)
        self.sks = validasi_sks(sks)
        self.tugas = validasi_nilai_angka(tugas, "Nilai tugas")
        self.uts = validasi_nilai_angka(uts, "Nilai UTS")
        self.uas = validasi_nilai_angka(uas, "Nilai UAS")
        self.semester = validasi_semester(semester)
        self.atribut = atribut

    def nilai_akhir(self):
        total = sum(getattr(self, k) * bobot for k, bobot in BOBOT_KOMPONEN.items())
        assert 0 <= total <= 100, f"Nilai akhir di luar rentang 0-100: {total}"
        return round(total, 2)

    def nilai_huruf(self):
        nilai = self.nilai_akhir()
        return next((huruf for batas, huruf in BATAS_HURUF if nilai >= batas), "E")

    def bobot(self):
        return BOBOT_HURUF[self.nilai_huruf()]

    def lulus(self):
        return self.bobot() >= BOBOT_LULUS_MIN

    def info_lengkap(self):
        return f"{self.nama} ({self.sks} SKS)" + "".join(f", {k}: {v}" for k, v in self.atribut.items())

    def ke_baris(self):
        """Satu baris teks untuk disimpan ke file."""
        kolom = [self.semester, self.nama, self.sks, f"{self.tugas:g}", f"{self.uts:g}", f"{self.uas:g}"]
        kolom += [f"{k}={str(v).replace(';', ',')}" for k, v in self.atribut.items()]
        return ";".join(map(str, kolom))


class SemesterKRS:
    """Kumpulan mata kuliah dalam satu semester."""

    def __init__(self, nomor):
        self.nomor = nomor
        self.daftar_matkul = []

    def tambah_matkul(self, matkul):
        self.daftar_matkul.append(matkul)

    def hitung_total_sks(self):
        return total_sks_diambil(*[mk.sks for mk in self.daftar_matkul])

    def hitung_total_mutu(self):
        return sum(mk.sks * mk.bobot() for mk in self.daftar_matkul)

    def hitung_ip_semester(self):
        sks = self.hitung_total_sks()
        return self.hitung_total_mutu() / sks if sks else 0.0

    def filter_matkul_lulus(self):
        return list(filter(lambda mk: mk.lulus(), self.daftar_matkul))

    def urutkan_berdasarkan_bobot_nilai(self):
        """Urutkan dari nilai tertinggi."""
        return sorted(self.daftar_matkul, key=lambda mk: (mk.bobot(), mk.nilai_akhir()), reverse=True)


def hitung_ipk(*daftar_semester):
    """IPK dari sejumlah semester sekaligus (*args)."""
    sks = total_sks_diambil(*[s.hitung_total_sks() for s in daftar_semester])
    mutu = sum(s.hitung_total_mutu() for s in daftar_semester)
    return mutu / sks if sks else 0.0


def kelompokkan_per_semester(daftar_matkul):
    """Kelompokkan mata kuliah ke SemesterKRS, terurut menurut nomor semester."""
    kelompok = {}
    for mk in daftar_matkul:
        kelompok.setdefault(mk.semester, SemesterKRS(mk.semester)).tambah_matkul(mk)
    return [kelompok[nomor] for nomor in sorted(kelompok)]


def buat_laporan(daftar_semester, nomor):
    """Teks laporan satu semester + IP semester + IPK sampai semester itu."""
    semester = next((s for s in daftar_semester if s.nomor == nomor), None)
    if semester is None:
        return f"Semester {nomor} belum memiliki data."

    garis = "-" * 65
    baris = [f"LAPORAN HASIL STUDI - SEMESTER {nomor}", garis,
             f"{'Mata Kuliah':<34}{'SKS':>4}{'Nilai':>8}{'Huruf':>6}  Status", garis]
    for mk in semester.urutkan_berdasarkan_bobot_nilai():
        status = "Lulus" if mk.lulus() else "Tidak lulus"
        baris.append(f"{mk.nama[:33]:<34}{mk.sks:>4}{mk.nilai_akhir():>8.2f}{mk.nilai_huruf():>6}  {status}")
    baris.append(garis)

    sampai_sini = [s for s in daftar_semester if s.nomor <= nomor]
    baris += [
        f"{'Total SKS semester':<24}: {semester.hitung_total_sks()}",
        f"{'Mata kuliah lulus':<24}: {len(semester.filter_matkul_lulus())} dari {len(semester.daftar_matkul)}",
        f"{f'IP semester {nomor}':<24}: {semester.hitung_ip_semester():.2f}",
        f"{f'IPK s.d. semester {nomor}':<24}: {hitung_ipk(*sampai_sini):.2f}",
    ]
    keterangan = [f"  - {mk.info_lengkap()}" for mk in semester.daftar_matkul if mk.atribut]
    if keterangan:
        baris += ["Keterangan:"] + keterangan
    return "\n".join(baris)
