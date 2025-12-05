# Analisis Numerik
**Semester Gasal 2025/2026**
**TK 2: Optimization, Interpolation & Numerical Integration**
**Tim Dosen dan Asisten Dosen Analisis Numerik**

**Deadline:** Rabu, 3 Desember 2025 pukul 23.59 WIB

---

## Petunjuk

1.  Project dikerjakan secara berkelompok, pembagiannya dapat dilihat di SCELE Anum.
2.  Baca dan pahami Petunjuk Penulisan Dokumen Project Anum yang tersedia pada SCeLE.
3.  Dilarang menggunakan pustaka algoritma-algoritma utama, seperti optimisasi, interpolasi, turunan, dan integral. Gunakan algoritma yang diimplementasikan sendiri.
4.  Contoh format penamaan berkas: `TK2 D18_220669420_2109345786.pdf`
5.  Kelompok Anda diharapkan juga melampirkan README untuk menjalankan code yang digunakan, sehingga mendapatkan hasil yang sama dengan eksperimen kelompok Anda.
6.  Berkas project di-zip bersamaan dengan code yang kelompok kalian gunakan dalam project ini. Pengumpulan perkelompok hanya diwakilkan oleh 1 anggota kelompok. Submisi lebih dari 1 anggota perlu dikonfirmasi ke pihak Asisten Dosen selambat-lambatnya $H+1$ deadline. Tim Asisten Dosen akan memilih submisi secara acak apabila tidak ada konfirmasi.
7.  Tuliskan Nama Kelompok, Nama, dan NPM anggota kelompok pada bagian halaman sampul pada berkas project Anda.
8.  Awali berkas project Anda dengan pernyataan "Dengan ini, kami menyatakan bahwa tugas ini adalah hasil pekerjaan kelompok sendiri" disertai tanda tangan tiap anggota kelompok pada halaman pertama berkas project Anda. Tanpa pernyataan ini, project Anda tidak akan diperiksa.
9.  Pelanggaran peraturan kejujuran akademis akan diproses sesuai peraturan yang sudah dijelaskan di BRP.
10. Tidak ada toleransi terhadap keterlambatan! Biasakan untuk mengumpulkan project paling tidak 1 jam sebelum deadline.

### Pakta Integritas
Dengan ini, kami menyatakan bahwa tugas ini adalah hasil pekerjaan kelompok sendiri.

---

Kelompok Anda harus mengerjakan proyek wajib dan salah satu dari dua proyek pilihan:
1.  Optimisasi Numerik untuk Hamiltonian Cycle Problem
2.  Ilustrasi dengan Bézier Curve

## Proyek Wajib [50%]

### 1. The Z-Score

Probabilitas suatu variabel acak $Z$ yang memiliki distribusi normal bernilai kurang dari $z$, dihitung dengan integral:

$$P(Z\le z)=\Phi(z)=\int_{-\infty}^{z}\frac{1}{\sqrt{2\pi}}e^{-z^{2}/2}dz$$

Integral ini dihitung secara numerik. Implementasikan beberapa fungsi MATLAB/Octave yang menerima dua bilangan riil $a$ dan $b$ sehingga $a\le b$ serta toleransi galat $TOL$ dan menghitung probabilitas $P(a\le Z\le b)$ dengan galat kurang dari $TOL$. Setiap fungsi menggunakan metode integrasi numerik yang berbeda-beda:

i)  Metode composite berbasis cubic splines untuk fungsi-fungsi yang terdefinisi secara diskret.
ii) Metode adaptive berbasis Simpson $3/8$.
iii) Menjabarkan Gaussian Quadratures dengan menyelesaikan suatu sistem persamaan nonlinear, kemudian mengintegralkannya menggunakan metode Romberg.

Jelaskan bagaimana Anda menjamin bahwa galatnya memenuhi apa yang diminta dan analisis secara teoretis maupun eksperimental mengenai kompleksitas masing-masing metode dalam menjamin galatnya kurang dari $TOL$. Tampilkan hasilnya dalam bentuk tabel maupun grafik.

---

## Proyek Pilihan [50%]

### 2. Optimization for Hamiltonian Cycle Problem

Pelajari makalah ini yang membahas terkait aplikasi optimisasi numerik untuk permasalahan matematika diskret.

![Fig 1: Ilustrasi peta rute dengan pertanyaan "WHAT'S THE SHORTEST ROUTE TO VISIT ALL LOCATIONS AND RETURN?"]

**Fig. 1:** Ilustrasi Aa Num yang bingung menentukan skema visit nasabah dengan ongkos taksi termurah.

Tugas Anda adalah membahas jawaban atas pertanyaan-pertanyaan berikut:

i)  Deskripsikan permasalahan optimisasi numerik (berkendala) yang dapat digunakan untuk menyelesaikan permasalahan Hamiltonian Cycle.
ii) Implementasikan fungsi yang menerima matriks keterhubungan graf dan mengeluarkan fungsi objektif yang akan dioptimisasi.
iii) Jelaskan kendala-kendala apa yang dihadapi dalam optimisasi fungsi objektif berkendala ini dan pendekatan apa yang dilakukan untuk menyelesaikan.
iv) Implementasikan minimal dua algoritma yang relevan untuk mengoptimalkan fungsi objektif berkendala tersebut.
v)  Lakukan pula eksperimen dengan berbagai kombinasi skenario algoritma usulan Anda sendiri. Jelaskan kombinasi skenario apa saja yang Anda pilih.
    a)  Algoritma optimisasi yang digunakan (implementasi kelompok Anda sendiri) [minimal 2].
    b)  Variasi pilihan titik tebakan awal untuk algoritma optimisasi [apakah ada usul tebakan awal yang baik?]
    c)  Graf yang punya Hamiltonian Cycle dan yang tidak punya [masing-masing minimal 5].
    d)  Ukuran graf bervariasi (minimal 5 variasi) agar perbedaan waktu eksekusi terlihat.
vi) Analisis dan interpretasi hasil eksperimen.

---

### 3. Bézier Curves Artwork Illustration

Kurva Bézier adalah jenis spline yang memungkinkan pengguna untuk mengontrol kemiringan (slope) pada titik-titik simpul (knots). Sebagai konsekuensinya dari kebebasan tambahan tersebut, kelicinan (smoothness) turunan pertama dan kedua di sepanjang titik simpul yang secara otomatis dijamin pada cubic splines tidak lagi terjamin. Bézier Spline cocok digunakan dalam kasus terdapat sudut tajam (turunan pertama yang tidak kontinu) atau perubahan kelengkungan yang mendadak (turunan kedua yang tidak kontinu) diperlukan.

Kurva Bézier merupakan salah satu dasar utama dalam desain dan manufaktur berbantuan komputer. Dalam proyek ini, akan diperlihatkan salah satu aplikasi Bézier Spline, yakni untuk menirukan gambar eksisting menjadi bentuk ilustrasi statik.

![Fig 2: Ilustrasi logo makara UI menggunakan Bézier Curves (Kiri: Kuning, Kanan: Outline Putih di atas Hitam)]

**Fig. 2:** Ilustrasi logo makara UI menggunakan Bézier Curves.

Tugas Anda adalah membahas jawaban atas pertanyaan-pertanyaan berikut:

i)  Jelaskan apa masukan dan keluaran dari Bézier Curves.
ii) Jelaskan bagaimana representasi kurvanya dan perhitungan matematis kurvanya.
iii) Pelajari dan jelaskan implementasi program 3.7 "Freehand Draw Program Using Bézier Spline" pada buku Timothy Sauer. Hubungkan dengan penjelasan Anda pada bagian ii).
iv) Berikan contoh perhitungan kurva Bézier secara analitik.
v)  Gunakan program pada bagian iii) untuk menggambar ilustrasi tiruan hal apapun yang kalian inginkan. Program Anda dapat dikombinasikan menggunakan pustaka seperti `cv2` pada Python untuk mendapatkan titik-titik interpolasi dari gambar yang akan diilustrasikan. Jelaskan keterhubungan banyaknya kurva Bézier terhadap kualitas gambar. Dapatkah kualitas gambar yang serupa didapatkan dengan kurva Bézier yang lebih sedikit daripada yang kelompok Anda dapatkan saat membuat ilustrasi?
vi) Tulis sebuah berkas PDF yang menggambarkan ilustrasi yang dibuat pada bagian v). Program harus diawali dengan perintah `m` untuk bergerak ke titik pertama, diikuti oleh serangkaian perintah `c` (jumlah menyesuaikan kebutuhan gambar) dan sebuah perintah `stroke` atau `fill`. Perintah-perintah ini harus ditempatkan di antara tag `stream` dan `endstream`. Uji berkas Anda dengan membukanya di PDF viewer. Untuk mengerjakan tugas ini, Anda perlu mempelajari format berkas PDF dan contoh pada bagian Reality Check "Fonts from Bézier Curve" dari buku Timothy Sauer baik nomor 2 maupun nomor 3. Anda harus menjelaskan langkah-langkah pekerjaan Anda.