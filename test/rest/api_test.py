import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )

    def test_api_divide_exact(self):
        url = f"{BASE_URL}/calc/divide/6/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "2.0", "ERROR DIVDE EXACT"
        )

    def test_api_divide_decimal(self):
        url = f"{BASE_URL}/calc/divide/7/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3.5", "ERROR DIVDE DECIMAL"
        )

    def test_api_divide_negative(self):
        url = f"{BASE_URL}/calc/divide/10/-2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "-5.0", "ERROR DIVIDE NEGATIVE"
        )

    def test_api_divide_by_one(self):
        url = f"{BASE_URL}/calc/divide/9/1"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "9.0", "ERROR DIVIDE BY ONE"
        )

    def test_api_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/5/0"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail(
                f"Se esperaba codigo HTTP 406 en {url}"
            )
        except HTTPError as e:
            self.assertEqual(
                e.code, 406, f"Se esperaba codigo 406, pero se recibio {e.code} en {url}"
            )
        
    
    def test_api_divide_char(self):
        url = f"{BASE_URL}/calc/divide/z/3"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail(
                f"Se esperaba codigo HTTP 400 en {url}"
            )
        except HTTPError as e:
            self.assertEqual(
                e.code, 400, f"Se esperaba codigo 400, pero se recibio {e.code} en {url}"
            )

    def test_api_multiply_basic(self):
        url = f"{BASE_URL}/calc/multiply/4/5"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "20", f"EROR MULTIPLY BASIC"
        )

    def test_api_multiply_negative(self):
        url = f"{BASE_URL}/calc/multiply/-3/6"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "-18", f"ERROR MULTIPLY NEGATIVE"
        )

    def test_api_multiply_by_zero(self):
        url = f"{BASE_URL}/calc/multiply/7/0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "0", f"ERROR MULTIPLY BY ZERO"
        )

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
