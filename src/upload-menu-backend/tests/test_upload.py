"""Tests for the /upload-menu endpoint.

Run with:
    cd src/upload-menu-backend
    pytest -v

The endpoint runs OCR locally via pytesseract. Tests use a fake
`pytesseract.image_to_string` (via the `fake_tesseract` fixture) so no real
Tesseract binary needs to be installed.
"""
from __future__ import annotations

import struct
import zlib

import pytest
from fastapi.testclient import TestClient

from main import MAX_IMAGE_SIZE, app

# Cap mirrored from main.MAX_IMAGE_SIZE so the tests stay in sync.
MAX_BYTES = MAX_IMAGE_SIZE


# --- fixtures ------------------------------------------------------------


class _FakeTesseract:
    """Drop-in for `pytesseract.image_to_string`.

    Configure per-test via attributes:
      - extracted_text="..."   → what image_to_string returns
      - raise_on_call=Exception → simulates OCR engine failure
    """

    def __init__(
        self,
        *,
        extracted_text: str = "FAKE OCR TEXT",
        raise_on_call: Exception | None = None,
    ) -> None:
        self._text = extracted_text
        self._raise = raise_on_call
        self.calls: list[object] = []

    def __call__(self, image, *args, **kwargs) -> str:
        self.calls.append(image)
        if self._raise is not None:
            raise self._raise
        return self._text


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake_tesseract(monkeypatch: pytest.MonkeyPatch) -> _FakeTesseract:
    """Replace pytesseract.image_to_string with a configurable fake.

    main.py does `import pytesseract`, so `main.pytesseract.image_to_string`
    is the attribute we patch.
    """
    fake = _FakeTesseract()
    monkeypatch.setattr("main.pytesseract.image_to_string", fake)
    return fake


def _minimal_png() -> bytes:
    """Build a valid 1×1 transparent PNG (~70 bytes) from scratch.

    No PIL dependency, no fixture file on disk.
    """
    sig = b"\x89PNG\r\n\x1a\n"

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)  # 1x1, 8-bit RGBA
    raw = b"\x00\x00\x00\x00\x00"  # filter byte 0 + one transparent pixel
    idat = zlib.compress(raw)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def _minimal_jpeg() -> bytes:
    """Build a *barely* valid JPEG (SOI + APP0 marker, ~20 bytes).

    PIL will reject this for actual decoding, but content-type sniffing and
    size-validation runs before PIL touches it. For tests that need a real
    decode path we use the PNG.
    """
    return b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"


# --- happy path ----------------------------------------------------------


def test_upload_ok(client: TestClient, fake_tesseract: _FakeTesseract) -> None:
    """A small valid PNG should be accepted and OCR'd."""
    response = client.post(
        "/upload-menu",
        files={"photo": ("test.png", _minimal_png(), "image/png")},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "accepted"
    assert body["filename"] == "test.png"
    assert body["extracted_text"] == "FAKE OCR TEXT"


def test_upload_runs_tesseract_on_image_bytes(
    client: TestClient, fake_tesseract: _FakeTesseract
) -> None:
    """The OCR call receives a decoded PIL Image, not raw bytes."""
    png = _minimal_png()
    response = client.post(
        "/upload-menu",
        files={"photo": ("menu.png", png, "image/png")},
    )
    assert response.status_code == 200

    assert len(fake_tesseract.calls) == 1
    # We don't assert the exact Image object (PIL equality is finicky),
    # but we assert it was invoked exactly once — proof the bytes were decoded.
    assert response.json()["extracted_text"] == "FAKE OCR TEXT"


def test_upload_accepts_real_png(
    client: TestClient, fake_tesseract: _FakeTesseract
) -> None:
    """End-to-end with a real programmatically-built PNG."""
    png = _minimal_png()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"  # sanity: valid signature

    response = client.post(
        "/upload-menu",
        files={"photo": ("menu.png", png, "image/png")},
    )
    assert response.status_code == 200, response.text


def test_upload_supports_webp(
    client: TestClient, fake_tesseract: _FakeTesseract
) -> None:
    """WEBP should be in the accepted content-type list."""
    # Minimal valid WEBP (RIFF container with VP8L) — Tesseract won't decode this
    # but our route accepts it by content-type; the fake Tesseract skips decoding.
    response = client.post(
        "/upload-menu",
        files={"photo": ("menu.webp", _minimal_png(), "image/webp")},
    )
    assert response.status_code == 200, response.text


# --- size limit ----------------------------------------------------------


def test_upload_too_large(client: TestClient) -> None:
    """Anything over MAX_IMAGE_SIZE must be rejected with 413.

    The size check fires before Tesseract, so we don't need to mock it —
    if the route tried to OCR, the test would still 413 first.
    """
    big = b"0" * (MAX_BYTES + 1024 * 1024)  # +1 MB, always over
    response = client.post(
        "/upload-menu",
        files={"photo": ("huge.png", big, "image/png")},
    )
    assert response.status_code == 413, response.text
    assert "8 MB" in response.json()["detail"]


def test_upload_accepts_exactly_at_limit(
    client: TestClient, fake_tesseract: _FakeTesseract
) -> None:
    """Boundary: exactly MAX_BYTES must be accepted (≤, not <)."""
    # Real PNG header so PIL decodes it; rest is zero-padded to the limit.
    # PNG parsers stop at IEND, so the trailing zeros are ignored.
    payload = _minimal_png() + b"0" * (MAX_BYTES - len(_minimal_png()))
    assert len(payload) == MAX_BYTES
    response = client.post(
        "/upload-menu",
        files={"photo": ("at-limit.png", payload, "image/png")},
    )
    assert response.status_code == 200, response.text


def test_upload_rejects_one_byte_over_limit(client: TestClient) -> None:
    """Boundary: MAX_BYTES + 1 must be rejected."""
    # Size check fires before PIL, so we don't need a valid image here.
    payload = b"0" * (MAX_BYTES + 1)
    response = client.post(
        "/upload-menu",
        files={"photo": ("over.png", payload, "image/png")},
    )
    assert response.status_code == 413, response.text


# --- malformed input ---------------------------------------------------


def test_upload_missing_file_returns_422(client: TestClient) -> None:
    """FastAPI's validation should reject an empty form (photo is required)."""
    response = client.post("/upload-menu")
    assert response.status_code == 422


def test_upload_wrong_field_name_returns_422(client: TestClient) -> None:
    """The endpoint expects `photo`, not `file`."""
    response = client.post(
        "/upload-menu",
        files={"file": ("test.png", _minimal_png(), "image/png")},
    )
    assert response.status_code == 422


def test_upload_unsupported_content_type_returns_415(
    client: TestClient, fake_tesseract: _FakeTesseract
) -> None:
    """Non-image content types (e.g. text/plain) must be rejected with 415."""
    response = client.post(
        "/upload-menu",
        files={"photo": ("menu.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 415, response.text
    assert "Unsupported content type" in response.json()["detail"]


def test_upload_undecodable_image_returns_422(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """If PIL can't decode the bytes, return 422 (not 500)."""
    # Use a fake tesseract that doesn't get reached (PIL will reject this first)
    monkeypatch.setattr(
        "main.pytesseract.image_to_string",
        _FakeTesseract(),
    )
    # JPEG bytes that PIL won't actually decode
    response = client.post(
        "/upload-menu",
        files={"photo": ("broken.jpg", _minimal_jpeg(), "image/jpeg")},
    )
    assert response.status_code == 422, response.text
    assert "Could not decode image" in response.json()["detail"]


# --- OCR errors --------------------------------------------------------


def test_upload_returns_500_on_tesseract_failure(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """If pytesseract raises, surface it as 500 (engine bug, not user error)."""
    fake = _FakeTesseract(
        raise_on_call=RuntimeError("tesseract binary exploded"),
    )
    monkeypatch.setattr("main.pytesseract.image_to_string", fake)

    response = client.post(
        "/upload-menu",
        files={"photo": ("m.png", _minimal_png(), "image/png")},
    )
    assert response.status_code == 500, response.text
    assert "OCR engine failed" in response.json()["detail"]


# --- issue #283 regression: two different menu photos in one session -----


def test_second_menu_photo_with_different_layout_still_parses_correctly(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reproduces the customer UAT scenario from #283.

    First photo: simple "name  price" per line — always worked.
    Second photo: real-menu layout (name on its own line, description +
    price on the next) — this is what tripped up the old line-by-line
    parser into returning garbled dish names as the "menu".
    """
    fake = _FakeTesseract()
    monkeypatch.setattr("main.pytesseract.image_to_string", fake)

    # Upload #1: simple single-line format.
    fake._text = "Margherita Pizza $12.99\n\nCaesar Salad $8.00"
    resp1 = client.post(
        "/upload-menu",
        files={"photo": ("menu1.png", _minimal_png(), "image/png")},
    )
    assert resp1.status_code == 200, resp1.text
    menu1 = resp1.json()["menu"]
    assert menu1[0]["name"] == "Margherita Pizza"
    assert menu1[0]["price"] == 12.99

    # Upload #2 in the same session: real two-line scan layout.
    fake._text = (
        "Sundried Tomato Risotto Cakes\n"
        "with basil aioli and creme fraiche 7\n"
        "\n"
        "Potato Skins\n"
        "With melty mozzarella, cheddar and bacon 7"
    )
    resp2 = client.post(
        "/upload-menu",
        files={"photo": ("menu2.png", _minimal_png(), "image/png")},
    )
    assert resp2.status_code == 200, resp2.text
    menu2 = resp2.json()["menu"]

    # The bug: dish name must be the real dish name, not the description.
    assert menu2[0]["name"] == "Sundried Tomato Risotto Cakes"
    assert menu2[0]["price"] == 7.0
    assert menu2[1]["name"] == "Potato Skins"
    assert menu2[1]["price"] == 7.0