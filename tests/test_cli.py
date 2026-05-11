from __future__ import annotations

from sfmapi_bench.cli import main


def test_list_presets(capsys) -> None:
    assert main(["list-presets"]) == 0
    out = capsys.readouterr().out
    assert "generic" in out
    assert "hloc" in out
