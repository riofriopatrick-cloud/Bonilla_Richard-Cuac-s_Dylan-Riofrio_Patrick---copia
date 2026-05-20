from datetime import datetime


def guardar_log(mensaje):
    with open("registro_descuentos.txt", "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")


def calcular_precio_final(precio_original, descuento):

    if descuento < 0 or descuento > 100:
        raise ValueError("El descuento debe estar entre 0 y 100.")

    if precio_original <= 0:
        raise ValueError("El precio original debe ser positivo.")

    precio_final = precio_original * (1 - descuento / 100)

    if descuento >= 80:
        precio_final = precio_final * 0.95

    precio_final = round(precio_final, 2)

    return precio_final


def main():
    try:
        precio = float(input("Coloque el precio original: "))
        descuento = float(input("Coloque el valor del porcentaje de descuento: "))

        resultado = calcular_precio_final(precio, descuento)

        print(f"\nEl precio final es: ${resultado}")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log = (
            f"[{fecha}] "
            f"Precio Original: ${precio} | "
            f"Descuento: {descuento}% | "
            f"Precio Final: ${resultado}"
        )

        guardar_log(log)

        print("Resultado guardado en registro_descuentos.txt")

    except ValueError as error:
        print("Error:", error)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        guardar_log(f"[{fecha}] ERROR: {error}")


if __name__ == "__main__":
    main()