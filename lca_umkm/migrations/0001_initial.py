import django.db.models.deletion
from django.db import migrations, models


def seed_lca_data(apps, schema_editor):
    ProfilUMKM = apps.get_model("lca_umkm", "ProfilUMKM")
    FaktorEmisiInventory = apps.get_model("lca_umkm", "FaktorEmisiInventory")
    AktivitasProduksi = apps.get_model("lca_umkm", "AktivitasProduksi")

    profil = ProfilUMKM.objects.create(
        nama_umkm="Es Degan Mak DEG",
        jenis_usaha="UMKM minuman es kelapa muda",
        lokasi_usaha="Jl. Terusan Bendungan Sigura-gura, Malang",
        produk_acuan="Es degan 500 ml",
        satuan_produk="porsi",
        batas_sistem=(
            "Batas sistem cradle-to-gate sederhana: pengadaan gelas plastik PP "
            "sampai produk es degan 500 ml siap disajikan kepada konsumen."
        ),
    )
    faktor = FaktorEmisiInventory.objects.create(
        nama_inventory="Gelas plastik PP sekali pakai",
        kategori_inventory="Kemasan plastik",
        satuan_inventory="kg",
        faktor_kg_co2e="3.6310",
        sumber_data="Estimasi LCA SLI Kelompok 3 dari hotspot kemasan plastik",
        keterangan=(
            "Faktor emisi disederhanakan dari kontribusi kemasan plastik pada analisis "
            "GWP produk es degan. Nilai ini digunakan sebagai database satu inventory."
        ),
    )
    AktivitasProduksi.objects.bulk_create([
        AktivitasProduksi(
            profil_umkm=profil,
            faktor_inventory=faktor,
            tanggal_produksi="2026-05-01",
            nama_batch="Operasional 2 Hari A",
            jumlah_produk="1000.00",
            jumlah_bahan_baku="200.00",
            produk_reject="10.00",
            jumlah_unit_inventory="1000.00",
            berat_per_unit_inventory_kg="0.0100",
            jumlah_inventory="10.00",
            durasi_produksi_jam="16.00",
            biaya_inventory="350000.00",
            pemasok_inventory="Toko kemasan Malang",
            kualitas_data="primer",
            catatan_perbaikan="Kurangi gelas plastik sekali pakai atau evaluasi alternatif biodegradable.",
            catatan="Data contoh berdasarkan konsumsi gelas plastik sekitar 1.000 unit per dua hari.",
        ),
        AktivitasProduksi(
            profil_umkm=profil,
            faktor_inventory=faktor,
            tanggal_produksi="2026-05-03",
            nama_batch="Operasional 2 Hari B",
            jumlah_produk="920.00",
            jumlah_bahan_baku="185.00",
            produk_reject="12.00",
            jumlah_unit_inventory="920.00",
            berat_per_unit_inventory_kg="0.0100",
            jumlah_inventory="9.20",
            durasi_produksi_jam="15.00",
            biaya_inventory="322000.00",
            pemasok_inventory="Toko kemasan Malang",
            kualitas_data="primer",
            catatan_perbaikan="Catat defect gelas dan mulai uji pemilahan limbah plastik.",
            catatan="Data contoh berdasarkan operasional minuman es kelapa muda.",
        ),
        AktivitasProduksi(
            profil_umkm=profil,
            faktor_inventory=faktor,
            tanggal_produksi="2026-05-05",
            nama_batch="Operasional 2 Hari C",
            jumlah_produk="1080.00",
            jumlah_bahan_baku="215.00",
            produk_reject="8.00",
            jumlah_unit_inventory="1080.00",
            berat_per_unit_inventory_kg="0.0100",
            jumlah_inventory="10.80",
            durasi_produksi_jam="17.00",
            biaya_inventory="378000.00",
            pemasok_inventory="Toko kemasan Malang",
            kualitas_data="primer",
            catatan_perbaikan="Prioritaskan skenario kemasan biodegradable untuk penjualan ramai.",
            catatan="Data contoh berdasarkan operasional minuman es kelapa muda.",
        ),
    ])


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FaktorEmisiInventory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama_inventory", models.CharField(default="Gelas plastik PP sekali pakai", max_length=100)),
                ("kategori_inventory", models.CharField(default="Kemasan plastik", max_length=80)),
                ("satuan_inventory", models.CharField(default="kg", max_length=30)),
                ("faktor_kg_co2e", models.DecimalField(decimal_places=4, default=3.631, max_digits=10)),
                ("sumber_data", models.CharField(default="Estimasi LCA SLI Kelompok 3 dari hotspot kemasan plastik", max_length=180)),
                ("keterangan", models.TextField(default="Faktor emisi disederhanakan dari kontribusi kemasan plastik pada analisis GWP produk es degan. Nilai ini digunakan sebagai database satu inventory.")),
            ],
            options={
                "verbose_name": "Faktor Emisi Inventory",
                "verbose_name_plural": "Faktor Emisi Inventory",
            },
        ),
        migrations.CreateModel(
            name="ProfilUMKM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama_umkm", models.CharField(default="Es Degan Mak DEG", max_length=120)),
                ("jenis_usaha", models.CharField(default="UMKM minuman es kelapa muda", max_length=120)),
                ("lokasi_usaha", models.CharField(default="Jl. Terusan Bendungan Sigura-gura, Malang", max_length=160)),
                ("produk_acuan", models.CharField(default="Es degan 500 ml", max_length=100)),
                ("satuan_produk", models.CharField(default="porsi", max_length=30)),
                ("batas_sistem", models.TextField(default="Batas sistem cradle-to-gate sederhana: pengadaan gelas plastik PP sampai produk es degan 500 ml siap disajikan kepada konsumen.")),
            ],
            options={
                "verbose_name": "Profil UMKM",
                "verbose_name_plural": "Profil UMKM",
            },
        ),
        migrations.CreateModel(
            name="AktivitasProduksi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tanggal_produksi", models.DateField()),
                ("nama_batch", models.CharField(max_length=100)),
                ("jumlah_produk", models.DecimalField(decimal_places=2, max_digits=10)),
                ("jumlah_bahan_baku", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("produk_reject", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("jumlah_unit_inventory", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("berat_per_unit_inventory_kg", models.DecimalField(decimal_places=4, default=0.01, max_digits=10)),
                ("jumlah_inventory", models.DecimalField(decimal_places=2, max_digits=10)),
                ("durasi_produksi_jam", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("biaya_inventory", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("pemasok_inventory", models.CharField(blank=True, default="", max_length=120)),
                ("kualitas_data", models.CharField(choices=[("primer", "Data primer"), ("estimasi", "Estimasi lapangan"), ("sekunder", "Data sekunder")], default="primer", max_length=30)),
                ("catatan_perbaikan", models.TextField(blank=True, default="")),
                ("catatan", models.TextField(blank=True, default="")),
                ("dibuat_pada", models.DateTimeField(auto_now_add=True)),
                ("faktor_inventory", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="lca_umkm.faktoremisiinventory")),
                ("profil_umkm", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lca_umkm.profilumkm")),
            ],
            options={
                "verbose_name": "Aktivitas Produksi",
                "verbose_name_plural": "Aktivitas Produksi",
                "ordering": ["-tanggal_produksi", "-id"],
            },
        ),
        migrations.RunPython(seed_lca_data, migrations.RunPython.noop),
    ]
