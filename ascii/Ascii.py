# ==========================================================
# Nama Skrip: ASCII.py
# Deskripsi: Skrip ini menyediakan pilihan untuk membuat ASCII dari gambar Offline dan Online.
# Pembuat: [SCREENLAVERS]
# Tanggal: [27-10-2024]
# ==========================================================

import os
import requests
from PIL import Image
import numpy as np
import mimetypes
import time  # Import time module for sleep function
import platform  # Import platform module to detect OS

# Kode warna ANSI untuk teks berwarna di terminal
GREEN = "\033[92m"
RED = "\033[91m"
WHITE = "\033[97m"
BLUE = "\033[94m"  # Kode warna untuk biru
YELLOW = "\033[93m"  # Kode warna untuk kuning
RESET = "\033[0m"  # Untuk mengatur ulang warna teks ke default

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
    print(" " * 40, end="\r")  # Clear the countdown line

# Fungsi utama untuk mengonversi gambar menjadi ASCII
def image_to_ascii(image_path, new_width=100, output_folder="ascii_output", output_file="output.txt"):
    # Buka dan ubah ukuran gambar
    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # Menjaga proporsi
    image = image.resize((new_width, new_height))
    image = image.convert("L")  # Konversi ke grayscale

    # Konversi gambar ke array ASCII
    ascii_image = ""
    pixels = np.array(image)
    for row in pixels:
        ascii_image += "".join(pixel_to_ascii(pixel) for pixel in row) + "\n"

    # Pisahkan hasil ASCII menjadi dua bagian: atas dan bawah
    ascii_lines = ascii_image.splitlines()
    mid_point = len(ascii_lines) // 2
    top_half = "\n".join(ascii_lines[:mid_point])
    bottom_half = "\n".join(ascii_lines[mid_point:])

    # Tampilkan hasil ASCII dengan dua warna di terminal
    for line in top_half.splitlines():
        print(f"{RED}{line}{RESET}")
        time.sleep(0.05)  # Delay for typing effect
    for line in bottom_half.splitlines():
        print(f"{WHITE}{line}{RESET}")
        time.sleep(0.05)  # Delay for typing effect

    # Meminta konfirmasi untuk menyimpan hasil ASCII
    while True:
        save = input(f"{BLUE}Apakah Anda ingin menyimpan hasil ASCII ini ke dalam file? (yes/no): {RESET}").strip().lower()
        if save == "yes":
            # Membuat folder output jika belum ada
            os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, output_file)

            # Simpan hasil ASCII ke file
            with open(output_path, "w") as f:
                f.write(ascii_image)

            print(f"{GREEN}Hasil ASCII disimpan di folder '{output_folder}' dengan nama file '{output_file}'{RESET}")
            break  # Keluar dari loop jika berhasil menyimpan
        elif save == "no":
            print(f"{RED}Hasil ASCII tidak disimpan.{RESET}")
            time.sleep(2)  # Jeda waktu sebelum kembali ke menu
            break  # Keluar dari loop jika tidak ingin menyimpan
        else:
            print(f"{RED}Input tidak valid. Silakan masukkan 'yes' atau 'no'.{RESET}")

# Fungsi untuk mengunduh gambar dari URL
def download_image_from_url(folder_name="downloaded_images"):
    while True:
        image_url = input(f"{BLUE}Masukkan URL gambar yang ingin diunduh (harus JPG): {RESET}").strip()
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Memicu exception jika status tidak OK
            
            # Mengambil jenis konten dari header response
            content_type = response.headers['Content-Type']
            extension = mimetypes.guess_extension(content_type.split(';')[0]) or '.jpg'  # Default to .jpg if unknown

            # Validasi: pastikan format gambar adalah JPG
            if extension.lower() != '.jpg':
                print(f"{RED}Format gambar tidak valid. Silakan masukkan URL yang mengarah ke gambar JPG.{RESET}")
                continue  # Kembali ke awal loop untuk meminta URL yang baru
            
            # Membuat folder untuk menyimpan gambar yang diunduh
            os.makedirs(folder_name, exist_ok=True)
            image_path = os.path.join(folder_name, f"downloaded_image{extension}")  # Nama file untuk menyimpan gambar
            
            with open(image_path, "wb") as f:
                f.write(response.content)
            print(f"{GREEN}Gambar berhasil diunduh dari {image_url} dan disimpan di '{folder_name}' sebagai '{os.path.basename(image_path)}'.{RESET}")

            # Meminta konfirmasi untuk melanjutkan atau kembali ke menu utama
            while True:
                proceed = input(f"{BLUE}Apakah Anda ingin melanjutkan untuk mengonversi gambar ini menjadi ASCII? (yes/no): {RESET}").strip().lower()
                if proceed == "yes":
                    return image_path  # Kembalikan path gambar untuk konversi
                elif proceed == "no":
                    print(f"{GREEN}Kembali ke menu utama.{RESET}")
                    time.sleep(2)  # Jeda waktu sebelum kembali ke menu
                    return None  # Kembali ke menu utama tanpa mengembalikan path
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
        countdown(5)  # Hitung mundur 5 detik sebelum kembali ke menu
    clear_terminal()  # Clear terminal after processing

# Fungsi menu utama
def main_menu():
    while True:
        clear_terminal()  # Clear terminal at the beginning of the menu
        print(f"{GREEN}=== Menu Pilihan ==={RESET}")
        print(f"{YELLOW}1. Jalankan Skrip ASCII dari file lokal{RESET}")
        print(f"{YELLOW}2. Unduh gambar dari URL dan jalankan Skrip ASCII{RESET}")
        print(f"{YELLOW}3. Keluar{RESET}")
        
        choice = input(f"{BLUE}Silakan pilih (1/2/3): {RESET}").strip()

        if choice == "1":
            image_to_ascii("Picture/logo.jpg", new_width=100, output_folder="Hasil", output_file="output_ascii.txt")
            print(f"{GREEN}Konversi selesai!{RESET}")
            countdown(5)  # Hitung mundur 5 detik sebelum kembali ke menu
            clear_terminal()  # Clear terminal after processing
        elif choice == "2":
            pilihan_kedua()
        elif choice == "3":
            print(f"{GREEN}Terima kasih telah menggunakan program ini!{RESET}")
            break  # Keluar dari program
        else:
            print(f"{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")

# Menjalankan menu utama
if __name__ == "__main__":
    main_menu()
