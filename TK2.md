Berikut adalah hasil ekstraksi dokumen PDF ke dalam format Markdown dengan penggunaan LaTeX sesuai permintaan Anda:

# Analisis Numerik
[cite_start]**Semester Gasal 2025/2026** [cite: 1, 2]
[cite_start]**TK 2: Optimization, Interpolation & Numerical Integration** [cite: 3]
[cite_start]**Tim Dosen dan Asisten Dosen Analisis Numerik** [cite: 4]
[cite_start]**Deadline: Rabu, 3 Desember 2025 pukul 23.59 WIB** [cite: 5]

---

## Petunjuk
1. [cite_start]Project dikerjakan secara berkelompok, pembagiannya dapat dilihat di SCeLE Anum. [cite: 8]
2. [cite_start]Baca dan pahami Petunjuk Penulisan Dokumen Project Anum yang tersedia pada SCeLE. [cite: 9]
3. Dilarang menggunakan pustaka algoritma-algoritma utama, seperti optimisasi, interpolasi, turunan, dan integral. [cite_start]Gunakan algoritma yang diimplementasikan sendiri. [cite: 10]
4. [cite_start]Contoh format penamaan berkas: `TK2_D18_220669420_2109345786.pdf`. [cite: 11]
5. [cite_start]Kelompok Anda diharapkan juga melampirkan README untuk menjalankan code yang digunakan, sehingga mendapatkan hasil yang sama dengan eksperimen kelompok Anda. [cite: 12]
6. Berkas project di-zip bersamaan dengan code yang kelompok kalian gunakan dalam project ini. Pengumpulan perkelompok hanya diwakilkan oleh 1 anggota kelompok. Submisi lebih dari 1 anggota perlu dikonfirmasi ke pihak Asisten Dosen selambat-lambatnya $H+1$ deadline. [cite_start]Tim Asisten Dosen akan memilih submisi secara acak apabila tidak ada konfirmasi. [cite: 13, 14, 15]
7. [cite_start]Tuliskan Nama Kelompok, Nama, dan NPM anggota kelompok pada bagian halaman sampul pada berkas project Anda. [cite: 16]
8. Awali berkas project Anda dengan pernyataan "Dengan ini, kami menyatakan bahwa tugas ini adalah hasil pekerjaan kelompok sendiri" disertai tanda tangan tiap anggota kelompok pada halaman pertama berkas project Anda. [cite_start]Tanpa pernyataan ini, project Anda tidak akan diperiksa. [cite: 17, 18]
9. [cite_start]Pelanggaran peraturan kejujuran akademis akan diproses sesuai peraturan yang sudah dijelaskan di BRP. [cite: 19]
10. Tidak ada toleransi terhadap keterlambatan! [cite_start]Biasakan untuk mengumpulkan project paling tidak 1 jam sebelum deadline. [cite: 20, 21, 23]

### Pakta Integritas
[cite_start]Dengan ini, kami menyatakan bahwa tugas ini adalah hasil pekerjaan kelompok sendiri. [cite: 22, 24]

---

## Deskripsi Tugas
[cite_start]Kelompok Anda harus mengerjakan **proyek wajib** dan **salah satu** dari dua proyek pilihan: [cite: 26]
1. [cite_start]Optimisasi Numerik untuk Hamiltonian Cycle Problem [cite: 27]
2. [cite_start]Ilustrasi dengan Bézier Curve [cite: 28]

---

### Proyek Wajib [50%]
#### [cite_start]1. The Z-Score [cite: 29, 30]

[cite_start]Probabilitas suatu variabel acak $Z$ yang memiliki distribusi normal bernilai kurang dari $z$, dihitung dengan integral: [cite: 31]

[cite_start]$$P(Z\le z)=\Phi(z)=\int_{-\infty}^{z}\frac{1}{\sqrt{2\pi}}e^{-z^{2}/2}dz$$ [cite: 32]

Integral ini dihitung secara numerik. [cite_start]Implementasikan beberapa fungsi MATLAB/Octave yang menerima dua bilangan riil $a$ dan $b$ sehingga $a\le b$ serta toleransi galat TOL dan menghitung probabilitas $P(a\le Z\le b)$ dengan galat kurang dari TOL. [cite: 33]

[cite_start]Setiap fungsi menggunakan metode integrasi numerik yang berbeda-beda: [cite: 34]
1.  [cite_start]Metode composite berbasis cubic splines untuk fungsi-fungsi yang terdefinisi secara diskret. [cite: 35]
2.  [cite_start]Metode adaptive berbasis Simpson $3/8$. [cite: 36]
3.  [cite_start]Menjabarkan Gaussian Quadratures dengan menyelesaikan suatu sistem persamaan nonlinear, kemudian mengintegralkannya menggunakan metode Romberg. [cite: 37]

Jelaskan bagaimana Anda menjamin bahwa galatnya memenuhi apa yang diminta dan analisis secara teoretis maupun eksperimental mengenai kompleksitas masing-masing metode dalam menjamin galatnya kurang dari TOL. [cite_start]Tampilkan hasilnya dalam bentuk tabel maupun grafik. [cite: 38, 39]

---

### Proyek Pilihan [50%]
#### [cite_start]2. Optimization for Hamiltonian Cycle Problem [cite: 41, 42]

[cite_start]Pelajari makalah ini yang membahas terkait aplikasi optimisasi numerik untuk permasalahan matematika diskret. [cite: 43]

> [cite_start]"WHAT'S THE SHORTEST ROUTE TO VISIT ALL LOCATIONS AND RETURN?" [cite: 44]
> *Fig. [cite_start]1: Ilustrasi Aa Num yang bingung menentukan skema visit nasabah dengan ongkos taksi termurah.* [cite: 45]

[cite_start]Tugas Anda adalah membahas jawaban atas pertanyaan-pertanyaan berikut: [cite: 46]

[cite_start]i) Deskripsikan permasalahan optimisasi numerik (berkendala) yang dapat digunakan untuk menyelesaikan permasalahan Hamiltonian Cycle. [cite: 47]

[cite_start]ii) Implementasikan fungsi yang menerima matriks keterhubungan graf dan mengeluarkan fungsi objektif yang akan dioptimisasi. [cite: 48]

[cite_start]iii) Jelaskan kendala-kendala apa yang dihadapi dalam optimisasi fungsi objektif berkendala ini dan pendekatan apa yang dilakukan untuk menyelesaikan. [cite: 49]

[cite_start]iv) Implementasikan minimal dua algoritma yang relevan untuk mengoptimalkan fungsi objektif berkendala tersebut. [cite: 50]

v) Lakukan pula eksperimen dengan berbagai kombinasi skenario algoritma usulan Anda sendiri. [cite_start]Jelaskan kombinasi skenario apa saja yang Anda pilih. [cite: 51]
* [cite_start]a) Algoritma optimisasi yang digunakan (implementasi kelompok Anda sendiri) [minimal 2]. [cite: 52]
* [cite_start]b) Variasi pilihan titik tebakan awal untuk algoritma optimisasi [apakah ada usul tebakan awal yang baik?]. [cite: 53]
* [cite_start]c) Graf yang punya Hamiltonian Cycle dan yang tidak punya [masing-masing minimal 5]. [cite: 54]
* [cite_start]d) Ukuran graf bervariasi (minimal 5 variasi) agar perbedaan waktu eksekusi terlihat. [cite: 55]

[cite_start]vi) Analisis dan interpretasi hasil eksperimen. [cite: 56]

---

### Proyek Pilihan [50%]
#### [cite_start]3. Bézier Curves Artwork Illustration [cite: 57, 58]

Kurva Bézier adalah jenis spline yang memungkinkan pengguna untuk mengontrol kemiringan (slope) pada titik-titik simpul (knots). [cite_start]Sebagai konsekuensinya dari kebebasan tambahan tersebut, kelicinan (smoothness) turunan pertama dan kedua di sepanjang titik simpul yang secara otomatis dijamin pada cubic splines tidak lagi terjamin. [cite: 59, 60]

Bézier Spline cocok digunakan dalam kasus terdapat sudut tajam (turunan pertama yang tidak kontinu) atau perubahan kelengkungan yang mendadak (turunan kedua yang tidak kontinu) diperlukan. [cite_start]Kurva Bézier merupakan salah satu dasar utama dalam desain dan manufaktur berbantuan komputer. [cite: 61, 62]

[cite_start]Dalam proyek ini, akan diperlihatkan salah satu aplikasi Bézier Spline, yakni untuk menirukan gambar eksisting menjadi bentuk ilustrasi statik. [cite: 63]

> *Fig. [cite_start]2: Ilustrasi logo makara UI menggunakan Bézier Curves* [cite: 64]

[cite_start]Tugas Anda adalah membahas jawaban atas pertanyaan-pertanyaan berikut: [cite: 65]

[cite_start]i) Jelaskan apa masukan dan keluaran dari Bézier Curves. [cite: 65]

[cite_start]ii) Jelaskan bagaimana representasi kurvanya dan perhitungan matematis kurvanya. [cite: 66]

iii) Pelajari dan jelaskan implementasi program 3.7 "Freehand Draw Program Using Bézier Spline" pada buku Timothy Sauer. [cite_start]Hubungkan dengan penjelasan Anda pada bagian ii). [cite: 66, 67]

[cite_start]iv) Berikan contoh perhitungan kurva Bézier secara analitik. [cite: 68]

v) Gunakan program pada bagian iii) untuk menggambar ilustrasi tiruan hal apapun yang kalian inginkan. Program Anda dapat dikombinasikan menggunakan pustaka seperti `cv2` pada Python untuk mendapatkan titik-titik interpolasi dari gambar yang akan diilustrasikan. Jelaskan keterhubungan banyaknya kurva Bézier terhadap kualitas gambar. [cite_start]Dapatkah kualitas gambar yang serupa didapatkan dengan kurva Bézier yang lebih sedikit daripada yang kelompok Anda dapatkan saat membuat ilustrasi? [cite: 69, 70, 71]

vi) Tulis sebuah berkas PDF yang menggambarkan ilustrasi yang dibuat pada bagian v). Program harus diawali dengan perintah `m` untuk bergerak ke titik pertama, diikuti oleh 21 perintah `c` dan sebuah perintah `stroke` atau `fill`. Perintah-perintah ini harus ditempatkan di antara tag `stream` dan `endstream`. Uji berkas Anda dengan membukanya di PDF viewer. [cite_start]Untuk mengerjakan tugas ini, Anda perlu mempelajari format berkas PDF dan contoh pada bagian Reality Check "Fonts from Bézier Curve" dari buku Timothy Sauer baik nomor 2 maupun nomor 3. Anda harus menjelaskan langkah-langkah pekerjaan Anda. [cite: 72, 73, 75, 76]