from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lca_umkm", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="biaya_inventory",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="catatan_perbaikan",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="durasi_produksi_jam",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="jumlah_bahan_baku",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="kualitas_data",
            field=models.CharField(choices=[("primer", "Data primer"), ("estimasi", "Estimasi lapangan"), ("sekunder", "Data sekunder")], default="primer", max_length=30),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="metode_proses",
            field=models.CharField(choices=[("penggorengan", "Penggorengan"), ("pemanggangan", "Pemanggangan"), ("pengeringan", "Pengeringan"), ("campuran", "Campuran")], default="penggorengan", max_length=30),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="pemasok_inventory",
            field=models.CharField(blank=True, default="", max_length=120),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="produk_reject",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="aktivitasproduksi",
            name="suhu_proses_c",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
