"""
Modul untuk deteksi kontur dengan OpenCV dan generasi Freeman Chain Code.
Menampilkan hasil menggunakan Matplotlib (menghindari cv2.imshow error).
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
        # Dapatkan titik berikutnya, gunakan modulo % untuk kembali ke titik awal 
        # pada iterasi terakhir (menangani kontur tertutup).
        p2 = contour[(i + 1) % len(contour)][0] 

        dx = p2[0] - p1[0] # Perbedaan X
        dy = p2[1] - p1[1] # Perbedaan Y (Ingat: Y positif ke bawah)

        # Dengan CHAIN_APPROX_NONE, dx/dy harusnya hanya -1, 0, atau 1.
        # Normalisasi sign memastikan ini, meskipun secara teori tidak perlu.
        norm_dx = np.sign(dx) 
        norm_dy = np.sign(dy)
        
        # Cari kode arah dari dictionary berdasarkan perpindahan (dx, dy)
        code = directions.get((norm_dx, norm_dy)) 
        if code is not None:
            chain_code.append(code)

    return chain_code

def process_contour_detection(img_path, threshold_value=127):
    """
    Fungsi utama untuk deteksi kontur dan generasi chain code.
    
    Args:
        img_path: Path ke file gambar
        threshold_value: Nilai threshold untuk binarisasi (default: 127)
        
    Returns:
        dict: Dictionary berisi hasil pemrosesan {
            'success': bool,
            'message': str,
            'num_contours': int,
            'chain_code': list,
            'img': numpy.ndarray,
            'binary_img': numpy.ndarray,
            'img_display': numpy.ndarray
        }
    """
    try:
        # 1. Pemuatan Citra (langsung grayscale)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) 
        if img is None:
            return {
                'success': False,
                'message': f"Citra tidak ditemukan di: {img_path}",
                'num_contours': 0,
                'chain_code': [],
                'img': None,
                'binary_img': None,
                'img_display': None
            }

        # 2. Binarisasi (Objek gelap di latar terang -> THRESH_BINARY_INV)
        _, binary_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY_INV) 

        # 3. Deteksi Kontur (Wajib CHAIN_APPROX_NONE)
        contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # 4. Proses Kontur Terbesar
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Visualisasi
            img_display = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(img_display, [largest_contour], -1, (0, 255, 0), 2)

            # Generasi Kode Rantai
            chain_code_result = generate_freeman_chain_code(largest_contour)
            
            return {
                'success': True,
                'message': f"Berhasil mendeteksi {len(contours)} kontur",
                'num_contours': len(contours),
                'chain_code': chain_code_result,
                'chain_code_length': len(chain_code_result),
                'img': img,
                'binary_img': binary_img,
                'img_display': img_display,
                'figure': None  # Will be created by show_results
            }
        else:
            return {
                'success': False,
                'message': "Tidak ada kontur yang terdeteksi",
                'num_contours': 0,
                'chain_code': [],
                'img': img,
                'binary_img': binary_img,
                'img_display': cv2.cvtColor(img, cv2.COLOR_GRAY2BGR),
                'figure': None
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f"Error: {str(e)}",
            'num_contours': 0,
            'chain_code': [],
            'img': None,
            'binary_img': None,
            'img_display': None
        }

def show_results(result):
    """Menampilkan hasil dalam matplotlib window (menghindari cv2.imshow error)"""
    if not result['success']:
        print(result['message'])
        return
        
    print(f"Jumlah Kontur Ditemukan: {result['num_contours']}")
    print(f"Kode Rantai Kontur Terbesar (Panjang {result['chain_code_length']}):")
    print(result['chain_code'])

    # Buat figure matplotlib
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    
    # Tampilkan citra asli
    axs[0].imshow(result['img'], cmap='gray')
    axs[0].set_title('Citra Asli (Grayscale)')
    axs[0].axis('off')
    
    # Tampilkan citra biner
    axs[1].imshow(result['binary_img'], cmap='gray')
    axs[1].set_title('Citra Biner (Threshold)')
    axs[1].axis('off')
    
    # Tampilkan kontur terdeteksi (convert BGR to RGB)
    img_rgb = cv2.cvtColor(result['img_display'], cv2.COLOR_BGR2RGB)
    axs[2].imshow(img_rgb)
    axs[2].set_title(f'Kontur Terdeteksi ({result["num_contours"]} kontur)')
    axs[2].axis('off')
    
    plt.tight_layout()
    plt.suptitle("Deteksi Kontur + Freeman Chain Code", fontsize=14, y=1.02)
    
    # Simpan figure ke result untuk save output
    result['figure'] = fig
    
    plt.show()

# Untuk menjalankan sebagai script standalone
if __name__ == "__main__":
    img_path = 'WINWORD_GND0i7aMnp.png'
    result = process_contour_detection(img_path)
    show_results(result)
