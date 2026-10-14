#!/usr/bin/env python3
"""
Basit TCP port tarayıcı (eğitim amaçlı).

Yalnızca kendi makinende, kendi laboratuvarında veya yazılı izin aldığın
sistemlerde kullan. İzinsiz tarama yasa dışı olabilir.

Örnekler:
    python port_scanner.py                       # 127.0.0.1, 1-1024
    python port_scanner.py -t 192.168.1.10 -p 20-100
    python port_scanner.py -t scanme.nmap.org -p 1-1000
"""

import argparse
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor

LOCAL_TARGETS = {"127.0.0.1", "localhost", "::1"}


def parse_ports(text: str) -> list[int]:
    """'80', '20-100' veya '22,80,443' biçimlerini port listesine çevirir."""
    ports = set()
    for part in text.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        elif part:
            ports.add(int(part))
    if not ports or min(ports) < 1 or max(ports) > 65535:
        raise ValueError("Portlar 1-65535 arasında olmalı.")
    return sorted(ports)


def scan_port(host: str, port: int, timeout: float) -> int | None:
    """Port açıksa port numarasını, değilse None döndürür."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port
    except (OSError, socket.timeout):
        return None


def service_name(port: int) -> str:
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "bilinmiyor"


def main() -> int:
    parser = argparse.ArgumentParser(description="Basit TCP port tarayıcı")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="Hedef IP veya alan adı")
    parser.add_argument("-p", "--ports", default="1-1024", help="Örn: 80, 20-100, 22,80,443")
    parser.add_argument("--timeout", type=float, default=0.5, help="Bağlantı zaman aşımı (sn)")
    parser.add_argument("--threads", type=int, default=100, help="Eşzamanlı iş parçacığı sayısı")
    args = parser.parse_args()

    try:
        ports = parse_ports(args.ports)
        ip = socket.gethostbyname(args.target)
    except (ValueError, socket.gaierror) as err:
        print(f"Hata: {err}")
        return 1

    # Yerel olmayan hedeflerde izin teyidi iste
    if args.target not in LOCAL_TARGETS:
        answer = input(f"{args.target} sistemini tarama iznin var mı? (e/h): ").strip().lower()
        if answer != "e":
            print("İzin yok, tarama iptal edildi.")
            return 1

    print(f"\nHedef: {args.target} ({ip}) | {len(ports)} port taranıyor...\n")
    start = time.time()

    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        results = pool.map(lambda p: scan_port(ip, p, args.timeout), ports)
        open_ports = [p for p in results if p is not None]

    if open_ports:
        print(f"{'PORT':<8}{'DURUM':<8}SERVİS")
        for port in open_ports:
            print(f"{port:<8}{'açık':<8}{service_name(port)}")
    else:
        print("Açık port bulunamadı.")

    print(f"\nTarama {time.time() - start:.2f} saniyede tamamlandı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
