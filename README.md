# Invisible Watermarking
Menambahkan watermark pada foto wajah sendiri, kemudian menguji ketahanan watermark terhadap kompresi JPEG dengan beberapa nilai *Quality Factor* (QF).

## Identitas

Nama: Gregory William Sutjipto  
NIM: 18224010

## Deskripsi Tugas

Tugas ini bertujuan untuk menyisipkan watermark pada foto wajah sendiri, melakukan kompresi JPEG dengan beberapa nilai QF, lalu mengevaluasi apakah watermark masih dapat diekstrak kembali setelah proses kompresi.

Watermark yang digunakan berupa citra biner berukuran 32x32 piksel dengan teks `WM`.

## Metode

Metode yang digunakan adalah watermarking berbasis DCT (*Discrete Cosine Transform*). Foto wajah dikonversi ke channel luminance, kemudian watermark biner disisipkan pada koefisien DCT dari blok 8x8.

Setelah watermark disisipkan, gambar hasil watermarking dikompres menggunakan JPEG dengan berbagai nilai QF. Watermark kemudian diekstrak kembali dari setiap gambar hasil kompresi untuk melihat tingkat keberhasilan ekstraksi.

## Quality Factor yang Diuji

Nilai QF yang diuji adalah:

100, 95, 90, 80, 70, 60, 50, 40, 30, 20, 10, dan 5.

Dalam eksperimen ini, watermark dianggap berhasil diekstrak apabila:

1. Nilai QF minimal 30.
2. Nilai Bit Error Rate (BER) tidak melebihi 0.30.

Dengan aturan tersebut, QF di bawah 30 dianggap gagal, meskipun nilai BER masih berada di bawah 0.30.

## Hasil Evaluasi

| QF | BER | Accuracy | Status |
|---:|---:|---:|---|
| 100 | 0.000000 | 1.000000 | OK |
| 95 | 0.000000 | 1.000000 | OK |
| 90 | 0.000000 | 1.000000 | OK |
| 80 | 0.000000 | 1.000000 | OK |
| 70 | 0.000000 | 1.000000 | OK |
| 60 | 0.000000 | 1.000000 | OK |
| 50 | 0.000000 | 1.000000 | OK |
| 40 | 0.000000 | 1.000000 | OK |
| 30 | 0.045898 | 0.954102 | OK |
| 20 | 0.185547 | 0.814453 | GAGAL |
| 10 | 0.144531 | 0.855469 | GAGAL |
| 5 | 0.089844 | 0.910156 | GAGAL |

## Grafik Evaluasi

![Grafik BER vs QF](hasil_watermarking/grafik_BER_vs_QF.png)

## Contoh Hasil Ekstraksi Watermark

### Watermark Asli

![Watermark Asli](hasil_watermarking/02_watermark_asli.png)

### Watermark Hasil Ekstraksi QF 100

![QF 100](hasil_watermarking/watermark_ekstrak_QF_100.png)

### Watermark Hasil Ekstraksi QF 30

![QF 30](hasil_watermarking/watermark_ekstrak_QF_30.png)

### Watermark Hasil Ekstraksi QF 5

![QF 5](hasil_watermarking/watermark_ekstrak_QF_5.png)

## Analisis

Berdasarkan hasil pengujian, watermark dapat diekstrak dengan sangat baik pada QF 100 hingga QF 40, karena nilai BER adalah 0.000000 dan accuracy mencapai 1.000000. Hal ini menunjukkan bahwa kompresi JPEG pada rentang QF tersebut belum merusak informasi watermark.

Pada QF 30, watermark masih dapat diekstrak dengan baik, tetapi mulai mengalami sedikit error. Nilai BER pada QF 30 adalah 0.045898 dengan accuracy 0.954102. Karena nilai BER masih di bawah 0.30 dan QF masih memenuhi batas minimal, maka statusnya masih dianggap OK.

Pada QF 20, QF 10, dan QF 5, watermark dinyatakan gagal. Hal ini bukan hanya karena kompresi semakin kuat, tetapi juga karena aturan eksperimen menetapkan bahwa watermark hanya dianggap berhasil sampai QF minimal 30. Oleh karena itu, QF di bawah 30 tetap diberi status GAGAL.

## Kesimpulan

Berdasarkan hasil eksperimen, watermark masih dapat diekstrak dengan baik hingga QF 30. Pada QF 30, watermark masih memiliki accuracy sebesar 0.954102 dan BER sebesar 0.045898, sehingga masih memenuhi batas keberhasilan.

Watermark mulai dianggap tidak berhasil diekstrak ketika nilai QF diturunkan di bawah 30. Dengan demikian, batas minimum QF yang masih dapat diterima dalam eksperimen ini adalah QF 30.
