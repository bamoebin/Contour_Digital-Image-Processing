"""
UI Utama untuk Image Processing - Contour Detection & Analysis
Aplikasi GUI untuk menjalankan berbagai modul pemrosesan citra:
1. Contour Detection (OpenCV Windows)
2. Contour Detection (Matplotlib)
3. Canny Edge Detection
4. Integral Projection Analysis
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from PIL import Image, ImageTk
import cv2
from datetime import datetime

# Import modul-modul yang sudah dibuat
try:
    import contour_main_module
    import contour_matplotlib_module
    import crack_code_module
    import integral_projection_module
except ImportError as e:
    messagebox.showerror("Import Error", f"Gagal mengimpor modul: {e}\nPastikan semua file modul ada di folder yang sama.")
    exit()

# Buat folder output jika belum ada
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


class ImageProcessingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing - Contour Detection & Analysis")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Set minimum size
        self.root.minsize(800, 600)
        
        # Variabel untuk menyimpan path gambar
        self.img_path = tk.StringVar()
        self.current_image = None
        self.last_result = None  # Untuk menyimpan hasil terakhir
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup semua komponen UI"""
        
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Preview bisa expand
        main_frame.rowconfigure(4, weight=2)  # Log bisa expand lebih besar
        
        # ========== HEADER ==========
        header_frame = ttk.LabelFrame(main_frame, text="Pilih Gambar Input", padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        ttk.Label(header_frame, text="Path Gambar:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        path_entry = ttk.Entry(header_frame, textvariable=self.img_path, width=50)
        path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        browse_btn = ttk.Button(header_frame, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=(5, 0))
        
        # ========== IMAGE PREVIEW ==========
        preview_frame = ttk.LabelFrame(main_frame, text="Preview Gambar", padding="10")
        preview_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_label = ttk.Label(preview_frame, text="Belum ada gambar dipilih", anchor=tk.CENTER)
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ========== PROCESSING MODULES ==========
        modules_frame = ttk.LabelFrame(main_frame, text="Modul Pemrosesan Citra", padding="10")
        modules_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Grid layout untuk tombol (2x2)
        modules_frame.columnconfigure(0, weight=1)
        modules_frame.columnconfigure(1, weight=1)
        modules_frame.rowconfigure(0, weight=1)
        modules_frame.rowconfigure(1, weight=1)
        
        # Button 1: Contour Detection (Matplotlib)
        btn1 = ttk.Button(
            modules_frame,
            text="1. Contour Detection\n(View 1: Matplotlib 3-panel)",
            command=self.run_contour_main,
            width=35
        )
        btn1.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button 2: Contour Detection (Matplotlib)
        btn2 = ttk.Button(
            modules_frame,
            text="2. Contour Detection\n(View 2: Matplotlib 4-panel + Text)",
            command=self.run_contour_matplotlib,
            width=35
        )
        btn2.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button 3: Canny Edge Detection
        btn3 = ttk.Button(
            modules_frame,
            text="3. Canny Edge Detection\n(Crack/Tepi Analysis)",
            command=self.run_canny_edge,
            width=35
        )
        btn3.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button 4: Integral Projection
        btn4 = ttk.Button(
            modules_frame,
            text="4. Integral Projection\n(Segmentasi & Analisis)",
            command=self.run_integral_projection,
            width=35
        )
        btn4.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ========== PARAMETER FRAME ==========
        param_frame = ttk.LabelFrame(main_frame, text="Parameter (Opsional)", padding="10")
        param_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Threshold untuk binarisasi
        ttk.Label(param_frame, text="Threshold Binarisasi:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.threshold_var = tk.IntVar(value=127)
        ttk.Spinbox(param_frame, from_=0, to=255, textvariable=self.threshold_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Canny thresholds
        ttk.Label(param_frame, text="Canny Low Th:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.canny_low_var = tk.IntVar(value=50)
        ttk.Spinbox(param_frame, from_=0, to=255, textvariable=self.canny_low_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(param_frame, text="Canny High Th:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.canny_high_var = tk.IntVar(value=150)
        ttk.Spinbox(param_frame, from_=0, to=255, textvariable=self.canny_high_var, width=10).grid(row=0, column=5, sticky=tk.W, padx=5)
        
        # ========== LOG OUTPUT ==========
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ========== FOOTER ==========
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(footer_frame, text="© 2025 - Digital Image Processing", 
                 foreground="gray").pack(side=tk.LEFT)
        
        save_btn = ttk.Button(footer_frame, text="💾 Save Output", command=self.save_output)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        clear_log_btn = ttk.Button(footer_frame, text="Clear Log", command=self.clear_log)
        clear_log_btn.pack(side=tk.RIGHT, padx=5)
        
        help_btn = ttk.Button(footer_frame, text="Help", command=self.show_help)
        help_btn.pack(side=tk.RIGHT)
        
    def browse_file(self):
        """Browse dan pilih file gambar"""
        filename = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.img_path.set(filename)
            self.load_preview(filename)
            self.log(f"Gambar dipilih: {os.path.basename(filename)}")
    
    def load_preview(self, img_path):
        """Load dan tampilkan preview gambar"""
        try:
            # Baca gambar dengan OpenCV
            img = cv2.imread(img_path)
            if img is None:
                self.log("Error: Tidak dapat membaca gambar", error=True)
                return
            
            # Convert BGR to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize untuk preview (max 400x300)
            h, w = img_rgb.shape[:2]
            max_width, max_height = 400, 300
            
            if w > max_width or h > max_height:
                ratio = min(max_width/w, max_height/h)
                new_w, new_h = int(w*ratio), int(h*ratio)
                img_rgb = cv2.resize(img_rgb, (new_w, new_h))
            
            # Convert ke PhotoImage
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            # Update preview
            self.preview_label.configure(image=img_tk, text="")
            self.preview_label.image = img_tk  # Keep reference
            self.current_image = img_path
            
        except Exception as e:
            self.log(f"Error loading preview: {str(e)}", error=True)
    
    def log(self, message, error=False):
        """Tambahkan pesan ke log"""
        if error:
            message = f"❌ ERROR: {message}"
        else:
            message = f"✓ {message}"
        
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.update()
    
    def clear_log(self):
        """Hapus semua log"""
        self.log_text.delete(1.0, tk.END)
    
    def validate_image(self):
        """Validasi apakah gambar sudah dipilih"""
        if not self.img_path.get() or not os.path.exists(self.img_path.get()):
            messagebox.showwarning("Peringatan", "Silakan pilih gambar terlebih dahulu!")
            return False
        return True
    
    def run_contour_main(self):
        """Jalankan modul Contour Detection (OpenCV Windows)"""
        if not self.validate_image():
            return
        
        self.log("Menjalankan Contour Detection (OpenCV)...")
        try:
            result = contour_main_module.process_contour_detection(
                self.img_path.get(),
                threshold_value=self.threshold_var.get()
            )
            
            if result['success']:
                self.log(result['message'])
                self.log(f"Jumlah kontur: {result['num_contours']}")
                if result['chain_code']:
                    self.log(f"Panjang chain code: {result['chain_code_length']}")
                    # Tampilkan sebagian chain code
                    chain_preview = str(result['chain_code'][:50])
                    if len(result['chain_code']) > 50:
                        chain_preview += "..."
                    self.log(f"Chain code: {chain_preview}")
                
                # Simpan hasil untuk save nanti
                self.last_result = {'type': 'contour_main', 'data': result}
                
                # Tampilkan window OpenCV
                contour_main_module.show_results(result)
            else:
                self.log(result['message'], error=True)
                
        except Exception as e:
            self.log(f"Error: {str(e)}", error=True)
    
    def run_contour_matplotlib(self):
        """Jalankan modul Contour Detection (Matplotlib)"""
        if not self.validate_image():
            return
        
        self.log("Menjalankan Contour Detection (Matplotlib)...")
        try:
            result = contour_matplotlib_module.process_contour_with_matplotlib(
                self.img_path.get(),
                threshold_value=self.threshold_var.get()
            )
            
            if result['success']:
                self.log(result['message'])
                # Simpan hasil untuk save nanti
                self.last_result = {'type': 'contour_matplotlib', 'data': result}
                # Tampilkan figure Matplotlib
                contour_matplotlib_module.show_results(result)
            else:
                self.log(result['message'], error=True)
                
        except Exception as e:
            self.log(f"Error: {str(e)}", error=True)
    
    def run_canny_edge(self):
        """Jalankan modul Canny Edge Detection"""
        if not self.validate_image():
            return
        
        self.log("Menjalankan Canny Edge Detection...")
        try:
            result = crack_code_module.process_canny_edge_detection(
                self.img_path.get(),
                low_threshold=self.canny_low_var.get(),
                high_threshold=self.canny_high_var.get()
            )
            
            if result['success']:
                self.log(result['message'])
                # Simpan hasil untuk save nanti
                self.last_result = {'type': 'canny_edge', 'data': result}
                # Tampilkan figure Matplotlib
                crack_code_module.show_results(result)
            else:
                self.log(result['message'], error=True)
                
        except Exception as e:
            self.log(f"Error: {str(e)}", error=True)
    
    def run_integral_projection(self):
        """Jalankan modul Integral Projection"""
        if not self.validate_image():
            return
        
        self.log("Menjalankan Integral Projection Analysis...")
        try:
            result = integral_projection_module.process_integral_projection(
                self.img_path.get(),
                use_otsu=True
            )
            
            if result['success']:
                self.log(result['message'])
                # Simpan hasil untuk save nanti
                self.last_result = {'type': 'integral_projection', 'data': result}
                # Tampilkan figure Matplotlib
                integral_projection_module.show_results(result)
            else:
                self.log(result['message'], error=True)
                
        except Exception as e:
            self.log(f"Error: {str(e)}", error=True)
    
    def save_output(self):
        """Save hasil pemrosesan ke folder output"""
        if not self.last_result:
            messagebox.showwarning("Peringatan", "Belum ada hasil untuk disimpan!\nJalankan salah satu modul terlebih dahulu.")
            return
        
        try:
            # Generate timestamp untuk nama file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(self.img_path.get()))[0]
            
            result_type = self.last_result['type']
            result_data = self.last_result['data']
            
            saved_files = []
            
            if result_type == 'contour_main':
                # Save gambar hasil
                if result_data.get('img_display') is not None:
                    output_path = os.path.join(OUTPUT_DIR, f"{base_name}_contour_{timestamp}.png")
                    cv2.imwrite(output_path, result_data['img_display'])
                    saved_files.append(output_path)
                
                # Save chain code ke text file
                if result_data.get('chain_code'):
                    txt_path = os.path.join(OUTPUT_DIR, f"{base_name}_chaincode_{timestamp}.txt")
                    with open(txt_path, 'w') as f:
                        f.write("Freeman Chain Code\n")
                        f.write("==================\n")
                        f.write(f"Source Image: {os.path.basename(self.img_path.get())}\n")
                        f.write(f"Timestamp: {timestamp}\n")
                        f.write(f"Number of Contours: {result_data['num_contours']}\n")
                        f.write(f"Chain Code Length: {result_data['chain_code_length']}\n\n")
                        f.write(f"Chain Code:\n{result_data['chain_code']}\n")
                    saved_files.append(txt_path)
            
            elif result_type in ['contour_matplotlib', 'canny_edge', 'integral_projection']:
                # Save matplotlib figure
                if result_data.get('figure'):
                    fig_name_map = {
                        'contour_matplotlib': 'contour_plot',
                        'canny_edge': 'canny_edge',
                        'integral_projection': 'integral_proj'
                    }
                    output_path = os.path.join(OUTPUT_DIR, f"{base_name}_{fig_name_map[result_type]}_{timestamp}.png")
                    result_data['figure'].savefig(output_path, dpi=150, bbox_inches='tight')
                    saved_files.append(output_path)
            
            if saved_files:
                self.log("✅ Hasil disimpan ke folder output/:")
                for f in saved_files:
                    self.log(f"   • {os.path.basename(f)}")
                messagebox.showinfo("Sukses", f"Hasil berhasil disimpan!\n\n{len(saved_files)} file tersimpan di folder output/")
            else:
                self.log("Tidak ada data yang bisa disimpan", error=True)
                
        except Exception as e:
            self.log(f"Error saat menyimpan: {str(e)}", error=True)
            messagebox.showerror("Error", f"Gagal menyimpan hasil:\n{str(e)}")
    
    def show_help(self):
        """Tampilkan help dialog"""
        help_text = """
IMAGE PROCESSING - CONTOUR DETECTION & ANALYSIS
v2.2 - October 2025

CARA PENGGUNAAN:
1. Klik tombol "Browse..." untuk memilih gambar input
2. Preview gambar akan ditampilkan (auto-resize)
3. (Opsional) Sesuaikan parameter threshold sesuai kebutuhan
4. Klik salah satu tombol modul untuk memproses gambar
5. Hasil akan muncul di window Matplotlib
6. Klik "💾 Save Output" untuk simpan hasil ke folder output/

MODUL YANG TERSEDIA:

1. Contour Detection (View 1: Matplotlib 3-panel)
   - Deteksi kontur menggunakan OpenCV + Matplotlib
   - Menghasilkan Freeman Chain Code
   - Menampilkan 3 panel: asli, biner, kontur
   - ✅ Fix: Tidak lagi pakai cv2.imshow (avoid error)

2. Contour Detection (View 2: Matplotlib 4-panel + Text)
   - Sama seperti modul 1 dengan layout berbeda
   - Menampilkan 4 subplot: asli, biner, kontur, chain code text
   - Cocok untuk analisis detail dan dokumentasi

3. Canny Edge Detection
   - Deteksi tepi menggunakan algoritma Canny
   - Berguna untuk analisis retakan/crack
   - Parameter: Canny Low/High Threshold
   - Output: 3 panel (asli, blur, edges)

4. Integral Projection Analysis
   - Analisis proyeksi integral horizontal & vertikal
   - Berguna untuk segmentasi teks atau objek
   - Otomatis menggunakan Otsu thresholding
   - Layout: GridSpec dengan grafik proyeksi

FITUR BARU:
✅ UI Responsif - Window bisa di-resize (min: 800x600)
✅ No cv2.imshow - Semua pakai Matplotlib (avoid error)
✅ Auto-save - Simpan hasil dengan timestamp
✅ Preview auto-adjust - Gambar otomatis fit di preview area

PARAMETER:
- Threshold Binarisasi: Untuk kontur detection (0-255, default: 127)
- Canny Low Th: Tepi lemah (0-255, default: 50)
- Canny High Th: Tepi kuat (0-255, default: 150)

TIPS:
• Objek gelap + latar terang → threshold 127
• Objek terang + latar gelap → threshold ~80
• Noise tinggi → naikkan Canny threshold
• Detail halus → turunkan Canny threshold

TROUBLESHOOTING:
• Window tidak responsif → ✅ FIXED (resize freely!)
• cv2.imshow error → ✅ FIXED (now using Matplotlib)
• Import error → pip install opencv-python numpy matplotlib pillow

© 2025 - Digital Image Processing Praktikum Minggu 8
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Panduan Penggunaan v2.2")
        help_window.geometry("700x600")
        help_window.resizable(True, True)
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
        
        close_btn = ttk.Button(help_window, text="Tutup", command=help_window.destroy)
        close_btn.pack(pady=10)


def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    root = tk.Tk()
    app = ImageProcessingUI(root)
    
    # Welcome message
    app.log("Selamat datang di Image Processing Tool!")
    app.log("Silakan pilih gambar untuk memulai...")
    
    root.mainloop()


if __name__ == "__main__":
    main()
