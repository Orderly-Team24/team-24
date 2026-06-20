"""Tests for the /upload-menu endpoint.

Run with:
    cd src/upload-menu-backend
    pytest -v

The endpoint forwards the photo to an OCR service over HTTP. Tests use a
fake httpx.AsyncClient (via the `fake_ocr` fixture) so no real OCR service
needs to be running.
"""
from __future__ import annotations

import struct
import zlib

import httpx
import pytest
from fastapi.testclient import TestClient

from main import MAX_IMAGE_SIZE, app

# Cap mirrored from main.MAX_IMAGE_SIZE so the tests stay in sync.
MAX_BYTES = MAX_IMAGE_SIZE


# --- fixtures ------------------------------------------------------------


class _FakeResponse:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if 400 <= self.status_code:
            raise httpx.HTTPStatusError(
                "fake error", request=None, response=self
            )


class _FakeOCRClient:
    """Drop-in for httpx.AsyncClient that records calls and returns fakes.

    Configure per-test via attributes:
      - response_status=200 (default) → fake 200 OK
      - raise_on_post=httpx.TimeoutException(...) → simulates OCR timeout
      - raise_on_post=httpx.ConnectError(...)    → simulates OCR unreachable
    """

    def __init__(
        self,
        *,
        response_status: int = 200,
        raise_on_post: Exception | None = None,
    ) -> None:
        self._status = response_status
        self._raise = raise_on_post
        self.calls: list[dict] = []

    async def __aenter__(self) -> "_FakeOCRClient":
        return self

    async def __aexit__(self, *exc) -> None:
        return None

    async def post(self, url: str, **kwargs) -> _FakeResponse:
        self.calls.append({"url": url, **kwargs})
        if self._raise is not None:
            raise self._raise
        return _FakeResponse(self._status)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake_ocr(monkeypatch: pytest.MonkeyPatch) -> _FakeOCRClient:
    """Replace httpx.AsyncClient with a configurable fake.

    main.py does `import httpx`, so `main.httpx` is the module object we patch.
    The route's `httpx.AsyncClient(...)` then resolves to our fake.
    """
    fake = _FakeOCRClient()
    monkeypatch.setattr("main.httpx.AsyncClient", lambda *a, **kw: fake)
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


# --- happy path ----------------------------------------------------------


def test_upload_ok(client: TestClient, fake_ocr: _FakeOCRClient) -> None:
    """A small valid JPEG should be accepted and forwarded to the OCR service."""
    response = client.post(
        "/upload-menu",
        files={"photo": ("test.jpg", b"fake-jpeg-bytes", "image/jpeg")},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body == {"status": "accepted", "filename": "test.jpg"}


def test_upload_forwards_correctly_to_ocr(
    client: TestClient, fake_ocr: _FakeOCRClient
) -> None:
    """Verify the OCR call carries the right URL, filename, content-type, and bytes."""
    payload = b"payload-bytes-here"
    response = client.post(
        "/upload-menu",
        files={"photo": ("menu.jpg", payload, "image/jpeg")},
    )
    assert response.status_code == 200

    assert len(fake_ocr.calls) == 1
    call = fake_ocr.calls[0]
    assert call["url"] == "http://localhost:8002/extract-text"

    # httpx `files=` dict: {"photo": (filename, bytes, content_type)}
    files = call["files"]
    assert files["photo"][0] == "menu.jpg"      # filename preserved
    assert files["photo"][1] == payload         # bytes forwarded verbatim
    assert files["photo"][2] == "image/jpeg"    # content type forwarded


def test_upload_accepts_real_png(client: TestClient, fake_ocr: _FakeOCRClient) -> None:
    """End-to-end with a real programmatically-built PNG."""
    png = _minimal_png()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"  # sanity: valid signature

    response = client.post(
        "/upload-menu",
        files={"photo": ("menu.png", png, "image/png")},
    )
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "accepted"


# --- size limit ----------------------------------------------------------


def test_upload_too_large(client: TestClient) -> None:
    """Anything over MAX_IMAGE_SIZE must be rejected with 413.

    The size check fires before the OCR call, so we don't need to mock httpx —
    if the route tried to make the call, the test would still 413 first.
    """
    big = b"0" * (MAX_BYTES + 1024 * 1024)  # +1 MB, always over
    response = client.post(
        "/upload-menu",
        files={"photo": ("huge.jpg", big, "image/jpeg")},
    )
    assert response.status_code == 413, response.text
    assert "8 MB" in response.json()["detail"]


def test_upload_accepts_exactly_at_limit(
    client: TestClient, fake_ocr: _FakeOCRClient
) -> None:
    """Boundary: exactly MAX_BYTES must be accepted (≤, not <)."""
    payload = b"0" * MAX_BYTES
    response = client.post(
        "/upload-menu",
        files={"photo": ("at-limit.jpg", payload, "image/jpeg")},
    )
    assert response.status_code == 200, response.text


def test_upload_rejects_one_byte_over_limit(client: TestClient) -> None:
    """Boundary: MAX_BYTES + 1 must be rejected."""
    payload = b"0" * (MAX_BYTES + 1)
    response = client.post(
        "/upload-menu",
        files={"photo": ("over.jpg", payload, "image/jpeg")},
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
        files={"file": ("test.jpg", b"x", "image/jpeg")},
    )
    assert response.status_code == 422


# --- OCR service errors ------------------------------------------------


def test_upload_returns_504_on_ocr_timeout(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When the OCR service times out, the route should return 504."""
    fake = _FakeOCRClient(raise_on_post=httpx.TimeoutException("slow"))
    monkeypatch.setattr("main.httpx.AsyncClient", lambda *a, **kw: fake)

    response = client.post(
        "/upload-menu",
        files={"photo": ("m.jpg", b"x", "image/jpeg")},
    )
    assert response.status_code == 504, response.text
    assert "timeout" in response.json()["detail"].lower()


def test_upload_returns_502_on_ocr_http_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When the OCR service returns an HTTP error, the route should return 502."""
    fake = _FakeOCRClient(response_status=500)
    monkeypatch.setattr("main.httpx.AsyncClient", lambda *a, **kw: fake)

    response = client.post(
        "/upload-menu",
        files={"photo": ("m.jpg", b"x", "image/jpeg")},
    )
    assert response.status_code == 502, response.text
    assert "OCR service error" in response.json()["detail"]


def test_upload_returns_502_on_ocr_connection_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When the OCR service is unreachable, the route should return 502."""
    fake = _FakeOCRClient(raise_on_post=httpx.ConnectError("connection refused"))
    monkeypatch.setattr("main.httpx.AsyncClient", lambda *a, **kw: fake)

    response = client.post(
        "/upload-menu",
        files={"photo": ("m.jpg", b"x", "image/jpeg")},
    )
    assert response.status_code == 502, response.text