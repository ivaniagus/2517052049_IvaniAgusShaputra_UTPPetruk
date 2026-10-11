BATAS_LULUS = 70

def hitung_rata_rata(*nilai):
    """Menghitung rata-rata dari nilai (*args ke tuple)."""
    if not nilai:
        return 0
    return sum(nilai) / len(nilai)

def cek_status(rata_rata, batas=BATAS_LULUS):
    """Menentukan status kelulusan berdasarkan nilai rata-rata dan batas kelulusan."""
    return "Lulus" if rata_rata >= batas else "Tidak Lulus"

def tampilkan_hasil(nama, *nilai, batas=BATAS_LULUS):
    """Menampilkan nama, rata-rata, dan status kelulusan mahasiswa."""
    rata = hitung_rata_rata(*nilai)
    status = cek_status(rata)
    
    print(f"Nama : {nama}")
    print(f"Rata-rata : {rata}")
    print(f"Status : {status}")


if __name__ == '__main__':
    tampilkan_hasil("Budi", 80, 75, 90)
    tampilkan_hasil("Sari", 60, 65, 55, 70)