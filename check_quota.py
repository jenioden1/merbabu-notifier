import requests
import os
from datetime import datetime

# ============================================================
# KONFIGURASI — isi ini sebelum deploy
# ============================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")

JALUR_TARGET = "Suwanting"
BULAN_TARGET = "April"   # bisa ganti "Mei", "Juni", dst
TAHUN_TARGET = "2026"

# Halaman cek kuota publik (tidak perlu login)
URL_CEK_KUOTA = "https://booking.tngunungmerbabu.org/app/index.php/cek_kuota/list"

# ============================================================


def send_telegram(message: str):
    """Kirim pesan ke Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    print(f"[✓] Notif Telegram terkirim: {resp.status_code}")


def cek_kuota() -> bool:
    """
    Scrape halaman cek_kuota/list yang bisa diakses publik (tanpa login).
    Kembalikan True jika kuota jalur+bulan target ditemukan di halaman.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(URL_CEK_KUOTA, headers=headers, timeout=20)
        resp.raise_for_status()
        html = resp.text.lower()

        print(f"[i] Halaman berhasil diakses ({len(html)} chars)")

        # Deteksi: apakah jalur + bulan target muncul di halaman?
        jalur_ok = JALUR_TARGET.lower() in html
        bulan_ok = BULAN_TARGET.lower() in html
        tahun_ok = TAHUN_TARGET in html

        print(f"[i] Jalur '{JALUR_TARGET}' ditemukan : {jalur_ok}")
        print(f"[i] Bulan  '{BULAN_TARGET}' ditemukan : {bulan_ok}")
        print(f"[i] Tahun  '{TAHUN_TARGET}'  ditemukan : {tahun_ok}")

        return jalur_ok and bulan_ok and tahun_ok

    except requests.RequestException as e:
        # Jangan crash — cukup log error, tidak kirim notif (biar ga spam)
        print(f"[!] Gagal fetch halaman: {e}")
        print("[!] Script akan coba lagi di run berikutnya.")
        return False


def main():
    print(f"[*] Cek kuota Merbabu via {JALUR_TARGET} untuk {BULAN_TARGET} {TAHUN_TARGET}...")
    print(f"[*] Waktu: {datetime.now().strftime('%d %b %Y %H:%M')} WIB")
    print(f"[*] URL  : {URL_CEK_KUOTA}")

    kuota_tersedia = cek_kuota()

    if kuota_tersedia:
        pesan = (
            f"🏔️ <b>KUOTA MERBABU SUDAH BUKA!</b>\n\n"
            f"✅ Jalur <b>{JALUR_TARGET}</b> — <b>{BULAN_TARGET} {TAHUN_TARGET}</b> "
            f"sudah tersedia!\n\n"
            f"🔗 Langsung booking di:\n"
            f"<a href='https://booking.tngunungmerbabu.org/app/'>booking.tngunungmerbabu.org</a>\n\n"
            f"⏰ Jangan telat, kuota cepat habis!\n"
            f"🕐 Dicek: {datetime.now().strftime('%d %b %Y %H:%M')} WIB"
        )
        send_telegram(pesan)
        print("[✓] Kuota TERSEDIA — notifikasi terkirim!")
    else:
        print(f"[-] Kuota {BULAN_TARGET} jalur {JALUR_TARGET} belum tersedia. Coba lagi nanti.")


if __name__ == "__main__":
    main()
