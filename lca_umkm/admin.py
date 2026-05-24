from django.contrib import admin

from . import models


@admin.register(models.ProfilUMKM)
class ProfilUMKMAdmin(admin.ModelAdmin):
    list_display = ("nama_umkm", "jenis_usaha", "lokasi_usaha", "produk_acuan")


@admin.register(models.FaktorEmisiInventory)
class FaktorEmisiInventoryAdmin(admin.ModelAdmin):
    list_display = ("nama_inventory", "kategori_inventory", "satuan_inventory", "faktor_kg_co2e")


@admin.register(models.AktivitasProduksi)
class AktivitasProduksiAdmin(admin.ModelAdmin):
    list_display = (
        "tanggal_produksi",
        "nama_batch",
        "jumlah_produk",
        "jumlah_bahan_baku",
        "produk_reject",
        "jumlah_inventory",
        "emisi_kg_co2e",
        "kualitas_data",
    )
    list_filter = ("tanggal_produksi", "faktor_inventory", "kualitas_data")
    search_fields = ("nama_batch", "catatan")
