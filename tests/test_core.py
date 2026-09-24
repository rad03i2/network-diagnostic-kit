from unittest.mock import MagicMock, patch

import pytest

from network_diagnostic_kit.core import dns_lookup, http_check, local_info, tcp_connect


def test_dns_lookup_collects_unique_addresses():
    fake = [(2, 1, 6, "", ("1.1.1.1", 0)), (2, 1, 6, "", ("1.1.1.1", 0)), (2, 1, 6, "", ("8.8.8.8", 0))]
    with patch("socket.getaddrinfo", return_value=fake):
        result = dns_lookup("example.test")
    assert result.ok
    assert result.detail == "1.1.1.1, 8.8.8.8"


def test_tcp_validates_port():
    with pytest.raises(ValueError, match="port"):
        tcp_connect("localhost", 70000)


def test_tcp_success():
    context = MagicMock()
    context.__enter__.return_value = object()
    with patch("socket.create_connection", return_value=context) as connect:
        result = tcp_connect("localhost", 443, 1)
    assert result.ok
    connect.assert_called_once_with(("localhost", 443), timeout=1)


def test_http_rejects_non_http_scheme():
    with pytest.raises(ValueError, match="http"):
        http_check("ftp://example.test/file")


def test_http_status_success():
    response = MagicMock(status=204, reason="No Content")
    connection = MagicMock()
    connection.getresponse.return_value = response
    with patch("http.client.HTTPSConnection", return_value=connection):
        result = http_check("https://example.test/health")
    assert result.ok
    assert "204" in result.detail
    connection.close.assert_called_once()


def test_local_info_has_expected_keys():
    info = local_info()
    assert {"hostname", "addresses", "platform", "python"} <= info.keys()
