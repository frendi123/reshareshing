import os
import datetime
import requests
import asyncio
import telegram

# ================================================================
# KONFIGURASI
# ================================================================
def load_config(file):
    try:
        with open(file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: File {file} tidak ditemukan!")
        exit()

TELEGRAM_BOT_TOKEN = load_config('token.txt')
TELEGRAM_CHAT_ID = load_config('idchat.txt')
TELEGRAM_THREAD_ID = load_config('threads.txt')
WEBHOOK_URL = load_config('webhook.txt')  # URL webhook diambil dari file webhook.txt

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# ================================================================
# FUNGSI UTAMA (RESHARESHING)
# ================================================================
def handle_reshareshing():
    FOLDER_NAME = 'data_reshareshing'
    FILE_FIELDS = [
        'situs', 'roadmap', 'whitepiper', 'faucet', 'funding',
        'block_explorer', 'informasi_teamnya', 'twitter',
        'telegram', 'discord', 'github', 'dokumentasi', 'backer'
    ]
    MAIN_FIELDS = {
        "nama_proyek": "Masukkan Nama Proyek          : ",
        "snapshot": "Masukkan Snapshot (YYYY-MM-DD): ",
        "listing_info": "Masukkan Informasi Listing    : "
    }

    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

    # Tanyakan apakah menggunakan data baru
    use_new_data = input("Apakah anda pakai data baru? (y/n): ").strip().lower()
    if use_new_data == 'y':
        # Hapus file data lama
        for file in os.listdir(FOLDER_NAME):
            file_path = os.path.join(FOLDER_NAME, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Data lama telah dihapus, silakan masukkan data baru.\n")
        force_prompt = True  # Selalu minta input untuk data utama
    elif use_new_data == 'n':
        print("Menggunakan data yang sudah ada (jika tersedia)")
        force_prompt = False  # Gunakan data yang sudah ada jika ada
    else:
        print("Input tidak dikenali, menggunakan data yang sudah ada (jika tersedia)")
        force_prompt = False

    # Fungsi untuk field utama
    def get_main_field_value(field, prompt, force_prompt):
        file_path = os.path.join(FOLDER_NAME, f"{field}.txt")
        if os.path.exists(file_path):
            if force_prompt:
                new_value = input(prompt).strip()
                if new_value:
                    with open(file_path, 'w') as f:
                        f.write(new_value)
                    return new_value
                else:
                    with open(file_path, 'r') as f:
                        return f.read().strip()
            else:
                with open(file_path, 'r') as f:
                    return f.read().strip()
        else:
            value = input(prompt).strip()
            with open(file_path, 'w') as f:
                f.write(value)
            return value

    # Jika force_prompt True, prompt akan muncul; jika tidak, langsung ambil nilai yang ada
    project_name = get_main_field_value("nama_proyek", MAIN_FIELDS["nama_proyek"], force_prompt)
    snapshot_date = get_main_field_value("snapshot", MAIN_FIELDS["snapshot"], force_prompt)
    listing_info = get_main_field_value("listing_info", MAIN_FIELDS["listing_info"], force_prompt)

    def get_field_value(field):
        file_path = os.path.join(FOLDER_NAME, f"{field}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read().strip()
        else:
            value = input(f"Masukkan link {field.replace('_', ' ')}: ").strip()
            with open(file_path, 'w') as f:
                f.write(value)
            return value

    field_values = [get_field_value(field) for field in FILE_FIELDS]

    # Input feedback: tampilkan prompt langsung
    feedback = input("\n›› Masukan Feedback Anda (tekan Enter untuk skip): ").strip()

    # Susun data: total 18 elemen 
    # (timestamp, nama proyek, 13 field, snapshot, listing info, feedback)
    data = [
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        project_name,
        *field_values,
        snapshot_date,
        listing_info,
        feedback
    ]
    return data, FILE_FIELDS

# ================================================================
# FUNGSI PENGIRIMAN
# ================================================================
async def send_telegram(summary):
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=summary,
        message_thread_id=int(TELEGRAM_THREAD_ID),
        parse_mode="HTML"  # Menggunakan HTML sebagai parse mode
    )

def send_to_sheets(data, sheet_name):
    payload = {
        "record": data,
        "sheetName": sheet_name
    }
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print("Response dari webhook:", response.text)
        return response.status_code
    except Exception as e:
        print("Error saat mengirim ke Google Sheets:", e)
        return None

# ================================================================
# TAMPILAN UTAMA
# ================================================================
def print_boxed(title, lines):
    max_length = max(len(line) for line in lines) if lines else 0
    max_length = max(max_length, len(title), 40)
    separator = '═' * (max_length + 2)

    print(f"\n╔{separator}╗")
    print(f"║ {title.center(max_length)} ║")
    print(f"╠{separator}╣")
    for line in lines:
        print(f"║ {line.ljust(max_length)} ║")
    print(f"╚{separator}╝")

def main():
    print("\n" + "═" * 40)
    print(" DROPXJUNGLER - RESHARESHING TOOLS ".center(40))
    print("═" * 40)

    while True:
        data, file_fields = handle_reshareshing()

        labels = (
            ["Timestamp", "Nama Proyek"] +
            [field.capitalize().replace('_', ' ') for field in file_fields] +
            ["Tanggal Snapshot", "Informasi Listing", "Feedback"]
        )

        preview_lines = [f"{label}: {value}" for label, value in zip(labels, data)]
        print_boxed("PREVIEW DATA RESHARESHING", preview_lines)

        confirm = input("Apakah anda yakin (y/n): ").strip().lower()
        if confirm == 'y':
            break
        else:
            print("\nMengulang input data...\n")

    # Mengubah summary menjadi format HTML
    summary = "📋 <b>Ringkasan Data Reshareshing</b>\n\n" + "\n".join(
        [f"• <b>{label}</b>: {value}" for label, value in zip(labels, data)]
    )
    asyncio.run(send_telegram(summary))
    status = send_to_sheets(data, "reshareshing")
    print(f"\n✅ Status pengiriman: {'Berhasil' if status == 200 else 'Gagal'}!")

if __name__ == '__main__':
    main()
