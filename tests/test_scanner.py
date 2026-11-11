"""Unit tests for multimodal-steganography-scanner."""
import unittest
from multimodal_steganography_scanner.scanner import SteganographyScanner

class TestSteganographyScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = SteganographyScanner()

    def test_clean_gradient(self):
        # Deterministic smooth gradient
        data = bytes([10, 11, 12, 13, 14, 15] * 20)
        res = self.scanner.scan(data)
        self.assertFalse(res.is_suspicious)

    def test_random_noise_flagged(self):
        # Pure random high entropy bytes
        import random
        random.seed(42)
        data = bytes([random.randint(0, 255) for _ in range(1000)])
        res = self.scanner.scan(data)
        self.assertTrue(res.is_suspicious)
