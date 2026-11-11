"""Core Multimodal Steganography Scanner implementation."""
import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ScanResult:
    is_suspicious: bool
    lsb_entropy: float
    high_freq_ratio: float
    risk_score: float
    details: List[str]

class SteganographyScanner:
    """Analyzes raw pixel byte streams for LSB entropy anomalies and high-frequency perturbation spikes."""
    
    def __init__(self, entropy_threshold: float = 0.95, perturbation_threshold: float = 0.4):
        self.entropy_threshold = entropy_threshold
        self.perturbation_threshold = perturbation_threshold

    def calculate_lsb_entropy(self, pixel_bytes: bytes) -> float:
        """Measures Shannon entropy of the least significant bit (LSB) across pixel bytes."""
        if not pixel_bytes:
            return 0.0
        
        lsb_counts = [0, 0]
        for b in pixel_bytes:
            lsb = b & 1
            lsb_counts[lsb] += 1
            
        total = len(pixel_bytes)
        p0 = lsb_counts[0] / total
        p1 = lsb_counts[1] / total

        entropy = 0.0
        if p0 > 0:
            entropy -= p0 * math.log2(p0)
        if p1 > 0:
            entropy -= p1 * math.log2(p1)

        return round(entropy, 3)

    def calculate_high_frequency_variance(self, pixel_bytes: bytes) -> float:
        """Computes adjacent pixel delta variance to detect noise injections."""
        if len(pixel_bytes) < 2:
            return 0.0
        deltas = [abs(pixel_bytes[i] - pixel_bytes[i-1]) for i in range(1, len(pixel_bytes))]
        avg_delta = sum(deltas) / len(deltas)
        # Ratio of large jitter deltas (> 30)
        jitter_count = sum(1 for d in deltas if d > 30)
        return round(jitter_count / len(deltas), 3)

    def scan(self, pixel_bytes: bytes) -> ScanResult:
        entropy = self.calculate_lsb_entropy(pixel_bytes)
        high_freq = self.calculate_high_frequency_variance(pixel_bytes)
        details = []

        # In natural images LSB entropy is somewhat random, but uniform 1.000 across thousands of bytes
        # combined with high frequency variance indicates artificial payload embedding.
        is_suspicious = False
        if entropy > self.entropy_threshold and high_freq > self.perturbation_threshold:
            is_suspicious = True
            details.append("Detected high LSB entropy coupled with abnormal high-frequency noise spikes.")
        elif entropy > 0.999 and len(pixel_bytes) > 200:
            is_suspicious = True
            details.append("Detected near-perfect LSB bit uniformity typical of encrypted stego payload.")

        risk_score = round((entropy * 0.5) + (high_freq * 0.5), 2)

        return ScanResult(
            is_suspicious=is_suspicious,
            lsb_entropy=entropy,
            high_freq_ratio=high_freq,
            risk_score=risk_score,
            details=details
        )
