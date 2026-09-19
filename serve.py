#!/usr/bin/env python3
"""
Локальный сервер для dkn.su
Автоматически перенаправляет любые 404 ошибки на 404.html и поддерживает чистые ссылки без .html
"""

import os
import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Папка с файлами сайта
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_site")
if not os.path.exists(BASE_DIR):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DknHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        # Получаем физический путь к файлу
        path = self.translate_path(self.path)

        # 1. Если запрашивается путь без .html (например /blog или /204)
        if not os.path.exists(path) and not path.endswith(os.sep):
            html_candidate = path + ".html"
            if os.path.exists(html_candidate):
                self.path = self.path + ".html"
                return super().do_GET()

        # 2. Если файл/директория не найдены — отдаем 404.html
        if not os.path.exists(path):
            self.serve_404()
            return

        return super().do_GET()

    def serve_404(self):
        path_404 = os.path.join(BASE_DIR, "404.html")
        if os.path.exists(path_404):
            self.send_response(404, "Not Found")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            with open(path_404, "rb") as f:
                content = f.read()
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "Page Not Found")

def run(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, DknHandler)
    print(f"[*] Сервер dkn.su запущен: http://localhost:{port}")
    print(f"[*] Корневая директория: {BASE_DIR}")
    print("[*] Ошибки 404 автоматически отдают 404.html")
    print("[*] Нажмите Ctrl + C для остановки")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Сервер остановлен.")

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run(port)
