# prueba.py
# Suite de pruebas TDD para el módulo descuento.py
# Registra automáticamente resultados en auditoria.log

import unittest
import logging
import os
import sys
from datetime import datetime
from io import StringIO

# ─── Configuración del logger de auditoría ────────────────────────────────────

LOG_FILE = "auditoria.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger("auditoria")


# ─── Importación del módulo bajo prueba ───────────────────────────────────────

try:
    from descuento import aplicar_descuento, calcular_iva, precio_final
    logger.info("Módulo 'descuento.py' importado correctamente.")
except ImportError as e:
    logger.critical(f"No se pudo importar 'descuento.py': {e}")
    sys.exit(1)

try:
    from main import ejecutar
    logger.info("Módulo 'main.py' importado correctamente.")
except ImportError as e:
    logger.critical(f"No se pudo importar 'main.py': {e}")
    sys.exit(1)


# ─── Runner personalizado que escribe cada resultado en el log ─────────────────

class AuditoriaTestResult(unittest.TestResult):
    """Extiende TestResult para registrar cada prueba en auditoria.log."""

    def startTest(self, test):
        super().startTest(test)
        logger.info(f"INICIO | {test.id()}")

    def addSuccess(self, test):
        super().addSuccess(test)
        logger.info(f"✔ PASÓ  | {test.id()}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        mensaje = self._excinfo_to_str(err)
        logger.error(f"✘ FALLÓ | {test.id()}\n{mensaje}")

    def addError(self, test, err):
        super().addError(test, err)
        mensaje = self._excinfo_to_str(err)
        logger.error(f"✘ ERROR | {test.id()}\n{mensaje}")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        logger.warning(f"⚠ OMITIDO | {test.id()} — {reason}")

    @staticmethod
    def _excinfo_to_str(err):
        import traceback
        return "".join(traceback.format_exception(*err)).strip()


class AuditoriaTestRunner:
    """Runner que usa AuditoriaTestResult y resume los resultados en el log."""

    def run(self, suite):
        logger.info("=" * 60)
        logger.info(f"INICIO DE SUITE — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)

        result = AuditoriaTestResult()
        suite.run(result)

        total   = result.testsRun
        fallos  = len(result.failures)
        errores = len(result.errors)
        omitidos = len(result.skipped)
        exitosos = total - fallos - errores - omitidos

        logger.info("-" * 60)
        logger.info(f"RESUMEN | Total: {total} | ✔ Pasaron: {exitosos} | "
                    f"✘ Fallaron: {fallos} | ✘ Errores: {errores} | ⚠ Omitidos: {omitidos}")
        logger.info("=" * 60)

        # También mostrar en consola
        print(f"\n{'='*60}")
        print(f"  RESULTADOS DE PRUEBAS TDD")
        print(f"{'='*60}")
        print(f"  Total ejecutadas : {total}")
        print(f"  ✔ Pasaron        : {exitosos}")
        print(f"  ✘ Fallaron       : {fallos}")
        print(f"  ✘ Con error      : {errores}")
        print(f"  ⚠ Omitidas       : {omitidos}")
        print(f"{'='*60}")
        print(f"  Log guardado en  : {os.path.abspath(LOG_FILE)}")
        print(f"{'='*60}\n")

        if fallos or errores:
            print("  Detalle de fallos / errores:")
            for test, traza in result.failures + result.errors:
                print(f"\n  [{test.id()}]")
                print(f"  {traza.splitlines()[-1]}")

        return result


# ─── CASOS DE PRUEBA ──────────────────────────────────────────────────────────

class TestAplicarDescuento(unittest.TestCase):
    """Pruebas para la función aplicar_descuento(precio, porcentaje)."""

    def test_descuento_cero(self):
        """Sin descuento el precio no cambia."""
        resultado = aplicar_descuento(100, 0)
        self.assertEqual(resultado, 100,
            "Con 0 % de descuento el precio debe permanecer igual.")

    def test_descuento_50_porciento(self):
        """50 % de descuento sobre 200 debe dar 100."""
        resultado = aplicar_descuento(200, 50)
        self.assertEqual(resultado, 100,
            "50 % de descuento sobre 200 debe resultar en 100.")

    def test_descuento_10_porciento(self):
        """10 % sobre 150 debe dar 135."""
        resultado = aplicar_descuento(150, 10)
        self.assertAlmostEqual(resultado, 135.0, places=2,
            msg="10 % de descuento sobre 150 debe resultar en 135.")

    def test_descuento_100_porciento(self):
        """100 % de descuento debe dar 0."""
        resultado = aplicar_descuento(500, 100)
        self.assertEqual(resultado, 0,
            "100 % de descuento debe resultar en precio 0.")

    def test_precio_negativo_lanza_excepcion(self):
        """Un precio negativo debe lanzar ValueError."""
        with self.assertRaises(ValueError,
                msg="Un precio negativo debe lanzar ValueError."):
            aplicar_descuento(-50, 10)

    def test_descuento_negativo_lanza_excepcion(self):
        """Un porcentaje de descuento negativo debe lanzar ValueError."""
        with self.assertRaises(ValueError,
                msg="Un porcentaje negativo debe lanzar ValueError."):
            aplicar_descuento(100, -5)

    def test_descuento_mayor_100_lanza_excepcion(self):
        """Un descuento mayor a 100 % debe lanzar ValueError."""
        with self.assertRaises(ValueError,
                msg="Descuento > 100 debe lanzar ValueError."):
            aplicar_descuento(100, 110)


class TestCalcularIva(unittest.TestCase):
    """Pruebas para la función calcular_iva(precio, porcentaje_iva)."""

    def test_iva_default_12(self):
        """IVA por defecto es 12 % (Ecuador)."""
        resultado = calcular_iva(100)
        self.assertAlmostEqual(resultado, 12.0, places=2,
            msg="IVA del 12 % sobre 100 debe ser 12.")

    def test_iva_personalizado(self):
        """IVA del 15 % sobre 200 debe ser 30."""
        resultado = calcular_iva(200, 15)
        self.assertAlmostEqual(resultado, 30.0, places=2,
            msg="IVA del 15 % sobre 200 debe ser 30.")

    def test_iva_cero(self):
        """IVA del 0 % debe dar 0."""
        resultado = calcular_iva(500, 0)
        self.assertEqual(resultado, 0,
            "IVA del 0 % debe dar 0.")

    def test_iva_precio_negativo_lanza_excepcion(self):
        """Precio negativo debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            calcular_iva(-100)


class TestPrecioFinal(unittest.TestCase):
    """Pruebas de integración para precio_final(precio, descuento, iva)."""

    def test_estructura_resultado(self):
        """El resultado debe contener todas las claves requeridas."""
        resultado = precio_final(100, 10)
        claves = {"precio_original", "descuento_aplicado",
                  "precio_con_descuento", "iva", "total"}
        self.assertEqual(set(resultado.keys()), claves,
            f"El dict debe tener exactamente las claves: {claves}")

    def test_calculo_completo(self):
        """
        precio=100, descuento=10%, IVA=12% sobre precio ORIGINAL.
        precio_con_descuento = 90
        iva                  = 12  (12 % de 100, precio original)
        total                = 90 + 12 = 102
        """
        r = precio_final(100, 10, 12)
        self.assertEqual(r["precio_original"],    100)
        self.assertAlmostEqual(r["descuento_aplicado"], 10.0,  places=2)
        self.assertAlmostEqual(r["precio_con_descuento"], 90.0, places=2)
        self.assertAlmostEqual(r["iva"],          12.0,  places=2)
        self.assertAlmostEqual(r["total"],        102.0, places=2)

    def test_sin_descuento_sin_iva(self):
        """Sin descuento ni IVA el total debe ser igual al precio original."""
        r = precio_final(200, 0, 0)
        self.assertEqual(r["total"], 200)

    def test_precio_cero(self):
        """Un precio de 0 debe producir total 0."""
        r = precio_final(0, 20, 12)
        self.assertEqual(r["total"], 0)


class TestMain(unittest.TestCase):
    """Pruebas para la función ejecutar() de main.py."""

    def _capturar_salida(self, inputs):
        """Helper: simula entradas del usuario y captura la salida en consola."""
        from unittest.mock import patch
        from io import StringIO
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                ejecutar()
                return mock_out.getvalue()

    def test_ejecutar_retorna_none_o_no_lanza(self):
        """ejecutar() no debe lanzar excepción con entradas válidas."""
        from unittest.mock import patch
        try:
            with patch("builtins.input", side_effect=["100", "10", "n"]):
                ejecutar()
        except Exception as e:
            self.fail(f"ejecutar() lanzó una excepción inesperada: {e}")

    def test_salida_contiene_precio_original(self):
        """La salida debe mostrar el precio original ingresado."""
        salida = self._capturar_salida(["200", "15", "n"])
        self.assertIn("200", salida,
            "La salida debe mostrar el precio original (200).")

    def test_salida_contiene_precio_con_descuento(self):
        """La salida debe mostrar el precio con descuento aplicado."""
        salida = self._capturar_salida(["100", "10", "n"])
        self.assertIn("90", salida,
            "La salida debe mostrar el precio con descuento (90).")

    def test_salida_contiene_iva(self):
        """La salida debe mencionar el IVA."""
        salida = self._capturar_salida(["100", "0", "n"])
        salida_lower = salida.lower()
        self.assertIn("iva", salida_lower,
            "La salida debe mencionar la palabra 'IVA'.")

    def test_salida_contiene_total(self):
        """La salida debe mostrar el total final."""
        salida = self._capturar_salida(["100", "10", "n"])
        salida_lower = salida.lower()
        self.assertIn("total", salida_lower,
            "La salida debe mostrar la palabra 'total'.")

    def test_precio_invalido_no_rompe_programa(self):
        """Ingresar texto en lugar de número debe manejarse sin crash."""
        from unittest.mock import patch
        try:
            with patch("builtins.input", side_effect=["abc", "100", "10", "n"]):
                ejecutar()
        except (ValueError, TypeError, StopIteration):
            self.fail("ejecutar() no debe romperse con entrada inválida.")

    def test_descuento_invalido_no_rompe_programa(self):
        """Un descuento fuera de rango debe manejarse sin crash."""
        from unittest.mock import patch
        try:
            with patch("builtins.input", side_effect=["100", "150", "10", "n"]):
                ejecutar()
        except (ValueError, TypeError, StopIteration):
            self.fail("ejecutar() no debe romperse con descuento > 100.")

    def test_repetir_calculo(self):
        """Responder 's' debe permitir hacer otro cálculo sin crash."""
        from unittest.mock import patch
        try:
            with patch("builtins.input", side_effect=["100", "10", "s", "200", "20", "n"]):
                ejecutar()
        except StopIteration:
            self.fail("ejecutar() debe soportar múltiples cálculos al responder 's'.")


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestAplicarDescuento))
    suite.addTests(loader.loadTestsFromTestCase(TestCalcularIva))
    suite.addTests(loader.loadTestsFromTestCase(TestPrecioFinal))
    suite.addTests(loader.loadTestsFromTestCase(TestMain))

    runner = AuditoriaTestRunner()
    resultado = runner.run(suite)

    sys.exit(0 if resultado.wasSuccessful() else 1)