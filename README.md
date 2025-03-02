
# Reshareshing Tools

Reshareshing Tools adalah skrip Python command-line untuk mengumpulkan data proyek dan mengirimkannya ke Telegram serta Google Sheets.

## Fitur
- Pengumpulan data proyek dari input pengguna dan file konfigurasi
- Preview data sebelum pengiriman
- Pengiriman data otomatis ke Telegram dan Google Sheets
- Pengumpulan feedback pengguna

## Instalasi
1. **Clone repository ini.**
2. **Instal dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Buat file konfigurasi:**  
   Isi file berikut dengan informasi yang sesuai:
   - `token.txt` (Telegram Bot Token)
   - `idchat.txt` (Telegram Chat ID)
   - `threads.txt` (Telegram Thread ID)
   - `webhook.txt` (URL webhook Google Sheets)

   Pastikan file-file ini diabaikan dengan `.gitignore`.

## Penggunaan
Jalankan skrip dengan perintah:
```bash
python reshareshing.py
```

## Struktur Proyek
```
├── reshareshing.py         # Skrip utama
├── .gitignore              # File untuk mengabaikan file sensitif
├── token.txt               # Konfigurasi: Telegram Bot Token
├── idchat.txt              # Konfigurasi: Telegram Chat ID
├── threads.txt             # Konfigurasi: Telegram Thread ID
├── webhook.txt             # Konfigurasi: URL webhook untuk Google Sheets
├── requirements.txt        # Dependencies Python
└── data_reshareshing/      # Folder untuk menyimpan data proyek
```
```

Anda dapat mengupload README ini ke GitHub agar pengguna lain dapat memahami cara kerja dan penggunaan proyek ini.
