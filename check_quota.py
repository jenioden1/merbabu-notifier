import requests
import os
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")

JALUR_TARGET = "Suwanting"
BULAN_TARGET = "04"
TAHUN_TARGET = "2026"

URL_CEK_KUOTA = (
    f"https://booking.tngunungmerbabu.org/app/index.php/"
    f"cek_kuota/list?bulan={BULAN_TARGET}&tahun={TAHUN_TARGET}"
)

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    print(f"[✓] Notif terkirim")

def cek_kuota() -> bool:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(URL_CEK_KUOTA, headers=headers, timeout=20)
        resp.raise_for_status()
        html = resp.text.lower()
        print(f"[i] Halaman diakses ({len(html)} chars)")
        if "data tidak ditemukan" in html:
            print("[-] April belum dibuka")
            return False
        jalur_ok = JALUR_TARGET.lower() in html
        print(f"[i] Suwanting ditemukan: {jalur_ok}")
        return jalur_ok
    except requests.RequestException as e:
        print(f"[!] Gagal fetch: {e}")
        return False

def main():
    print(f"[*] {datetime.now().strftime('%d %b %Y %H:%M')} WIB — cek kuota April {TAHUN_TARGET} jalur {JALUR_TARGET}")
    if cek_kuota():
        send_telegram(
            f"🏔️ <b>KUOTA MERBABU APRIL 2026 SUDAH BUKA!</b>\n\n"
            f"✅ Jalur <b>{JALUR_TARGET}</b> sudah tersedia!\n\n"
            f"🔗 <a href='https://booking.tngunungmerbabu.org/app/'>booking.tngunungmerbabu.org</a>\n\n"
            f"⏰ Jangan telat, kuota cepat habis!\n"
            f"🕐 {datetime.now().strftime('%d %b %Y %H:%M')} WIB"
        )
    else:
        print("[-] Belum tersedia. Cek lagi 20 menit.")

if __name__ == "__main__":
    main()
