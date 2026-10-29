import os
from google import genai
from google.genai import types

# Inisialisasi client Gemini (pastikan API key sudah diset di environment variables)
client = genai.Client()


def generate_lab_report(prompt_instruksi, image_path):
  # Memuat gambar screenshot praktikum
  image_file = client.files.upload(file=image_path)

  # Mengirim instruksi teks modul dan gambar screenshot ke AI
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[
          image_file,
          (
              f"Berikut adalah instruksi tugas praktikum:\n{prompt_instruksi}\n\n"
              "Tolong buatkan:\n"
              "1. Pembahasan dan analisis mendalam dari hasil screenshot di atas sesuai instruksi.\n"
              "2. Perbaikan atau kode program lengkap jika diperlukan."
          ),
      ],
  )

  return response.text


# Contoh penggunaan
# hasil_laporan = generate_lab_report("Buat laporan untuk praktikum koneksi database PHP.", "screenshot_hasil.png")
# print(hasil_laporan)