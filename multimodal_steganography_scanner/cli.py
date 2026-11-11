"""CLI for multimodal-steganography-scanner."""
import sys
import argparse
from .scanner import SteganographyScanner

def main():
    parser = argparse.ArgumentParser(description="Multimodal Steganography Scanner CLI")
    parser.add_argument("--demo", action="store_true", help="Run scan on clean vs stego pixel buffers")
    args = parser.parse_args()

    if args.demo:
        scanner = SteganographyScanner()
        # Clean smooth image gradient
        clean_bytes = bytes([i % 256 for i in range(500)])
        # Injected noise stego
        import os
        stego_bytes = os.urandom(500)

        res_clean = scanner.scan(clean_bytes)
        res_stego = scanner.scan(stego_bytes)
        print(f"Clean Buffer: Suspicious={res_clean.is_suspicious}, Score={res_clean.risk_score}")
        print(f"Stego Buffer: Suspicious={res_stego.is_suspicious}, Score={res_stego.risk_score}, Details={res_stego.details}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
