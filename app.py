import os
from google import genai
from PIL import Image
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Lab Report & Code Assistant", page_icon="🤖", layout="wide"
)

st.title("🎓 Lab Report & Code Assistant")
st.markdown(
    "Unggah instruksi tugas praktikum dan screenshot hasil kerjamu. AI"
    " akan otomatis membuatkan pembahasan laporan dan kode programnya!"
)

# Sidebar untuk panduan singkat
with st.sidebar:
  st.header("Panduan Penggunaan:")
  st.markdown("1. Masukkan modul/instruksi tugas di kolom kiri.")
  st.markdown("2. Unggah screenshot hasil praktikum di kolom kanan.")
  st.markdown("3. Klik tombol **'Generate Laporan & Kode'**.")

  api_key_input = st.text_input(
      "Gemini API Key (Opsional jika sudah diset)", type="password"
  )

# Inisialisasi client Gemini
try:
  if api_key_input:
    client = genai.Client(api_key=api_key_input)
  else:
    client = genai.Client()  # Mengambil otomatis dari os.environ['GEMINI_API_KEY']
except Exception as e:
  st.error(
      f"Gagal menginisialisasi Gemini Client. Pastikan API Key sudah benar. Error:"
      f" {e}"
  )

# Layout utama dibagi 2 kolom
col1, col2 = st.columns(2)

with col1:
  st.subheader("1. Instruksi / Modul Tugas")
  prompt_instruksi = st.text_area(
      "Tuliskan soal, modul, atau instruksi praktikum di sini:",
      height=200,
      placeholder=(
          "Contoh: Buatlah laporan praktikum modul koneksi database menggunakan"
          " PHP dan jelaskan alur alogoritmanya."
      ),
  )

with col2:
  st.subheader("2. Screenshot Hasil Praktikum")
  uploaded_image = st.file_uploader(
      "Pilih file screenshot (PNG/JPG):", type=["png", "jpg", "jpeg"]
  )

  if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(
        image, caption="Preview Screenshot Praktikum", use_container_width=True
    )

# Tombol Eksekusi
if st.button("🚀 Generate Laporan & Kode", type="primary"):
  if not prompt_instruksi and not uploaded_image:
    st.warning("Mohon isi instruksi tugas atau unggah screenshot terlebih dahulu!")
  else:
    with st.spinner("Sedang Menganalisis Tugas dan Screenshot... Sabar ya! ⏳"):
      try:
        contents_payload = []

        # Masukkan gambar jika ada
        if uploaded_image:
          temp_image_path = "temp_screenshot.png"
          image.save(temp_image_path)
          image_file_ref = client.files.upload(file=temp_image_path)
          contents_payload.append(image_file_ref)

        # Susun prompt teks lengkap untuk AI
        full_prompt = f"""
                Bertindaklah sebagai asisten praktikum dan expert programmer senior di bidang Informatika. 
                Berikut adalah instruksi/modul tugas praktikum dari mahasiswa:
                \n\n--- INSTRUKSI ---\n{prompt_instruksi}\n--- AKHIR INSTRUKSI ---
                
                Tugasmu adalah membuatkan hasil laporan praktikum yang komprehensif dan profesional dengan format berikut:
                1. **Analisis & Pembahasan Mendalam**: Menjelaskan hasil dari screenshot yang dilampirkan secara sistematis sesuai standar laporan resmi.
                2. **Source Code / Perbaikan Kode**: Menyediakan kode program lengkap, bersih, dan berstandar industri jika diperlukan.
                3. **Kesimpulan**: Ringkasan singkat dari praktikum tersebut.
                """

        contents_payload.append(full_prompt)

        # Panggil model Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents_payload
        )

        # Tampilkan hasil di layar
        st.success("Berhasil men-generate laporan!")
        st.markdown("### 📝 Hasil Pembahasan & Kode Program:")
        st.markdown(response.text)

      except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")