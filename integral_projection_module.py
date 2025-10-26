"""
Modul untuk analisis proyeksi integral (Integral Projection).
Berguna untuk segmentasi dan analisis teks atau objek dalam citra.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_integral_projection(img_path, threshold_value=0, use_otsu=True):
    """
    Fungsi untuk analisis proyeksi integral pada citra.
    
    Args:
        img_path: Path ke file gambar
        threshold_value: Nilai threshold untuk binarisasi (default: 0, akan menggunakan Otsu)
        use_otsu: Gunakan metode Otsu untuk threshold otomatis (default: True)
        
    Returns:
        dict: Dictionary berisi hasil pemrosesan dan figure matplotlib
    """
    try:
        # 1. Pemuatan Citra (langsung grayscale)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {
                'success': False,
                'message': f"Citra tidak ditemukan di: {img_path}",
                'figure': None
            }

        # 2. Binarisasi
        # Gunakan Otsu untuk otomatisasi jika kontras baik
        # Jika teks hitam di latar putih, gunakan THRESH_BINARY_INV
        if use_otsu:
            _, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        else:
            _, binary_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY_INV)

        # Normalisasi ke 0 dan 1 (Objek=1, Latar=0)
        binary_norm = binary_img / 255.0

        # 3. Proyeksi Horizontal (Sum per Kolom -> Profil Vertikal)
        horizontal_projection = np.sum(binary_norm, axis=0)

        # 4. Proyeksi Vertikal (Sum per Baris -> Profil Horizontal)
        vertical_projection = np.sum(binary_norm, axis=1)

        # 5. Visualisasi Hasil
        height, width = binary_norm.shape

        # Buat figure dan axes dengan GridSpec
        fig = plt.figure(figsize=(10, 8))
        gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                              left=0.1, right=0.9, bottom=0.1, top=0.9,
                              wspace=0.05, hspace=0.05)

        # Axes untuk citra biner (pojok kiri bawah)
        ax_img = fig.add_subplot(gs[1, 0])
        ax_img.imshow(binary_norm, cmap='gray')
        ax_img.set_title('Citra Biner (Objek=1)')
        ax_img.set_xlabel('Indeks Kolom')
        ax_img.set_ylabel('Indeks Baris')

        # Axes untuk Proyeksi Horizontal (di atas citra biner)
        ax_hproj = fig.add_subplot(gs[0, 0], sharex=ax_img)
        ax_hproj.plot(np.arange(width), horizontal_projection, color='blue')
        ax_hproj.set_title('Proyeksi Horizontal (Profil Vertikal)')
        ax_hproj.set_ylabel('Jumlah Piksel')
        ax_hproj.grid(True, alpha=0.3)
        plt.setp(ax_hproj.get_xticklabels(), visible=False)

        # Axes untuk Proyeksi Vertikal (di kanan citra biner)
        ax_vproj = fig.add_subplot(gs[1, 1], sharey=ax_img)
        ax_vproj.plot(vertical_projection, np.arange(height), color='red')
        ax_vproj.set_title('Proyeksi Vertikal')
        ax_vproj.set_xlabel('Jumlah Piksel')
        ax_vproj.grid(True, alpha=0.3)
        ax_vproj.invert_yaxis()
        plt.setp(ax_vproj.get_yticklabels(), visible=False)

        plt.suptitle("Analisis Proyeksi Integral", fontsize=14)

        return {
            'success': True,
            'message': "Analisis proyeksi integral berhasil",
            'figure': fig,
            'horizontal_projection': horizontal_projection,
            'vertical_projection': vertical_projection,
            'binary_img': binary_img
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Error: {str(e)}",
            'figure': None
        }

def show_results(result):
    """Menampilkan hasil dalam matplotlib window"""
    if not result['success']:
        print(result['message'])
        return
        
    print(result['message'])
    if result['figure']:
        plt.show()

# Untuk menjalankan sebagai script standalone
if __name__ == "__main__":
    img_path = 'tier1.png'
    result = process_integral_projection(img_path)
    show_results(result)
