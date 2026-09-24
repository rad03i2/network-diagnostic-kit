from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .core import CheckResult, diagnose, dns_lookup, http_check, local_info, ping, tcp_connect

VERSION = "1.0.0"


def _result_payload(result: CheckResult) -> dict[str, Any]:
    return result.to_dict()


def _print_result(result: CheckResult) -> None:
    mark = "PASS" if result.ok else "FAIL"
    latency = f" {result.latency_ms:.2f} ms" if result.latency_ms is not None else ""
    print(f"[{mark}] {result.check:<5} {result.target}{latency} — {result.detail}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="netdiag", description="Safe, cross-platform network diagnostics.")
    parser.add_argument("--version", action="version", version=f"Network Diagnostic Kit {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = parser.add_subparsers(dest="command", required=True)

    dns = sub.add_parser("dns", help="Resolve a hostname")
    dns.add_argument("host")
    dns.add_argument("--json", action="store_true")

    tcp = sub.add_parser("tcp", help="Test a TCP connection")
    tcp.add_argument("host")
    tcp.add_argument("port", type=int)
    tcp.add_argument("--timeout", type=float, default=3.0)
    tcp.add_argument("--json", action="store_true")

    http = sub.add_parser("http", help="Check an HTTP(S) endpoint")
    http.add_argument("url")
    http.add_argument("--timeout", type=float, default=5.0)
    http.add_argument("--json", action="store_true")

    p = sub.add_parser("ping", help="Send one ICMP ping using the OS utility")
    p.add_argument("host")
    p.add_argument("--timeout", type=float, default=3.0)
    p.add_argument("--json", action="store_true")

    info = sub.add_parser("info", help="Show local network identity")
    info.add_argument("--json", action="store_true")

    diag = sub.add_parser("diagnose", help="Run DNS, TCP and optional ping checks")
    diag.add_argument("host")
    diag.add_argument("--port", type=int, default=443)
    diag.add_argument("--timeout", type=float, default=3.0)
    diag.add_argument("--no-ping", action="store_true")
    diag.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "dns":
            result = dns_lookup(args.host)
        elif args.command == "tcp":
            result = tcp_connect(args.host, args.port, args.timeout)
        elif args.command == "http":
            result = http_check(args.url, args.timeout)
        elif args.command == "ping":
            result = ping(args.host, args.timeout)
        elif args.command == "info":
            payload = local_info()
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(f"Hostname: {payload['hostname']}\nAddresses: {', '.join(payload['addresses']) or 'none'}\nPlatform: {payload['platform']}\nPython: {payload['python']}")
            return 0
        else:
            results = diagnose(args.host, args.port, args.timeout, not args.no_ping)
            if args.json:
                print(json.dumps([_result_payload(item) for item in results], ensure_ascii=False, indent=2))
            else:
                for item in results:
                    _print_result(item)
            return 0 if all(item.ok for item in results) else 1

        if args.json:
            print(json.dumps(_result_payload(result), ensure_ascii=False, indent=2))
        else:
            _print_result(result)
        return 0 if result.ok else 1
    except (ValueError, OverflowError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
