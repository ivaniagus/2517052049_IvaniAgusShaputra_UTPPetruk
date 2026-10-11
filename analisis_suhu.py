BATAS_PANAS = 32

# Tahap 1: Baca data
def baca_data(nama_file="suhu.txt"):
    data = []
    try:
        with open(nama_file, "r") as f:
            for baris in f:
                baris = baris.strip()
                if not baris:
                    continue
                hari, suhu = baris.split(";")
                data.append({"hari": hari, "suhu": int(suhu)})
    except FileNotFoundError:
        print(f"Error: file '{nama_file}' tidak ditemukan.")
        return None
    return data


# Tahap 2: Analisis
def hitung_rata_rata(*suhu):
    return sum(suhu) / len(suhu)


def analisis(data, batas_panas=BATAS_PANAS):
    rata_rata = hitung_rata_rata(*[d["suhu"] for d in data])
    kunci_suhu = lambda d: d["suhu"]
    tertinggi = max(data, key=kunci_suhu)
    terendah = min(data, key=kunci_suhu)

    
    kategori_hari = lambda d: "Panas" if d["suhu"] >= batas_panas else "Normal"
    kategori = [{"hari": d["hari"], "suhu": d["suhu"], "kategori": kategori_hari(d)}
                for d in data]

    jumlah_panas = len([k for k in kategori if k["kategori"] == "Panas"])

    return {
        "rata_rata": rata_rata,
        "tertinggi": tertinggi,
        "terendah": terendah,
        "kategori": kategori,
        "jumlah_panas": jumlah_panas,
    }


# Tahap 3: Tulis laporan
def buat_laporan(hasil):
    baris = ["LAPORAN SUHU HARIAN", "=" * 30]
    for k in hasil["kategori"]:
        baris.append(f"{k['hari']:<8}: {k['suhu']} C  ({k['kategori']})")
    baris.append("-" * 30)
    baris.append(f"Rata-rata suhu   : {hasil['rata_rata']:.2f} C")
    baris.append(f"Suhu paling tinggi   : {hasil['tertinggi']['suhu']} C "
                 f"({hasil['tertinggi']['hari']})")
    baris.append(f"Suhu paling rendah    : {hasil['terendah']['suhu']} C "
                 f"({hasil['terendah']['hari']})")
    baris.append(f"Total hari Panas: {hasil['jumlah_panas']} hari")
    return "\n".join(baris)


def tulis_laporan(teks, nama_file="laporan_suhu.txt"):
    with open(nama_file, "w") as f:
        f.write(teks + "\n")


def main():
    data = baca_data("suhu.txt")
    if data is None:
        return
    hasil = analisis(data, batas_panas=BATAS_PANAS)
    laporan = buat_laporan(hasil)
    tulis_laporan(laporan, "laporan_suhu.txt")
    print(laporan)


if __name__ == "__main__":
    main()