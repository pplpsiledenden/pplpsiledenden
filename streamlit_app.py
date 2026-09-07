import streamlit as st

st.set_page_config(
    page_title="Hotel Academy",
    page_icon="🏨",
    layout="centered"
)

st.title("🏨 Hotel Academy")
st.subheader("Level Up Skill Perhotelan Kamu dengan Cara Modern! ✨")

menu = st.selectbox("Pilih Menu:", ["🏠 Beranda", "📚 Materi Pelatihan", "📝 Cek Sertifikat"])

if menu == "🏠 Beranda":
    st.write("Selamat datang di platform pelatihan perhotelan khusus Gen Z!")
    st.write("Di sini kamu bisa belajar Front Office, Housekeeping, dan langsung dapat sertifikat.")

elif menu == "📚 Materi Pelatihan":
    st.write("### Kelas Perhotelan Tersedia:")
    st.write("1. **Front Office**: Komunikasi profesional & Handling Check-in.")
    st.write("2. **Housekeeping**: Standar kebersihan kamar bintang 5.")

elif menu == "📝 Cek Sertifikat":
    st.write("### Verifikasi Sertifikat Siswa")
    id_siswa = st.text_input("Masukkan ID Siswa Kamu:")
    nama_siswa = st.text_input("Masukkan Nama Lengkap:")
    tahun = st.text_input("Tahun Lulus:")
    
    if st.button("Cari Sertifikat"):
        if id_siswa and nama_siswa and tahun:
            st.info(f"Fitur verifikasi untuk {nama_siswa} (ID: {id_siswa}) lulusan tahun {tahun} sedang disiapkan!")
        else:
            st.warning("Silakan isi data kamu dengan lengkap.")
