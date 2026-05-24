from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase

from .lca_engine import hitung_dampak_lca


class AlgoritmaLCATests(SimpleTestCase):
    def test_hitung_emisi_dan_intensitas_satu_inventory(self):
        faktor = SimpleNamespace(faktor_kg_co2e=Decimal("3.0"), satuan_inventory="kg")
        aktivitas = SimpleNamespace(
            id=1,
            tanggal_produksi="2026-04-20",
            nama_batch="Batch Uji",
            jumlah_produk=Decimal("50"),
            jumlah_bahan_baku=Decimal("10"),
            produk_reject=Decimal("1"),
            jumlah_unit_inventory=Decimal("50"),
            berat_per_unit_inventory_kg=Decimal("0.0100"),
            jumlah_inventory=Decimal("10"),
            durasi_produksi_jam=Decimal("5"),
            biaya_inventory=Decimal("100000"),
            pemasok_inventory="Pemasok uji",
            catatan_perbaikan="",
            faktor_inventory=faktor,
            catatan="",
            emisi_kg_co2e=Decimal("30"),
            intensitas_kg_co2e_per_produk=Decimal("0.6"),
            yield_produksi_persen=Decimal("5"),
            reject_rate_persen=Decimal("1.9608"),
            produktivitas_per_jam=Decimal("10"),
            biaya_inventory_per_produk=Decimal("2000"),
            get_kualitas_data_display=lambda: "Data primer",
        )

        hasil = hitung_dampak_lca([aktivitas])

        self.assertEqual(hasil["total_emisi"], Decimal("30.00"))
        self.assertEqual(hasil["intensitas"], Decimal("0.600"))
        self.assertEqual(hasil["kategori_dampak"]["label"], "Rendah")
        self.assertEqual(hasil["biaya_per_produk"], Decimal("2000.00"))
