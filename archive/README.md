# Archive - File Standalone Versi Lama

Folder ini berisi **4 file Python standalone** versi lama yang masih dapat dijalankan secara terpisah tanpa UI.

##  File yang Tersedia

### 1. `1.py`
- **Fungsi:** Deteksi kontur + Freeman Chain Code
- **Tampilan:** Window OpenCV (cv2.imshow)
- **Cara jalankan:**
  ```powershell
  python 1.py
  ```
- **Edit dulu:** Ubah variabel `img_path` di line ~44 dengan path gambar Anda

### 2. `2.py`
- **Fungsi:** Deteksi kontur + Freeman Chain Code
- **Tampilan:** Matplotlib (4 subplot)
- **Cara jalankan:**
  ```powershell
  python 2.py
  ```
- **Edit dulu:** Ubah variabel `img_path` di line ~41 dengan path gambar Anda

### 3. `3.py`
- **Fungsi:** Canny Edge Detection (untuk analisis crack/retakan)
- **Tampilan:** Matplotlib (3 subplot)
- **Cara jalankan:**
  ```powershell
  python 3.py
  ```
- **Edit dulu:** Ubah variabel `img_path` di line ~7 dengan path gambar Anda

### 4. `4.py`
- **Fungsi:** Analisis Proyeksi Integral (horizontal & vertikal)
- **Tampilan:** Matplotlib (GridSpec layout)
- **Cara jalankan:**
  ```powershell
  python 4.py
  ```
- **Edit dulu:** Ubah variabel `img_path` di line ~7 dengan path gambar Anda

##  Mengapa File Ini Disimpan?

1. **Backup** - Kode asli sebagai referensi
2. **Testing cepat** - Tidak perlu buka UI untuk testing sederhana
3. **Pembelajaran** - Membandingkan versi lama vs baru
4. **Standalone** - Bisa dijalankan di environment tanpa tkinter

## Perbedaan dengan Versi Modul Baru

| Aspek | File Archive (Lama) | Modul Baru |
|-------|---------------------|------------|
| **Cara jalankan** | Langsung dengan `python namafile.py` | Dipanggil dari UI atau import sebagai modul |
| **Input gambar** | Hardcoded di variabel `img_path` | Dipilih melalui file browser di UI |
| **Output** | Langsung tampil di window | Return dictionary, bisa disimpan otomatis |
| **Parameter** | Edit manual di kode | Adjust di UI sebelum jalankan |
| **Reusability** | Script standalone, tidak bisa diimport | Fungsi yang bisa dipanggil dari kode lain |

## Rekomendasi

- **Gunakan UI (`main_ui.py`)** untuk penggunaan normal 
- **Gunakan file archive** hanya untuk:
  - Testing cepat tanpa buka UI
  - Debugging modul tertentu
  - Belajar implementasi detail

## Catatan Bug Fix

File `2.py` di folder ini **SUDAH DIPERBAIKI**:
- Fixed logic wrapping text untuk chain code
- Text wrapping sekarang berfungsi dengan benar

---

Jika ada pertanyaan, lihat dokumentasi utama di folder parent atau klik tombol "Help" di UI.
