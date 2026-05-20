import testtools
from descuentos import calcular_precio_final


class TestCalcularPrecioFinalTestTools(testtools.TestCase):

    def test_descuento_normal(self):
        self.assertEqual(calcular_precio_final(100, 20), 80.00)

    def test_descuento_cero(self):
        self.assertEqual(calcular_precio_final(100, 0), 100.00)

    def test_descuento_100(self):
        self.assertEqual(calcular_precio_final(100, 100), 0.00)

    def test_descuento_mayor_80_aplica_extra(self):
        self.assertEqual(calcular_precio_final(100, 80), 19.00)

    def test_precio_negativo(self):
        self.assertRaises(ValueError, calcular_precio_final, -100, 20)

    def test_precio_cero(self):
        self.assertRaises(ValueError, calcular_precio_final, 0, 20)

    def test_descuento_negativo(self):
        self.assertRaises(ValueError, calcular_precio_final, 100, -10)

    def test_descuento_mayor_a_100(self):
        self.assertRaises(ValueError, calcular_precio_final, 100, 120)


if __name__ == "__main__":
    import unittest
    unittest.main()