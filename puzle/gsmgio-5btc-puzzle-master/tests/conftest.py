"""Isolate test-suite file writes under pytest's tmp_path.

Several legacy solver ``run()`` and ``evaluate()`` entry points write their
``*_audit.json`` / ``*_experiment.json`` artifacts directly to
``PACKAGE_ROOT``. Without write redirection, running ``pytest`` silently
overwrites committed evidence artifacts on disk (for example, truncating
``intertwined_password_coherence_audit.json`` to ``limit=400``).

This autouse fixture intercepts every write targeting a path inside
``PACKAGE_ROOT`` (outside ``tmp_path``) and redirects it to the mirrored path
under ``tmp_path``, while serving reads of already-redirected paths from
``tmp_path`` so assertions that read back written files continue to pass.
"""

from __future__ import annotations

from pathlib import Path
import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


@pytest.fixture(autouse=True)
def _isolate_package_writes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    tmp_root = tmp_path.resolve()
    redirected: dict[Path, Path] = {}

    orig_write_text = Path.write_text
    orig_write_bytes = Path.write_bytes
    orig_read_text = Path.read_text
    orig_read_bytes = Path.read_bytes
    orig_exists = Path.exists
    orig_open = Path.open

    def _redirect_for_write(path: Path) -> Path:
        resolved = path.resolve()
        if _is_under(resolved, PACKAGE_ROOT) and not _is_under(resolved, tmp_root):
            rel = resolved.relative_to(PACKAGE_ROOT)
            dest = tmp_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            redirected[resolved] = dest
            return dest
        return path

    def _resolve_for_read(path: Path) -> Path:
        resolved = path.resolve()
        return redirected.get(resolved, path)

    def patched_write_text(self: Path, data: str, *args, **kwargs):
        return orig_write_text(_redirect_for_write(self), data, *args, **kwargs)

    def patched_write_bytes(self: Path, data: bytes):
        return orig_write_bytes(_redirect_for_write(self), data)

    def patched_read_text(self: Path, *args, **kwargs):
        return orig_read_text(_resolve_for_read(self), *args, **kwargs)

    def patched_read_bytes(self: Path):
        return orig_read_bytes(_resolve_for_read(self))

    def patched_exists(self: Path, *args, **kwargs):
        return orig_exists(_resolve_for_read(self), *args, **kwargs)

    def patched_open(self: Path, mode: str = "r", *args, **kwargs):
        if any(flag in mode for flag in ("w", "a", "x", "+")):
            return orig_open(_redirect_for_write(self), mode, *args, **kwargs)
        return orig_open(_resolve_for_read(self), mode, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", patched_write_text)
    monkeypatch.setattr(Path, "write_bytes", patched_write_bytes)
    monkeypatch.setattr(Path, "read_text", patched_read_text)
    monkeypatch.setattr(Path, "read_bytes", patched_read_bytes)
    monkeypatch.setattr(Path, "exists", patched_exists)
    monkeypatch.setattr(Path, "open", patched_open)
