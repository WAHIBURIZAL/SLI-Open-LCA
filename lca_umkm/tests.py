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
            jumlah_inventory=Decimal("10"),
            faktor_inventory=faktor,
            catatan="",
            emisi_kg_co2e=Decimal("30"),
            intensitas_kg_co2e_per_produk=Decimal("0.6"),
        )

        hasil = hitung_dampak_lca([aktivitas])

        self.assertEqual(hasil["total_emisi"], Decimal("30.00"))
        self.assertEqual(hasil["intensitas"], Decimal("0.600"))
        self.assertEqual(hasil["kategori_dampak"]["label"], "Rendah")
