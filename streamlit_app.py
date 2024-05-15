import streamlit as st
import os
from pathlib import Path

# Konfigurasi direktori utama
BASE_DIR = Path("uploads")
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

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

# Fungsi untuk mengubah nama file
def ubah_nama_file(file_path, new_name):
    try:
        new_file_path = file_path.parent / new_name
        file_path.rename(new_file_path)
        st.success(f"File '{file_path.name}' berhasil diubah namanya menjadi '{new_name}'.")
    except Exception as e:
        st.error(f"Gagal mengubah nama file: {e}")

# Fungsi untuk menghapus file
def hapus_file(file_path):
    try:
        file_path.unlink()
        st.success(f"File '{file_path.name}' berhasil dihapus.")
    except Exception as e:
        st.error(f"Gagal menghapus file: {e}")

# Fungsi untuk menampilkan isi folder
def tampilkan_isi_folder(path):
    items = list(path.iterdir())
    files = [item for item in items if item.is_file()]
    folders = [item for item in items if item.is_dir()]
    
    st.write(f"Isi folder: {path.relative_to(BASE_DIR)}")
    if path != BASE_DIR and st.button("Kembali ke folder utama"):
        st.experimental_set_query_params(path="")
    
    st.write("### Folder")
    for folder in folders:
        if st.button(f"📁 {folder.name}", key=f"folder_{folder.name}"):
            st.experimental_set_query_params(path=str(folder.relative_to(BASE_DIR)))
    
    st.write("### File")
    for file in files:
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        with col1:
            st.write(f"📄 {file.name}")
        with col2:
            new_name = st.text_input(f"Ubah nama: {file.name}", key=f"rename_{file.name}")
            if st.button(f"Ubah Nama", key=f"btn_rename_{file.name}"):
                if new_name:
                    ubah_nama_file(file, new_name)
                else:
                    st.error("Nama file baru tidak boleh kosong.")
        with col3:
            if st.button(f"Hapus", key=f"btn_delete_{file.name}"):
                hapus_file(file)
        with col4:
            with open(file, "rb") as f:
                st.download_button(
                    label="Download",
                    data=f,
                    file_name=file.name,
                    mime="application/octet-stream",
                    key=f"download_{file.name}"
                )
        with col5:
            if file.suffix in [".txt", ".md", ".py", ".csv"]:
                with open(file, "r") as f:
                    content = f.read()
                    if st.button(f"Buka", key=f"open_{file.name}"):
                        st.code(content, language=file.suffix.lstrip("."))

# Aplikasi Streamlit
st.title("Simple Drive with Streamlit")

# Membaca query parameter untuk navigasi folder
query_params = st.experimental_get_query_params()
current_path_str = query_params.get("path", [""])[0]
current_path = BASE_DIR / current_path_str

# Membuat folder baru
st.header("Buat Folder")
folder_name = st.text_input("Nama Folder")
if st.button("Buat Folder"):
    if folder_name:
        buat_folder(current_path / folder_name)
        st.success(f"Folder '{folder_name}' berhasil dibuat.")
    else:
        st.error("Nama folder tidak boleh kosong")

# Mengunggah file baru
st.header("Unggah File")
uploaded_file = st.file_uploader("Pilih File")
if st.button("Unggah File"):
    if uploaded_file:
        tambah_dokumen(current_path_str, uploaded_file)
    else:
        st.error("File harus dipilih")

# Tampilkan isi folder saat ini
tampilkan_isi_folder(current_path)
