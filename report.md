# Laporan Proyek: Bézier Curves Artwork Illustration

## Jawaban Pertanyaan

### i) Masukan dan Keluaran Bézier Curves
**Masukan**:
- Sekumpulan titik kontrol $P_0, P_1, \dots, P_n$. Untuk kurva Bézier kubik, terdapat 4 titik kontrol: $P_0$ (titik awal), $P_1, P_2$ (titik kontrol arah/lengkungan), dan $P_3$ (titik akhir).
- Parameter $t$ dalam rentang $[0, 1]$.

**Keluaran**:
- Sebuah titik $B(t)$ pada bidang 2D yang merupakan posisi kurva pada parameter $t$.

### ii) Representasi dan Perhitungan Matematis
Kurva Bézier derajat $n$ didefinisikan oleh persamaan parametrik menggunakan polinomial Bernstein:
$$ B(t) = \sum_{i=0}^n \binom{n}{i} (1-t)^{n-i} t^i P_i, \quad 0 \le t \le 1 $$

Untuk kasus **Cubic Bézier** ($n=3$), persamaannya adalah:
$$ B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3 $$

Representasi ini menjamin bahwa kurva dimulai di $P_0$ (saat $t=0$) dan berakhir di $P_3$ (saat $t=1$). Garis singgung di $P_0$ searah dengan vektor $\vec{P_0 P_1}$, dan di $P_3$ searah dengan $\vec{P_2 P_3}$.

### iii) Implementasi Program 3.7 "Freehand Draw"
Program "Freehand Draw" pada buku Timothy Sauer biasanya menggunakan pendekatan interpolasi spline atau fitting. Dalam implementasi kami, kami menggunakan pendekatan **Least Squares Fitting**.
- Kami membagi kontur gambar menjadi segmen-segmen.
- Untuk setiap segmen, kami menetapkan $P_0$ dan $P_3$ sebagai titik ujung.
- Kami mencari $P_1$ dan $P_2$ yang meminimalkan jumlah kuadrat jarak antara titik-titik data asli dengan kurva Bézier yang dihasilkan.
- Hal ini dilakukan dengan menyelesaikan sistem persamaan linear yang diturunkan dari turunan parsial fungsi error terhadap koordinat $P_1$ dan $P_2$.

### iv) Contoh Perhitungan Analitik
Misalkan kita ingin membuat kurva Bézier kubik yang menghubungkan $P_0=(0,0)$ dan $P_3=(10,0)$ dengan titik kontrol $P_1=(2,5)$ dan $P_2=(8,5)$.

Untuk $t=0.5$ (titik tengah parameter):
$$ B(0.5) = (0.5)^3 P_0 + 3(0.5)^2 (0.5) P_1 + 3(0.5) (0.5)^2 P_2 + (0.5)^3 P_3 $$
$$ B(0.5) = 0.125(0,0) + 0.375(2,5) + 0.375(8,5) + 0.125(10,0) $$
$$ x = 0 + 0.75 + 3 + 1.25 = 5 $$
$$ y = 0 + 1.875 + 1.875 + 0 = 3.75 $$
Jadi, $B(0.5) = (5, 3.75)$.

### v) Implementasi dan Kualitas Gambar
Kami menggunakan `cv2` untuk mendeteksi kontur dari gambar "Makara UI".
- **Keterhubungan kurva vs kualitas**: Semakin banyak kurva Bézier yang digunakan, semakin akurat kurva tersebut dapat mengikuti detail kontur yang kompleks.
- **Efisiensi**: Dengan menggunakan *Least Squares Fitting* yang adaptif (memecah kurva hanya jika error terlalu besar), kami dapat mencapai kualitas tinggi dengan jumlah kurva yang optimal (420 kurva untuk logo kompleks Makara UI). Jika kami menggunakan interpolasi titik-per-titik sederhana, kami akan membutuhkan ribuan segmen garis. Kurva Bézier memungkinkan representasi bentuk lengkung yang mulus dengan data yang jauh lebih sedikit.

### vi) Langkah-langkah Pembuatan PDF
Program kami (`pdf_generator.py`) menulis berkas PDF secara manual dengan struktur:
1.  **Header**: `%PDF-1.4`
2.  **Body**: Mendefinisikan objek-objek PDF (Catalog, Pages, Page, Content Stream).
3.  **Content Stream**: Berisi operator grafik vektor:
    - `x y m`: *Move to* $(x, y)$.
    - `x1 y1 x2 y2 x3 y3 c`: *Cubic Bézier curve* ke $(x_3, y_3)$ dengan kontrol $(x_1, y_1)$ dan $(x_2, y_2)$.
    - `S`: *Stroke* (gambar garis).
4.  **Xref Table**: Tabel referensi silang yang mencatat posisi byte setiap objek.
5.  **Trailer**: Menunjuk ke objek Root (Catalog) dan lokasi `xref`.
6.  **EOF**: Penanda akhir file.

Hasil akhir disimpan sebagai `output_makara.pdf` dan dapat dibuka di PDF viewer standar.
