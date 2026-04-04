import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def df(url):
    print(f"download dari {url}...")
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise ConnectionError(f"gagal, status {r.status_code}")
    return [x.strip().lower() for x in r.text.splitlines() if x.strip()]

def cd(base_url, delay=1.5):
    u_input = input("berapa halaman? (angka / 'max'): ").strip().lower()
    if u_input in ["max", "maks"]:
        confirm = input("beneran semua? (y/n): ").strip().lower()
        if confirm == "y":
            max_pages = float("inf")
        else:
            print("dibatalkan, pake default 30")
            max_pages = 30
    else:
        try:
            max_pages = int(u_input)
            if max_pages <= 0:
                print("minimal 1, pake default 30")
                max_pages = 30
        except:
            print("input salah, pake default 30")
            max_pages = 30

    print(f"crawl {base_url}, max {max_pages} halaman")
    visited, t_visit = set(), [base_url]
    all_words = set()
    n = 0

    while t_visit and n < max_pages:
        url = t_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code != 200:
                continue

            words = e_words(r.text)
            all_words.update(words)
            n += 1
            print(f"  [{n}] {url} — +{len(words)}, total {len(all_words)}")

            soup = BeautifulSoup(r.text, 'html.parser')
            dom = urlparse(base_url).netloc
            for a in soup.find_all('a', href=True):
                link = urljoin(url, a['href'])
                if urlparse(link).netloc == dom and link not in visited:
                    t_visit.append(link)

            time.sleep(delay)
        except Exception as e:
            print(f"  skip {url}: {e}")
            continue

    print(f"selesai — {len(all_words)} kata dari {n} halaman")
    return sorted(all_words)

def e_words(html):
    s = BeautifulSoup(html, "html.parser")
    for tag in s(['script', 'style', 'nav', 'footer']):
        tag.decompose()
    text = s.get_text(' ')
    return [w.lower() for w in re.findall(r'\b[a-zA-Z]{2,}\b', text)]

def s_words(words, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(set(words))))
    kb = os.path.getsize(path) / 1024
    print(f"disimpan di {path} ({kb:.1f} KB)")

def l_words(path):
    with open(path, encoding='utf-8') as f:
        return [line.strip().lower() for line in f if line.strip()]