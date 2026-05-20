from faker import Faker
import random
import csv

fake = Faker("es_ES")

with open("datos_prueba_descuentos.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)

    escritor.writerow(["producto", "precio_original", "descuento"])

    for i in range(20):
        producto = fake.word().capitalize()
        precio_original = round(random.uniform(1, 500), 2)
        descuento = random.randint(0, 100)

        escritor.writerow([producto, precio_original, descuento])

print("Datos de prueba generados en datos_prueba_descuentos.csv")