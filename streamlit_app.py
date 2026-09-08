import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. SETUP HALAMAN & DATABASE LOKAL
# ==========================================
st.set_page_config(page_title="PPLP SILE DENDEN LOMBOK", page_icon="🏫", layout="wide")

# Database Sementara untuk Struktur Organisasi (Model Vertikal memanjang ke atas)
if "struktur_data" not in st.session_state:
    st.session_state.struktur_data = {
        "top": {"jabatan": "", "nama": "", "foto": None},
        "mid_1": {"jabatan": "", "nama": "", "foto": None},
        "mid_2": {"jabatan": "", "nama": "", "foto": None},
        "bot_1": {"jabatan": "", "nama": "", "foto": None},
        "bot_2": {"jabatan": "", "nama": "", "foto": None},
        "bot_3": {"jabatan": "", "nama": "", "foto": None},
        "bot_4": {"jabatan": "", "nama": "", "foto": None},
    }

# Mock Database Absensi Sementara (Format Kolom sesuai Sheets: ID, Nama, Tgl 1-31, Total)
kolom_absen = ["No. ID", "Nama"] + [str(i) for i in range(1, 32)] + ["Hadir", "Tidak Hadir"]
if "absensi_guru" not in st.session_state:
    st.session_state.absensi_guru = pd.DataFrame(columns=kolom_absen)
if "absensi_siswa" not in st.session_state:
    st.session_state.absensi_siswa = pd.DataFrame(columns=kolom_absen)

# Mock Database Kas Sementara (Dua Tab/Sheet Berbeda)
if "kas_sheet1_siswa" not in st.session_state:
    st.session_state.kas_sheet1_siswa = pd.DataFrame([
        {"No. ID": "001", "Nama Siswa": "Contoh Nama Siswa 1", "Status Kelulusan": "Aktif Belajar", "Sisa Utang (Rp)": 5000000}
    ])
if "kas_sheet2_jurnal" not in st.session_state:
    st.session_state.kas_sheet2_jurnal = pd.DataFrame([
        {"Tanggal": "2026-09-08", "Keterangan": "Saldo Awal Kas", "Uang Masuk (Rp)": 10000000, "Uang Keluar (Rp)": 0}
    ])

if "is_admin_logged_in" not in st.session_state:
    st.session_state.is_admin_logged_in = False

# ==========================================
# 2. SISTEM VISUAL (CSS TEMA BROSUR & HP)
# ==========================================
st.markdown("""
    <style>
        [data-testid="stSidebar"] { background-color: #F8FAFC !important; border-right: 1px solid #E2E8F0 !important; }
        .header-lembaga { text-align: center; background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%); color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-bottom: 4px solid #FBBF24; }
        .header-subtitle { font-size: 11px; letter-spacing: 1px; color: #FBBF24; font-weight: bold; text-transform: uppercase; }
        
        .section-card { background: #FFFFFF; border-radius: 8px; padding: 15px; margin-bottom: 15px; border-left: 4px solid #1E3A8A; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .section-title-custom { color: #1E3A8A; font-size: 15px; font-weight: bold; margin-bottom: 8px; text-transform: uppercase; border-bottom: 1px solid #E2E8F0; padding-bottom: 4px; }
        
        /* Desain Bagan Organisasi Vertikal Memanjang ke Atas */
        .box-bagan-vertikal { background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px; }
        .box-bagan-vertikal.node-direktur { border-top: 4px solid #EF4444; }
        .box-bagan-vertikal.node-wadir { border-top: 4px solid #F59E0B; }
        .box-bagan-vertikal.node-staf { border-top: 4px solid #10B981; }
        .text-jabatan { font-size: 10px; font-weight: bold; color: #64748B; margin: 0; text-transform: uppercase; }
        .text-nama { font-size: 13px; font-weight: 800; color: #1E293B; margin: 4px 0 0 0; }
        .placeholder-foto { width: 100px; height: 120px; background-color: #E2E8F0; border: 2px dashed #94A3B8; border-radius: 6px; margin: 8px auto; display: flex; align-items: center; justify-content: center; color: #64748B; font-size: 10px; }
        
        .jurusan-item { background: #F1F5F9; padding: 8px 12px; margin-bottom: 6px; border-radius: 4px; font-size: 13px; font-weight: bold; color: #1E3A8A; border-left: 3px solid #3B82F6; }
        .paket-box { border-radius: 8px; padding: 12px; margin-bottom: 15px; border-left: 5px solid #FBBF24; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .paket-reguler { background-color: #FEF3C7; border-left-color: #D97706; }
        .paket-gold { background-color: #FFFBEB; border-left-color: #F59E0B; }
        .paket-platinum { background-color: #EFF6FF; border-left-color: #2563EB; }
        .paket-title { font-weight: 800; font-size: 14px; color: #1F2937; text-transform: uppercase; }
        .paket-harga { font-size: 15px; font-weight: 800; color: #1E3A8A; margin-top: 5px; }
        
        .sup-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 6px; }
        .sup-item { background: #FFFFFF; border: 1px solid #E2E8F0; padding: 8px; border-radius: 4px; font-size: 11px; font-weight: bold; text-align: center; color: #475569; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
        .whatsapp-float { position: fixed; bottom: 15px; right: 15px; background-color: #25D366; color: white !important; border-radius: 30px; padding: 8px 14px; font-weight: bold; font-size: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); z-index: 9999; text-decoration: none; display: flex; align-items: center; gap: 5px; }
    </style>
""", unsafe_allow_html=True)

# Fungsi Pembantu Render Kotak Vertikal Struktur Organisasi
def render_kotak_vertikal(key_id, class_node="node-staf", label_def="STAF"):
    staf = st.session_state.struktur_data[key_id]
    with st.container():
        st.markdown(f'<div class="box-bagan-vertikal {class_node}">', unsafe_allow_html=True)
        st.markdown(f'<p class="text-jabatan">{staf["jabatan"] if staf["jabatan"] else label_def}</p>', unsafe_allow_html=True)
        
        if staf["foto"] is not None:
            st.image(staf["foto"], width=120)
        else:
            st.markdown('<div class="placeholder-foto">📷<br>(Upload Foto)</div>', unsafe_allow_html=True)
            
        st.markdown(f'<p class="text-nama">{staf["nama"] if staf["nama"] else "Belum Diisi"}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.is_admin_logged_in:
            with st.popover("⚙️ Edit Kotak", use_container_width=True, key=f"pop_{key_id}"):
                st.session_state.struktur_data[key_id]["jabatan"] = st.text_input("Jabatan:", value=staf["jabatan"], key=f"jab_{key_id}")
                st.session_state.struktur_data[key_id]["nama"] = st.text_input("Nama:", value=staf["nama"], key=f"nam_{key_id}")
                f_upload = st.file_uploader("Upload Foto:", type=["jpg","jpeg","png"], key=f"f_{key_id}")
                if f_upload: st.session_state.struktur_data[key_id]["foto"] = f_upload.read()
                if st.button("Simpan Data 💾", key=f"btn_{key_id}", use_container_width=True): st.rerun()

# ==========================================
# 3. SIDEBAR NAVIGATION SYSTEM (NESTED)
# ==========================================
with st.sidebar:
    st.markdown('<div style="text-align:center; padding:10px 0;"><span style="font-size:35px;">🏫</span><h4 style="color:#1E3A8A; margin:5px 0 0 0; font-weight:800; font-size:15px;">PPLP SILE DENDEN</h4></div>', unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio(
        "MENU NAVIGASI:",
        ["1. PROFIL", "2. PROGRAM LEMBAGA", "3. SUPPORTED BY", "4. ABSENSI", "5. KAS LEMBAGA"]
    )
    
    # Sub-Menu Router Dinamis berbasis pilihan Menu Utama Anda
    sub_menu = None
    if menu == "1. PROFIL":
        st.markdown("---")
        sub_menu = st.radio("PILIH SUB-MENU PROFIL:", ["Sub-Fitur A: Profil Lembaga", "Sub-Fitur B: Struktur Organisasi"])
    elif menu == "2. PROGRAM LEMBAGA":
        st.markdown("---")
        sub_menu = st.radio("PILIH SUB-MENU PROGRAM:", ["Sub-Fitur A: Jurusan", "Sub-Fitur B: Syarat Pendaftaran", "Sub-Fitur C: Biaya Pendidikan"])
    elif menu == "4. ABSENSI":
        st.markdown("---")
        sub_menu = st.radio("PILIH SUB-MENU ABSENSI:", ["Sub-Fitur A: Absensi Guru", "Sub-Fitur B: Absensi Siswa"])
        
    st.divider()
    st.markdown("**🔐 Ruang Panel Admin**")
    if not st.session_state.is_admin_logged_in:
        u_adm = st.text_input("Username:", key="u_adm")
        p_adm = st.text_input("Password:", type="password", key="p_adm")
        if st.button("Masuk Admin 🚀", use_container_width=True):
            if u_adm == "admin" and p_adm == "12345":
                st.session_state.is_admin_logged_in = True
                st.rerun()
            else: st.error("Salah!")
    else:
        st.success("Mode Pengeditan Admin Aktif")
        if st.button("Keluar Admin 🚪", use_container_width=True):
            st.session_state.is_admin_logged_in = False
            st.rerun()

# ==========================================
# 4. KONTEN UTAMA ROUTER
# ==========================================
st.markdown('<div class="header-lembaga"><div class="header-subtitle">PUSAT PENDIDIKAN & LATIHAN PARIWISATA</div><h2 style="margin:5px 0 0 0; color:white; font-size:20px; font-weight:800;">SILE DENDEN LOMBOK</h2></div>', unsafe_allow_html=True)

# ------------------------------------------
# 1. MENU PROFIL
# ------------------------------------------
if menu == "1. PROFIL":
    if sub_menu == "Sub-Fitur A: Profil Lembaga":
        st.markdown("""
        <div class="section-card">
            <div class="section-title-custom">Tentang PPLP Sile Denden Lombok</div>
            <p style="font-size:12px; color:#334155; line-height:1.6; text-align:justify; margin:0 0 15px 0;">
                Persaingan kerja global dan jejak digital sistem yang semakin canggih sangat dibutuhkan Sumber Daya Manusia (SDM) yang handal, siap pakai dan berdaya saing. 
                PPLP Sile Denden dengan Visi & Misi Membantu Pemerintah yaitu mencerdaskan kehidupan bangsa Indonesia untuk mendapatkan pekerjaan yang layak. 
            </p>
