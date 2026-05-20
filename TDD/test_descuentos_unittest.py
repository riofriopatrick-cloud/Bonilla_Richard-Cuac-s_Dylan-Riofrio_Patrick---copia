import unittest
from descuentos import calcular_precio_final


class TestCalcularPrecioFinal(unittest.TestCase):

    def test_descuento_normal(self):
        self.assertEqual(calcular_precio_final(100, 20), 80.00)

    def test_descuento_cero(self):
        self.assertEqual(calcular_precio_final(100, 0), 100.00)

    def test_descuento_100(self):
        self.assertEqual(calcular_precio_final(100, 100), 0.00)

    def test_descuento_mayor_80(self):
        self.assertEqual(calcular_precio_final(100, 80), 19.00)

    def test_precio_negativo(self):
        with self.assertRaises(ValueError):
            calcular_precio_final(-100, 20)

    def test_descuento_invalido(self):
        with self.assertRaises(ValueError):
            calcular_precio_final(100, 150)


if __name__ == "__main__":
    unittest.main()