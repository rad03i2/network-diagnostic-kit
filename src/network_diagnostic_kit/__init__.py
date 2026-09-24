"""Network Diagnostic Kit public API."""

from .core import CheckResult, diagnose, dns_lookup, http_check, local_info, ping, tcp_connect

__all__ = ["CheckResult", "diagnose", "dns_lookup", "http_check", "local_info", "ping", "tcp_connect"]
__version__ = "1.0.0"
