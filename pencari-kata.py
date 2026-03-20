import re
import os
import sys
import time
import requests
from collections import defaultdict
from tkinter import Tk, filedialog

help_msg = """
cara pake:
  _  => 1 huruf sembarang        contoh: b_la  = bola, bela, bila
  =  => bebas berapa huruf aja   contoh: b=la  = bla, bela, berlapis
  (kosong) => cari dari awal     contoh: bel   = beli, belok, belajar

stop / quit = keluar
bantuan     = tampilkan ini lagi
"""

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
    r.withdraw()    # hide windows kosong
    r.attributes('-topmost', True)  # majuin dialog

    path = filedialog.askopenfilename(
        title="pilih file kamus (.txt)",
        filetypes=[("Text file", "*.txt")]
    )
    r.destroy()

    if not path:
        raise ValueError("Gada file yang dipilih")
    print(f"baca file: {path}")

    with open(path, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

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

    # prefix: startswith > regex
    if not has_wild:
        pool = [w for sub in idx[first].values() for w in sub] if first and first in idx else word_list
        return [w for w in pool if w.startswith(pola)]

    # bangun regex inline, per karakter
    pat = ''
    for c in pola:
        if c == '_':   pat += '.'
        elif c == '=': pat += '.*'
        else:          pat += re.escape(c)
    rx = re.compile(f'^{pat}$')

    # kandidat sekecil mungkin
    if first and first in idx:
        pool = idx[first][fixlen] if fixlen and fixlen in idx[first] else [w for sub in idx[first].values() for w in sub]
    elif fixlen:
        pool = [w for sub in idx.values() for w in sub.get(fixlen, [])]
    else:
        pool = word_list
    return [w for w in pool if rx.match(w)]

def main():
    print("sumber kamus:")
    print("  1 = Google Drive")
    print("  0 = file lokal")

    pilih = input("pilih: ").strip()

    try:
        if pilih == '1':
            link = input("link gdrive: ").strip()
            words = load_from_gdrive(link)
        elif pilih == '0':
            words = load_local()
        else:
            print("pilihan ga valid")
            return
        
    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)

    print(f"{len(words):,} kata dimuat")
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