import re
import time
import sys
import requests
from collections import defaultdict
from tkinter import Tk, filedialog

# --- info cara pake ---
help_msg = """
cara pake:
  _  => 1 huruf sembarang        contoh: b_la  = bola, bela, bila
  =  => bebas berapa huruf aja   contoh: b=la  = bla, bela, berlapis
  (kosong) => cari dari awal     contoh: bel   = beli, belok, belajar

stop / quit = keluar
bantuan     = tampilkan ini lagi
"""

# ambil id dari link gdrive
def get_gdrive_id(link):
    try:
        return link.split('/d/')[1].split('/')[0]
    except:
        raise ValueError("link gdrive-nya ga bener deh")

def load_from_gdrive(link):
    fid = get_gdrive_id(link)
    url = f'https://drive.google.com/uc?export=download&id={fid}'
    print("downloading...")
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        raise ConnectionError(f"gagal, status: {r.status_code}")
    words = [x.strip().lower() for x in r.text.splitlines() if x.strip()]
    return words

def load_local():
    Tk().withdraw()
    p = filedialog.askopenfilename(
        title="pilih file kamus (.txt)",
        filetypes=[("Text file", "*.txt")]
    )
    if not p:
        raise ValueError("ga ada file dipilih")
    print(f"baca file: {p}")
    with open(p, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

# bikin index buat nyepatin search
# struktur: index[huruf_pertama][panjang] = [list kata]
# misal index['b'][4] = ['bola','batu','beli',...]
def build_index(word_list):
    idx = defaultdict(lambda: defaultdict(list))
    for w in word_list:
        if not w:
            continue
        first = w[0]
        n = len(w)
        idx[first][n].append(w)
    # debug: uncomment buat liat distribusinya
    # for h in sorted(idx): print(h, {k: len(v) for k,v in idx[h].items()})
    return idx

def parse_pattern(p):
    has_eq   = '=' in p
    has_wild = has_eq or ('_' in p)

    # huruf awal cuma berguna kalau bukan wildcard
    first = p[0] if p and p[0] not in ('_','=') else None

    # kalau ada '=', panjang ga bisa ditentukan
    # kalau ada '_' aja, tiap _ = 1 huruf jadi panjang = len(pola)
    fixed_len = len(p) if not has_eq else None

    return first, fixed_len, not has_wild   # first, len, is_prefix

# _ jadi . (1 char), = jadi .* (bebas)
def to_regex(p):
    has_wild = ('_' in p) or ('=' in p)
    parts = re.split(r'([_=])', p)

    tmp = []
    for chunk in parts:
        if chunk == '_':   tmp.append('.')
        elif chunk == '=': tmp.append('.*')
        else:              tmp.append(re.escape(chunk))

    core = ''.join(tmp)
    pattern = f'^{core}$' if has_wild else f'^{core}.*$'
    return re.compile(pattern)

def search(word_list, idx, pola):
    first, fixed_len, is_prefix = parse_pattern(pola)

    # shortcut: prefix search pake startswith, ga perlu regex sama sekali
    if is_prefix:
        pool = (
            [w for sub in idx[first].values() for w in sub]
            if first and first in idx
            else word_list
        )
        return [w for w in pool if w.startswith(pola)]

    rx = to_regex(pola)
    
    # pilih kandidat sekecil mungkin sebelum regex
    if first and first in idx:
        if fixed_len and fixed_len in idx[first]:
            pool = idx[first][fixed_len]              # paling sempit
        else:
            pool = [w for sub in idx[first].values() for w in sub]
    elif fixed_len:
        pool = [w for sub in idx.values() for w in sub.get(fixed_len, [])]
    else:
        pool = word_list   # worst case, tapi jarang

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
    t0 = time.perf_counter()
    idx = build_index(words)
    t1 = time.perf_counter()
    print(f"index siap ({len(idx)} huruf, {(t1-t0)*1000:.1f} ms)\n")

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
            print(f"{len(found)} kata ketemu({ms:.2f} ms)")
            print('\n'.join(found))
        else:
            print(f"ga ketemu ({ms:.2f} ms)")

        print('-' * 28)

if __name__ == '__main__':
    main()