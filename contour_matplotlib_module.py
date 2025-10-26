"""
Modul untuk deteksi kontur dengan OpenCV dan generasi Freeman Chain Code.
Menampilkan hasil menggunakan Matplotlib (subplot).
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_freeman_chain_code(contour):
    """
    Menghasilkan Kode Rantai Freeman 8-arah dari kontur OpenCV.
    ASUMSI: kontur didapat dari findContours dengan CHAIN_APPROX_NONE.
    """
    chain_code = []
    if len(contour) < 2:
        return chain_code # Kontur harus punya minimal 2 titik

    # Pemetaan (dx, dy) ke kode arah Freeman (sumbu Y positif ke bawah)
    directions = {
        (1, 0): 0, (1, 1): 1, (0, 1): 2, (-1, 1): 3,
        (-1, 0): 4, (-1, -1): 5, (0, -1): 6, (1, -1): 7
    }

    for i in range(len(contour)):
        p1 = contour[i][0] # Titik saat ini (format: [[x, y]])
        p2 = contour[(i + 1) % len(contour)][0]

        dx = p2[0] - p1[0] # Perbedaan X
        dy = p2[1] - p1[1] # Perbedaan Y (Ingat: Y positif ke bawah)

        norm_dx = np.sign(dx)
        norm_dy = np.sign(dy)

        code = directions.get((norm_dx, norm_dy))
        if code is not None:
            chain_code.append(code)

    return chain_code

def process_contour_with_matplotlib(img_path, threshold_value=127):
    """
    Fungsi utama untuk deteksi kontur dan visualisasi dengan Matplotlib.
    
    Args:
        img_path: Path ke file gambar
        threshold_value: Nilai threshold untuk binarisasi (default: 127)
        
    Returns:
        dict: Dictionary berisi hasil pemrosesan dan figure matplotlib
    """
    try:
        # 1. Pemuatan Citra (langsung grayscale)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {
                'success': False,
                'message': f"Citra tidak ditemukan atau tidak dapat dibaca di: {img_path}",
                'figure': None
            }

        # 2. Binarisasi
        _, binary_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY_INV)

        # 3. Deteksi Kontur
        contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # --- Persiapan Visualisasi dengan Matplotlib ---
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        # Plot Citra Asli (Grayscale)
        axs[0, 0].imshow(img, cmap='gray')
        axs[0, 0].set_title('Citra Asli (Grayscale)')
        axs[0, 0].axis('off')

        # Plot Citra Biner
        axs[0, 1].imshow(binary_img, cmap='gray')
        axs[0, 1].set_title('Citra Biner (Hasil Threshold)')
        axs[0, 1].axis('off')

        # Variabel untuk menyimpan hasil jika kontur ditemukan
        chain_code_str = "Tidak ada kontur ditemukan."
        img_contour_display = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # 4. Proses Kontur dan Generasi Kode Rantai
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            # Gambar kontur
            img_contour_display = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(img_contour_display, [largest_contour], -1, (0, 255, 0), 2)

            # Generasi Kode Rantai
            chain_code_result = generate_freeman_chain_code(largest_contour)

            # Format teks kode rantai untuk ditampilkan (dengan wrapping)
            max_line_len = 70
            wrapped_code = ""
            current_line = ""
            for i, code_str in enumerate(map(str, chain_code_result)):
                item = code_str + (", " if i < len(chain_code_result) - 1 else "")
                if len(current_line) + len(item) > max_line_len and current_line:
                    wrapped_code += current_line + "\n"
                    current_line = item
                else:
                    current_line += item
            wrapped_code += current_line

            chain_code_str = (
                f"Jumlah Kontur Total: {len(contours)}\n"
                f"Kode Rantai Kontur Terbesar (Panjang {len(chain_code_result)}):\n"
                f"{wrapped_code}"
            )

        # Plot Citra dengan Kontur Terdeteksi
        img_rgb_display = cv2.cvtColor(img_contour_display, cv2.COLOR_BGR2RGB)
        axs[1, 0].imshow(img_rgb_display)
        axs[1, 0].set_title('Kontur Terbesar Terdeteksi')
        axs[1, 0].axis('off')

        # Area untuk menampilkan Teks Kode Rantai
        axs[1, 1].axis('off')
        axs[1, 1].text(0.05, 0.95,
                       chain_code_str,
                       ha='left',
                       va='top',
                       fontsize=9,
                       wrap=True,
                       family='monospace')
        axs[1, 1].set_title('Hasil Kode Rantai')

        # --- Tampilkan Figure Matplotlib ---
        plt.tight_layout(pad=1.5)
        plt.suptitle("Analisis Kode Rantai (Matplotlib)", fontsize=16)
        plt.subplots_adjust(top=0.92)

        return {
            'success': True,
            'message': "Visualisasi berhasil dibuat",
            'figure': fig
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
        
    if result['figure']:
        plt.show()

# Untuk menjalankan sebagai script standalone
if __name__ == "__main__":
    img_path = 'WINWORD_GND0i7aMnp.png'
    result = process_contour_with_matplotlib(img_path)
    show_results(result)
