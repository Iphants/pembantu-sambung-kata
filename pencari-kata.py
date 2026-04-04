import re
import os
import sys
import time
import requests
from collections import defaultdict
from tkinter import Tk, filedialog
from dictionary_source import cd, s_words, l_words

help_msg = """
cara pake:
  _  => 1 huruf sembarang        contoh: b_la  = bola, bela, bila
  =  => bebas berapa huruf aja   contoh: b=la  = bla, bela, berlapis
  (kosong) => cari dari awal     contoh: bel   = beli, belok, belajar

stop / quit = keluar
bantuan     = tampilkan ini lagi
"""

# ---- ambil kata ----

def get_gdrive_id(link):
    try:
        return link.split('/d/')[1].split('/')[0]
    except:
        raise ValueError("link gdrive nya ga bener")

def load_from_gdrive(link):
    fid = get_gdrive_id(link)
    url = f'https://drive.google.com/uc?export=download&id={fid}'
    print("downloading...")
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        raise ConnectionError(f"gagal, status: {r.status_code}")
    return [x.strip().lower() for x in r.text.splitlines() if x.strip()]

def load_local():
    r = Tk()
    r.withdraw()
    r.attributes('-topmost', True)
    path = filedialog.askopenfilename(
        title="pilih file kamus (.txt)",
        filetypes=[("Text file", "*.txt")]
    )
    r.destroy()
    if not path:
        raise ValueError("gada file yang dipilih")
    print(f"baca file: {path}")
    with open(path, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def ambil_kata():
    print("\nsumber kamus:")
    print("  1 = Google Drive")
    print("  2 = Ambil Dari Website")
    pilih = input("pilih: ").strip()

    if pilih == '1':
        return load_from_gdrive(input("link gdrive: ").strip())
    elif pilih == '2':
        url = input("url website: ").strip()
        return cd(url)
    else:
        raise ValueError("pilihan ga valid")

# ---- opsional simpan ----

def tawarin_simpan(words):
    print(f"\n{len(words):,} kata ditemukan")
    print("\nsimpan daftar kata ini biar ga perlu download lagi?")
    print("  0 = simpan")
    print("  1 = ga usah (sementara aja)")
    if input("pilih: ").strip() == '0':
        nama = input("nama file (default: wordlist.txt): ").strip() or "wordlist.txt"
        s_words(words, nama)
    else:
        print("oke, kamus cuma dipakai sementara")

# ---- index & search ----

def build_index(word_list):
    idx = defaultdict(lambda: defaultdict(list))
    for w in word_list:
        idx[w[0]][len(w)].append(w)
    return idx

def search(word_list, idx, pola):
    has_eq   = '=' in pola
    has_wild = has_eq or ('_' in pola)
    first    = pola[0] if pola[0] not in ('_', '=') else None
    fixlen   = len(pola) if not has_eq else None

    if not has_wild:
        pool = [w for sub in idx[first].values() for w in sub] if first and first in idx else word_list
        return [w for w in pool if w.startswith(pola)]

    pat = ''
    for c in pola:
        if c == '_':   pat += '.'
        elif c == '=': pat += '.*'
        else:          pat += re.escape(c)
    rx = re.compile(f'^{pat}$')

    if first and first in idx:
        pool = idx[first][fixlen] if fixlen and fixlen in idx[first] else [w for sub in idx[first].values() for w in sub]
    elif fixlen:
        pool = [w for sub in idx.values() for w in sub.get(fixlen, [])]
    else:
        pool = word_list
    return [w for w in pool if rx.match(w)]

# ---- main ----

def main():
    # kalau udah punya wordlist, langsung load aja
    print("punya file wordlist yang sudah disimpan sebelumnya?")
    print("  1 = Ya")
    print("  0 = Tidak / Ambil Baru")

    try:
        if input("pilih: ").strip() == '1':
            words = load_local()   # pake dialog yang sama
        else:
            words = ambil_kata()
            tawarin_simpan(words)
    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)

    print(f"\n{len(words):,} kata dimuat")
    print("bikin index...")
    t0  = time.perf_counter()
    idx = build_index(words)
    print(f"index siap ({len(idx)} huruf, {(time.perf_counter()-t0)*1000:.1f} ms)\n")
    print(help_msg)

    while True:
        try:
            pola = input("pola: ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nkeluar")
            break
        if not pola:
            continue
        if pola in ('stop', 'quit', 'q'):
            print("program berhenti")
            break
        if pola in ('bantuan', 'help', '?'):
            print(help_msg)
            continue

        t0    = time.perf_counter()
        found = search(words, idx, pola)
        ms    = (time.perf_counter() - t0) * 1000
        if found:
            print(f"{len(found)} kata ketemu ({ms:.2f} ms)")
            print('\n'.join(found))
        else:
            print(f"ga ketemu ({ms:.2f} ms)")
        print('-' * 28)

if __name__ == '__main__':
    main()