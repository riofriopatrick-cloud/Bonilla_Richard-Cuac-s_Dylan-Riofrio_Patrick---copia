# main.py
# Interfaz principal del programa de descuentos

from descuento import precio_final


def mostrar_resultados(resultado):
    """Muestra en pantalla los resultados del cálculo."""

    print("\n" + "=" * 40)
    print("      RESULTADO DEL CÁLCULO")
    print("=" * 40)

    print(f"Precio original       : ${resultado['precio_original']}")
    print(f"Descuento aplicado    : ${resultado['descuento_aplicado']}")
    print(f"Precio con descuento  : ${resultado['precio_con_descuento']}")
    print(f"IVA                   : ${resultado['iva']}")
    print(f"TOTAL                 : ${resultado['total']}")

    print("=" * 40 + "\n")


def pedir_numero(mensaje):
    """
    Solicita un número al usuario y valida la entrada.
    No permite texto inválido.
    """

    while True:
        try:
            valor = float(input(mensaje))
            return valor

        except ValueError:
            print("❌ Error: Debe ingresar un número válido.\n")


def ejecutar():
    """
    Función principal del programa.
    Compatible con las pruebas TDD de prueba.py
    """

    continuar = "s"

    while continuar.lower() == "s":

        try:
            print("\n=== CALCULADORA DE DESCUENTOS ===\n")

            precio = pedir_numero("Ingrese el precio: ")
            descuento = pedir_numero("Ingrese el descuento (%): ")

            resultado = precio_final(precio, descuento)

            mostrar_resultados(resultado)

        except ValueError as e:
            print(f"❌ Error: {e}")

        except Exception as e:
            print(f"❌ Error inesperado: {e}")

        continuar = input("¿Desea realizar otro cálculo? (s/n): ")

    print("\nPrograma finalizado.")


# Punto de entrada
if __name__ == "__main__":
    ejecutar()