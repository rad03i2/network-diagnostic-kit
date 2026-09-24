from __future__ import annotations

import http.client
import ipaddress
import platform
import socket
import subprocess
import time
from dataclasses import asdict, dataclass
from typing import Any
from urllib.parse import urlparse


@dataclass(frozen=True)
class CheckResult:
    check: str
    target: str
    ok: bool
    latency_ms: float | None = None
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _host(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("target must not be empty")
    if len(value) > 253:
        raise ValueError("target is too long")
    return value


def dns_lookup(host: str) -> CheckResult:
    host = _host(host)
    started = time.perf_counter()
    try:
        infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        addresses = sorted({item[4][0] for item in infos})
        elapsed = (time.perf_counter() - started) * 1000
        return CheckResult("dns", host, True, round(elapsed, 2), ", ".join(addresses))
    except socket.gaierror as exc:
        elapsed = (time.perf_counter() - started) * 1000
        return CheckResult("dns", host, False, round(elapsed, 2), str(exc))


def tcp_connect(host: str, port: int, timeout: float = 3.0) -> CheckResult:
    host = _host(host)
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    target = f"{host}:{port}"
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = (time.perf_counter() - started) * 1000
            return CheckResult("tcp", target, True, round(elapsed, 2), "connection established")
    except OSError as exc:
        elapsed = (time.perf_counter() - started) * 1000
        return CheckResult("tcp", target, False, round(elapsed, 2), str(exc))


def http_check(url: str, timeout: float = 5.0) -> CheckResult:
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL must use http:// or https:// and include a host")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    connection_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    started = time.perf_counter()
    conn = connection_cls(parsed.hostname, port, timeout=timeout)
    try:
        conn.request("HEAD", path, headers={"User-Agent": "network-diagnostic-kit/1.0"})
        response = conn.getresponse()
        response.read()
        elapsed = (time.perf_counter() - started) * 1000
        ok = 200 <= response.status < 400
        return CheckResult("http", url, ok, round(elapsed, 2), f"HTTP {response.status} {response.reason}")
    except OSError as exc:
        elapsed = (time.perf_counter() - started) * 1000
        return CheckResult("http", url, False, round(elapsed, 2), str(exc))
    finally:
        conn.close()


def ping(host: str, timeout: float = 3.0) -> CheckResult:
    host = _host(host)
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    system = platform.system().lower()
    if system == "windows":
        command = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), host]
    else:
        command = ["ping", "-c", "1", "-W", str(max(1, int(timeout))), host]
    started = time.perf_counter()
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 1, check=False)
        elapsed = (time.perf_counter() - started) * 1000
        detail = (proc.stdout or proc.stderr).strip().splitlines()[-1:] or ["no output"]
        return CheckResult("ping", host, proc.returncode == 0, round(elapsed, 2), detail[0])
    except (OSError, subprocess.TimeoutExpired) as exc:
        elapsed = (time.perf_counter() - started) * 1000
        return CheckResult("ping", host, False, round(elapsed, 2), str(exc))


def local_info() -> dict[str, Any]:
    hostname = socket.gethostname()
    addresses: set[str] = set()
    try:
        for item in socket.getaddrinfo(hostname, None):
            address = item[4][0]
            try:
                ip = ipaddress.ip_address(address.split("%", 1)[0])
                if not ip.is_loopback:
                    addresses.add(address)
            except ValueError:
                continue
    except socket.gaierror:
        pass
    return {"hostname": hostname, "addresses": sorted(addresses), "platform": platform.system(), "python": platform.python_version()}


def diagnose(host: str, port: int = 443, timeout: float = 3.0, include_ping: bool = True) -> list[CheckResult]:
    host = _host(host)
    results = [dns_lookup(host), tcp_connect(host, port, timeout)]
    if include_ping:
        results.append(ping(host, timeout))
    return results
