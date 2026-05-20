import unittest
from testtools import TestCase
from testtools.matchers import Equals
from descuentos import calcular_precio_final


class TestTDDDescuentos(TestCase):

    def test_descuento_80_aplica_extra(self):
        resultado = calcular_precio_final(100, 80)
        self.assertThat(resultado, Equals(19.00))


if __name__ == "__main__":
    unittest.main()