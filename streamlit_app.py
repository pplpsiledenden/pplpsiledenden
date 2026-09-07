import streamlit as st
import pandas as pd
from datetime import datetime
import io

# ==========================================
# 1. PENGATURAN HALAMAN UTAMA
# ==========================================
st.set_page_config(page_title="Sistem PPLP SILEDENDEN", page_icon="🏫", layout="wide")

# Inisialisasi Penyimpanan Data Sementara (Simulasi Database)
if "kegiatan_list" not in st.session_state:
    st.session_state.kegiatan_list = [{"judul": "Penerimaan Mahasiswa Baru 2025/2026", "tanggal": "08 Sep 2026", "isi": "Pendaftaran resmi dibuka!", "kategori": "Pengumuman"}]

if "sertifikat_db" not in st.session_state:
    # Contoh data awal sertifikat siswa
    st.session_state.sertifikat_db = {
        "12345": {"nama": "Muhamad Johan Efendi", "tahun": "2024", "predikat": "Sangat Memuaskan", "program": "Butler"},
        "67890": {"nama": "Suryani", "tahun": "2025", "predikat": "Dengan Pujian", "program": "Cashier"}
    }

if "absensi_siswa" not in st.session_state:
    st.session_state.absensi_siswa = pd.DataFrame(columns=["Tanggal", "Nama Siswa", "Status"])

if "absensi_guru" not in st.session_state:
    st.session_state.absensi_guru = pd.DataFrame(columns=["Tanggal", "Nama Guru", "Status"])

if "data_kas" not in st.session_state:
    st.session_state.data_kas = pd.DataFrame([
        {"Nama Siswa": "Budi Santoso", "Paket": "Reguler", "Tagihan": 7000000, "Status": "Lunas"},
        {"Nama Siswa": "Siti Rahma", "Paket": "Gold", "Tagihan": 9750000, "Status": "Belum Lunas"},
        {"Nama Siswa": "Lalu Ahmad", "Paket": "Platinum", "Tagihan": 15750000, "Status": "Lunas"},
    ])

# Menu Navigasi Samping
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>PPLP SILEDENDEN LOMBOK</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio(
        "MENU UTAMA:",
        ["Brosur & Berita", "Verifikasi & Unduh Sertifikat", "Sistem Absensi (Siswa & Guru)", "Audit Kas Lembaga (Diagram)", "Panel Admin (Input Data)"]
    )
    st.divider()
    st.caption("Sistem Manajemen Terintegrasi v2.0")

# ==========================================
# 2. MENU: BROSUR & BERITA
# ==========================================
if menu == "Brosur & Berita":
    st.title("🏫 Brosur Digital & Informasi Lembaga")
    st.markdown("<p style='font-style: italic; background-color: #FEF3C7; padding: 10px; border-radius: 5px;'><b>Izin Dinas Pendidikan No:</b> 421.9/563/Disdik</p>", unsafe_allow_html=True)
    
    # Rangkuman Singkat Brosur
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 💼 7 Program Keterampilan")
        st.markdown("1. F&B Product | 2. F&B Service | 3. Front Office | 4. House Keeping | 5. English For Jobs | 6. Tours & Travel | 7. Barista")
    with col2:
        st.write("### 💳 Investasi Pendidikan")
        st.markdown("* **Paket Reguler:** Rp 7.000.000,-\n* **Paket Gold:** Rp 9.750.000,-\n* **Paket Platinum:** Rp 15.750.000,-")
        
    st.divider()
    st.write("### 📰 Papan Informasi & Kegiatan")
    for idx, keg in enumerate(reversed(st.session_state.kegiatan_list)):
        st.info(f"**{keg['judul']}** ({keg['tanggal']}) - *Kategori: {keg['kategori']}*\n\n{keg['isi']}")

# ==========================================
# 3. MENU: VERIFIKASI & UNDUH SERTIFIKAT (PUBLIK)
# ==========================================
elif menu == "Verifikasi & Unduh Sertifikat":
    st.title("🎓 Sistem Verifikasi Sertifikat Kelulusan")
    st.write("Silakan masukkan data kelulusan Anda untuk memverifikasi keaslian dan mengunduh sertifikat digital.")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        search_id = st.text_input("Masukkan Nomor ID Siswa:")
    with col_s2:
        search_nama = st.text_input("Masukkan Nama Lengkap:")
    with col_s3:
        search_tahun = st.text_input("Masukkan Tahun Lulus:")

    if st.button("Cari Sertifikat 🔍"):
        if search_id in st.session_state.sertifikat_db:
            data = st.session_state.sertifikat_db[search_id]
            # Validasi kecocokan Nama dan Tahun Lulus
            if search_nama.lower() in data["nama"].lower() and search_tahun == data["tahun"]:
                st.success("✅ DATA SERTIFIKAT DITEMUKAN & VALID!")
                
                # Menampilkan rincian data
                st.markdown(f"""
                * **Nama Lulusan:** {data['nama']}
                * **Nomor ID:** {search_id}
                * **Program Studi:** {data['program']}
                * **Tahun Kelulusan:** {data['tahun']}
                * **Predikat Kelulusan:** {data['predikat']}
                """)
                
                # --- FITUR GENERATE FILE TEKS (Pondasi Download) ---
                # Menggunakan file Txt/Markdown sederhana sebagai simulasi download instan di HP
                isi_sertifikat = f"SERTIFIKAT KELULUSAN RESMI\nPPLP SILEDENDEN LOMBOK\n\nNama: {data['nama']}\nID: {search_id}\nProgram: {data['program']}\nTahun: {data['tahun']}\nPredikat: {data['predikat']}\n\nValiditas Terverifikasi Sistem Elektronik."
                st.download_button(
                    label="📥 Download Sertifikat Resmi",
                    data=isi_sertifikat,
                    file_name=f"Sertifikat_{data['nama']}.txt",
                    mime="text/plain"
                )
            else:
                st.error("❌ Data nama atau tahun lulus tidak cocok dengan Nomor ID.")
        else:
            st.error("❌ Nomor ID Siswa tidak terdaftar di sistem kami.")

# ==========================================
# 4. MENU: SISTEM ABSENSI (OTOMATIS AUDIT)
# ==========================================
elif menu == "Sistem Absensi (Siswa & Guru)":
    st.title("📅 Presensi Elektronik & Audit Kehadiran Otomatis")
    
    tab1, tab2 = st.tabs(["Absensi Siswa", "Absensi Guru"])
    
    with tab1:
        st.subheader("Formulir Absen Siswa Harian")
        with st.form("form_absen_siswa"):
            nama_s = st.text_input("Nama Siswa:")
            status_s = st.radio("Status Kehadiran:", ["Hadir", "Izin", "Sakit", "Alpa"], horizontal=True)
            btn_s = st.form_submit_button("Simpan Absen Siswa")
            if btn_s and nama_s:
                new_row = {"Tanggal": datetime.now().strftime("%d-%m-%Y"), "Nama Siswa": nama_s, "Status": status_s}
                st.session_state.absensi_siswa = pd.concat([st.session_state.absensi_siswa, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Absen {nama_s} berhasil dicatat!")

        st.write("#### 📊 Audit Otomatis Kehadiran Siswa")
        if not st.session_state.absensi_siswa.empty:
            st.dataframe(st.session_state.absensi_siswa, use_container_width=True)
            # Hitung Otomatis Jumlah
            audit_s = st.session_state.absensi_siswa["Status"].value_counts()
            st.write(f"**Total Audit:** Hadir: {audit_s.get('Hadir', 0)} | Izin: {audit_s.get('Izin', 0)} | Sakit: {audit_s.get('Sakit', 0)} | Alpa: {audit_s.get('Alpa', 0)}")
        else:
            st.info("Belum ada data absensi hari ini.")

    with tab2:
        st.subheader("Formulir Absen Guru / Instruktur")
        with st.form("form_absen_guru"):
            nama_g = st.text_input("Nama Guru:")
            status_g = st.radio("Status:", ["Hadir", "Izin", "Alpa"], horizontal=True, key="absen_g")
            btn_g = st.form_submit_button("Simpan Absen Guru")
            if btn_g and nama_g:
                new_row_g = {"Tanggal": datetime.now().strftime("%d-%m-%Y"), "Nama Guru": nama_g, "Status": status_g}
                st.session_state.absensi_guru = pd.concat([st.session_state.absensi_guru, pd.DataFrame([new_row_g])], ignore_index=True)
                st.success(f"Absen Guru {nama_g} berhasil dicatat!")

        st.write("#### 📊 Audit Otomatis Kehadiran Guru")
        if not st.session_state.absensi_guru.empty:
            st.dataframe(st.session_state.absensi_guru, use_container_width=True)
            audit_g = st.session_state.absensi_guru["Status"].value_counts()
            st.write(f"**Total Audit Guru:** Hadir: {audit_g.get('Hadir', 0)} | Izin: {audit_g.get('Izin', 0)} | Alpa: {audit_g.get('Alpa', 0)}")
        else:
            st.info("Belum ada data absensi guru hari ini.")

# ==========================================
# 5. MENU: AUDIT KAS LEMBAGA (DIAGRAM LINGKARAN)
# ==========================================
elif menu == "Audit Kas Lembaga (Diagram)":
    st.title("📈 Laporan Keuangan & Keuangan Kas Pembayaran Siswa")
    st.write("Audit otomatis status pelunasan biaya pendidikan siswa berdasarkan data kas masuk.")
    
    st.dataframe(st.session_state.data_kas, use_container_width=True)
    
    # Hitung Jumlah Lunas dan Belum Lunas
    hitung_status = st.session_state.data_kas["Status"].value_counts()
    lunas = hitung_status.get("Lunas", 0)
    belum_lunas = hitung_status.get("Belum Lunas", 0)
    
    st.divider()
    st.write("### 📊 Audit Diagram Lingkaran Status Pembayaran")
    
    # Membuat diagram lingkaran menggunakan komponen bawaan Streamlit (Chart Bar/Area karena kesederhanaan HP, atau pie menggunakan Dataframe)
    chart_data = pd.DataFrame({
        "Status Pembayaran": ["Lunas", "Belum Lunas"],
        "Jumlah Siswa": [lunas, belum_lunas]
    })
    
    # Tampilan visual ringkasan kas keuangan
    c1, c2 = st.columns(2)
    with c1:
        st.write("#### Grafik Batang Distribusi Pelunasan Kas:")
        st.bar_chart(chart_data.set_index("Status Pembayaran"))
    with c2:
        st.write("#### 🧮 Ringkasan Nominal Audit Anggaran:")
        total_lunas_idr = st.session_state.data_kas[st.session_state.data_kas["Status"] == "Lunas"]["Tagihan"].sum()
        total_belum_idr = st.session_state.data_kas[st.session_state.data_kas["Status"] == "Belum Lunas"]["Tagihan"].sum()
        
        st.metric("Total Dana Kas Masuk (Lunas)", f"Rp {total_lunas_idr:,}")
        st.metric("Total Piutang Anggaran (Belum Lunas)", f"Rp {total_belum_idr:,}")

# ==========================================
# 6. MENU: PANEL ADMIN INPUT DATA
