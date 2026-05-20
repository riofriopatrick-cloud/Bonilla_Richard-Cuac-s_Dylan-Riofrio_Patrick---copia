import pytest
from descuentos import calcular_precio_final


def test_descuento_normal():
    resultado = calcular_precio_final(100, 20)
    assert resultado == 80.00


def test_descuento_cero():
    resultado = calcular_precio_final(100, 0)
    assert resultado == 100.00


def test_descuento_100():
    resultado = calcular_precio_final(100, 100)
    assert resultado == 0.00


def test_descuento_mayor_80_aplica_extra():
    resultado = calcular_precio_final(100, 80)
    assert resultado == 19.00


def test_precio_negativo():
    with pytest.raises(ValueError):
        calcular_precio_final(-100, 20)


def test_descuento_negativo():
    with pytest.raises(ValueError):
        calcular_precio_final(100, -10)


def test_descuento_mayor_a_100():
    with pytest.raises(ValueError):
        calcular_precio_final(100, 120)