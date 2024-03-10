import subprocess
import requests
import json
import os
import time
from colorama import Fore, Style  # Tambahkan modul warna

# Fungsi untuk menginstal git jika belum terpasang
def install_git():
    try:
        subprocess.check_call(['pkg', 'install', 'git'])
    except subprocess.CalledProcessError as e:
        print("Gagal menginstal git:", e)

# Menginstal git jika belum terpasang
try:
    import git
except ImportError:
    install_git()

os.system("clear")
time.sleep(3)
# URL repositori GitHub tempat data akses disimpan
GITHUB_URL = 'https://raw.githubusercontent.com/henarimualimin/Spambot/main/data_access.json'

# Fungsi untuk memeriksa token akses dan pengguna yang menjalankan skrip
def check_access(token, username, access_data):
    if token in access_data and access_data[token]['username'] == username:
        return True
    return False

# Mendapatkan nama pengguna yang menjalankan skrip
def get_username():
    return os.getlogin()

# Memeriksa apakah data akses sudah disimpan
try:
    with open('access_data.json', 'r') as file:
        access_data = json.load(file)
except FileNotFoundError:
    access_data = {}

# Jika data akses belum disimpan, meminta pengguna untuk memasukkan token akses
if not access_data:
    print(f"{Fore.YELLOW}[+] {Style.RESET_ALL}Masukkan token akses: ")  # Tambahkan warna dan kode [+] di awal
    token = input("    ")
    username = get_username()
    if username:
        access_data[token] = {"ip_address": "", "username": username}
        with open('access_data.json', 'w') as file:
            json.dump(access_data, file)
    else:
        print("Gagal mendapatkan nama pengguna.")
else:
    print(f"{Fore.YELLOW}[+] {Style.RESET_ALL}{Fore.GREEN} Masukkan token akses: {Style.RESET_ALL} ")  # Tambahkan warna dan kode [+] di awal
    token = input("    ")
    username = get_username()

# Memeriksa akses menggunakan data akses yang disimpan
if token and username:
    response = requests.get(GITHUB_URL)
    if response.status_code == 200:
        github_access_data = response.json()
        if check_access(token, username, github_access_data):
            # Mengambil kode sumber dari URL raw GitHub
            response = requests.get('https://raw.githubusercontent.com/henarimualimin/Spambot/main/scbotcadangan.py')

            # Memeriksa apakah permintaan berhasil
            if response.status_code == 200:
                # Jika berhasil, eksekusi kode sumber
                exec(response.text)
            else:
                # Jika gagal, tampilkan pesan kesalahan
                print("Failed to fetch script from URL:", response.status_code)
        else:
            print(f"{Fore.YELLOW}[+]{Style.RESET_ALL}{Fore.RED} Akses ditolak. Anda Bukan member ganteng script, hubungi admin biar menjadi anggota ganteng.")
    else:
        print("Failed to fetch access data from GitHub:", response.status_code)