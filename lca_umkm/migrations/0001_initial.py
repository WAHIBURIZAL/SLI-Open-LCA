import django.db.models.deletion
from django.db import migrations, models


def seed_lca_data(apps, schema_editor):
    ProfilUMKM = apps.get_model("lca_umkm", "ProfilUMKM")
    FaktorEmisiInventory = apps.get_model("lca_umkm", "FaktorEmisiInventory")
    AktivitasProduksi = apps.get_model("lca_umkm", "AktivitasProduksi")

    profil = ProfilUMKM.objects.create(
        nama_umkm="UMKM Keripik Pisang Nusantara",
        jenis_usaha="Produksi makanan ringan",
        lokasi_usaha="Yogyakarta, Indonesia",
        produk_acuan="Keripik pisang",
        satuan_produk="kg",
        batas_sistem=(
            "Batas sistem sederhana: pembelian LPG sampai pemakaian energi panas "
            "untuk satu batch produksi keripik pisang."
        ),
    )
    faktor = FaktorEmisiInventory.objects.create(
        nama_inventory="Gas LPG",
        kategori_inventory="Energi proses penggorengan",
        satuan_inventory="kg",
        faktor_kg_co2e="3.0000",
        sumber_data="Dataset contoh studi kasus UMKM Indonesia",
        keterangan=(
            "Faktor emisi contoh untuk simulasi LCA sederhana. Nilai dapat disesuaikan "
            "dengan literatur atau data supplier yang digunakan."
        ),
    )
    AktivitasProduksi.objects.bulk_create([
        AktivitasProduksi(
            profil_umkm=profil,
            faktor_inventory=faktor,
            tanggal_produksi="2026-04-20",
            nama_batch="Batch Senin",
            jumlah_produk="48.00",
            jumlah_bahan_baku="80.00",
            produk_reject="4.00",
            jumlah_inventory="18.00",
            durasi_produksi_jam="6.00",
            biaya_inventory="324000.00",
            suhu_proses_c="165.00",
            metode_proses="penggorengan",
            pemasok_inventory="Agen LPG lokal",
            kualitas_data="primer",
            catatan_perbaikan="Pantau stabilitas suhu dan kapasitas wajan.",
            catatan="Data contoh untuk simulasi awal LCA.",
        ),
        AktivitasProduksi(
            profil_umkm=profil,
            faktor_inventory=faktor,
            tanggal_produksi="2026-04-24",
            nama_batch="Batch Jumat",
            jumlah_produk="55.00",
            jumlah_bahan_baku="88.00",
            produk_reject="3.50",
            jumlah_inventory="19.50",
            durasi_produksi_jam="6.50",
            biaya_inventory="351000.00",
            suhu_proses_c="165.00",
            metode_proses="penggorengan",
            pemasok_inventory="Agen LPG lokal",
            kualitas_data="primer",
            catatan_perbaikan="Pantau stabilitas suhu dan kapasitas wajan.",
            catatan="Data contoh untuk simulasi awal LCA.",
        ),
        AktivitasProduksi(
            profil_umkm=profil,
            faktor_inventory=faktor,
            tanggal_produksi="2026-04-27",
            nama_batch="Batch Senin Besar",
            jumlah_produk="62.00",
            jumlah_bahan_baku="96.00",
            produk_reject="4.20",
            jumlah_inventory="20.00",
            durasi_produksi_jam="7.00",
            biaya_inventory="360000.00",
            suhu_proses_c="165.00",
            metode_proses="penggorengan",
            pemasok_inventory="Agen LPG lokal",
            kualitas_data="primer",
            catatan_perbaikan="Pantau stabilitas suhu dan kapasitas wajan.",
            catatan="Data contoh untuk simulasi awal LCA.",
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
                ("nama_inventory", models.CharField(default="Gas LPG", max_length=100)),
                ("kategori_inventory", models.CharField(default="Energi proses penggorengan", max_length=80)),
                ("satuan_inventory", models.CharField(default="kg", max_length=30)),
                ("faktor_kg_co2e", models.DecimalField(decimal_places=4, default=3.0, max_digits=10)),
                ("sumber_data", models.CharField(default="Dataset contoh studi kasus UMKM Indonesia", max_length=180)),
                ("keterangan", models.TextField(default="Faktor emisi contoh untuk simulasi LCA sederhana. Nilai dapat disesuaikan dengan literatur atau data supplier yang digunakan.")),
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
                ("nama_umkm", models.CharField(default="UMKM Keripik Pisang Nusantara", max_length=120)),
                ("jenis_usaha", models.CharField(default="Produksi makanan ringan", max_length=120)),
                ("lokasi_usaha", models.CharField(default="Yogyakarta, Indonesia", max_length=160)),
                ("produk_acuan", models.CharField(default="Keripik pisang", max_length=100)),
                ("satuan_produk", models.CharField(default="kg", max_length=30)),
                ("batas_sistem", models.TextField(default="Batas sistem sederhana: pembelian LPG sampai pemakaian energi panas untuk satu batch produksi keripik pisang.")),
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
                ("jumlah_inventory", models.DecimalField(decimal_places=2, max_digits=10)),
                ("durasi_produksi_jam", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("biaya_inventory", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("suhu_proses_c", models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ("metode_proses", models.CharField(choices=[("penggorengan", "Penggorengan"), ("pemanggangan", "Pemanggangan"), ("pengeringan", "Pengeringan"), ("campuran", "Campuran")], default="penggorengan", max_length=30)),
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
