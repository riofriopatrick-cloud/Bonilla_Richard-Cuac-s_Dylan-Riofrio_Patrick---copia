# descuento.py
# Módulo de cálculo de descuentos e IVA
# Implementado mediante TDD — todas las funciones pasan las pruebas de prueba.py


def aplicar_descuento(precio, porcentaje_descuento):
    """
    Aplica un descuento porcentual al precio y retorna el precio con descuento.

    Args:
        precio (float): Precio original. Debe ser >= 0.
        porcentaje_descuento (float): Porcentaje de descuento (0 – 100).

    Returns:
        float: Precio tras aplicar el descuento.

    Raises:
        ValueError: Si el precio es negativo o el porcentaje está fuera de [0, 100].
    """
    if precio < 0:
        raise ValueError(f"El precio no puede ser negativo. Recibido: {precio}")
    if not (0 <= porcentaje_descuento <= 100):
        raise ValueError(
            f"El porcentaje de descuento debe estar entre 0 y 100. "
            f"Recibido: {porcentaje_descuento}"
        )

    descuento = precio * (porcentaje_descuento / 100)
    return round(precio - descuento, 2)


def calcular_iva(precio, porcentaje_iva=12):
    """
    Calcula el monto de IVA sobre el precio dado.

    Args:
        precio (float): Base imponible. Debe ser >= 0.
        porcentaje_iva (float): Porcentaje de IVA. Por defecto 12 % (Ecuador).

    Returns:
        float: Monto de IVA calculado.

    Raises:
        ValueError: Si el precio es negativo.
    """
    if precio < 0:
        raise ValueError(f"El precio no puede ser negativo. Recibido: {precio}")

    return round(precio * (porcentaje_iva / 100), 2)


def precio_final(precio, porcentaje_descuento, porcentaje_iva=12):
    """
    Calcula el precio final aplicando primero el descuento y luego sumando
    el IVA calculado sobre el precio ORIGINAL.

    Args:
        precio (float): Precio original.
        porcentaje_descuento (float): Porcentaje de descuento a aplicar.
        porcentaje_iva (float): Porcentaje de IVA sobre el precio original.

    Returns:
        dict: {
            'precio_original'     : float,
            'descuento_aplicado'  : float,   # monto descontado
            'precio_con_descuento': float,
            'iva'                 : float,   # IVA sobre precio original
            'total'               : float    # precio_con_descuento + iva
        }
    """
    precio_descuento = aplicar_descuento(precio, porcentaje_descuento)
    monto_descuento  = round(precio - precio_descuento, 2)
    iva              = calcular_iva(precio, porcentaje_iva)
    total            = round(precio_descuento + iva, 2)

    return {
        "precio_original"     : precio,
        "descuento_aplicado"  : monto_descuento,
        "precio_con_descuento": precio_descuento,
        "iva"                 : iva,
        "total"               : total,
    }