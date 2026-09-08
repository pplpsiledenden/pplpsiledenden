import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. INITIALIZATION & DATABASE CONFIGURATION
# ==========================================
st.set_page_config(page_title="PPLP SILE DENDEN", page_icon="🏫", layout="wide")

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
        "top": {"jabatan": "Direktur", "nama": "Nama Direktur", "foto": None},
        "mid_1": {"jabatan": "Wadir I", "nama": "Nama Wadir I", "foto": None},
        "mid_2": {"jabatan": "Wadir II", "nama": "Nama Wadir II", "foto": None},
        "bot_1": {"jabatan": "Staf 1", "nama": "Nama Staf 1", "foto": None},
        "bot_2": {"jabatan": "Staf 2", "nama": "Nama Staf 2", "foto": None},
        "bot_3": {"jabatan": "Staf 3", "nama": "Nama Staf 3", "foto": None},
        "bot_4": {"jabatan": "Staf 4", "nama": "Nama Staf 4", "foto": None},
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
        .welcome-banner { background-color: #FBBF24; color: #1E3A8A; text-align: center; padding: 10px; font-weight: 800; font-size: 13px; border-radius: 6px; margin-bottom: 15px; border: 2px solid #1E3A8A; }
        .header-lembaga { text-align: center; background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%); color: white; padding: 20px 15px; border-radius: 12px; margin-bottom: 20px; border-bottom: 5px solid #FBBF24; }
        .header-subtitle { font-size: 11px; letter-spacing: 1px; color: #FBBF24; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
        .paket-box { border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #FBBF24; }
        .paket-reguler { background-color: #FEF3C7; border-left-color: #D97706; }
        .paket-gold { background-color: #FFFBEB; border-left-color: #F59E0B; }
        .paket-platinum { background-color: #EFF6FF; border-left-color: #2563EB; }
        .paket-title { font-weight: 800; font-size: 14px; margin-bottom: 5px; color: #1F2937; }
        .paket-harga { font-size: 15px; font-weight: 800; color: #1E3A8A; text-align: right; }
        .whatsapp-float { position: fixed; bottom: 20px; right: 20px; background-color: #25D366; color: white !important; border-radius: 50px; text-align: center; padding: 12px 20px; font-weight: bold; font-size: 14px; box-shadow: 2px 4px 12px rgba(0,0,0,0.2); z-index: 9999; text-decoration: none; display: flex; align-items: center; gap: 8px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def render_kotak_staf(key_id, width_px, height_px, label_ukuran):
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
            with st.popover("⚙️ Kelola Kotak", use_container_width=True, key=f"pop_{key_id}"):
                input_jabatan = st.text_input("Input Jabatan:", value=staf["jabatan"], key=f"jab_{key_id}")
                input_nama = st.text_input("Input Nama:", value=staf["nama"], key=f"txt_{key_id}")
                input_foto = st.file_uploader("Upload Foto:", type=["png", "jpg", "jpeg"], key=f"file_{key_id}")
                c_b1, c_b2 = st.columns(2)
                if c_b1.button("Simpan 💾", key=f"save_{key_id}", use_container_width=True):
                    st.session_state.struktur_data[key_id]["jabatan"] = input_jabatan
                    st.session_state.struktur_data[key_id]["nama"] = input_nama
                    if input_foto is not None: 
                        st.session_state.struktur_data[key_id]["foto"] = input_foto.read()
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
            <span style="font-weight: 800; color: #1E3A8A; font-size: 16px;">PPLP SILE DENDEN</span>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Pilih Menu Layanan:",
        ["🏠 Beranda", "👥 Struktur Organisasi", "📝 Absensi", "💰 Cek Kas/Tagihan", "🎓 Verifikasi Sertifikat"]
    )
    
    st.divider()
    
    st.markdown("**🔐 Ruang Admin**")
    if not st.session_state.is_admin_logged_in:
        username = st.text_input("Username:", key="admin_user")
        password = st.text_input("Password:", type="password", key="admin_pass")
        if st.button("Masuk 🚀", use_container_width=True):
            if username == "admin" and password == "12345":
                st.session_state.is_admin_logged_in = True
                st.success("Login Berhasil!")
                st.rerun()
            else:
                st.error("Kredensial Salah!")
    else:
        st.write("Anda masuk sebagai **Admin**")
        if st.button("Keluar Logout 🚪", use_container_width=True):
            st.session_state.is_admin_logged_in = False
            st.rerun()

# ==========================================
# 5. MAIN CONTENT ROUTER
# ==========================================
st.markdown('<div class="welcome-banner">Selamat Datang di Sistem Informasi PPLP SILE DENDEN</div>', unsafe_allow_html=True)

if menu == "🏠 Beranda":
    st.markdown('<div class="header-lembaga"><div class="header-subtitle">Pusat Pelatihan Kerja</div><h1>PPLP SILE DENDEN</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📢 Pengumuman & Kegiatan Terbaru")
        for keg in st.session_state.kegiatan_list:
            with st.chat_message("user", avatar="🔔"):
                st.markdown(f"**{keg['judul']}** ({keg['tanggal']})")
                st.caption(f"Kategori: {keg['kategori']}")
                st.write(keg['isi'])
    with col2:
        st.subheader("💼 Paket Program")
        st.markdown('<div class="paket-box paket-reguler"><div class="paket-title">Reguler</div><div class="paket-harga">Rp 7.000.000</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="paket-box paket-gold"><div class="paket-title">Gold</div><div class="paket-harga">Rp 9.750.000</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="paket-box paket-platinum"><div class="paket-title">Platinum</div><div class="paket-harga">Rp 15.750.000</div></div>', unsafe_allow_html=True)

elif menu == "👥 Struktur Organisasi":
    st.subheader("Bagan Struktur Organisasi PPLP")
    c_top1, c_top2, c_top3 = st.columns(3)
    with c_top2: render_kotak_staf("top", 200, 150, "Direktur")
    st.write("") 
    c_mid1, c_mid2 = st.columns(2)
