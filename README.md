# LCA UMKM Indonesia

Aplikasi Django sederhana yang meniru alur dasar OpenLCA untuk studi kasus UMKM Indonesia. Project ini hanya berisi modul LCA: database inventory, aktivitas produksi, algoritma perhitungan dampak, hotspot, dan interpretasi hasil.

## Studi Kasus

- UMKM: Es Degan Mak DEG
- Produk acuan: 1 porsi es degan 500 ml
- Batas sistem: cradle-to-gate sederhana
- Inventory utama: Gelas plastik PP sekali pakai
- Kategori dampak: emisi gas rumah kaca dalam kg CO2e
- Functional unit: 1 porsi produk

## Algoritma

```text
emisi_kg_co2e = jumlah_inventory x faktor_kg_co2e
intensitas = total_emisi_kg_co2e / total_produk
kontribusi_batch = emisi_batch / total_emisi x 100
total_berat_plastik = jumlah_gelas x berat_per_gelas
```

## Halaman

- `/` dashboard LCA
- `/database/` pengaturan profil UMKM dan faktor emisi inventory
- `/admin/` Django Admin

## Menjalankan

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deploy ke Vercel

Project sudah menyertakan `vercel.json`, `runtime.txt`, dan `.vercelignore`.

Langkah deploy:

```powershell
vercel
```

Untuk production, isi environment variable berikut di dashboard Vercel:

```text
DJANGO_SECRET_KEY=isi-secret-key-sendiri
DJANGO_DEBUG=False
```

Catatan: Vercel memakai serverless function, sehingga SQLite hanya cocok untuk demo. Aplikasi ini otomatis membuat database SQLite sementara di `/tmp/db.sqlite3` saat cold start agar halaman tidak error. Data input di Vercel dapat hilang saat instance berganti. Untuk data permanen, gunakan database eksternal seperti PostgreSQL.
