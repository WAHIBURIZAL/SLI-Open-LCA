# LCA UMKM Indonesia

Aplikasi Django sederhana yang meniru alur dasar OpenLCA untuk studi kasus UMKM Indonesia. Project ini hanya berisi modul LCA: database inventory, aktivitas produksi, algoritma perhitungan dampak, dan dashboard hasil.

## Studi Kasus

- UMKM: produksi keripik pisang
- Inventory utama: Gas LPG
- Kategori dampak: emisi gas rumah kaca dalam kg CO2e
- Functional unit: 1 kg produk

## Algoritma

```text
emisi_kg_co2e = jumlah_inventory x faktor_kg_co2e
intensitas = total_emisi_kg_co2e / total_produk
kontribusi_batch = emisi_batch / total_emisi x 100
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
