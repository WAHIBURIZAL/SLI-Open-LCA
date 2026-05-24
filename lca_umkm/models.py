from django.db import models


class ProfilUMKM(models.Model):
    nama_umkm = models.CharField(max_length=120, default="UMKM Keripik Pisang Nusantara")
    jenis_usaha = models.CharField(max_length=120, default="Produksi makanan ringan")
    lokasi_usaha = models.CharField(max_length=160, default="Yogyakarta, Indonesia")
    produk_acuan = models.CharField(max_length=100, default="Keripik pisang")
    satuan_produk = models.CharField(max_length=30, default="kg")
    batas_sistem = models.TextField(
        default=(
            "Batas sistem sederhana: pembelian LPG sampai pemakaian energi panas "
            "untuk satu batch produksi keripik pisang."
        )
    )

    class Meta:
        verbose_name = "Profil UMKM"
        verbose_name_plural = "Profil UMKM"

    def __str__(self):
        return self.nama_umkm


class FaktorEmisiInventory(models.Model):
    nama_inventory = models.CharField(max_length=100, default="Gas LPG")
    kategori_inventory = models.CharField(max_length=80, default="Energi proses penggorengan")
    satuan_inventory = models.CharField(max_length=30, default="kg")
    faktor_kg_co2e = models.DecimalField(max_digits=10, decimal_places=4, default=3.0000)
    sumber_data = models.CharField(max_length=180, default="Dataset contoh studi kasus UMKM Indonesia")
    keterangan = models.TextField(
        default=(
            "Faktor emisi contoh untuk simulasi LCA sederhana. Nilai dapat disesuaikan "
            "dengan literatur atau data supplier yang digunakan."
        )
    )

    class Meta:
        verbose_name = "Faktor Emisi Inventory"
        verbose_name_plural = "Faktor Emisi Inventory"

    def __str__(self):
        return f"{self.nama_inventory} ({self.faktor_kg_co2e} kg CO2e/{self.satuan_inventory})"


class AktivitasProduksi(models.Model):
    METODE_PROSES_CHOICES = [
        ("penggorengan", "Penggorengan"),
        ("pemanggangan", "Pemanggangan"),
        ("pengeringan", "Pengeringan"),
        ("campuran", "Campuran"),
    ]
    KUALITAS_DATA_CHOICES = [
        ("primer", "Data primer"),
        ("estimasi", "Estimasi lapangan"),
        ("sekunder", "Data sekunder"),
    ]

    profil_umkm = models.ForeignKey(ProfilUMKM, on_delete=models.CASCADE)
    faktor_inventory = models.ForeignKey(FaktorEmisiInventory, on_delete=models.PROTECT)
    tanggal_produksi = models.DateField()
    nama_batch = models.CharField(max_length=100)
    jumlah_produk = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah_bahan_baku = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    produk_reject = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    jumlah_inventory = models.DecimalField(max_digits=10, decimal_places=2)
    durasi_produksi_jam = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    biaya_inventory = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    suhu_proses_c = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    metode_proses = models.CharField(max_length=30, choices=METODE_PROSES_CHOICES, default="penggorengan")
    pemasok_inventory = models.CharField(max_length=120, blank=True, default="")
    kualitas_data = models.CharField(max_length=30, choices=KUALITAS_DATA_CHOICES, default="primer")
    catatan_perbaikan = models.TextField(blank=True, default="")
    catatan = models.TextField(blank=True, default="")
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tanggal_produksi", "-id"]
        verbose_name = "Aktivitas Produksi"
        verbose_name_plural = "Aktivitas Produksi"

    def __str__(self):
        return f"{self.nama_batch} - {self.tanggal_produksi}"

    @property
    def emisi_kg_co2e(self):
        return self.jumlah_inventory * self.faktor_inventory.faktor_kg_co2e

    @property
    def intensitas_kg_co2e_per_produk(self):
        if not self.jumlah_produk:
            return 0
        return self.emisi_kg_co2e / self.jumlah_produk

    @property
    def yield_produksi_persen(self):
        if not self.jumlah_bahan_baku:
            return 0
        return (self.jumlah_produk / self.jumlah_bahan_baku) * 100

    @property
    def reject_rate_persen(self):
        total_output = self.jumlah_produk + self.produk_reject
        if not total_output:
            return 0
        return (self.produk_reject / total_output) * 100

    @property
    def produktivitas_per_jam(self):
        if not self.durasi_produksi_jam:
            return 0
        return self.jumlah_produk / self.durasi_produksi_jam

    @property
    def biaya_inventory_per_produk(self):
        if not self.jumlah_produk:
            return 0
        return self.biaya_inventory / self.jumlah_produk
