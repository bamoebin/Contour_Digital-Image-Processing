# Image Processing - Contour Detection & Analysis

Aplikasi GUI untuk pemrosesan citra digital dengan fokus pada deteksi kontur, analisis tepi, dan proyeksi integral.

## 📋 Fitur Utama

### 1. **Contour Detection (Matplotlib 3-panel)**
- Deteksi kontur objek dalam citra
- Generasi Freeman Chain Code (8-arah)
- Visualisasi menggunakan Matplotlib (3 panel)
- Output: Citra asli, biner, dan kontur terdeteksi
- **Fix:** Tidak lagi menggunakan cv2.imshow yang sering error

### 2. **Contour Detection (Matplotlib 4-panel)**
- Sama dengan modul 1, namun dengan layout berbeda
- Tampilan 4 subplot: citra asli, biner, kontur, dan chain code
- Cocok untuk analisis detail dan dokumentasi
- Text wrapping otomatis untuk chain code

### 3. **Canny Edge Detection**
- Deteksi tepi menggunakan algoritma Canny
- Gaussian blur untuk reduksi noise
- Parameter threshold yang dapat disesuaikan
- Berguna untuk analisis retakan/crack pada citra

### 4. **Integral Projection Analysis**
- Proyeksi horizontal dan vertikal
- Otsu thresholding otomatis
- Visualisasi dengan GridSpec layout
- Berguna untuk segmentasi teks dan objek

## 🚀 Cara Menjalankan

### Prasyarat
Pastikan Python 3.x dan library berikut sudah terinstal:
```bash
pip install opencv-python numpy matplotlib pillow
```

### Menjalankan Aplikasi UI
```bash
python main_ui.py
```

### Menjalankan Modul Secara Standalone
Setiap modul dapat dijalankan secara terpisah:

```bash
# Contour Detection (OpenCV)
python contour_main_module.py

# Contour Detection (Matplotlib)
python contour_matplotlib_module.py

# Canny Edge Detection
python crack_code_module.py

# Integral Projection
python integral_projection_module.py
```

> **Catatan:** Untuk menjalankan secara standalone, edit variabel `img_path` di dalam file modul sesuai dengan path gambar Anda.

## 📁 Struktur File

```
contour-opencv-lilproject/
│
├── main_ui.py                          # ⭐ UI Utama (Jalankan file ini)
│
├── contour_main_module.py              # Modul 1: Contour + Chain Code (OpenCV)
├── contour_matplotlib_module.py        # Modul 2: Contour + Chain Code (Matplotlib)
├── crack_code_module.py                # Modul 3: Canny Edge Detection
├── integral_projection_module.py       # Modul 4: Integral Projection
│
├── archive/                            # 📦 File standalone versi lama (backup)
│   ├── countour-detection-main.py
│   ├── countour-detection-alt-with-plt.py
│   ├── crack-code_countour.py
│   └── integral-projection_countour.py
│
├── images/                             # 📁 Folder untuk gambar input (opsional)
├── output/                             # 💾 Folder hasil output (auto-generated)
│
├── README.md                           # 📖 Dokumentasi lengkap
└── CARA_MENJALANKAN.md                 # 📖 Quick start guide
```

> **Catatan:** 
> - File di folder `archive/` adalah versi standalone yang masih bisa dijalankan langsung
> - Folder `output/` akan otomatis dibuat saat menjalankan UI
> - Folder `images/` opsional, untuk mengorganisir gambar input Anda

## 🎯 Cara Penggunaan UI

1. **Jalankan Aplikasi:**
   ```bash
   python main_ui.py
   ```

2. **Pilih Gambar:**
   - Klik tombol "Browse..." untuk memilih file gambar
   - Preview akan ditampilkan otomatis
   - Supported formats: PNG, JPG, JPEG, BMP, TIFF

3. **Sesuaikan Parameter (Opsional):**
   - **Threshold Binarisasi:** 0-255 (default: 127)
   - **Canny Low Threshold:** 0-255 (default: 50)
   - **Canny High Threshold:** 0-255 (default: 150)

4. **Pilih Modul:**
   - Klik salah satu dari 4 tombol modul
   - Hasil akan ditampilkan di window terpisah
   - Log output akan muncul di area log

5. **Tutup Window Hasil:**
   - OpenCV: Tekan tombol apapun di keyboard
   - Matplotlib: Klik tombol close (X) di window

6. **Simpan Hasil (Opsional):**
   - Setelah proses selesai, klik tombol "💾 Save Output"
   - Hasil akan disimpan ke folder `output/` dengan timestamp
   - Format: `namafile_jenismodul_timestamp.png/txt`

## 📊 Parameter dan Tuning

### Threshold Binarisasi
- **Fungsi:** Memisahkan objek dari latar belakang
- **Range:** 0-255
- **Tips:** 
  - Objek gelap + latar terang → gunakan 127
  - Citra high contrast → nilai lebih rendah/tinggi

### Canny Threshold
- **Low Threshold:** Tepi lemah (default: 50)
- **High Threshold:** Tepi kuat (default: 150)
- **Rule of thumb:** High = 2-3× Low
- **Tips:**
  - Noise tinggi → naikkan threshold
  - Detail halus → turunkan threshold

### Integral Projection
- Otomatis menggunakan Otsu thresholding
- Tidak perlu adjustment manual

## 🔧 Troubleshooting

### Error: cv2.imshow tidak berfungsi
```
error: (-2:Unspecified error) The function is not implemented. 
Rebuild the library with Windows, GTK+ 2.x or Cocoa support.
```

**Solusi:** ✅ Sudah diperbaiki!
- Modul 1 & 2 sekarang menggunakan **Matplotlib** untuk tampilan
- Tidak lagi bergantung pada cv2.imshow
- Semua visualisasi menggunakan Matplotlib yang lebih kompatibel

### Error: "Citra tidak ditemukan"
- Pastikan path gambar benar
- Gunakan tombol Browse untuk memilih file
- Pastikan format file didukung

### Window OpenCV tidak muncul
**Solusi:** ✅ Tidak lagi relevan - semua modul sekarang menggunakan Matplotlib

### UI tidak responsif saat resize
**Solusi:** ✅ Sudah diperbaiki!
- Window sekarang dapat di-resize dengan smooth
- Semua komponen mengikuti ukuran window
- Minimum size: 800x600 pixels
- Preview gambar dan log otomatis adjust

### Import Error
- Install dependencies: `pip install opencv-python numpy matplotlib pillow`
- Pastikan semua file modul ada di folder yang sama

### Preview tidak muncul
- Pastikan Pillow terinstal: `pip install pillow`
- Coba gambar dengan format berbeda

## 📝 Contoh Output

### Contour Detection
- **Input:** Gambar objek (grayscale/color)
- **Output:** 
  - Jumlah kontur terdeteksi
  - Freeman Chain Code (list integer 0-7)
  - Visualisasi kontur dengan warna hijau

### Canny Edge Detection
- **Input:** Gambar apapun
- **Output:** 
  - Gambar asli
  - Hasil Gaussian blur
  - Peta tepi (edge map)

### Integral Projection
- **Input:** Gambar dengan objek/teks
- **Output:** 
  - Grafik proyeksi horizontal (atas)
  - Grafik proyeksi vertikal (kanan)
  - Citra biner (tengah)

## 💾 Fitur Save Output

Setelah menjalankan salah satu modul, Anda dapat menyimpan hasil dengan:
1. Klik tombol **"💾 Save Output"** di bagian bawah
2. File akan otomatis tersimpan di folder `output/` dengan format:
   - **Contour Detection:** Gambar hasil + file .txt berisi chain code
   - **Canny/Matplotlib:** Gambar hasil visualisasi
3. Nama file: `namafile_jenismodul_YYYYMMDD_HHMMSS.png/txt`

Contoh:
```
output/
├── sample_contour_20251025_143022.png
├── sample_chaincode_20251025_143022.txt
├── sample_canny_edge_20251025_143045.png
└── sample_integral_proj_20251025_143110.png
```

## 🎓 Informasi Akademis

- **Mata Kuliah:** Digital Image Processing
- **Praktikum:** Minggu 8
- **Topik:** Contour Detection, Edge Detection, Integral Projection
- **Semester:** 5

## 🐛 Bug Fixes

### v2.2 (Current - October 25, 2025)
✅ **MAJOR FIX:** Replaced cv2.imshow with Matplotlib (fix OpenCV GUI error)
✅ **UI Responsiveness:** Fixed grid weights - window sekarang fully responsive
✅ Added minimum window size (800x600)
✅ Preview dan log area sekarang auto-resize
✅ Updated button labels untuk clarity
✅ Increased default window size ke 1000x750

### v2.1
✅ Added "Save Output" feature untuk simpan hasil ke folder output/
✅ Auto-create folder output/ saat aplikasi dijalankan
✅ Reorganized structure: file lama dipindah ke folder archive/
✅ Added folder images/ untuk mengorganisir gambar input
✅ Improved file naming dengan timestamp

### v2.0
✅ Fixed line wrapping logic di `countour-detection-alt-with-plt.py`
✅ Refactored semua modul menjadi fungsi reusable
✅ Dibuat UI terpadu dengan tkinter
✅ Added error handling di semua modul
✅ Added preview gambar di UI
✅ Added parameter adjustment di UI

### v1.0 (Original)
- Script standalone untuk setiap modul
- Manual path input
- No centralized UI

## 📄 License

Educational project - Kuliah Semester 5

## 👨‍💻 Support

Jika ada pertanyaan atau menemukan bug, silakan:
1. Klik tombol "Help" di aplikasi untuk panduan lengkap
2. Periksa log output untuk error details
3. Pastikan semua dependencies terinstal dengan benar

---

**Happy Image Processing! 🖼️✨**
