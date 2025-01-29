from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

base_url = "https://putusan3.mahkamahagung.go.id/direktori/index/pengadilan/pn-sleman/kategori/narkotika-dan-psikotropika-1/tahunjenis/putus/tahun/2024/page/{page}.html" # Anda bisa menganti dengan link serupa

response = requests.get(base_url)

# Cek apakah permintaan berhasil dilakukan
if response.status_code == 200:
    html_content = response.text
else:
    print('Gagal mengambil halaman:', response.status_code)

# Inisialisasi halaman awal dan akhir
page_awal = 1
page_akhir = 5

# Loop untuk mengambil data hingga halaman 3
for page in range(page_awal, page_akhir):
    url = base_url.format(page=page)

    response = requests.get(url)

    if response.status_code == 200:
        # Parsing konten HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cari elemen <strong> yang memiliki <a> di dalamnya
        strong_tags = soup.find_all('strong')

        for strong in strong_tags:
            # Cari elemen <a> di dalam <strong>
            link = strong.find('a')
            if link:
                # Ambil teks dan href dari elemen <a>
                title = link.text.strip()
                href = link['href']

                print(f"Judul: {title}")
                print(f"URL: {href}\n")
    else:
        print(f"Gagal mengakses halaman {page}.")

# Buka file CSV untuk menulis data
with open('putusan_links.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Putusan', 'Link'])

    # Loop untuk halaman
    for page in range(page_awal, page_akhir):
        url = base_url.format(page=page)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            strong_tags = soup.find_all('strong')

            for strong in strong_tags:
                link = strong.find('a')
                if link:
                    title = link.text.strip()
                    href = link['href']
                    writer.writerow([title, href])

df = pd.read_csv('putusan_links.csv')
df.head()

# Baca semua link pada putusan_links.csv
link = df.drop(columns=['Putusan'])
link.head()

# Siapkan file CSV untuk menyimpan data
with open('putusan_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(["No Putusan", "Lembaga Peradilan", "Barang Bukti", "Amar Putusan"])

    # Loop melalui setiap URL dalam file CSV
    for url in link['Link']:
        response = requests.get(url)

        if response.status_code == 200:
            # Parsing konten HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Cari tabel
            table = soup.find('table', {'class': 'table'})

            # Dictionary untuk menyimpan data
            data = {
                "No Putusan": None,
                "Lembaga Peradilan": None,
                "Barang Bukti": [],
                "Amar Putusan": []
            }

            if table:
                rows = table.find_all('tr')

                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) == 2:
                        label = cols[0].text.strip()
                        value = cols[1].text.strip()

                        # Cocokkan label dengan key dictionary
                        if label == "Nomor":
                            data["No Putusan"] = value
                        elif label == "Lembaga Peradilan":
                            data["Lembaga Peradilan"] = value

                    # Cari dan ambil konten Barang Bukti
                    barang_bukti_ul = row.find('ul')
                    if barang_bukti_ul:
                        data["Barang Bukti"] = [li.text.strip() for li in barang_bukti_ul.find_all('li')]

                    # Jika Barang Bukti masih kosong, cari dengan teks
                    if not data["Barang Bukti"]:
                      if "Menetapkan barang bukti berupa" in row.text:
                        barang_bukti_start = row.text.split("Menetapkan barang bukti berupa")[1]

                        if "Dirampas" in barang_bukti_start:
                          barang_bukti_end = barang_bukti_start.split("Dirampas")[0]
                          data["Barang Bukti"] = [barang_bukti_end.strip()]

                        if "Dimusnahkan" in barang_bukti_start:
                          barang_bukti_end = barang_bukti_start.split("Dimusnahkan")[0]
                          data["Barang Bukti"] = [barang_bukti_end.strip()]

                        if "dirampas" in barang_bukti_start:
                          barang_bukti_end = barang_bukti_start.split("dirampas")[0]
                          data["Barang Bukti"] = [barang_bukti_end.strip()]

                        if "dimusnahkan" in barang_bukti_start:
                          barang_bukti_end = barang_bukti_start.split("dimusnahkan")[0]
                          data["Barang Bukti"] = [barang_bukti_end.strip()]

                    # Cari dan ambil konten Amar Putusan
                    amar_putusan_elements = row.find_all(['ol', 'ul', 'p'])
                    for element in amar_putusan_elements:
                        data["Amar Putusan"].append(element.text.strip())

            # Menulis data ke CSV
            writer.writerow([data["No Putusan"], data["Lembaga Peradilan"], "; ".join(data["Barang Bukti"]), "; ".join(data["Amar Putusan"])])
            print(f"Data untuk URL {url} berhasil disimpan.")
        else:
            print(f"Gagal mengakses halaman {url}.")

# Tampilkan hasil crawling data untuk seluruh link yang di ekstrak
hasil = pd.read_csv('putusan_data.csv')
hasil.head()

hasil.isnull().sum()

