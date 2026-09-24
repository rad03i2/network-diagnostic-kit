import json
from unittest.mock import patch

from network_diagnostic_kit.cli import main
from network_diagnostic_kit.core import CheckResult


def test_dns_json(capsys):
    with patch("network_diagnostic_kit.cli.dns_lookup", return_value=CheckResult("dns", "x", True, 1.2, "127.0.0.1")):
        assert main(["dns", "x", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True


def test_failed_check_returns_one():
    with patch("network_diagnostic_kit.cli.tcp_connect", return_value=CheckResult("tcp", "x:1", False, 2.0, "refused")):
        assert main(["tcp", "x", "1"]) == 1


def test_invalid_input_returns_two(capsys):
    assert main(["tcp", "x", "0"]) == 2
    assert "port" in capsys.readouterr().err


def test_diagnose_aggregates_status():
    results = [CheckResult("dns", "x", True), CheckResult("tcp", "x:443", False)]
    with patch("network_diagnostic_kit.cli.diagnose", return_value=results):
        assert main(["diagnose", "x", "--no-ping"]) == 1
