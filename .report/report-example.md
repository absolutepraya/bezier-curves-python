# **LAPORAN TEKNIS TUGAS KELOMPOK ANALISIS NUMERIK** ***Studi Kinerja Metode Spline, Simpson Adaptif, dan Kuadratur Gauss dalam Komputasi Z-Score Presisi Tinggi***

![][image1]

**Disusun oleh Kelompok C10:**

Argya Farel Kasyara			2306152424  
Alexander William Lim		2306207505	  
Jason Kent Winata                 	2206081313	  
Daffa Abhipraya Putra		2306245131	

**Fakultas Ilmu Komputer**  
**Universitas Indonesia**  
**2025**

*"Dengan ini, kami menyatakan bahwa tugas ini adalah hasil pekerjaan kelompok sendiri."*

|  ![][image2] Argya Farel Kasyara 2306152424 |  |  | \[TDD\] Alexander William Lim 2306207505 |  |  |
| ----- | ----- | ----- | :---: | ----- | ----- |
| \[TDD\] Jason Kent Winata 2206081313 |  |  | ![][image3] Daffa Abhipraya Putra 2306245131 |  |  |

**Rangkuman**

**Daftar Isi**

# **1\. Pendahuluan**

**1.1 Latar Belakang**

Distribusi normal, atau sering disebut sebagai distribusi Gaussian, merupakan distribusi probabilitas yang memegang peranan fundamental dalam statistika, ilmu data, dan berbagai bidang rekayasa. Salah satu aplikasi utamanya adalah penentuan probabilitas variabel acak melalui *Standard Normal Distribution* (Z-Score). Probabilitas bahwa variabel acak [![][image4]](https://www.codecogs.com/eqnedit.php?latex=Z#0) berada dalam rentang tertentu didefinisikan oleh integral dari fungsi densitas probabilitasnya:

[![][image5]](https://www.codecogs.com/eqnedit.php?latex=P\(a%20%5Cleq%20Z%20%5Cleq%20b\)%20%3D%20%5Cint_%7Ba%7D%5E%7Bb%7D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%5Cpi%7D%7D%20e%5E%7B-z%5E2%2F2%7D%20%5C%2C%20dz#0)

Meskipun fungsi ini krusial, terdapat tantangan matematis mendasar dalam penggunaannya: integral tak tentu

 [![][image6]](https://www.codecogs.com/eqnedit.php?latex=%5Cint%20e%5E%7B-z%5E2%2F2%7D%20%5C%2C%20dz#0) 

tidak memiliki solusi analitik dalam bentuk tertutup (*closed-form solution*) yang dapat diekspresikan dengan fungsi-fungsi elementer. Konsekuensinya, nilai probabilitas eksak tidak dapat dihitung secara langsung menggunakan teorema dasar kalkulus. Oleh karena itu, pendekatan metode numerik menjadi satu-satunya solusi untuk mendapatkan nilai hampiran (aproksimasi) dengan tingkat presisi yang dapat diterima.

Dalam komputasi saintifik, tantangan bukan hanya sekadar menghitung nilai hampiran, melainkan bagaimana menjamin bahwa galat (*error*) dari hasil perhitungan tersebut berada di bawah batas toleransi ([![][image7]](https://www.codecogs.com/eqnedit.php?latex=TOL#0)) yang ditentukan, sekaligus meminimalkan biaya komputasi (kompleksitas waktu).

**1.2 Rumusan Masalah**

Permasalahan utama yang dikaji dalam proyek ini adalah bagaimana mengimplementasikan dan membandingkan efektivitas algoritma integrasi numerik tingkat lanjut untuk menghitung [![][image8]](https://www.codecogs.com/eqnedit.php?latex=P\(a%20%5Cleq%20Z%20%5Cleq%20b\)#0). Secara spesifik, laporan ini akan membahas:

1. Bagaimana akurasi metode Composite Cubic Splines dalam menangani fungsi yang didefinisikan secara diskret.  
2. Bagaimana strategi Adaptive Simpson 3/8 bekerja untuk meminimalkan galat secara dinamis pada interval integrasi.  
3. Bagaimana efektivitas penjabaran Gaussian Quadratures melalui penyelesaian sistem persamaan nonlinear yang digabungkan dengan metode Romberg.  
4. Bagaimana perbandingan kompleksitas komputasi dan konvergensi galat dari ketiga metode tersebut dalam mencapai toleransi [![][image9]](https://www.codecogs.com/eqnedit.php?latex=TOL#0).

**1.3 Tujuan Penulisan**

Tujuan dari penyusunan laporan teknis ini adalah:

1. Membangun fungsi komputasi dalam lingkungan MATLAB/Octave untuk ketiga metode numerik yang ditentukan.  
2. Membuktikan secara teoretis dan eksperimental bahwa algoritma yang disusun mampu menghasilkan output dengan galat absolut lebih kecil dari nilai [![][image10]](https://www.codecogs.com/eqnedit.php?latex=TOL#0) yang diberikan.  
3. Menyajikan analisis komparatif mengenai efisiensi dan kompleksitas masing-masing metode melalui visualisasi grafik dan tabel data.

**1.4 Batasan Masalah**

Lingkup pembahasan dalam laporan ini dibatasi pada:

* Objek integrasi adalah fungsi densitas probabilitas normal baku.  
* Input parameter berupa batas bawah [![][image11]](https://www.codecogs.com/eqnedit.php?latex=a#0), batas atas [![][image12]](https://www.codecogs.com/eqnedit.php?latex=b#0) (di mana [![][image13]](https://www.codecogs.com/eqnedit.php?latex=a%20%5Cleq%20b#0)), dan toleransi galat [![][image14]](https://www.codecogs.com/eqnedit.php?latex=TOL#0).  
* Metode yang digunakan terbatas pada Composite Cubic Splines, Adaptive Simpson 3/8, dan kombinasi Gaussian Quadratures-Romberg.

# **2\. Dasar Teori**

## **2.1 Fungsi Densitas Probabilitas Normal dan Z-Score**

Distribusi normal standar merupakan distribusi probabilitas kontinu yang memiliki nilai rata-rata ([![][image15]](https://www.codecogs.com/eqnedit.php?latex=%5Cmu#0)) nol dan simpangan baku ([![][image16]](https://www.codecogs.com/eqnedit.php?latex=%5Csigma#0)) satu. Fungsi densitas probabilitas (PDF) untuk variabel acak normal standar [![][image17]](https://www.codecogs.com/eqnedit.php?latex=Z#0) didefinisikan sebagai:

[![][image18]](https://www.codecogs.com/eqnedit.php?latex=f\(z\)%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%5Cpi%7D%7D%20e%5E%7B-z%5E2%2F2%7D#0)

Probabilitas kumulatif bahwa variabel acak [![][image19]](https://www.codecogs.com/eqnedit.php?latex=Z#0) berada dalam interval [![][image20]](https://www.codecogs.com/eqnedit.php?latex=%5Ba%2C%20b%5D#0) dinyatakan sebagai integral tentu dari fungsi densitasnya:

[![][image21]](https://www.codecogs.com/eqnedit.php?latex=P\(a%20%5Cleq%20Z%20%5Cleq%20b\)%20%3D%20%5Cint_%7Ba%7D%5E%7Bb%7D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%5Cpi%7D%7D%20e%5E%7B-z%5E2%2F2%7D%20%5C%2C%20dz#0)

Mengingat fungsi [![][image22]](https://www.codecogs.com/eqnedit.php?latex=e%5E%7B-z%5E2%2F2%7D#0) tidak memiliki anti turunan dalam bentuk elementer tertutup (closed-form antiderivative), evaluasi integral ini harus dilakukan menggunakan metode integrasi numerik untuk mendapatkan nilai aproksimasi dengan tingkat presisi yang ditentukan.

## **2.2 Integrasi Numerik Berbasis *Composite Cubic Splines***

Metode *Cubic Spline* digunakan untuk mendekati fungsi [![][image23]](https://www.codecogs.com/eqnedit.php?latex=f\(x\)#0) pada interval [![][image24]](https://www.codecogs.com/eqnedit.php?latex=%5Ba%2C%20b%5D#0) dengan membagi interval tersebut menjadi [![][image25]](https://www.codecogs.com/eqnedit.php?latex=n#0) sub-interval [![][image26]](https://www.codecogs.com/eqnedit.php?latex=%5Bx_i%2C%20x_%7Bi%2B1%7D%5D#0). Pada setiap sub-interval, fungsi didekati oleh polinomial derajat tiga [![][image27]](https://www.codecogs.com/eqnedit.php?latex=S_i\(x\)#0).

### **2.2.1. Definisi Spline Kubik**

Fungsi spline [![][image28]](https://www.codecogs.com/eqnedit.php?latex=S\(x\)#0) dibangun dengan ketentuan bahwa [![][image29]](https://www.codecogs.com/eqnedit.php?latex=S\(x\)#0), [![][image30]](https://www.codecogs.com/eqnedit.php?latex=S'\(x\)#0), dan [![][image31]](https://www.codecogs.com/eqnedit.php?latex=S''\(x\)#0) harus kontinu di seluruh titik simpul (*knots*) [![][image32]](https://www.codecogs.com/eqnedit.php?latex=x_i#0). Pada interval ke\-[![][image33]](https://www.codecogs.com/eqnedit.php?latex=i#0) di mana [![][image34]](https://www.codecogs.com/eqnedit.php?latex=x%20%5Cin%20%5Bx_i%2C%20x_%7Bi%2B1%7D%5D#0), polinomial didefinisikan sebagai:

[![][image35]](https://www.codecogs.com/eqnedit.php?latex=S_i\(x\)%20%3D%20a_i%20%2B%20b_i\(x%20-%20x_i\)%20%2B%20c_i\(x%20-%20x_i\)%5E2%20%2B%20d_i\(x%20-%20x_i\)%5E3#0)

Koefisien [![][image36]](https://www.codecogs.com/eqnedit.php?latex=a_i%2C%20b_i%2C%20c_i%2C#0) dan [![][image37]](https://www.codecogs.com/eqnedit.php?latex=d_i#0) ditentukan dengan menyelesaikan sistem persamaan linear yang dibentuk dari syarat batas dan kontinuitas fungsi, yang umumnya menghasilkan matriks tridiagonal.

### **2.2.2. Formulasi Integrasi**

Integral total diselesaikan dengan menjumlahkan integral dari setiap potongan spline. Untuk satu sub-interval dengan lebar [![][image38]](https://www.codecogs.com/eqnedit.php?latex=h_i%20%3D%20x_%7Bi%2B1%7D%20-%20x_i#0), integralnya adalah:

[![][image39]](https://www.codecogs.com/eqnedit.php?latex=%5Cint_%7Bx_i%7D%5E%7Bx_%7Bi%2B1%7D%7D%20S_i\(x\)%20%5C%2C%20dx%20%3D%20%5Csum_%7Bi%3D0%7D%5E%7Bn-1%7D%20%5Cleft\(%20a_i%20h_i%20%2B%20%5Cfrac%7Bb_i%7D%7B2%7Dh_i%5E2%20%2B%20%5Cfrac%7Bc_i%7D%7B3%7Dh_i%5E3%20%2B%20%5Cfrac%7Bd_i%7D%7B4%7Dh_i%5E4%20%5Cright\)#0)

Metode ini memiliki galat pemotongan (*truncation error*) sebesar [![][image40]](https://www.codecogs.com/eqnedit.php?latex=O\(h%5E4\)#0), yang berarti konvergensi galat sebanding dengan pangkat empat dari ukuran langkah.

## **2.3 Metode *Adaptive Simpson 3/8***

Aturan Simpson 3/8 adalah metode Newton-Cotes tertutup yang mendekati fungsi menggunakan polinomial interpolasi Lagrange derajat tiga yang melewati empat titik ekuidistan.

### **2.3.1. Formulasi Simpson 3/8**

Diberikan interval [![][image41]](https://www.codecogs.com/eqnedit.php?latex=%5Ba%2C%20b%5D#0) dengan lebar [![][image42]](https://www.codecogs.com/eqnedit.php?latex=H%20%3D%20b%20-%20a#0) dan ukuran langkah [![][image43]](https://www.codecogs.com/eqnedit.php?latex=h%20%3D%20H%2F3#0), integral aproksimasi [![][image44]](https://www.codecogs.com/eqnedit.php?latex=I#0) dihitung sebagai:

[![][image45]](https://www.codecogs.com/eqnedit.php?latex=I%20%5Capprox%20%5Cfrac%7B3h%7D%7B8%7D%20%5Cleft%5B%20f\(x_0\)%20%2B%203f\(x_1\)%20%2B%203f\(x_2\)%20%2B%20f\(x_3\)%20%5Cright%5D#0)

### **2.3.2. Algoritma Adaptif dan Estimasi Galat**

Untuk menjamin galat kurang dari toleransi ([![][image46]](https://www.codecogs.com/eqnedit.php?latex=%5Ctext%7BTOL%7D#0)), metode adaptif membagi interval secara rekursif berdasarkan perilaku fungsi. Prosedur ini melibatkan langkah-langkah:

1. Hitung integral [![][image47]](https://www.codecogs.com/eqnedit.php?latex=S_1#0) pada interval penuh [![][image48]](https://www.codecogs.com/eqnedit.php?latex=%5Ba%2C%20b%5D#0).  
2. Bagi interval menjadi dua bagian: [![][image49]](https://www.codecogs.com/eqnedit.php?latex=%5Ba%2C%20c%5D#0) dan [![][image50]](https://www.codecogs.com/eqnedit.php?latex=%5Bc%2C%20b%5D#0) dengan [![][image51]](https://www.codecogs.com/eqnedit.php?latex=c%20%3D%20\(a%2Bb\)%2F2#0). Hitung integral pada kedua sub-interval tersebut untuk mendapatkan total [![][image52]](https://www.codecogs.com/eqnedit.php?latex=S_2#0).  
3. Estimasi galat relatif ([![][image53]](https://www.codecogs.com/eqnedit.php?latex=E#0)) menggunakan prinsip Ekstrapolasi Richardson:  
   [![][image54]](https://www.codecogs.com/eqnedit.php?latex=E%20%5Capprox%20%5Cfrac%7B%7CS_2%20-%20S_1%7C%7D%7B15%7D#0)  
4. Kriteria Berhenti: Jika [![][image55]](https://www.codecogs.com/eqnedit.php?latex=E%20%3C%20%5Ctext%7BTOL%7D#0), maka [![][image56]](https://www.codecogs.com/eqnedit.php?latex=S_2#0) diterima sebagai hasil. Jika tidak, prosedur diulangi secara rekursif untuk masing-masing sub-interval hingga kriteria terpenuhi.

## **2.4 Penjabaran *Gaussian Quadratures* dan Metode Romberg**

Bagian ini membahas penurunan teoretis *Gaussian Quadrature* melalui sistem nonlinear dan implementasi numerik menggunakan Metode Romberg.

### **2.4.1. Penjabaran *Gaussian Quadrature* (Sistem Nonlinear)**

*Gaussian Quadrature* bertujuan mendapatkan presisi integral tertinggi dengan memilih titik evaluasi [![][image57]](https://www.codecogs.com/eqnedit.php?latex=x_i#0) dan bobot [![][image58]](https://www.codecogs.com/eqnedit.php?latex=w_i#0) secara optimal. Aproksimasi integral dinyatakan sebagai:

[![][image59]](https://www.codecogs.com/eqnedit.php?latex=%5Cint_%7B-1%7D%5E%7B1%7D%20f\(x\)%20%5C%2C%20dx%20%5Capprox%20%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20w_i%20f\(x_i\)#0)

Untuk menentukan [![][image60]](https://www.codecogs.com/eqnedit.php?latex=n#0) titik dan [![][image61]](https://www.codecogs.com/eqnedit.php?latex=n#0) bobot (total [![][image62]](https://www.codecogs.com/eqnedit.php?latex=2n#0) variabel), kita menyusun sistem persamaan nonlinear menggunakan metode koefisien tak tentu, di mana formula harus eksak untuk polinomial basis [![][image63]](https://www.codecogs.com/eqnedit.php?latex=x%5Ek#0) hingga derajat [![][image64]](https://www.codecogs.com/eqnedit.php?latex=2n-1#0):

[![][image65]](https://www.codecogs.com/eqnedit.php?latex=%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20w_i%20x_i%5Ek%20%3D%20%5Cint_%7B-1%7D%5E%7B1%7D%20x%5Ek%20%5C%2C%20dx%2C%20%5Cquad%20k%20%3D%200%2C%201%2C%20%5Cdots%2C%202n-1#0)

Penyelesaian sistem ini menghasilkan titik-titik [![][image66]](https://www.codecogs.com/eqnedit.php?latex=x_i#0) yang merupakan akar-akar dari Polinomial Legendre [![][image67]](https://www.codecogs.com/eqnedit.php?latex=P_n\(x\)#0).

### **2.4.2. Metode Integrasi Romberg**

Metode Romberg digunakan untuk menghitung integral dengan presisi tinggi menggunakan ekstrapolasi berulang dari Aturan Trapesium.

1. Tingkat Dasar (Trapezoidal Rule):  
   Hitung aproksimasi integral [![][image68]](https://www.codecogs.com/eqnedit.php?latex=R_%7Bk%2C1%7D#0) dengan membagi interval menjadi [![][image69]](https://www.codecogs.com/eqnedit.php?latex=2%5E%7Bk-1%7D#0) segmen.  
2. Ekstrapolasi Richardson:  
   Tingkatkan orde akurasi dengan mengombinasikan dua aproksimasi sebelumnya menggunakan rumus rekursif:  
   [![][image70]](https://www.codecogs.com/eqnedit.php?latex=R_%7Bk%2C%20j%7D%20%3D%20R_%7Bk%2C%20j-1%7D%20%2B%20%5Cfrac%7BR_%7Bk%2C%20j-1%7D%20-%20R_%7Bk-1%2C%20j-1%7D%7D%7B4%5E%7Bj-1%7D%20-%201%7D#0)  
   dimana $R\_{k,j}$ adalah aproksimasi integral dengan orde galat [![][image71]](https://www.codecogs.com/eqnedit.php?latex=O\(h%5E%7B2j%7D\)#0).  
3. Konvergensi:  
   Iterasi dihentikan ketika selisih absolut antara dua estimasi diagonal terakhir memenuhi toleransi:  
   [![][image72]](https://www.codecogs.com/eqnedit.php?latex=%7CR_%7Bk%2C%20k%7D%20-%20R_%7Bk-1%2C%20k-1%7D%7C%20%3C%20%5Ctext%7BTOL%7D#0)

# **3\. Metodologi Eksperimen**

## **3.1 Skenario Pengujian**

## **3.2 Lingkungan Pengujian**

	

# **4\. Hasil dan Analisis**

### 

# **5\. Kesimpulan**

# **Daftar Referensi**

# **Lampiran**
