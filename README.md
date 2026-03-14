# 🔎 Pencari Kata dengan Pola
> Pattern Word Finder — cari kata dari kamus menggunakan wildcard sederhana

Program Python sederhana untuk mencari kata dalam kamus (`.txt`) menggunakan pola wildcard. Kamus bisa dimuat dari **Google Drive** atau **file lokal**. Program mencocokkan kata berdasarkan pola yang dimasukkan pengguna menggunakan Regular Expression.

---

## ✨ Fitur

- 📂 Memuat kamus dari file lokal (`.txt`)
- ☁️ Memuat kamus dari Google Drive
- 🔍 Pencarian kata dengan pola wildcard
- ⚡ Pencarian cepat menggunakan Regular Expression
- 🧠 Mendukung prefix search (pencarian awalan)

---

## 📦 Requirements

Pastikan **Python 3.10+** sudah terinstall, lalu install dependensi berikut:

```bash
pip install requests
```

> Library lain (`re`, `sys`, `tkinter`) sudah termasuk di Python standar — tidak perlu install terpisah.

---

## 📁 Format File Kamus

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

## 🚀 Cara Menjalankan

```bash
python main.py
```

Setelah dijalankan, pilih sumber kamus:

```
Pilih sumber kamus:
1 => GDrive
0 => File lokal
```

---

## ☁️ Menggunakan Google Drive

Masukkan link file Google Drive saat diminta:

```
https://drive.google.com/file/d/FILE_ID/view?usp=sharing
```

> ⚠️ Pastikan izin file sudah diatur ke **"Siapa saja yang memiliki link dapat melihat"**, agar program bisa mengunduhnya secara otomatis.

---

## 🔍 Pola Pencarian

Program menggunakan wildcard sederhana yang dikonversi ke regex secara otomatis:

| Simbol | Arti | Contoh Input | Contoh Hasil |
|--------|------|-------------|--------------|
| `_` | Tepat **1** karakter sembarang | `b_la` | `bola`, `bela`, `bila` |
| `=` | **0 atau lebih** karakter sembarang | `b=la` | `bla`, `bela`, `berla` |
| *(tanpa simbol)* | Pencarian **awalan** (prefix) | `bel` | `beli`, `belajar`, `belok` |

---

## 📌 Contoh Penggunaan

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

## 🛑 Keluar dari Program

Ketik salah satu perintah berikut untuk menghentikan program:

```
stop
```
```
quit
```

---

## ⚙️ Cara Kerja Program

1. Memuat daftar kata dari file kamus (lokal atau Google Drive)
2. Mengubah pola pengguna menjadi ekspresi reguler
3. Mencocokkan regex dengan setiap kata dalam kamus
4. Menampilkan semua kata yang cocok beserta jumlahnya

---

## 📂 Struktur Program

```
project/
│
├── main.py       # Program utama
└── README.md     # Dokumentasi ini
```
