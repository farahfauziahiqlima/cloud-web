import streamlit as st
import os
from pathlib import Path

# Fungsi untuk membuat folder
def buat_folder(nama_folder):
    try:
        os.makedirs(nama_folder, exist_ok=True)
        st.success(f"Folder '{nama_folder}' berhasil dibuat atau sudah ada.")
    except Exception as e:
        st.error(f"Gagal membuat folder: {e}")

# Fungsi untuk menambahkan dokumen ke dalam folder
def tambah_dokumen(nama_folder, file):
    try:
        folder_path = Path(nama_folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / file.name
        with open(file_path, 'wb') as f:
            f.write(file.getbuffer())
        st.success(f"File '{file.name}' berhasil diunggah ke folder '{nama_folder}'.")
    except Exception as e:
        st.error(f"Gagal menambahkan dokumen: {e}")

# Aplikasi Streamlit
st.title("Simple Drive with Streamlit")

# Membuat folder
st.header("Buat Folder")
nama_folder = st.text_input("Nama Folder")
if st.button("Buat Folder"):
    if nama_folder:
        buat_folder(os.path.join("uploads", nama_folder))
    else:
        st.error("Nama folder tidak boleh kosong")

# Mengunggah file
st.header("Unggah File")
upload_folder = st.text_input("Nama Folder untuk Unggah")
uploaded_file = st.file_uploader("Pilih File")
if st.button("Unggah File"):
    if upload_folder and uploaded_file:
        tambah_dokumen(os.path.join("uploads", upload_folder), uploaded_file)
    else:
        st.error("Nama folder dan file harus diisi")

# Jalankan aplikasi dengan menjalankan perintah berikut di terminal:
# streamlit run app.py
