import unittest

from analisis_suhu import analisis, hitung_rata_rata, baca_data

DATA = [
    {"hari": "Senin", "suhu": 31},
    {"hari": "Selasa", "suhu": 33},
    {"hari": "Rabu", "suhu": 29},
    {"hari": "Kamis", "suhu": 35},
    {"hari": "Jumat", "suhu": 32},
    {"hari": "Sabtu", "suhu": 30},
    {"hari": "Minggu", "suhu": 28},
]


class TestAnalisisSuhu(unittest.TestCase):
    def test_rata_rata(self):
        hasil = analisis(DATA)
        self.assertAlmostEqual(hasil["rata_rata"], 31.1428571, places=4)
        self.assertEqual(hitung_rata_rata(10, 20, 30), 20)

    def test_tertinggi_dan_terendah(self):
        hasil = analisis(DATA)
        self.assertEqual(hasil["tertinggi"], {"hari": "Kamis", "suhu": 35})
        self.assertEqual(hasil["terendah"], {"hari": "Minggu", "suhu": 28})

    def test_kategori_dan_jumlah_panas(self):
        hasil = analisis(DATA)
        kat = {k["hari"]: k["kategori"] for k in hasil["kategori"]}
        self.assertEqual(kat["Jumat"], "Panas")  
        self.assertEqual(kat["Senin"], "Normal")
        self.assertEqual(hasil["jumlah_panas"], 3)  

    def test_keyword_argument_batas_panas(self):
        hasil = analisis(DATA, batas_panas=30)
        self.assertEqual(hasil["jumlah_panas"], 5)



if __name__ == "__main__":
    unittest.main()