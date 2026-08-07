#!/usr/bin/env python3
"""
Ses Görselleştiriciyi Otomatik Tarayıcıda Aç
----------------------------------------------
Bu script, ses_gorsellestirici.html dosyasını yerel bir sunucu
üzerinden yayınlar ve varsayılan tarayıcınızda otomatik olarak açar.

Neden doğrudan dosyayı açmak yerine sunucu kullanıyoruz?
Tarayıcılar "file://" ile açılan sayfalarda mikrofon (getUserMedia)
erişimine izin vermeyebilir. Yerel bir sunucu (http://localhost)
üzerinden açmak bu sorunu çözer.

Kullanım:
    python3 baslat.py

Not: ses_gorsellestirici.html dosyasının bu script ile AYNI KLASÖRDE
olması gerekir.
"""

import http.server
import socketserver
import threading
import webbrowser
import os
import sys

PORT = 8000
HTML_FILE = "ses_gorsellestirici.html"


def find_free_port(start_port):
    """Eğer PORT doluysa, boş bir port bulana kadar dener."""
    import socket
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
        port += 1
    raise RuntimeError("Boş port bulunamadı.")


def run(parcalar=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, HTML_FILE)

    if not os.path.exists(html_path):
        print(f"HATA: '{HTML_FILE}' dosyası bulunamadı.")
        print(f"Bu scriptin, HTML dosyasıyla aynı klasörde olduğundan emin olun:")
        print(f"  {script_dir}")
        sys.exit(1)

    os.chdir(script_dir)

    port = find_free_port(PORT)

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("localhost", port), handler) as httpd:
        url = f"http://localhost:{port}/{HTML_FILE}"
        print(f"Sunucu başlatıldı: {url}")
        print("Tarayıcı otomatik açılıyor... Durdurmak için CTRL+C basın.")

        # Tarayıcıyı ayrı bir thread'de biraz gecikmeyle aç (sunucunun
        # tam olarak ayağa kalkmasını garantilemek için)
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu durduruldu.")
            httpd.shutdown()


if __name__ == "__main__":
    main()
