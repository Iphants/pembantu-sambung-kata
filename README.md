#  Pencari Kata dengan Pola
> Pattern Word Finder — cari kata dari kamus menggunakan wildcard sederhana

Program Python sederhana untuk mencari kata dalam kamus (`.txt`) menggunakan pola wildcard. Kamus bisa dimuat dari **Google Drive** atau **file lokal** atau **Crawl Website**. Program mencocokkan kata berdasarkan pola yang dimasukkan pengguna menggunakan Regular Expression.

---

##  Fitur

-  Memuat kamus dari file lokal (`.txt`)
-  Memuat kamus dari Google Drive
-  Memuat kamus dari Crawl Website
-  Pencarian kata dengan pola wildcard
-  Pencarian cepat menggunakan Regular Expression
-  Mendukung prefix search (pencarian awalan)

---

##  Requirements

Pastikan **Python 3.10+** sudah terinstall, lalu install dependensi berikut:

```bash
pip install requests
```

> Library lain (`re`, `sys`, `tkinter`) sudah termasuk di Python standar — tidak perlu install terpisah.

---

##  Format File Kamus

File kamus harus berupa **text file** (`.txt`) dengan satu kata per baris:

```
apel
anggur
bola
belajar
beli
belok
```

---

##  Cara Menjalankan

```bash
python pencari-kata.py
```

Setelah dijalankan, pilih sumber kamus:

```
punya file wordlist yang sudah disimpan sebelumnya?:
  1 = Ya ->(file lokal yang sudah didownload)
  0 = Tidak / Ambil Baru
```
```
sumber kamus:
  1 = Google Drive
  2 = Ambil Dari Website
```
---

##  Menggunakan Google Drive

Masukkan link file Google Drive saat diminta: (berupa gdrive .txt murni)

```
https://drive.google.com/file/d/FILE_ID/view?usp=sharing
```

>  Pastikan izin file sudah diatur ke **"Siapa saja yang memiliki link dapat melihat"**, agar program bisa mengunduhnya secara otomatis.

---

##  Menggunakan Website

Masukkan link Website saat diminta:

```
https://www.kompas.com/
```

> Website yang Bisa Dicrawl ialah konten HTML statis, dimana teks sudah tersedia saat halaman dimuat, jadi Website dengan konten dinamis seperti Website dengan fitur pencarian real-time tidak bisa 
( yang bisa: blog, berita. yang tidak bisa: kbbi dll)

  Peringatan Penggunaan Web Crawling

 Fitur crawling pada proyek ini hanya ditujukan untuk eksperimen dan pengambilan data sederhana, **bukan sebagai sumber kamus yang akurat atau lengkap**.

 Beberapa hal yang perlu diperhatikan:

* Data yang diambil dari website bersifat **tidak terkontrol**, sehingga:

* Bisa mengandung kata yang tidak relevan (nama orang, tempat, istilah asing, dll)
* Tidak menjamin keakuratan atau validitas sebagai kata bahasa Indonesia
* Hasil crawling sangat bergantung pada struktur website, yang dapat berubah sewaktu-waktu
* Website tertentu menggunakan JavaScript (dynamic content), sehingga tidak semua data dapat diambil dengan metode ini
* Penggunaan crawling dalam jumlah besar berpotensi melanggar kebijakan website (rate limit, blocking, dll)

### Rekomendasi

Untuk penggunaan yang lebih stabil dan akurat, disarankan menggunakan **wordlist/dataset yang sudah tersedia** dibandingkan melakukan crawling secara langsung.

Gunakan fitur crawling hanya jika:

* Untuk pembelajaran
* Untuk eksperimen
* Atau sebagai sumber data tambahan (bukan utama)


##  Pola Pencarian

Program menggunakan wildcard sederhana yang dikonversi ke regex secara otomatis:

| Simbol | Arti | Contoh Input | Contoh Hasil |
|--------|------|-------------|--------------|
| `_` | Tepat **1** karakter sembarang | `b_la` | `bola`, `bela`, `bila` |
| `=` | **0 atau lebih** karakter sembarang | `b=la` | `bla`, `bela`, `berla` |
| *(tanpa simbol)* | Pencarian **awalan** (prefix) | `bel` | `beli`, `belajar`, `belok` |

---

##  Contoh Penggunaan

**Input:**
```
masukkan pola: b_la
```

**Output:**
```
3 kata ketemu
bola
bela
bila
------------------------------
```

**Input:**
```
masukkan pola: bel
```

**Output:**
```
3 kata ketemu
beli
belajar
belok
------------------------------
```

---

##  Keluar dari Program

Ketik salah satu perintah berikut untuk menghentikan program:

```
stop
```
```
quit
```
---

##  Cara Kerja Program

1. Memuat daftar kata dari file kamus (lokal atau Google Drive atau Crawl Website)
2. Mengubah pola pengguna menjadi ekspresi reguler
3. Mencocokkan regex dengan setiap kata dalam kamus
4. Menampilkan semua kata yang cocok beserta jumlahnya

---

##  Struktur Program

```
project/
│
├── pencari-kata.py    # Program utama
├── dictionary_source.py # Crawl dari website
└── README.md     # Dokumentasi ini
```
