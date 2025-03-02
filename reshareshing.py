import os
import datetime
import requests
import json
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
        'telegram', 'discord', 'github', 'dokumentasi', 'backer','feedback'
    ]

    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

    def get_field_value(field):
        file_path = os.path.join(FOLDER_NAME, f"{field}.txt")
        value = ""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                value = f.read().strip()
        else:
            value = input(f"Masukkan link {field.replace('_', ' ')}: ")
            with open(file_path, 'w') as f:
                f.write(value)
        return value

    def manual_inputs():
        print("\n" + "═"*40)
        # Ganti input manual dengan nilai default
        project_name = "Default Project"
        snapshot_date = datetime.datetime.now().strftime('%Y-%m-%d')
        listing_info = "Coming Soon TGE"
        print(f"├─ Nama Proyek\t\t: {project_name}")
        print(f"├─ Snapshot (YYYY-MM-DD)\t: {snapshot_date}")
        print(f"└─ Informasi Listing\t: {listing_info}")
        return project_name, snapshot_date, listing_info

    project_name, snapshot_date, listing_info = manual_inputs()
    data = [
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        project_name,
        *[get_field_value(field) for field in FILE_FIELDS],
        snapshot_date,
        listing_info
    ]
    return data

# ================================================================
# FUNGSI PENGIRIMAN
# ================================================================
async def send_telegram(summary):
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=summary,
        message_thread_id=int(TELEGRAM_THREAD_ID),
        parse_mode="Markdown"
    )

def send_to_sheets(data, sheet_name):
    payload = {
        "record": data,
        "sheetName": sheet_name
    }
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    return response.status_code

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
    print("\n" + "═"*40)
    print(" DROP X JUNGLER - RESHARESHING TOOLS ".center(40))
    print("═"*40)

    data = handle_reshareshing()

    # Format preview
    labels = [
        "Timestamp", "Nama Proyek", "Situs", "Roadmap", "Whitepaper",
        "Faucet", "Funding", "Block Explorer", "Informasi Team", "Twitter",
        "Telegram", "Discord", "Github", "Dokumentasi", "Backer",
        "Tanggal Snapshot", "Informasi Listing"
    ]
    preview_lines = [f"{label}: {value}" for label, value in zip(labels, data)]
    print_boxed("PREVIEW DATA RESHARESHING", preview_lines)

    # Pengiriman data langsung tanpa konfirmasi
    summary = "📋 **Ringkasan Data Reshareshing**\n\n" + "\n".join(
        [f"• **{label}**: {value}" for label, value in zip(labels, data)]
    )
    asyncio.run(send_telegram(summary))
    status = send_to_sheets(data, "reshareshing")
    print(f"\n✅ Status pengiriman: {'Berhasil' if status == 200 else 'Gagal'}!")

    # Feedback untuk pengembangan
    print("\n════════════[ MASUKAN UNTUK PENGEMBANGAN ]═════════════")
    print("Bantu kami meningkatkan kualitas tools ini dengan:")
 
    feedback = input("\n›› Masukan Anda (tekan Enter untuk skip): ")

    if feedback:
        with open("feedback.txt", "a") as f:
            f.write(f"[{datetime.datetime.now()}] {feedback}\n")
        print("🗳️ Terima kasih atas masukannya!")

if __name__ == '__main__':
    main()
