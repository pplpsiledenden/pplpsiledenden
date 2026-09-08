import streamlit as st
import pandas as pd

# ==========================================
# 1. SETUP HALAMAN & DATABASE LOKAL
# ==========================================
st.set_page_config(page_title="PPLP SILE DENDEN LOMBOK", page_icon="🏫", layout="wide")

if "struktur_data" not in st.session_state:
    st.session_state.struktur_data = {
        "top": {"jabatan": "DIREKTUR", "nama": "Belum Diisi", "foto": None},
        "mid_1": {"jabatan": "WAKIL DIREKTUR I", "nama": "Belum Diisi", "foto": None},
        "mid_2": {"jabatan": "WAKIL DIREKTUR II", "nama": "Belum Diisi", "foto": None},
        "bot_1": {"jabatan": "STAF F&B PRODUCT", "nama": "Belum Diisi", "foto": None},
        "bot_2": {"jabatan": "STAF F&B SERVICE", "nama": "Belum Diisi", "foto": None},
        "bot_3": {"jabatan": "STAF FRONT OFFICE", "nama": "Belum Diisi", "foto": None},
        "bot_4": {"jabatan": "STAF ADMIN / BKK", "nama": "Belum Diisi", "foto": None},
    }

kolom_absen = ["No. ID", "Nama"] + [str(i) for i in range(1, 32)] + ["Hadir", "Tidak Hadir"]
if "absensi_guru" not in st.session_state: st.session_state.absensi_guru = pd.DataFrame(columns=kolom_absen)
if "absensi_siswa" not in st.session_state: st.session_state.absensi_siswa = pd.DataFrame(columns=kolom_absen)

if "kas_sheet1_siswa" not in st.session_state:
    st.session_state.kas_sheet1_siswa = pd.DataFrame([
        {"No. ID": "001", "Nama Siswa": "Contoh Nama Siswa 1", "Status Kelulusan": "Aktif Belajar", "Sisa Utang (Rp)": 5000000}
    ])
if "kas_sheet2_jurnal" not in st.session_state:
    st.session_state.kas_sheet2_jurnal = pd.DataFrame([
        {"Tanggal": "2026-09-08", "Keterangan": "Saldo Awal Kas", "Uang Masuk (Rp)": 10000000, "Uang Keluar (Rp)": 0}
    ])

if "is_admin_logged_in" not in st.session_state: st.session_state.is_admin_logged_in = False

# ==========================================
# 2. SISTEM VISUAL CSS STYLE
# ==========================================
st.markdown('<style>[data-testid="stSidebar"] { background-color: #F8FAFC !important; border-right: 1px solid #E2E8F0 !important; } .header-lembaga { text-align: center; background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%); color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-bottom: 4px solid #FBBF24; } .section-card { background: #FFFFFF; border-radius: 8px; padding: 15px; margin-bottom: 15px; border-left: 4px solid #1E3A8A; box-shadow: 0 1px 3px rgba(0,0,0,0.1); } .section-title-custom { color: #1E3A8A; font-size: 15px; font-weight: bold; margin-bottom: 8px; text-transform: uppercase; border-bottom: 1px solid #E2E8F0; padding-bottom: 4px; } .box-bagan-vertikal { background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px; } .box-bagan-vertikal.node-direktur { border-top: 4px solid #EF4444; } .box-bagan-vertikal.node-wadir { border-top: 4px solid #F59E0B; } .box-bagan-vertikal.node-staf { border-top: 4px solid #10B981; } .text-jabatan { font-size: 10px; font-weight: bold; color: #64748B; margin: 0; text-transform: uppercase; } .text-nama { font-size: 13px; font-weight: 800; color: #1E293B; margin: 4px 0 0 0; } .placeholder-foto { width: 100px; height: 120px; background-color: #E2E8F0; border: 2px dashed #94A3B8; border-radius: 6px; margin: 8px auto; display: flex; align-items: center; justify-content: center; color: #64748B; font-size: 10px; } .jurusan-item { background: #F1F5F9; padding: 8px 12px; margin-bottom: 6px; border-radius: 4px; font-size: 13px; font-weight: bold; color: #1E3A8A; border-left: 3px solid #3B82F6; } .paket-box { border-radius: 8px; padding: 12px; margin-bottom: 15px; border-left: 5px solid #FBBF24; box-shadow: 0 1px 3px rgba(0,0,0,0.05); } .paket-reguler { background-color: #FEF3C7; border-left-color: #D97706; } .paket-gold { background-color: #FFFBEB; border-left-color: #F59E0B; } .paket-platinum { background-color: #EFF6FF; border-left-color: #2563EB; } .paket-title { font-weight: 800; font-size: 14px; color: #1F2937; text-transform: uppercase; } .paket-harga { font-size: 15px; font-weight: 800; color: #1E3A8A; margin-top: 5px; } .sup-item { background: #FFFFFF; border: 1px solid #E2E8F0; padding: 8px; border-radius: 4px; font-size: 11px; font-weight: bold; text-align: center; color: #475569; box-shadow: 0 1px 2px rgba(0,0,0,0.02); } .whatsapp-float { position: fixed; bottom: 15px; right: 15px; background-color: #25D366; color: white !important; border-radius: 30px; padding: 8px 14px; font-weight: bold; font-size: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); z-index: 9999; text-decoration: none; display: flex; align-items: center; gap: 5px; }</style>', unsafe_allow_html=True)

def render_kotak_vertikal(key_id, class_node="node-staf", label_def="STAF"):
    staf = st.session_state.struktur_data[key_id]
    st.markdown(f'<div class="box-bagan-vertikal {class_node}"><p class="text-jabatan">{staf["jabatan"] if staf["jabatan"] else label_def}</p><div class="placeholder-foto">📷<br>(Upload Foto)</div><p class="text-nama">{staf["nama"] if staf["nama"] else "Belum Diisi"}</p></div>', unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR NAVIGATION SYSTEM
# ==========================================
with st.sidebar:
    st.markdown('<div style="text-align:center; padding:10px 0;"><span style="font-size:35px;">🏫</span><h4 style="color:#1E3A8A; margin:5px 0 0 0; font-weight:800; font-size:15px;">PPLP SILE DENDEN</h4></div>', unsafe_allow_html=True)
    st.divider()
    menu = st.radio("PILIH HALAMAN:", ["INFORMASI UTAMA (BROSUR)", "ABSENSI GURU & SISWA", "REKAP KAS LEMBAGA"])
    st.divider()
    st.markdown("**🔐 Login Admin**")
    if not st.session_state.is_admin_logged_in:
        u_adm = st.text_input("User:", key="u_adm")
        p_adm = st.text_input("Pass:", type="password", key="p_adm")
        if st.button("Masuk 🚀", use_container_width=True):
            if u_adm == "admin" and p_adm == "12345":
                st.session_state.is_admin_logged_in = True
                st.rerun()
            else: st.error("Salah!")
    else:
        st.success("Admin Aktif")
        if st.button("Keluar 🚪", use_container_width=True):
            st.session_state.is_admin_logged_in = False
            st.rerun()

# ==========================================
# 4. KONTEN UTAMA ROUTER
# ==========================================
st.markdown('<div class="header-lembaga"><h2 style="margin:0; color:white; font-size:20px; font-weight:800;">SILE DENDEN LOMBOK</h2></div>', unsafe_allow_html=True)

if menu == "INFORMASI UTAMA (BROSUR)":
    # BAGIAN 1: PROFIL LEMBAGA
    with st.container(border=True):
        st.markdown('<div class="section-title-custom">Tentang PPLP Sile Denden Lombok</div>', unsafe_allow_html=True)
        st.write("Persaingan kerja global dan jejak digital sistem yang semakin canggih sangat dibutuhkan Sumber Daya Manusia (SDM) yang handal, siap pakai dan berdaya saing. PPLP Sile Denden dengan Visi & Misi Membantu Pemerintah yaitu mencerdaskan kehidupan bangsa Indonesia untuk mendapatkan pekerjaan yang layak.")
        st.markdown('<div class="section-title-custom" style="margin-top:15px;">🎯 Visi & Misi</div>', unsafe_allow_html=True)
        st.write("Membantu program Pemerintah dalam menyerap dan mencerdaskan kehidupan bangsa, mengurangi angka pengangguran, serta menyiapkan tenaga kerja terampil, profesional, berdedikasi tinggi, berakhlak mulia di bidang industri perhotelan dan pariwisata baik skala nasional maupun internasional.")
    
    # BAGIAN 2: JURUSAN
    st.markdown('<div class="section-card"><div class="section-title-custom">7 Program Keterampilan Pilihan (Jurusan)</div>', unsafe_allow_html=True)
    for j in ["1. F&B Product / Tata Boga", "2. F&B Service / Restaurant & Bar", "3. Front Office", "4. House Keeping / Tata Graha", "5. English For Jobs", "6. Tours & Travel / Guide", "7. Barista"]:
        st.markdown(f'<div class="jurusan-item">{j}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # BAGIAN 3: SYARAT PENDAFTARAN
    with st.container(border=True):
        st.markdown('<div class="section-title-custom">📋 Ketentuan & Syarat Pendaftaran</div>', unsafe_allow_html=True)
        for s in ["1. Mengisi Formulir Pendaftaran Resmi", "2. Menyerahkan Salinan STTB / Ijazah Terakhir SLTA/SMK/Sederajat (2 Lembar)", "3. Menyerahkan Pas Photo Berwarna Ukuran 3x4 (5 Lembar)", "4. Membayar Biaya Uang Pendaftaran Awal Sebesar Rp. 200.000,-", "5. Membayar Biaya Daftar Ulang Sebesar Rp. 2.000.000,-", "6. Menyerahkan Photo Copy KTP dan Kartu Keluarga (KK)", "7. Menyerahkan Materai 10.000 (1 Lembar)"]:
            st.write(s)
        st.markdown('---')
        st.markdown('**🎁 Biaya Pendaftaran Sudah Termasuk:**')
        st.write("- Kursus Bahasa Inggris, Pakaian Seragam Lengkap, ID Card, Kartu BKK, Sertifikat Akademik, Sertifikat Table Manner & Uji Kompetensi dari Hotel Berbintang")
    
    # BAGIAN 4: BIAYA & PAKET PROGRAM
    with st.container(border=True):
        st.markdown('<div class="section-card"><div class="section-title-custom">💰 Informasi Rincian Biaya Pendidikan (Bisa Diangsur)</div></div>', unsafe_allow_html=True)
    col_bx1, col_bx2, col_bx3 = st.columns(3)
    with col_bx1: st.markdown('<div class="paket-box paket-reguler"><div class="paket-title">Paket Reguler</div><ul style="font-size:11px; color:#475569; padding-left:12px;"><li>Seragam Sekolah</li><li>Table Manner di Hotel</li><li>Praktek 5 Kompetensi</li></ul><div class="paket-harga">Rp. 7.000.000,-</div></div>', unsafe_allow_html=True)
