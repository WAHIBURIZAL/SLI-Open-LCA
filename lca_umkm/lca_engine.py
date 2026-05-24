from decimal import Decimal, ROUND_HALF_UP


def bulatkan(nilai, digit=2):
    pola = Decimal("1") if digit == 0 else Decimal("1." + ("0" * digit))
    return Decimal(nilai).quantize(pola, rounding=ROUND_HALF_UP)


def nilai_atau_nol(nilai):
    return nilai if nilai is not None else Decimal("0")


def hitung_dampak_lca(aktivitas_queryset):
    aktivitas = list(aktivitas_queryset)
    total_produk = sum((nilai_atau_nol(item.jumlah_produk) for item in aktivitas), Decimal("0"))
    total_bahan_baku = sum((nilai_atau_nol(item.jumlah_bahan_baku) for item in aktivitas), Decimal("0"))
    total_reject = sum((nilai_atau_nol(item.produk_reject) for item in aktivitas), Decimal("0"))
    total_inventory = sum((nilai_atau_nol(item.jumlah_inventory) for item in aktivitas), Decimal("0"))
    total_emisi = sum((item.emisi_kg_co2e for item in aktivitas), Decimal("0"))
    total_durasi = sum((nilai_atau_nol(item.durasi_produksi_jam) for item in aktivitas), Decimal("0"))
    total_biaya_inventory = sum((nilai_atau_nol(item.biaya_inventory) for item in aktivitas), Decimal("0"))
    intensitas = Decimal("0") if total_produk == 0 else total_emisi / total_produk
    target_intensitas = Decimal("1.00")
    inventory_per_produk = Decimal("0") if total_produk == 0 else total_inventory / total_produk
    yield_produksi = Decimal("0") if total_bahan_baku == 0 else (total_produk / total_bahan_baku) * Decimal("100")
    reject_rate = Decimal("0") if (total_produk + total_reject) == 0 else (total_reject / (total_produk + total_reject)) * Decimal("100")
    produktivitas = Decimal("0") if total_durasi == 0 else total_produk / total_durasi
    biaya_per_produk = Decimal("0") if total_produk == 0 else total_biaya_inventory / total_produk
    emisi_tertinggi = max((item.emisi_kg_co2e for item in aktivitas), default=Decimal("0"))

    detail_inventory = []
    for item in aktivitas:
        emisi = item.emisi_kg_co2e
        kontribusi = Decimal("0") if total_emisi == 0 else (emisi / total_emisi) * Decimal("100")
        skala_emisi = Decimal("0") if emisi_tertinggi == 0 else (emisi / emisi_tertinggi) * Decimal("100")
        detail_inventory.append({
            "id": item.id,
            "tanggal": item.tanggal_produksi,
            "nama_batch": item.nama_batch,
            "jumlah_produk": bulatkan(item.jumlah_produk),
            "jumlah_bahan_baku": bulatkan(item.jumlah_bahan_baku),
            "produk_reject": bulatkan(item.produk_reject),
            "jumlah_inventory": bulatkan(item.jumlah_inventory),
            "satuan_inventory": item.faktor_inventory.satuan_inventory,
            "emisi_kg_co2e": bulatkan(emisi),
            "intensitas": bulatkan(item.intensitas_kg_co2e_per_produk, 3),
            "yield_produksi": bulatkan(item.yield_produksi_persen, 1),
            "reject_rate": bulatkan(item.reject_rate_persen, 1),
            "produktivitas": bulatkan(item.produktivitas_per_jam, 2),
            "durasi": bulatkan(item.durasi_produksi_jam),
            "biaya_inventory": bulatkan(item.biaya_inventory),
            "biaya_per_produk": bulatkan(item.biaya_inventory_per_produk),
            "metode_proses": item.get_metode_proses_display(),
            "kualitas_data": item.get_kualitas_data_display(),
            "pemasok_inventory": item.pemasok_inventory,
            "suhu_proses_c": bulatkan(item.suhu_proses_c),
            "catatan_perbaikan": item.catatan_perbaikan,
            "kontribusi": bulatkan(kontribusi, 1),
            "skala_emisi": bulatkan(skala_emisi, 1),
            "catatan": item.catatan,
        })

    batch_terbaik = min(detail_inventory, key=lambda item: item["intensitas"], default=None)
    batch_terboros = max(detail_inventory, key=lambda item: item["intensitas"], default=None)
    capaian_target = Decimal("100") if intensitas <= target_intensitas and intensitas > 0 else (
        Decimal("0") if intensitas == 0 else (target_intensitas / intensitas) * Decimal("100")
    )

    return {
        "total_produk": bulatkan(total_produk),
        "total_bahan_baku": bulatkan(total_bahan_baku),
        "total_reject": bulatkan(total_reject),
        "total_inventory": bulatkan(total_inventory),
        "total_emisi": bulatkan(total_emisi),
        "total_durasi": bulatkan(total_durasi),
        "total_biaya_inventory": bulatkan(total_biaya_inventory),
        "intensitas": bulatkan(intensitas, 3),
        "inventory_per_produk": bulatkan(inventory_per_produk, 3),
        "yield_produksi": bulatkan(yield_produksi, 1),
        "reject_rate": bulatkan(reject_rate, 1),
        "produktivitas": bulatkan(produktivitas, 2),
        "biaya_per_produk": bulatkan(biaya_per_produk),
        "target_intensitas": bulatkan(target_intensitas, 2),
        "capaian_target": bulatkan(min(capaian_target, Decimal("100")), 0),
        "kategori_dampak": tentukan_kategori_dampak(intensitas),
        "detail_inventory": detail_inventory,
        "batch_terbaik": batch_terbaik,
        "batch_terboros": batch_terboros,
        "skenario": hitung_skenario(total_inventory, total_emisi),
        "interpretasi": susun_interpretasi(intensitas, inventory_per_produk, reject_rate, batch_terbaik, batch_terboros),
    }


def tentukan_kategori_dampak(intensitas):
    if intensitas <= Decimal("1.00"):
        return {
            "label": "Rendah",
            "kelas": "rendah",
            "rekomendasi": "Pemakaian inventory masih efisien untuk skala produksi saat ini.",
        }
    if intensitas <= Decimal("2.50"):
        return {
            "label": "Sedang",
            "kelas": "sedang",
            "rekomendasi": "Optimalkan ukuran batch dan pengaturan panas agar inventory lebih hemat.",
        }
    return {
        "label": "Tinggi",
        "kelas": "tinggi",
        "rekomendasi": "Periksa kebocoran energi, kapasitas batch, dan alternatif energi yang lebih rendah emisi.",
    }


def hitung_skenario(total_inventory, total_emisi):
    skenario_reduksi = []
    for persen in [Decimal("10"), Decimal("15"), Decimal("20")]:
        faktor = Decimal("1") - (persen / Decimal("100"))
        emisi_baru = total_emisi * faktor
        skenario_reduksi.append({
            "nama": f"Reduksi inventory {persen}%",
            "inventory": bulatkan(total_inventory * faktor),
            "emisi": bulatkan(emisi_baru),
            "penghematan": bulatkan(total_emisi - emisi_baru),
        })
    return skenario_reduksi


def susun_interpretasi(intensitas, inventory_per_produk, reject_rate, batch_terbaik, batch_terboros):
    interpretasi = [
        f"Rata-rata pemakaian inventory adalah {bulatkan(inventory_per_produk, 3)} satuan inventory per satuan produk.",
    ]
    if batch_terbaik:
        interpretasi.append(
            f"Batch paling efisien adalah {batch_terbaik['nama_batch']} dengan intensitas {batch_terbaik['intensitas']} kg CO2e per satuan produk."
        )
    if batch_terboros:
        interpretasi.append(
            f"Batch prioritas perbaikan adalah {batch_terboros['nama_batch']} karena intensitasnya paling tinggi."
        )
    if intensitas > Decimal("1.00"):
        interpretasi.append("Fokus perbaikan disarankan pada pengurangan inventory per batch dan stabilitas kapasitas produksi.")
    else:
        interpretasi.append("Performa saat ini sudah berada di bawah target contoh 1,00 kg CO2e per satuan produk.")
    if reject_rate > Decimal("5.00"):
        interpretasi.append("Reject rate di atas 5%, sehingga perbaikan mutu proses juga akan membantu menurunkan intensitas emisi per produk layak jual.")
    return interpretasi
