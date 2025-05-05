import requests
import tkinter as tk
from tkinter import messagebox

def get_token():
    url = "https://apirsdi.rsu-darulistiqomah.com/auth/GetToken"
    headers = {
        'kode_rs': '3324037',
        'password': 'user'
    }

    try:
        response = requests.get(url, headers=headers)
        result = response.text
        messagebox.showinfo("Response", result)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Gagal terhubung: {e}")

# Buat jendela GUI
window = tk.Tk()
window.title("RSMA Token")
window.geometry("300x150")

# Tombol Get Token
get_button = tk.Button(window, text="Get Token", command=get_token, width=20)
get_button.pack(pady=10)

# Tombol Keluar
exit_button = tk.Button(window, text="Keluar", command=window.quit, width=20)
exit_button.pack(pady=10)

# Jalankan GUI
window.mainloop()
