import re
import sys
import requests
from tkinter import Tk, filedialog

#Konfigurasi

Bantuan = """
Panduan pola pencarian:
_ (underscore) => tepat 1 karakter sembarang contoh => b_la => bola, bela, bila
= (sama dengan) => 0 atau lebih karakter sembarang, contoh => b=la => bla, bela, berla
Tanpa tanda =? pencarian awalan (prefix) contoh => bel => beli, belajar, belok....,

Ketik 'stop' atau 'quit' untuk keluar.
Ketik 'bantuan'  untuk menampilkan pesan ini. """ 

# muat dari gdrive #

def id_gdrive(link: str) -> str:
    try:
        return link.split('/d/') [1].split('/')[0]
    except IndexError:
        raise ValueError("Link Gdrive ga valid.")

def muat_kamus_gdrive(link: str):
    file_id = id_gdrive(link)
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    print("Download kamus dari gdrive...")
    resp = requests.get(url)
    if resp.status_code !=200:
        raise ConnectionError("Gagal download file.")
    return [line.strip().lower() for line in resp.text.splitlines() if line.strip()]

# Muat kamus dari lokal #
def muat_kamus_lokal():
    Tk().withdraw()
    path = filedialog.askopenfilename(title="pilih kamus (.txt)", filetypes=[("Text file", "*.txt")])
    if not path:
        raise ValueError ("Ga ada file di pilih.")
    print ("muat kamus dari file lokal...")
    with open(path, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]
    
# konversi pola ke regex #
def pola_regex(pola):
    ada_wildcard = ('_' in pola) or ('=' in pola)
    bagian = re.split(r'([_=])', pola)
    hasil = []
    
    for b in  bagian:
        if b == '_':
            hasil.append('.')
        elif b == '=':
            hasil.append('.*')
        else:
            hasil.append(re.escape(b))
    
    inti = ''.join(hasil)
    
    return f'^{inti}$' if ada_wildcard else f'^{inti}.*$'


# cari kata #
def cari (kamus, pola):
    regex = pola_regex(pola)
    return [k for k in kamus if re.match(regex, k)]

# utama #
def main():
    print("Pilih sumber kamus:")
    print("1 => GDrive")
    print("0 =>  FIle lokal")

    pilih = input ("Pilih: ").strip()
    try:
        if pilih == "1":
            link = input("Masukin link GDrive: ").strip()
            kamus = muat_kamus_gdrive(link)

        elif pilih == "0":
            kamus = muat_kamus_lokal()

        else:
            print("Pilihan ga valid.")
            return
        
    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)

    print(f"\n{len(kamus):,} kata berhasil dimuat.")
    print(Bantuan)

    while True:
        pola = input("masukkan pola: ").lower().strip()
        if pola == "stop":
            print("program berhenti")
            break
        
        hasil = cari(kamus, pola)

        if hasil:
            print(f"{len(hasil)} kata ketemu")
            print("\n".join(hasil))
        else:
            print("gada kata yang cocok.")

        print("-"*30)
if __name__ == "__main__":
    main ()