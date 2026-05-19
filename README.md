# Invisible Watermarking

Proyek ini menambahkan *invisible watermark* pada foto wajah sendiri menggunakan metode DCT, lalu menguji ketahanan watermark terhadap kompresi JPEG dengan beberapa nilai *Quality Factor* (QF).

## Identitas

- Nama: Gregory William Sutjipto
- NIM: 18224010

---

## Tujuan

1. Menyisipkan watermark ke foto wajah sendiri.
2. Menguji apakah watermark masih bisa diekstrak setelah gambar dikompresi JPEG.
3. Menentukan batas QF minimum yang masih dianggap berhasil.

---

## Metode Singkat

Metode yang digunakan adalah **DCT-based watermarking**.

- Foto diubah ke ukuran **512 × 512**
- Watermark dibuat dalam bentuk citra biner **32 × 32**
- Watermark disisipkan ke channel **luminance (Y)** pada blok **8 × 8**
- Hasil watermarking diuji dengan kompresi JPEG pada beberapa nilai QF
- Watermark diekstrak kembali dan dievaluasi dengan **BER** dan **Accuracy**

---

## Step by Step

### Step 1 — Menyiapkan foto wajah

Foto wajah dibaca, diperbaiki orientasinya, diubah ke format RGB, lalu di-*resize* menjadi 512 × 512.

![Foto Asli](hasil_watermarking/01_foto_asli.png)

---

### Step 2 — Membuat watermark biner

Watermark dibuat dalam bentuk citra biner 32 × 32 dengan teks `WM`.

![Watermark Asli](hasil_watermarking/02_watermark_asli.png)

---

### Step 3 — Menyisipkan watermark ke foto

Watermark disisipkan ke foto menggunakan metode DCT pada blok 8 × 8. Hasilnya adalah foto berwatermark yang secara visual masih mirip dengan foto asli.

![Foto Berwatermark](hasil_watermarking/03_foto_berwatermark_lossless.png)

---

### Step 4 — Mengekstrak watermark tanpa kompresi

Sebelum diuji dengan JPEG, watermark diekstrak terlebih dahulu dari gambar berwatermark tanpa kompresi untuk memastikan proses penyisipan berhasil.

![Watermark Ekstrak Tanpa Kompresi](hasil_watermarking/04_watermark_ekstrak_lossless.png)

---

### Step 5 — Mengompresi gambar dengan berbagai QF

Gambar berwatermark dikompresi menggunakan JPEG dengan nilai QF berikut:

`100, 95, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5`

---

### Step 6 — Mengekstrak watermark dari hasil JPEG

Setelah kompresi, watermark diekstrak kembali dari setiap gambar untuk melihat apakah watermark masih dapat dibaca.

#### Contoh hasil ekstraksi pada QF tinggi

**QF 100**

![Watermark QF 100](hasil_watermarking/watermark_ekstrak_QF_100.png)

#### Contoh hasil ekstraksi pada batas minimum OK

**QF 30**

![Watermark QF 30](hasil_watermarking/watermark_ekstrak_QF_30.png)

#### Contoh hasil ekstraksi pada QF sangat rendah

**QF 5**

![Watermark QF 5](hasil_watermarking/watermark_ekstrak_QF_5.png)

---

### Step 7 — Menghitung BER dan Accuracy

Kinerja watermark diukur menggunakan:

- **BER (Bit Error Rate)** = proporsi bit watermark yang salah saat diekstrak
- **Accuracy** = persentase bit watermark yang berhasil dibaca dengan benar

Watermark dianggap **OK** jika:

1. `QF >= 30`
2. `BER <= 0.30`

---

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

---

## Visualisasi Hasil

Grafik berikut menunjukkan hubungan antara QF dan BER.

![Grafik BER vs QF](hasil_watermarking/grafik_BER_vs_QF.png)

Semakin rendah nilai QF, kompresi JPEG semakin kuat dan kecenderungannya watermark menjadi semakin sulit dipertahankan.

---

## Kesimpulan

- Watermark berhasil disisipkan dan dapat diekstrak kembali dengan baik.
- Pada QF **100 sampai 40**, hasil ekstraksi masih sangat baik dengan BER = 0.
- Pada QF **30**, watermark masih dianggap berhasil karena BER = 0.045898 dan accuracy = 0.954102.
- Pada QF **20, 10, dan 5**, watermark dianggap gagal karena berada di bawah batas minimum QF yang ditetapkan, yaitu 30.

Jadi, **batas minimum QF yang masih dianggap OK dalam eksperimen ini adalah QF 30**.

---

## File Penting

- `watermarking.py` → kode program utama
- `hasil_watermarking/hasil_evaluasi_QF.csv` → hasil evaluasi dalam bentuk tabel
- `hasil_watermarking/grafik_BER_vs_QF.png` → grafik evaluasi
- `hasil_watermarking/` → seluruh output gambar hasil eksperimen