from decimal import Decimal, InvalidOperation
from datetime import timedelta

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from . import models
from .lca_engine import hitung_dampak_lca


def ambil_database_awal():
    profil, _ = models.ProfilUMKM.objects.get_or_create(id=1)
    faktor, _ = models.FaktorEmisiInventory.objects.get_or_create(id=1)

    if not models.AktivitasProduksi.objects.filter(profil_umkm=profil).exists():
        hari_ini = timezone.localdate()
        data_awal = [
            ("Batch Senin", Decimal("48.00"), Decimal("80.00"), Decimal("4.00"), Decimal("18.00"), Decimal("6.00"), Decimal("324000"), hari_ini - timedelta(days=14)),
            ("Batch Rabu", Decimal("55.00"), Decimal("88.00"), Decimal("3.50"), Decimal("19.50"), Decimal("6.50"), Decimal("351000"), hari_ini - timedelta(days=10)),
            ("Batch Sabtu", Decimal("62.00"), Decimal("96.00"), Decimal("4.20"), Decimal("20.00"), Decimal("7.00"), Decimal("360000"), hari_ini - timedelta(days=7)),
        ]
        for nama_batch, jumlah_produk, jumlah_bahan_baku, produk_reject, jumlah_inventory, durasi, biaya, tanggal in data_awal:
            models.AktivitasProduksi.objects.create(
                profil_umkm=profil,
                faktor_inventory=faktor,
                tanggal_produksi=tanggal,
                nama_batch=nama_batch,
                jumlah_produk=jumlah_produk,
                jumlah_bahan_baku=jumlah_bahan_baku,
                produk_reject=produk_reject,
                jumlah_inventory=jumlah_inventory,
                durasi_produksi_jam=durasi,
                biaya_inventory=biaya,
                suhu_proses_c=Decimal("165.00"),
                metode_proses="penggorengan",
                pemasok_inventory="Agen LPG lokal",
                kualitas_data="primer",
                catatan_perbaikan="Pantau stabilitas suhu dan kapasitas wajan.",
                catatan="Data contoh untuk simulasi awal LCA.",
            )

    return profil, faktor


def ambil_desimal(nilai, default="0"):
    try:
        return Decimal(str(nilai or default).replace(",", "."))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def dashboard_lca(request):
    profil, faktor = ambil_database_awal()

    if request.method == "POST":
        jumlah_produk = ambil_desimal(request.POST.get("jumlah_produk"))
        jumlah_bahan_baku = ambil_desimal(request.POST.get("jumlah_bahan_baku"))
        produk_reject = ambil_desimal(request.POST.get("produk_reject"))
        jumlah_inventory = ambil_desimal(request.POST.get("jumlah_inventory"))
        durasi_produksi_jam = ambil_desimal(request.POST.get("durasi_produksi_jam"))
        biaya_inventory = ambil_desimal(request.POST.get("biaya_inventory"))
        suhu_proses_c = ambil_desimal(request.POST.get("suhu_proses_c"))

        if jumlah_produk <= 0 or jumlah_inventory <= 0:
            messages.error(request, "Jumlah produk dan jumlah inventory harus lebih dari 0.")
            return redirect("dashboard_lca")
        if jumlah_bahan_baku and jumlah_produk > jumlah_bahan_baku:
            messages.error(request, "Jumlah produk tidak boleh lebih besar dari bahan baku masuk.")
            return redirect("dashboard_lca")
        if produk_reject < 0 or durasi_produksi_jam < 0 or biaya_inventory < 0:
            messages.error(request, "Reject, durasi, dan biaya tidak boleh bernilai negatif.")
            return redirect("dashboard_lca")

        models.AktivitasProduksi.objects.create(
            profil_umkm=profil,
            faktor_inventory=faktor,
            tanggal_produksi=request.POST.get("tanggal_produksi") or timezone.localdate(),
            nama_batch=request.POST.get("nama_batch") or "Batch produksi",
            jumlah_produk=jumlah_produk,
            jumlah_bahan_baku=jumlah_bahan_baku,
            produk_reject=produk_reject,
            jumlah_inventory=jumlah_inventory,
            durasi_produksi_jam=durasi_produksi_jam,
            biaya_inventory=biaya_inventory,
            suhu_proses_c=suhu_proses_c,
            metode_proses=request.POST.get("metode_proses") or "penggorengan",
            pemasok_inventory=request.POST.get("pemasok_inventory", ""),
            kualitas_data=request.POST.get("kualitas_data") or "primer",
            catatan_perbaikan=request.POST.get("catatan_perbaikan", ""),
            catatan=request.POST.get("catatan", ""),
        )
        messages.success(request, "Data inventory berhasil dihitung dan disimpan.")
        return redirect("dashboard_lca")

    aktivitas = models.AktivitasProduksi.objects.select_related(
        "profil_umkm", "faktor_inventory"
    ).filter(profil_umkm=profil)

    tanggal_awal = request.GET.get("tanggal_awal")
    tanggal_akhir = request.GET.get("tanggal_akhir")
    if tanggal_awal:
        aktivitas = aktivitas.filter(tanggal_produksi__gte=tanggal_awal)
    if tanggal_akhir:
        aktivitas = aktivitas.filter(tanggal_produksi__lte=tanggal_akhir)

    hasil = hitung_dampak_lca(aktivitas)
    chart_rows = list(reversed(hasil["detail_inventory"]))

    return render(request, "lca/dashboard.html", {
        "profil": profil,
        "faktor": faktor,
        "hasil": hasil,
        "tanggal_awal": tanggal_awal,
        "tanggal_akhir": tanggal_akhir,
        "chart_rows": chart_rows,
    })


def database_lca(request):
    profil, faktor = ambil_database_awal()

    if request.method == "POST":
        profil.nama_umkm = request.POST.get("nama_umkm") or profil.nama_umkm
        profil.jenis_usaha = request.POST.get("jenis_usaha") or profil.jenis_usaha
        profil.lokasi_usaha = request.POST.get("lokasi_usaha") or profil.lokasi_usaha
        profil.produk_acuan = request.POST.get("produk_acuan") or profil.produk_acuan
        profil.satuan_produk = request.POST.get("satuan_produk") or profil.satuan_produk
        profil.batas_sistem = request.POST.get("batas_sistem") or profil.batas_sistem
        profil.save()

        faktor.nama_inventory = request.POST.get("nama_inventory") or faktor.nama_inventory
        faktor.kategori_inventory = request.POST.get("kategori_inventory") or faktor.kategori_inventory
        faktor.satuan_inventory = request.POST.get("satuan_inventory") or faktor.satuan_inventory
        faktor.faktor_kg_co2e = ambil_desimal(request.POST.get("faktor_kg_co2e"), faktor.faktor_kg_co2e)
        faktor.sumber_data = request.POST.get("sumber_data") or faktor.sumber_data
        faktor.keterangan = request.POST.get("keterangan") or faktor.keterangan
        faktor.save()

        messages.success(request, "Database LCA berhasil diperbarui.")
        return redirect("database_lca")

    return render(request, "lca/database.html", {
        "profil": profil,
        "faktor": faktor,
    })


def hapus_aktivitas(request, aktivitas_id):
    aktivitas = get_object_or_404(models.AktivitasProduksi, id=aktivitas_id)
    if request.method == "POST":
        aktivitas.delete()
        messages.success(request, "Data aktivitas produksi berhasil dihapus.")
    return redirect("dashboard_lca")
