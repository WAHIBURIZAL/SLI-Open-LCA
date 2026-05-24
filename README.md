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
