import streamlit as st
import os
from pathlib import Path

# Konfigurasi direktori utama
BASE_DIR = Path("uploads")

# Membuat folder jika belum ada
def buat_folder(path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

# Fungsi untuk menambahkan dokumen ke dalam folder
def tambah_dokumen(folder, file):
    try:
        folder_path = BASE_DIR / folder
        buat_folder(folder_path)
        file_path = folder_path / file.name
        with open(file_path, 'wb') as f:
            f.write(file.getbuffer())
        st.success(f"File '{file.name}' berhasil diunggah ke folder '{folder}'.")
    except Exception as e:
        st.error(f"Gagal menambahkan dokumen: {e}")

# Fungsi untuk menampilkan isi folder
def tampilkan_isi_folder(path):
    items = list(path.iterdir())
    files = [item for item in items if item.is_file()]
    folders = [item for item in items if item.is_dir()]
    
    st.write(f"Isi folder: {path.relative_to(BASE_DIR)}")
    if st.button("Kembali ke folder utama"):
        st.experimental_set_query_params(path="")
    
    st.write("### Folder")
    for folder in folders:
        if st.button(f"📁 {folder.name}", key=str(folder)):
            st.experimental_set_query_params(path=folder.relative_to(BASE_DIR))
    
    st.write("### File")
    for file in files:
        st.write(f"📄 {file.name}")

# Aplikasi Streamlit
st.title("Simple Drive with Streamlit")

# Membaca query parameter untuk navigasi folder
query_params = st.experimental_get_query_params()
current_path = Path(query_params.get("path", [""])[0])

# Membuat folder baru
st.header("Buat Folder")
folder_name = st.text_input("Nama Folder")
if st.button("Buat Folder"):
    if folder_name:
        buat_folder(BASE_DIR / current_path / folder_name)
        st.success(f"Folder '{folder_name}' berhasil dibuat.")
    else:
        st.error("Nama folder tidak boleh kosong")

# Mengunggah file baru
st.header("Unggah File")
upload_folder = current_path
uploaded_file = st.file_uploader("Pilih File")
if st.button("Unggah File"):
    if uploaded_file:
        tambah_dokumen(upload_folder, uploaded_file)
    else:
        st.error("File harus dipilih")

# Tampilkan isi folder saat ini
tampilkan_isi_folder(BASE_DIR / current_path)
