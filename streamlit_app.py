import streamlit as st
import os
from pathlib import Path
import shutil

# Set Streamlit page configuration
st.set_page_config(
    page_title="In-Cloud"
)

## Konfigurasi direktori utama
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

# Fungsi untuk menghapus folder
def hapus_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        st.success(f"Folder '{folder_path.name}' berhasil dihapus beserta isinya.")
    except Exception as e:
        st.error(f"Gagal menghapus folder: {e}")

# Fungsi untuk mengubah nama folder
def ubah_nama_folder(folder_path, new_name):
    try:
        new_folder_path = folder_path.parent / new_name
        folder_path.rename(new_folder_path)
        st.success(f"Folder '{folder_path.name}' berhasil diubah namanya menjadi '{new_name}'.")
    except Exception as e:
        st.error(f"Gagal mengubah nama folder: {e}")

# Fungsi untuk menghitung ukuran total penyimpanan yang terpakai
def hitung_total_ukuran(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

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
        col1, col2 = st.columns([6, 1])
        with col1:
            if st.button(f"📁 {folder.name}", key=f"folder_{folder.name}"):
                st.experimental_set_query_params(path=str(folder.relative_to(BASE_DIR)))
        with col2:
            menu_options = ["⚙️", "Rename", "Delete"]
            action = st.selectbox("", menu_options, key=f"menu_folder_{folder.name}", label_visibility="collapsed")
            if action == "Rename":
                new_name = st.text_input(f"Ubah nama folder '{folder.name}'", key=f"rename_folder_{folder.name}_input")
                if st.button(f"Ubah Nama", key=f"btn_rename_folder_{folder.name}_confirm"):
                    if new_name:
                        ubah_nama_folder(folder, new_name)
                    else:
                        st.error("Nama folder baru tidak boleh kosong.")
            elif action == "Delete":
                if st.button(f"Hapus Folder", key=f"btn_delete_folder_{folder.name}_confirm"):
                    hapus_folder(folder)

    st.write("### File")
    for file in files:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"📄 {file.name}")
        with col2:
            menu_options = ["⚙️", "Rename", "Delete", "Download", "Open"]
            action = st.selectbox("", menu_options, key=f"menu_file_{file.name}", label_visibility="collapsed")
            if action == "Rename":
                new_name = st.text_input(f"Ubah nama file '{file.name}'", key=f"rename_{file.name}_input")
                if st.button(f"Ubah Nama", key=f"btn_rename_{file.name}_confirm"):
                    if new_name:
                        ubah_nama_file(file, new_name)
                    else:
                        st.error("Nama file baru tidak boleh kosong.")
            elif action == "Delete":
                if st.button(f"Hapus File", key=f"btn_delete_{file.name}_confirm"):
                    hapus_file(file)
            elif action == "Download":
                with open(file, "rb") as f:
                    st.download_button(
                        label="Download",
                        data=f,
                        file_name=file.name,
                        mime="application/octet-stream",
                        key=f"download_{file.name}"
                    )
            elif action == "Open":
                if file.suffix in [".txt", ".md", ".py", ".csv"]:
                    with open(file, "r") as f:
                        content = f.read()
                        st.code(content, language=file.suffix.lstrip("."))
                elif file.suffix in [".jpg", ".jpeg", ".png", ".gif"]:
                    st.image(str(file))
                elif file.suffix in [".pdf"]:
                    with open(file, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    st.warning("File type not supported for direct viewing.")

# Aplikasi Streamlit
st.title("LDK YARSI Storage")

# Membaca query parameter untuk navigasi folder
query_params = st.experimental_get_query_params()
current_path_str = query_params.get("path", [""])[0]
current_path = BASE_DIR / current_path_str

# Menampilkan total ukuran penyimpanan yang terpakai
total_storage_used = hitung_total_ukuran(BASE_DIR)
st.write(f"Total penyimpanan yang terpakai: {total_storage_used / (1024 * 1024):.2f} MB")

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
if uploaded_file and st.button("Unggah File"):
    if uploaded_file.size <= 1 * 1024 * 1024 * 1024:  # Check if file size is less than or equal to 1GB
        tambah_dokumen(current_path_str, uploaded_file)
    else:
        st.error("Ukuran file tidak boleh lebih dari 1GB")

# Tampilkan isi folder saat ini
tampilkan_isi_folder(current_path)
