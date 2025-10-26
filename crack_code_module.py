"""
Modul untuk deteksi tepi menggunakan algoritma Canny.
Berguna untuk analisis crack/retakan pada citra.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_canny_edge_detection(img_path, low_threshold=50, high_threshold=150, blur_kernel=(5, 5)):
    """
    Fungsi untuk deteksi tepi menggunakan Canny Edge Detection.
    
    Args:
        img_path: Path ke file gambar
        low_threshold: Threshold rendah untuk Canny (default: 50)
        high_threshold: Threshold tinggi untuk Canny (default: 150)
        blur_kernel: Ukuran kernel untuk Gaussian Blur (default: (5, 5))
        
    Returns:
        dict: Dictionary berisi hasil pemrosesan dan figure matplotlib
    """
    try:
        # 1. Pemuatan Citra
        img = cv2.imread(img_path)
        if img is None:
            return {
                'success': False,
                'message': f"Citra tidak ditemukan di: {img_path}",
                'figure': None
            }

        # 2. Konversi ke Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Reduksi Noise (Gaussian Blur)
        blurred = cv2.GaussianBlur(gray, blur_kernel, 0)

        # 4. Deteksi Tepi Canny
        edges = cv2.Canny(blurred, low_threshold, high_threshold)

        # 5. Visualisasi Hasil
        fig = plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 3, 1)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title('Citra Asli')
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.imshow(blurred, cmap='gray')
        plt.title('Grayscale + Gaussian Blur')
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.imshow(edges, cmap='gray')
        plt.title(f'Tepi Canny (Th={low_threshold},{high_threshold})')
        plt.axis('off')

        plt.tight_layout()
        plt.suptitle("Deteksi Tepi Canny", fontsize=16)
        plt.subplots_adjust(top=0.92)

        return {
            'success': True,
            'message': f"Deteksi tepi berhasil dengan threshold ({low_threshold}, {high_threshold})",
            'figure': fig,
            'edges': edges,
            'blurred': blurred,
            'original': img
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
    img_path = 'cameraman.png'
    result = process_canny_edge_detection(img_path)
    show_results(result)
