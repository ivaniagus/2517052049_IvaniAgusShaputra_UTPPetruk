"""testing.py - unit test.  Jalankan: python -m unittest krs_package.testing -v  (atau menu 5)"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from krs_package.fileio import baca_data, buat_file_data, tambah_data
from krs_package.processing import MataKuliah, SemesterKRS, hitung_ipk
from krs_package.validasi import DataTidakValidError, parse_baris, validasi_nama, validasi_nilai_angka, validasi_sks


def matkul_contoh():
    """Pemrograman Terstruktur 3 SKS = 81 (B), UI/Ux 2 SKS = 90 (A), Basis Data 4 SKS = 47.5 (D)."""
    return [MataKuliah("Pemrograman Terstruktur", 3, 80, 70, 90, 3),
            MataKuliah("UI/UX", 2, 90, 90, 90, 3),
            MataKuliah("Basis Data", 4, 60, 45, 40, 3)]


class TestValidasi(unittest.TestCase):
    def test_input_salah(self):
        for panggil in (lambda: validasi_nama("  "),
                        lambda: validasi_nilai_angka("-5"),
                        lambda: validasi_nilai_angka("101"),
                        lambda: validasi_sks("tiga"),
                        lambda: parse_baris("3;UI/UX;3;80")):
            with self.assertRaises(DataTidakValidError):
                panggil()

    def test_parse_baris(self):
        data = parse_baris("3;Sistem Operasi;3;80;75;85;dosen=Pak Yoga")
        self.assertEqual((data["nama"], data["dosen"]), ("Sistem Operasi", "Pak Yoga"))


class TestProcessing(unittest.TestCase):
    def setUp(self):
        self.semester = SemesterKRS(3)
        for mk in matkul_contoh():
            self.semester.tambah_matkul(mk)

    def test_nilai_dan_huruf(self):
        pemrograman_terstruktur, ui_ux, basis_data = matkul_contoh()
        self.assertEqual((pemrograman_terstruktur.nilai_akhir(), pemrograman_terstruktur.nilai_huruf()), (81.0, "B"))
        self.assertEqual(ui_ux.bobot(), 4)
        self.assertFalse(basis_data.lulus())

    def test_batas_huruf(self):
        huruf = lambda n: MataKuliah("X", 1, n, n, n).nilai_huruf()
        self.assertEqual([huruf(n) for n in (85, 84, 55, 40, 39)], list("ABCDE"))

    def test_assert_nilai_akhir(self):
        mk = MataKuliah("Uji", 2, 50, 50, 50)
        mk.uas = 1000                                    # sengaja dirusak
        with self.assertRaises(AssertionError):
            mk.nilai_akhir()

    def test_ip_dan_ipk(self):
        self.assertAlmostEqual(self.semester.hitung_ip_semester(), 21 / 9)   # (9+8+4)/9
        smt1, smt2 = SemesterKRS(1), SemesterKRS(2)
        smt1.tambah_matkul(MataKuliah("Basis Data", 4, 60, 45, 40))            # mutu 4
        smt2.tambah_matkul(MataKuliah("Pemrograman Terstruktur", 2, 90, 90, 90))           # mutu 8
        self.assertAlmostEqual(hitung_ipk(smt1, smt2), 2.0)
        self.assertEqual(hitung_ipk(), 0.0)

    def test_filter_dan_urutan(self):
        self.assertEqual([mk.nama for mk in self.semester.filter_matkul_lulus()], ["Pemrograman Terstruktur", "UI/UX"])
        self.assertEqual([mk.nama for mk in self.semester.urutkan_berdasarkan_bobot_nilai()],
                         ["UI/UX", "Pemrograman Terstruktur", "Basis Data"])


class TestFileIO(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = os.path.join(folder.name, "data_uji.txt")

    def test_buat_tambah_baca(self):
        self.assertTrue(buat_file_data(self.path))
        self.assertFalse(buat_file_data(self.path))                  # tidak menimpa
        mk = MataKuliah("Jaringan", 3, 87.5, 65, 72, 2, dosen="Pak Alwine")
        tambah_data(mk, self.path)
        daftar, dilewati = baca_data(self.path)
        self.assertEqual([m.ke_baris() for m in daftar], [mk.ke_baris()])
        self.assertEqual(dilewati, [])

    def test_baris_rusak_dilewati(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("# komentar\n3;Pemrograman Terstruktur;3;80;70;90\n3;;3;80;75;85\n"
                       "3;UI/UX;tiga;80;75;85\nbukan data\n3;Manajemen Proses Bisnis;2;70;70;70\n")
        daftar, dilewati = baca_data(self.path)
        self.assertEqual([m.nama for m in daftar], ["Pemrograman Terstruktur", "Manajemen Proses Bisnis"])
        self.assertEqual(len(dilewati), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
