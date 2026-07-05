#AstraSage Server Modülü
#Konum: utils/server_manager.py
#Amaç: 'as server add/delete' komutları ile birden fazla yerel web sunucusu yönetimi

import os
import shutil
import threading
import http.server
import socketserver

SERVER_DOCS_FOLDER = os.path.join("assets", "server_documents")
BASLANGIC_PORT = 5000
MAX_PORT_DENEME = 50

# Aktif sunucuları bellekte takip ediyoruz: {port: (server_nesnesi, thread_nesnesi)}
_aktif_sunucular = {}


def _bos_port_bul():
    for port in range(BASLANGIC_PORT, BASLANGIC_PORT + MAX_PORT_DENEME):
        if port not in _aktif_sunucular:
            return port
    return None


def _sunucu_calistir(port):
    os.makedirs(SERVER_DOCS_FOLDER, exist_ok=True)
    
    class SessizHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=SERVER_DOCS_FOLDER, **kwargs)
        
        def log_message(self, format, *args):
            pass  # terminalde gereksiz log mesajları basılmasın
    
    try:
        httpd = socketserver.TCPServer(("localhost", port), SessizHandler)
    except OSError as error:
        print(f"[HATA] Port {port} kullanılamıyor: {error}")
        return
    
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    
    _aktif_sunucular[port] = (httpd, thread)
    print(f"Sunucu başlatıldı: http://localhost:{port}")


def add_server(dosya_turu=None, dosya_ismi=None):
    """
    'as server add' veya 'as server add -html index.html' komutunun mantığı.
    """
    os.makedirs(SERVER_DOCS_FOLDER, exist_ok=True)
    
    if dosya_turu and dosya_ismi:
        gecerli_turler = {"html", "css", "js"}
        if dosya_turu not in gecerli_turler:
            print(f"[HATA] Geçersiz dosya türü: '{dosya_turu}'. Beklenen: html, css, js")
            return
        
        if not os.path.exists(dosya_ismi):
            print(f"[HATA] '{dosya_ismi}' bulunamadı.")
            return
        
        hedef_yol = os.path.join(SERVER_DOCS_FOLDER, os.path.basename(dosya_ismi))
        try:
            shutil.copy(dosya_ismi, hedef_yol)
            print(f"'{dosya_ismi}' sunucu dosyalarına eklendi: {hedef_yol}")
        except Exception as error:
            print(f"[HATA] Dosya kopyalanamadı: {error}")
            return
    
    port = _bos_port_bul()
    if port is None:
        print("[HATA] Kullanılabilir port bulunamadı.")
        return
    
    _sunucu_calistir(port)


def delete_server(port_str):
    """
    'as server delete <port>' komutunun mantığı.
    """
    try:
        port = int(port_str)
    except ValueError:
        print("[HATA] Port bir sayı olmalı. Örnek: as server delete 5000")
        return
    
    if port not in _aktif_sunucular:
        print(f"[HATA] Port {port}'da çalışan bir sunucu bulunamadı.")
        return
    
    httpd, thread = _aktif_sunucular[port]
    httpd.shutdown()
    httpd.server_close()
    del _aktif_sunucular[port]
    print(f"Port {port}'daki sunucu durduruldu.")


def list_servers():
    if len(_aktif_sunucular) == 0:
        print("Şu an çalışan bir sunucu yok.")
        return
    
    print("Aktif sunucular:")
    for port in _aktif_sunucular:
        print(f"  - http://localhost:{port}")
