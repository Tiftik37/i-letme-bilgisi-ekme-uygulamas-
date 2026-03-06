import os
import sys

# 1. KRİTİK AYAR: Tarayıcıları sistemin ana klasörüne kurması için
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

import time
import threading
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from playwright.sync_api import sync_playwright

class MapsScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KMT Dijital - Maps Scraper Pro (v4.0 Final)")
        self.root.geometry("850x700")
        
        # Stil
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=25, font=('Calibri', 10))
        style.configure("Treeview.Heading", font=('Calibri', 11, 'bold'))
        
        # --- ÜST MENÜ ---
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        setup_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="⚙️ Kurulum & Ayarlar", menu=setup_menu)
        setup_menu.add_command(label="Gerekli Tarayıcıları Yükle (Zorunlu)", command=self.install_browsers)
        setup_menu.add_separator()
        setup_menu.add_command(label="Hakkında", command=lambda: messagebox.showinfo("KMT", "Maps Scraper Pro v4.0"))

        # --- GİRİŞLER ---
        frame_top = ttk.LabelFrame(root, text="Arama Kriterleri", padding=10)
        frame_top.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_top, text="Sektör:").grid(row=0, column=0, padx=5, sticky="w")
        self.entry_sector = ttk.Entry(frame_top, width=25)
        self.entry_sector.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_top, text="Şehir/Bölge:").grid(row=0, column=2, padx=5, sticky="w")
        self.entry_city = ttk.Entry(frame_top, width=25)
        self.entry_city.grid(row=0, column=3, padx=5)
        
        ttk.Label(frame_top, text="Hedef Sayı:").grid(row=1, column=0, padx=5, sticky="w", pady=10)
        self.entry_count = ttk.Entry(frame_top, width=10)
        self.entry_count.insert(0, "50")
        self.entry_count.grid(row=1, column=1, padx=5, sticky="w")
        
        ttk.Label(frame_top, text="Tel Filtresi (Örn: 05):").grid(row=1, column=2, padx=5, sticky="w")
        self.entry_filter = ttk.Entry(frame_top, width=15)
        self.entry_filter.grid(row=1, column=3, padx=5, sticky="w")
        
        # --- TABLO ---
        frame_list = ttk.Frame(root)
        frame_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("sıra", "firma", "telefon", "puan", "durum")
        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("sıra", text="#")
        self.tree.column("sıra", width=40, anchor="center")
        self.tree.heading("firma", text="İşletme Adı")
        self.tree.column("firma", width=300)
        self.tree.heading("telefon", text="Telefon")
        self.tree.column("telefon", width=150, anchor="center")
        self.tree.heading("puan", text="Yıldız")
        self.tree.column("puan", width=80, anchor="center")
        self.tree.heading("durum", text="Durum")
        self.tree.column("durum", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- LOG ---
        frame_log = ttk.LabelFrame(root, text="İşlem Logları", padding=5)
        frame_log.pack(fill="x", padx=10, pady=5)
        self.log_box = tk.Text(frame_log, height=4, font=("Consolas", 8), state="disabled", bg="#f0f0f0")
        self.log_box.pack(fill="x")

        # --- BUTONLAR ---
        frame_bottom = ttk.Frame(root)
        frame_bottom.pack(fill="x", padx=10, pady=10)
        
        self.lbl_status = ttk.Label(frame_bottom, text="Hazır - İlk kullanımda menüden kurulum yapın.", font=("Arial", 9, "italic"), foreground="blue")
        self.lbl_status.pack(side="left", padx=5)
        
        self.btn_export = ttk.Button(frame_bottom, text="Excel'e Aktar", command=self.export_excel, state="disabled")
        self.btn_export.pack(side="right", padx=5)
        
        self.btn_start = ttk.Button(frame_bottom, text="BAŞLAT", command=self.start_thread)
        self.btn_start.pack(side="right", padx=5)
        
        self.scraped_data = []
        self.is_running = False

    def log_msg(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f">> {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def install_browsers(self):
        """EXE içinden kurulum yapan yeni fonksiyon"""
        response = messagebox.askyesno("Kurulum", "Gerekli tarayıcı dosyaları indirilecek (Yaklaşık 150MB).\n\nBu işlem internet hızına göre 1-3 dakika sürebilir.\nProgram bu sırada yanıt vermiyor gibi görünebilir, LÜTFEN KAPATMAYIN.\n\nBaşlatılsın mı?")
        
        if response:
            self.lbl_status.config(text="⬇️ İndiriliyor... Lütfen bekleyin.", foreground="red")
            self.log_msg("Kurulum başlatıldı... Bekleyiniz.")
            self.root.update() 

            def run_internal_install():
                try:
                    # EXE içindeki Playwright modülünü manuel çağırıyoruz
                    from playwright.__main__ import main as pw_cli
                    
                    # Sistemi kandırıp sanki komut satırına yazmışız gibi yapıyoruz
                    sys.argv = ["playwright", "install", "chromium"]
                    
                    try:
                        pw_cli() # Kurulumu başlatır
                    except SystemExit:
                        pass # İşlem bitince kod çıkış yapmak ister, bunu engelliyoruz
                    except Exception as e:
                        raise e
                    
                    # Başarılı olursa
                    self.root.after(0, lambda: messagebox.showinfo("Başarılı", "Kurulum Tamamlandı!\nProgramı kullanabilirsiniz."))
                    self.root.after(0, lambda: self.lbl_status.config(text="Hazır - Tarayıcı Yüklendi.", foreground="green"))
                    self.root.after(0, lambda: self.log_msg("Kurulum başarıyla bitti."))
                    
                except Exception as e:
                    err_msg = str(e)
                    self.root.after(0, lambda: messagebox.showerror("Hata", f"Kurulum hatası:\n{err_msg}"))
                    self.root.after(0, lambda: self.log_msg(f"KURULUM HATASI: {err_msg}"))
            
            threading.Thread(target=run_internal_install, daemon=True).start()

    def start_thread(self):
        if self.is_running: return
        
        sector = self.entry_sector.get().strip()
        city = self.entry_city.get().strip()
        
        if not sector or not city:
            messagebox.showwarning("Hata", "Sektör ve Şehir alanları zorunludur!")
            return
            
        self.is_running = True
        self.btn_start.config(state="disabled")
        self.btn_export.config(state="disabled")
        self.scraped_data = [] 
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        t = threading.Thread(target=self.run_scraper)
        t.start()

    def add_to_table(self, name, phone, rating, status="Eklendi"):
        row_id = len(self.scraped_data) + 1
        self.scraped_data.append({
            "İşletme Adı": name,
            "Telefon": phone,
            "Puan": rating,
            "Bölge": self.entry_city.get()
        })
        self.tree.insert("", "end", values=(row_id, name, phone, rating, status))
        self.tree.yview_moveto(1)

    def run_scraper(self):
        try:
            sector = self.entry_sector.get()
            city = self.entry_city.get()
            try:
                target = int(self.entry_count.get())
            except:
                target = 50
            phone_filter = self.entry_filter.get().strip()
            full_query = f"{sector} {city}"
            
            self.lbl_status.config(text=f"Harita açılıyor... ({full_query})")
            self.log_msg(f"İşlem başladı: {full_query}")
            
            processed_links = set()
            processed_identities = set()
            
            try:
                with sync_playwright() as p:
                    try:
                        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
                    except Exception as e:
                        raise Exception("Tarayıcı bulunamadı! Lütfen üst menüden 'Kurulum & Ayarlar' -> 'Gerekli Tarayıcıları Yükle' yapın.")

                    context = browser.new_context(locale="tr-TR")
                    page = context.new_page()
                    
                    page.goto("https://www.google.com/maps?hl=tr", timeout=60000)
                    time.sleep(2)
                    
                    try:
                        if page.get_by_text("Tümünü kabul et").count() > 0:
                            page.get_by_text("Tümünü kabul et").click()
                        elif page.locator("form[action*='consent'] button").count() > 0:
                            page.locator("form[action*='consent'] button").first.click()
                    except: pass

                    try:
                        self.lbl_status.config(text="Arama yapılıyor...")
                        search_box = page.locator("input#searchboxinput")
                        if search_box.count() == 0:
                            search_box = page.locator("input[name='q']")
                        
                        search_box.fill(full_query)
                        time.sleep(1)
                        page.keyboard.press("Enter")
                        page.wait_for_selector('div[role="feed"]', timeout=20000)
                    except Exception as e:
                        self.log_msg(f"Arama hatası: {e}")
                        browser.close()
                        return

                    self.lbl_status.config(text="Veri toplanıyor...")
                    consecutive_fails = 0
                    
                    while len(self.scraped_data) < target:
                        feed = page.locator('div[role="feed"]')
                        listings = feed.locator('a.hfpxzc').all()
                        feed.evaluate("element => element.scrollTop = element.scrollHeight")
                        time.sleep(2.5)
                        
                        added_count_loop = 0
                        for item in listings:
                            if len(self.scraped_data) >= target: break
                            link = item.get_attribute("href")
                            if not link or link in processed_links: continue
                            processed_links.add(link)
                            
                            try:
                                item.click()
                                time.sleep(1.5)
                                name_el = page.locator('h1.DUwDvf')
                                name = name_el.first.inner_text().strip() if name_el.count() > 0 else "İsimsiz"
                                
                                phone = "Yok"
                                phone_btn = page.locator('button[data-item-id^="phone:"]')
                                if phone_btn.count() > 0:
                                    phone = phone_btn.first.inner_text().strip()
                                
                                clean_check_phone = phone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
                                identity_key = (name, clean_check_phone)
                                if identity_key in processed_identities: continue
                                
                                rating = "-"
                                rating_el = page.locator('div.F7nice span[aria-hidden="true"]').first
                                if rating_el.count() > 0:
                                    rating = rating_el.inner_text().split("(")[0].strip()

                                if phone_filter:
                                    clean_p = phone.replace(" ", "")
                                    if not clean_p.startswith(phone_filter): continue
                                    if phone == "Yok": continue
                                
                                processed_identities.add(identity_key)
                                self.add_to_table(name, phone, rating)
                                self.log_msg(f"Eklendi: {name}")
                                added_count_loop += 1
                                consecutive_fails = 0
                            except: continue
                            
                        if added_count_loop == 0:
                            consecutive_fails += 1
                            self.lbl_status.config(text=f"Veri aranıyor... ({consecutive_fails}/4)")
                            time.sleep(2)
                            if consecutive_fails > 4: break
                                
                    browser.close()
                    self.lbl_status.config(text=f"Bitti! Toplam {len(self.scraped_data)} kayıt.")
                    messagebox.showinfo("İşlem Tamam", "Hedeflenen sayıya ulaşıldı.")
            except Exception as e:
                err = str(e)
                self.log_msg(f"KRİTİK HATA: {err}")
                if "Executable doesn't exist" in err or "Tarayıcı bulunamadı" in err:
                     messagebox.showerror("Tarayıcı Eksik", "Chrome tarayıcısı bulunamadı.\nLütfen 'Kurulum & Ayarlar' menüsünden yükleme yapın.")
                else:
                     messagebox.showerror("Hata", f"Hata oluştu:\n{err}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))
        finally:
            self.is_running = False
            self.btn_start.config(state="normal")
            self.btn_export.config(state="normal")

    def export_excel(self):
        if not self.scraped_data:
            messagebox.showwarning("Uyarı", "Veri yok!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], initialfile=f"GoogleMaps_Listesi.xlsx")
        if file_path:
            try:
                df = pd.DataFrame(self.scraped_data)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Başarılı", "Kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Kaydedilemedi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapsScraperApp(root)
    root.mainloop()