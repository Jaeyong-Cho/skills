#!/usr/bin/env python3
"""
Serve a built gallery directory over HTTP and print the URL to open.

Usage:
  python serve.py <gallery-dir> [port]

Defaults: binds 0.0.0.0:4800. Serves <gallery-dir>/index.html.
"""
import sys, os, http.server, socketserver, functools

HOST = "0.0.0.0"
DEFAULT_PORT = 4800

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    directory = os.path.abspath(sys.argv[1])
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    if not os.path.isfile(os.path.join(directory, "index.html")):
        sys.exit(f"no index.html in {directory} — build the gallery first")

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    with socketserver.TCPServer((HOST, port), handler) as httpd:
        print(f"serving {directory} at http://localhost:{port}/  (Ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")

if __name__ == "__main__":
    main()
