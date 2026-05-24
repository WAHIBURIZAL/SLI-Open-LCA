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

    if profil.nama_umkm != "Es Degan Mak DEG":
        profil.nama_umkm = "Es Degan Mak DEG"
        profil.jenis_usaha = "UMKM minuman es kelapa muda"
        profil.lokasi_usaha = "Jl. Terusan Bendungan Sigura-gura, Malang"
        profil.produk_acuan = "Es degan 500 ml"
        profil.satuan_produk = "porsi"
        profil.batas_sistem = (
            "Batas sistem cradle-to-gate sederhana: pengadaan gelas plastik PP "
            "sampai produk es degan 500 ml siap disajikan kepada konsumen."
        )
        profil.save()

    if faktor.nama_inventory != "Gelas plastik PP sekali pakai":
        faktor.nama_inventory = "Gelas plastik PP sekali pakai"
        faktor.kategori_inventory = "Kemasan plastik"
        faktor.satuan_inventory = "kg"
        faktor.faktor_kg_co2e = Decimal("3.6310")
        faktor.sumber_data = "Estimasi LCA SLI Kelompok 3 dari hotspot kemasan plastik"
        faktor.keterangan = (
            "Faktor emisi disederhanakan dari kontribusi kemasan plastik pada analisis "
            "GWP produk es degan. Nilai ini digunakan sebagai database satu inventory."
        )
        faktor.save()

    if not models.AktivitasProduksi.objects.filter(profil_umkm=profil).exists():
        hari_ini = timezone.localdate()
        data_awal = [
            ("Operasional 2 Hari A", Decimal("1000.00"), Decimal("200.00"), Decimal("10.00"), Decimal("1000.00"), Decimal("0.0100"), Decimal("16.00"), Decimal("350000"), hari_ini - timedelta(days=14)),
            ("Operasional 2 Hari B", Decimal("920.00"), Decimal("185.00"), Decimal("12.00"), Decimal("920.00"), Decimal("0.0100"), Decimal("15.00"), Decimal("322000"), hari_ini - timedelta(days=10)),
            ("Operasional 2 Hari C", Decimal("1080.00"), Decimal("215.00"), Decimal("8.00"), Decimal("1080.00"), Decimal("0.0100"), Decimal("17.00"), Decimal("378000"), hari_ini - timedelta(days=7)),
        ]
        for nama_batch, jumlah_produk, jumlah_bahan_baku, produk_reject, jumlah_unit, berat_unit, durasi, biaya, tanggal in data_awal:
            jumlah_inventory = jumlah_unit * berat_unit
            models.AktivitasProduksi.objects.create(
                profil_umkm=profil,
                faktor_inventory=faktor,
                tanggal_produksi=tanggal,
                nama_batch=nama_batch,
                jumlah_produk=jumlah_produk,
                jumlah_bahan_baku=jumlah_bahan_baku,
                produk_reject=produk_reject,
                jumlah_unit_inventory=jumlah_unit,
                berat_per_unit_inventory_kg=berat_unit,
                jumlah_inventory=jumlah_inventory,
                durasi_produksi_jam=durasi,
                biaya_inventory=biaya,
                pemasok_inventory="Toko kemasan Malang",
                kualitas_data="primer",
                catatan_perbaikan="Kurangi gelas plastik sekali pakai atau evaluasi alternatif biodegradable.",
                catatan="Data contoh berdasarkan konsumsi gelas plastik sekitar 1.000 unit per dua hari.",
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
        jumlah_unit_inventory = ambil_desimal(request.POST.get("jumlah_unit_inventory"))
        berat_per_unit_inventory_kg = ambil_desimal(request.POST.get("berat_per_unit_inventory_kg"), "0.0100")
        jumlah_inventory = ambil_desimal(request.POST.get("jumlah_inventory"))
        durasi_produksi_jam = ambil_desimal(request.POST.get("durasi_produksi_jam"))
        biaya_inventory = ambil_desimal(request.POST.get("biaya_inventory"))

        if jumlah_inventory <= 0 and jumlah_unit_inventory > 0 and berat_per_unit_inventory_kg > 0:
            jumlah_inventory = jumlah_unit_inventory * berat_per_unit_inventory_kg

        if jumlah_produk <= 0 or jumlah_inventory <= 0:
            messages.error(request, "Jumlah produk dan total berat inventory harus lebih dari 0.")
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
            jumlah_unit_inventory=jumlah_unit_inventory,
            berat_per_unit_inventory_kg=berat_per_unit_inventory_kg,
            jumlah_inventory=jumlah_inventory,
            durasi_produksi_jam=durasi_produksi_jam,
            biaya_inventory=biaya_inventory,
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
