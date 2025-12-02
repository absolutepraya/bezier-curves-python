# Bézier Curves Artwork Illustration

Proyek ini mengimplementasikan algoritma *Least Squares Fitting* untuk merepresentasikan gambar raster (kontur) menjadi sekumpulan kurva Bézier kubik dalam format PDF vektor.

## Prasyarat

Pastikan Anda telah menginstal Python 3 dan pustaka yang diperlukan:

```bash
pip install -r requirements.txt
```

## Struktur Direktori

- `input/`: Direktori tempat meletakkan gambar masukan (misal: `makara.png`).
- `output/`: Direktori tempat hasil PDF disimpan.
- `src/`: Berisi kode sumber Python.
  - `main.py`: Skript utama untuk menjalankan program.
  - `bezier_math.py`: Implementasi matematika Bézier dan kelas Point.
  - `curve_fitter.py`: Logika *fitting* kurva menggunakan *Least Squares*.
  - `image_processor.py`: Pengolahan citra untuk ekstraksi kontur.
  - `pdf_generator.py`: Generator file PDF manual.
- `README.md`: Petunjuk penggunaan.

## Cara Menjalankan

1.  Pastikan gambar yang ingin diproses (format .png, .jpg, dll) sudah ada di dalam folder `input/`.
2.  Buka terminal dan arahkan ke direktori *root* proyek ini.
3.  Jalankan perintah berikut:

    ```bash
    python3 src/main.py
    ```

4.  Program akan menampilkan daftar file gambar yang ada di folder `input/`.
5.  Pilih nomor gambar yang ingin diproses.
6.  Program akan memproses gambar tersebut dan menyimpan hasilnya di folder `output/` dengan nama `<nama_file>-output.pdf`.

## Catatan

- Algoritma ini diimplementasikan dari nol (from scratch) untuk bagian *fitting* dan matematika kurva, tanpa menggunakan fungsi *high-level* dari pustaka seperti `scipy` untuk optimisasinya.
- Pustaka `cv2` (OpenCV) hanya digunakan untuk membaca gambar dan mendapatkan titik-titik kontur awal.
