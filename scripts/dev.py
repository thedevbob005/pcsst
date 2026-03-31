from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "4173"))


class PCSSTHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def _rewrite_root(self) -> None:
        if self.path in {"", "/"}:
            self.path = "/docs/index.html"

    def do_GET(self) -> None:
        self._rewrite_root()
        return super().do_GET()

    def do_HEAD(self) -> None:
        self._rewrite_root()
        return super().do_HEAD()


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", PORT), PCSSTHandler)
    print(f"PCSST docs server running at http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
