# ==========================================================
# Nama Skrip: ASCII.py
# Deskripsi: Skrip ini menyediakan pilihan untuk membuat ASCII dari gambar Offline dan Online.
# Pembuat: [SCREENLAVERS]
# Tanggal: [27-10-2024]
# ==========================================================

import os
import time
import platform
import subprocess
import requests
from PIL import Image
import numpy as np
import mimetypes

# Daftar pustaka yang dibutuhkan
REQUIRED_LIBRARIES = ["requests", "Pillow", "numpy"]

# Fungsi untuk menginstal pustaka yang dibutuhkan
def install_libraries():
    for lib in REQUIRED_LIBRARIES:
        try:
            __import__(lib)
        except ImportError:
            print(f"Menginstal pustaka '{lib}'...")
            subprocess.check_call(["pip", "install", lib])

# Jalankan instalasi pustaka jika belum ada
install_libraries()

# Kode warna ANSI untuk teks berwarna di terminal
GREEN = "\033[92m"
RED = "\033[91m"
WHITE = "\033[97m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Karakter untuk ASCII, dari gelap ke terang
ascii_chars = " %#*+=-:. "

# Fungsi untuk mengonversi piksel menjadi karakter ASCII
def pixel_to_ascii(pixel_value):
    return ascii_chars[pixel_value // 32]

# Fungsi untuk menghapus tampilan terminal
def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

# Fungsi untuk hitung mundur
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{BLUE}Kembali ke menu dalam {i} detik...{RESET}", end="\r")
        time.sleep(1)
    print(" " * 40, end="\r")

# Fungsi utama untuk mengonversi gambar menjadi ASCII
def image_to_ascii(image_path, new_width=100, output_folder="ascii_output", output_file="output.txt"):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"{RED}Terjadi kesalahan saat membuka gambar: {e}{RESET}")
        return

    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    image = image.resize((new_width, new_height))
    image = image.convert("L")

    ascii_image = ""
    pixels = np.array(image)
    for row in pixels:
        ascii_image += "".join(pixel_to_ascii(pixel) for pixel in row) + "\n"

    ascii_lines = ascii_image.splitlines()
    mid_point = len(ascii_lines) // 2
    top_half = "\n".join(ascii_lines[:mid_point])
    bottom_half = "\n".join(ascii_lines[mid_point:])

    for line in top_half.splitlines():
        print(f"{RED}{line}{RESET}")
        time.sleep(0.05)
    for line in bottom_half.splitlines():
        print(f"{WHITE}{line}{RESET}")
        time.sleep(0.05)

    while True:
        save = input(f"{BLUE}Apakah Anda ingin menyimpan hasil ASCII ini ke dalam file? (yes/no): {RESET}").strip().lower()
        if save == "yes":
            os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, output_file)
            with open(output_path, "w") as f:
                f.write(ascii_image)
            print(f"{GREEN}Hasil ASCII disimpan di folder '{output_folder}' dengan nama file '{output_file}'{RESET}")

            # Menanyakan apakah ingin membuka file hasil ASCII
            open_file = input(f"{BLUE}Apakah Anda ingin membuka file hasil ASCII ini? (yes/no): {RESET}").strip().lower()
            if open_file == "yes":
                if platform.system() == "Windows":
                    os.startfile(output_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.call(["open", output_path])
                else:  # Linux
                    subprocess.call(["xdg-open", output_path])
            break
        elif save == "no":
            print(f"{RED}Hasil ASCII tidak disimpan.{RESET}")
            time.sleep(2)
            break
        else:
            print(f"{RED}Input tidak valid. Silakan masukkan 'yes' atau 'no'.{RESET}")

# Fungsi untuk mengunduh gambar dari URL
def download_image_from_url(folder_name="downloaded_images"):
    while True:
        image_url = input(f"{BLUE}Masukkan URL gambar yang ingin diunduh (format JPG atau PNG): {RESET}").strip()
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            content_type = response.headers['Content-Type']
            extension = mimetypes.guess_extension(content_type.split(';')[0]) or ''
            if extension.lower() not in ['.jpg', '.jpeg', '.png']:
                print(f"{RED}Format gambar tidak valid. Silakan masukkan URL yang mengarah ke gambar JPG atau PNG.{RESET}")
                continue

            os.makedirs(folder_name, exist_ok=True)
            image_path = os.path.join(folder_name, f"downloaded_image{extension}")

            with open(image_path, "wb") as f:
                f.write(response.content)
            print(f"{GREEN}Gambar berhasil diunduh dari {image_url} dan disimpan di '{folder_name}' sebagai '{os.path.basename(image_path)}'.{RESET}")

            while True:
                proceed = input(f"{BLUE}Apakah Anda ingin melanjutkan untuk mengonversi gambar ini menjadi ASCII? (yes/no): {RESET}").strip().lower()
                if proceed == "yes":
                    return image_path
                elif proceed == "no":
                    print(f"{GREEN}Kembali ke menu utama.{RESET}")
                    time.sleep(2)
                    return None
                else:
                    print(f"{RED}Input tidak valid. Silakan masukkan 'yes' atau 'no'.{RESET}")

        except requests.exceptions.RequestException as e:
            print(f"{RED}Terjadi kesalahan saat mengunduh gambar: {e}. Silakan coba lagi.{RESET}")

# Fungsi untuk pilihan nomor 2
def pilihan_kedua():
    image_path = download_image_from_url()
    if image_path:
        image_to_ascii(image_path, new_width=100, output_folder="Hasil", output_file="output_ascii.txt")
        print(f"{GREEN}Konversi selesai!{RESET}")
        countdown(5)
    clear_terminal()

# Fungsi untuk menampilkan tampilan menu yang diinginkan dengan warna hijau
def display_intro():
    print(f"{GREEN}")
    print("""
                 %%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%%%%%%%%%%%%                              
                  #:::::::::::= *--------------------------*                              
                   #:::::::::= *--------------------------*                               
                    #:::::::+ +--------------------------*                                
                     #:::::+ +--------------------------*                                 
                      #:::* =---------+++++++++++++++--*             ____________  _________  ____   ___ _   _________  ____                      
                       %-* =---------#               *+             / __/ ___/ _ \/ __/ __/ |/ / /  / _ | | / / __/ _ \/ __/                     
                         %=---------#                              _\ \/ /__/ , _/ _// _//    / /__/ __ | |/ / _// , _/\ \                       
                         #----------=---------------*             /___/\___/_/|_/___/___/_/|_/____/_/ |_|___/___/_/|_/___/                      
                          #------------------------+             ========================================================                        
                           #----------------------+                - PROGRAM  : FROM ZERO TO DEVELOPMENT                 
                            %--------------------+                 - TELEGRAM : @SCREENLAVERS                    
                             %========----------+                  - GITHUB   : https://github.com/SCREENLAVERS                      
                                     *---------+                                          
                                    *---------+                                           
                                %+==---------+                                            
                                 %----------+                                             
                                   =-------+                                              
                                    +-----+                                               
                                     *---+                                                
                                      #-+                                                 
                                       %    
    """)
    print(f"{RESET}")

# Fungsi menu utama
def main_menu():
    while True:
        clear_terminal()
        display_intro()  # Display the intro graphic with green color
        print(f"{GREEN}=== Menu Pilihan ==={RESET}")
        print(f"{YELLOW}1. Jalankan Skrip ASCII dari file lokal{RESET}")
        print(f"{YELLOW}2. Unduh gambar dari URL dan jalankan Skrip ASCII{RESET}")
        print(f"{YELLOW}3. Keluar{RESET}")
        
        choice = input(f"{BLUE}Silakan pilih (1/2/3): {RESET}").strip()

        if choice == "1":
            while True:
                image_path = input(f"{BLUE}Masukkan jalur file gambar lokal: {RESET}").strip()
                if os.path.exists(image_path):
                    image_to_ascii(image_path, new_width=100, output_folder="Hasil", output_file="output_ascii.txt")
                    print(f"{GREEN}Konversi selesai!{RESET}")
                    countdown(5)
                    break
                else:
                    print(f"{RED}Jalur file tidak valid. Silakan masukkan jalur yang benar.{RESET}")
            clear_terminal()
        elif choice == "2":
            pilihan_kedua()
        elif choice == "3":
            print(f"{GREEN}Terima kasih telah menggunakan program ini!{RESET}")
            break
        else:
            print(f"{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")

# Menjalankan menu utama
if __name__ == "__main__":
    main_menu()
