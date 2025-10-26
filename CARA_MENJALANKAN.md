### AUTHOR
231524006 Farras

# CARA MENJALANKAN APLIKASI

## 🚀 Quick Start

### 1. Install Dependencies (Jika belum)
```powershell
pip install opencv-python numpy matplotlib pillow
```

### 2. Jalankan UI Utama
```powershell
python main_ui.py
```

### 3. Gunakan Aplikasi
1. Klik "Browse..." untuk pilih gambar
2. Pilih salah satu dari 4 modul yang tersedia
3. Lihat hasil di window yang muncul
4. (Opsional) Klik "💾 Save Output" untuk simpan hasil

## 📌 Modul yang Tersedia

| No | Modul | Deskripsi | Tampilan |
|----|-------|-----------|----------|
| 1 | Contour Detection (View 1) | Deteksi kontur + Freeman Chain Code | Matplotlib 3-panel |
| 2 | Contour Detection (View 2) | Sama seperti #1 dengan 4 panel + text | Matplotlib 4-panel |
| 3 | Canny Edge Detection | Deteksi tepi untuk analisis crack | Matplotlib |
| 4 | Integral Projection | Proyeksi horizontal & vertikal | Matplotlib |

> **Note:** Semua modul menggunakan Matplotlib untuk menghindari error cv2.imshow

## ⚙️ Parameter Default

- **Threshold Binarisasi:** 127
- **Canny Low Threshold:** 50  
- **Canny High Threshold:** 150

Parameter dapat disesuaikan di UI sebelum menjalankan modul.

## 📂 File yang Diperlukan

✅ main_ui.py (File utama - JALANKAN INI)
✅ contour_main_module.py
✅ contour_matplotlib_module.py
✅ crack_code_module.py
✅ integral_projection_module.py

**Folder:**
- `archive/` - Berisi file standalone versi lama (masih bisa dijalankan manual)
- `images/` - Tempat menyimpan gambar input (opsional)
- `output/` - Hasil output otomatis tersimpan di sini

## ❓ Troubleshooting

**Error: ModuleNotFoundError**
```powershell
pip install opencv-python numpy matplotlib pillow
```

**Error: cv2.imshow tidak berfungsi**
```
error: (-2:Unspecified error) The function is not implemented
```
✅ **Sudah diperbaiki!** Semua modul sekarang menggunakan Matplotlib.

**UI tidak responsif saat resize**
✅ **Sudah diperbaiki!** Window sekarang fully responsive dengan minimum 800x600.

**Window tidak muncul (Matplotlib)**
- Pastikan tidak ada window Matplotlib lain yang terbuka
- Close window dengan tombol X
- Atau close via terminal dengan Ctrl+C

**Gambar tidak bisa dibaca**
- Pastikan format: PNG, JPG, JPEG, BMP, atau TIFF
- Pastikan path file benar (gunakan Browse)

## 💡 Tips

1. **Untuk objek gelap di latar terang:** gunakan threshold 127 (default)
2. **Untuk objek terang di latar gelap:** gunakan threshold lebih rendah (~80)
3. **Untuk edge detection halus:** turunkan Canny threshold
4. **Untuk edge detection kasar:** naikkan Canny threshold
5. **Simpan hasil:** Gunakan tombol "💾 Save Output" setelah proses selesai
6. **File lama:** Cek folder `archive/` untuk versi standalone yang bisa dijalankan manual

## 🗂️ Tentang Folder Archive

Folder `archive/` berisi 4 file Python versi lama yang **MASIH BISA DIGUNAKAN**:
- `countour-detection-main.py` - Versi standalone Contour Detection (OpenCV)
- `countour-detection-alt-with-plt.py` - Versi standalone Contour Detection (Matplotlib)
- `crack-code_countour.py` - Versi standalone Canny Edge Detection
- `integral-projection_countour.py` - Versi standalone Integral Projection

**Cara menjalankan file di archive:**
```powershell
cd archive
python countour-detection-main.py
```
> **Note:** Edit path gambar di dalam file sebelum menjalankan

---

Selamat menggunakan! 🎉
