import requests
import json
import tkinter as tk
from tkinter import messagebox

def log(text):
    output_text.config(state='normal')
    output_text.insert(tk.END, text + "\n")
    output_text.config(state='disabled')
    output_text.see(tk.END)

def simpan_token_ke_file(token):
    try:
        with open("token.txt", "w") as f:
            f.write(token)
        log("📁 Token disimpan ke 'token.txt'")
    except Exception as e:
        log(f"❌ Gagal menyimpan token: {e}")

def proses_otomatis():
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)  # Kosongkan log
    output_text.config(state='disabled')

    url_token = "http://localhost/rsma/auth/GetToken"
    headers_token = {
        'kode_rs': '3324037',
        'password': 'user'
    }

    try:
        log("🔄 Mengambil token...")
        response_token = requests.get(url_token, headers=headers_token)

        # Ambil rsma_token dari response JSON
        data_token = response_token.json()
        token = data_token.get("rsma_token", "").strip()

        if not token:
            log("❌ Gagal mendapatkan token dari rsma_token")
            return

        log(f"✅ Token diterima:\n{token}")
        simpan_token_ke_file(token)

        url_kamar = "http://localhost/rsma/kamar/update"
        payload = json.dumps([
            {"koderuang": "I042", "namaruang": "ABU BAKAR 7", "kapasitas": 9},
            {"koderuang": "I04", "namaruang": "ABU BAKAR 6 TEST", "kapasitas": 8},
            {"koderuang": "", "namaruang": "Salah Format", "kapasitas": -2}
        ])
        headers_kamar = {
            'kode_rs': '3324037',
            'password': 'user',
            'token_rsma': token,
            'Content-Type': 'application/json'
        }

        log("📤 Mengirim data kamar...")
        response_kamar = requests.post(url_kamar, headers=headers_kamar, data=payload)
        log(f"✅ Respons dari server:\n{response_kamar.text}")

    except requests.exceptions.RequestException as e:
        log(f"❌ Terjadi error:\n{e}")

# GUI setup
window = tk.Tk()
window.title("Kirim Data Kamar Otomatis")
window.geometry("500x400")

tk.Button(window, text="Proses (Get Token + Kirim Kamar)", command=proses_otomatis, width=40).pack(pady=10)
tk.Button(window, text="Keluar", command=window.quit, width=40).pack(pady=5)

# Kotak log
output_text = tk.Text(window, height=15, state='disabled', bg="#f0f0f0")
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

window.mainloop()
