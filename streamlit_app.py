import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. INITIALIZATION & DATABASE CONFIGURATION
# ==========================================
st.set_page_config(page_title="PPLP SILE DENDEN", page_icon="🏫", layout="wide")

# Validasi Database Sementara (Session State) agar data tetap aman saat berpindah menu
if "kegiatan_list" not in st.session_state:
    st.session_state.kegiatan_list = [
        {"judul": "Penerimaan Mahasiswa Baru 2025/2026", "tanggal": "08 Sep 2026", "isi": "Pendaftaran resmi dibuka! Silakan hubungi kontak admin.", "kategori": "Pengumuman"}
    ]

if "sertifikat_db" not in st.session_state:
    st.session_state.sertifikat_db = {
        "12345": {"nama": "Muhamad Johan Efendi", "tahun": "2026", "predikat": "Sangat Memuaskan", "program": "Butler"},
        "67890": {"nama": "Suryani", "tahun": "2026", "predikat": "Dengan Pujian", "program": "Cashier"}
    }

if "absensi_siswa" not in st.session_state:
    st.session_state.absensi_siswa = pd.DataFrame(columns=["Tanggal", "Jam Input", "Nama Siswa", "Status", "Keterangan"])

if "absensi_guru" not in st.session_state:
    st.session_state.absensi_guru = pd.DataFrame(columns=["Tanggal", "Jam Input", "Nama Guru", "Status", "Keterangan"])

if "data_kas" not in st.session_state:
    st.session_state.data_kas = pd.DataFrame([
        {"Nama Siswa": "Budi Santoso", "Paket": "Reguler", "Tagihan": 7000000, "Status": "Lunas"},
        {"Nama Siswa": "Siti Rahma", "Paket": "Gold", "Tagihan": 9750000, "Status": "Belum Lunas"},
        {"Nama Siswa": "Lalu Ahmad", "Paket": "Platinum", "Tagihan": 15750000, "Status": "Lunas"},
    ])

if "is_admin_logged_in" not in st.session_state:
    st.session_state.is_admin_logged_in = False

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

# ==========================================
# 2. CUSTOM VISUAL STYLE (CSS SYSTEM)
# ==========================================
st.markdown("""
    <style>
        [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E5E7EB !important; }
        .block-container { padding-top: 0.5rem !important; padding-bottom: 5rem !important; }
        .section-card { background: white; border-radius: 10px; padding: 18px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #E5E7EB; }
        .section-title { color: #1E3A8A; font-size: 16px; font-weight: 800; border-bottom: 2px solid #FBBF24; padding-bottom: 6px; margin-bottom: 12px; }
        
        @keyframes slideLeftRight { 0%, 100% { transform: translateX(-1%); } 50% { transform: translateX(1%); } }
        .welcome-banner { background-color: #FBBF24; color: #1E3A8A; text-align: center; padding: 10px; font-weight: 800; font-size: 13px; border-radius: 6px; margin-bottom: 15px; animation: slideLeftRight 6s infinite ease-in-out; border: 2px solid #1E3A8A; }
        
        .header-lembaga { text-align: center; background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%); color: white; padding: 20px 15px; border-radius: 12px; margin-bottom: 20px; border-bottom: 5px solid #FBBF24; }
        .header-subtitle { font-size: 11px; letter-spacing: 1px; color: #FBBF24; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
        
        .paket-box { border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #FBBF24; }
        .paket-reguler { background-color: #FEF3C7; border-left-color: #D97706; }
        .paket-gold { background-color: #FFFBEB; border-left-color: #F59E0B; }
        .paket-platinum { background-color: #EFF6FF; border-left-color: #2563EB; }
        .paket-title { font-weight: 800; font-size: 14px; margin-bottom: 5px; color: #1F2937; }
        .paket-harga { font-size: 15px; font-weight: 800; color: #1E3A8A; text-align: right; }

        .prog-badge { display: block; background-color: #F3F4F6; color: #1F2937; padding: 8px 12px; margin-bottom: 6px; border-radius: 6px; font-size: 13px; font-weight: 600; border-left: 3px solid #1E3A8A; }
        .sup-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-top: 10px; }
        .sup-item { background: #FFFFFF; border: 1px solid #E5E7EB; border-left: 4px solid #1E3A8A; padding: 12px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; text-align: center; color: #374151; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .aso-badge { display: inline-block; background-color: #EFF6FF; color: #1E40AF; padding: 4px 10px; margin: 3px; border-radius: 4px; font-size: 11px; font-weight: bold; border: 1px solid #BFDBFE; }
        
        .whatsapp-float { position: fixed; bottom: 20px; right: 20px; background-color: #25D366; color: white !important; border-radius: 50px; text-align: center; padding: 12px 20px; font-weight: bold; font-size: 14px; box-shadow: 2px 4px 12px rgba(0,0,0,0.2); z-index: 9999; text-decoration: none; display: flex; align-items: center; gap: 8px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS (KUMPULAN FUNGSI MODUL)
# ==========================================
def render_kotak_staf(key_id, width_px, height_px, label_ukuran):
    """Fungsi pembantu untuk merender kotak bagan organisasi secara konsisten"""
    staf = st.session_state.struktur_data[key_id]
    with st.container(border=True):
        if staf['jabatan']:
            st.markdown(f"<p style='margin:0 0 5px 0; font-size:11px; font-weight:bold; color:#1E3A8A; text-align:center;'>{staf['jabatan']}</p>", unsafe_allow_html=True)
        if staf["foto"] is not None:
            st.image(staf["foto"], use_container_width=True)
        else:
            st.markdown(f'<div style="width:100%; height:{height_px}px; background-color:#E5E7EB; border:2px dashed #9CA3AF; border-radius:4px; display:flex; align-items:center; justify-content:center; color:#6B7280; margin:5px 0;"><span style="font-size:18px;">📷</span><span style="font-size:9px;">({label_ukuran})</span></div>', unsafe_allow_html=True)
        if staf['nama']:
            st.markdown(f"<p style='margin:5px 0 0 0; font-size:12px; font-weight:800; text-align:center; color:#374151;'>{staf['nama']}</p>", unsafe_allow_html=True)
        
        if st.session_state.is_admin_logged_in:
            st.divider()
            with st.popover("⚙️ Kelola Kotak", use_container_width=True):
                input_jabatan = st.text_input("Input Jabatan:", value=staf["jabatan"], key=f"jab_{key_id}")
                input_nama = st.text_input("Input Nama:", value=staf["nama"], key=f"txt_{key_id}")
                input_foto = st.file_uploader("Upload Foto:", type=["png", "jpg", "jpeg"], key=f"file_{key_id}")
                c_b1, c_b2 = st.columns(2)
                if c_b1.button("Simpan 💾", key=f"save_{key_id}", use_container_width=True):
                    st.session_state.struktur_data[key_id]["jabatan"] = input_jabatan
                    st.session_state.struktur_data[key_id]["nama"] = input_nama
                    if input_foto is not None: st.session_state.struktur_data[key_id]["foto"] = input_foto
                    st.rerun()
                if c_b2.button("Hapus 🗑️", key=f"del_{key_id}", use_container_width=True):
                    st.session_state.struktur_data[key_id] = {"jabatan": "", "nama": "", "foto": None}
                    st.rerun()

# ==========================================
# 4. SIDEBAR NAVIGATION SYSTEM
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px 5px; margin-bottom: 20px; border-bottom: 2px solid #F3F4F6;">
            <span style="font-size: 24px;">🏫</span>
            <div style="font-size: 14px; font-weight: 700; color: #1F2937; line-height: 1.2;">PPLP SILEDENDEN<br><span style="font-size: 11px; font-weight: 400; color: #6B7280;">Lombok, NTB</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "MENU UTAMA:",
        ["PROFIL LEMBAGA", "PROGRAM & BIAYA", "SUPPORTED BY", "ABSENSI ELEKTRONIK", "KAS LEMBAGA", "VERIFIKASI SERTIFIKAT"]
    )
    
    st.divider()
    if st.session_state.is_admin_logged_in:
        st.success("🔒 Sesi Admin Aktif")
        if st.button("Logout Sistem Admin"):
            st.session_state.is_admin_logged_in = False
            st.rerun()
    else:
        st.caption("🔓 Mode Akses Publik")

# ==========================================
# 5. PUBLIC CORE MENUS CONTROLLER
# ==========================================

# --- MENU: PROFIL LEMBAGA ---
if menu == "PROFIL LEMBAGA":
    st.markdown('<div class="welcome-banner">✨ PUSAT PENDIDIKAN DAN LATIHAN PARIWISATA SILE DENDEN LOMBOK ✨</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="header-lembaga">
            <div class="header-subtitle">Yayasan Sile Denden Nusantara</div>
            <h2 style='color: #FBBF24; font-size: 22px; font-weight: 900; margin: 0;'>PROFIL & STRUKTUR</h2>
        </div>
    """, unsafe_allow_html=True)
    
    tab_prof1, tab_prof2 = st.tabs(["Profil Lembaga", "Struktur Organisasi"])
    
    with tab_prof1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 Tentang PPLP Sile Denden</div>', unsafe_allow_html=True)
