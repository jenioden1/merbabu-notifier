# 🏔️ Merbabu Quota Notifier — via Telegram + GitHub Actions

Auto-notifikasi Telegram ketika kuota pendakian **Gunung Merbabu via Suwanting** bulan **April 2026** sudah dibuka di [booking.tngunungmerbabu.org](https://booking.tngunungmerbabu.org/app/).

---

## ⚡ Cara Setup (5–10 menit)

### Langkah 1 — Buat Telegram Bot

1. Buka Telegram, cari **@BotFather**
2. Ketik `/newbot`
3. Ikuti instruksinya, kasih nama bot sesuka kamu (misal: `MerbabuNotifier`)
4. BotFather akan kasih **Bot Token** — simpan, bentuknya:  
   `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`

### Langkah 2 — Dapatkan Chat ID kamu

1. Cari bot **@userinfobot** di Telegram
2. Klik Start / ketik `/start`
3. Bot akan balas dengan **Id** kamu (angka, misal: `987654321`)
4. Simpan angka itu — ini adalah `TELEGRAM_CHAT_ID` kamu

### Langkah 3 — Upload ke GitHub

1. Buat repo baru di GitHub (boleh private)
2. Upload semua file ini ke repo:
   ```
   check_quota.py
   .github/workflows/check_quota.yml
   ```
3. Pastikan struktur foldernya seperti ini:
   ```
   repo/
   ├── check_quota.py
   └── .github/
       └── workflows/
           └── check_quota.yml
   ```

### Langkah 4 — Tambahkan Secrets di GitHub

1. Buka repo di GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Klik **New repository secret**, tambahkan 2 secret:

   | Name | Value |
   |------|-------|
   | `TELEGRAM_BOT_TOKEN` | Token dari BotFather |
   | `TELEGRAM_CHAT_ID` | ID kamu dari @userinfobot |

### Langkah 5 — Test manual

1. Buka tab **Actions** di repo GitHub kamu
2. Klik workflow **🏔️ Merbabu Quota Checker**
3. Klik **Run workflow** → **Run workflow**
4. Lihat log apakah berhasil

---

## ⏰ Jadwal Pengecekan

Script akan otomatis jalan **setiap 30 menit**, antara jam **07.00 – 22.00 WIB**.

> **Catatan:** GitHub Actions kadang delay 5–10 menit dari jadwal cron. Ini normal.

---

## 🔧 Kustomisasi

Edit bagian ini di `check_quota.py` kalau mau ganti pengaturan:

```python
JALUR_TARGET = "Suwanting"   # ganti jalur kalau perlu
BULAN_TARGET = "April"       # ganti bulan target
TAHUN_TARGET = "2026"
```

---

## 📩 Notif yang akan diterima

Kalau kuota sudah buka, kamu langsung dapat pesan Telegram seperti ini:

```
🏔️ KUOTA MERBABU SUDAH BUKA!

✅ Jalur Suwanting — April 2026 sudah tersedia!

🔗 Langsung booking di:
booking.tngunungmerbabu.org

⏰ Jangan telat, kuota cepat habis!
🕐 Dicek: 15 Mar 2026 09:30 WIB
```

---

## ❓ FAQ

**Q: Apakah ini 100% akurat?**  
A: Script mendeteksi kata kunci dari halaman website. Kalau website berubah struktur, mungkin perlu update script-nya. Tapi buat deteksi basic ini sudah cukup andal.

**Q: Apakah GitHub Actions gratis?**  
A: Ya, gratis untuk repo public maupun private (limit 2.000 menit/bulan — ini jauh lebih dari cukup).

**Q: Bagaimana kalau saya mau stop?**  
A: Buka tab Actions → klik workflow → **Disable workflow**.
