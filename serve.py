#!/usr/bin/env python3
"""
dkn.su — Динамический локальный сервер разработки
- Автоматически отслеживает изменения в файлах (_posts, _layouts, CSS, JS, HTML) и мгновенно пересобирает сайт
- Поддерживает Live-Reload в браузере (страница сама обновляется при сохранении файлов)
- Поддерживает чистые URL без .html
- Автоматически отдает 404.html при ошибках маршрутизации
"""

import os
import sys
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(PROJECT_DIR, "_site")

# Импорт функции сборщика
try:
    import build as site_builder
except ImportError:
    site_builder = None

# Версия сборки для Live-Reload
BUILD_VERSION = 1
rebuild_lock = threading.Lock()

# Список расширений для отслеживания
WATCH_EXTENSIONS = {".html", ".css", ".js", ".md", ".yml", ".yaml", ".json"}
IGNORE_DIRS = {"_site", ".git", "__pycache__", ".venv", "venv", "env", ".idea", ".vscode"}

def get_file_mtimes():
    """Собирает время последней модификации всех отслеживаемых файлов"""
    mtimes = {}
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Исключаем служебные директории
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f.startswith(".") or f == "serve.py":
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in WATCH_EXTENSIONS:
                fpath = os.path.join(root, f)
                try:
                    mtimes[fpath] = os.path.getmtime(fpath)
                except OSError:
                    pass
    return mtimes

def watch_and_rebuild():
    """Фоновый поток для отслеживания изменений и автоматической пересборки"""
    global BUILD_VERSION
    last_mtimes = get_file_mtimes()

    while True:
        time.sleep(0.5)
        current_mtimes = get_file_mtimes()

        if current_mtimes != last_mtimes:
            changed_files = []
            for p, mtime in current_mtimes.items():
                if p not in last_mtimes or last_mtimes[p] != mtime:
                    changed_files.append(os.path.relpath(p, PROJECT_DIR))
            for p in last_mtimes:
                if p not in current_mtimes:
                    changed_files.append(f"(удален) {os.path.relpath(p, PROJECT_DIR)}")

            last_mtimes = current_mtimes

            if changed_files and site_builder:
                file_summary = ", ".join(changed_files[:3])
                if len(changed_files) > 3:
                    file_summary += f" и еще {len(changed_files) - 3}"

                print(f"\n[*] [WATCHER] Изменения в: {file_summary}")
                with rebuild_lock:
                    try:
                        time.sleep(0.1)  # Задержка для завершения записи файла редактором
                        site_builder.build()
                        BUILD_VERSION += 1
                        print(f"[+] [WATCHER] Проект пересобран! (ревизия v{BUILD_VERSION})\n")
                    except Exception as e:
                        print(f"[!] [WATCHER] Ошибка сборки: {e}\n")

# Скрипт автоматического обновления страницы в браузере
LIVE_RELOAD_SNIPPET = """
<script>
/* dkn.su dev live-reload */
(function(){
    let lastVer = null;
    setInterval(async () => {
        try {
            const res = await fetch('/_livereload_version');
            const ver = await res.text();
            if (lastVer !== null && lastVer !== ver) {
                console.log('[dkn.su] Пересборка обнаружена, перезагрузка...');
                location.reload();
            }
            lastVer = ver;
        } catch (e) {}
    }, 700);
})();
</script>
</body>
""".encode("utf-8")

class DknHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def do_GET(self):
        # 1. Эндпоинт для Live-Reload
        if self.path == "/_livereload_version":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            payload = str(BUILD_VERSION).encode("utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        # 2. Определение физического пути
        path = self.translate_path(self.path)

        # Если путь без .html (например /blog или /204)
        if not os.path.exists(path) and not path.endswith(os.sep):
            html_candidate = path + ".html"
            if os.path.exists(html_candidate):
                path = html_candidate
                self.path = self.path + ".html"

        # Если запрашивается директория, проверяем index.html внутри нее
        if os.path.isdir(path):
            idx_candidate = os.path.join(path, "index.html")
            if os.path.exists(idx_candidate):
                path = idx_candidate

        # 3. Если файл не найден — отдаем кастомный 404.html
        if not os.path.exists(path):
            self.serve_404()
            return

        # 4. Если это HTML-файл — внедряем скрипт Live-Reload
        if path.endswith(".html") and os.path.isfile(path):
            self.serve_html_with_livereload(path)
            return

        return super().do_GET()

    def serve_html_with_livereload(self, file_path):
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            if b"</body>" in content:
                content = content.replace(b"</body>", LIVE_RELOAD_SNIPPET)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Internal error: {e}")

    def serve_404(self):
        path_404 = os.path.join(SITE_DIR, "404.html")
        if os.path.exists(path_404):
            self.send_response(404, "Not Found")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            with open(path_404, "rb") as f:
                content = f.read()
            if b"</body>" in content:
                content = content.replace(b"</body>", LIVE_RELOAD_SNIPPET)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "Page Not Found")

def run(port=8080):
    # Первичная сборка при запуске сервера
    if site_builder:
        print("[*] Первичная сборка проекта dkn.su перед запуском...")
        try:
            site_builder.build()
        except Exception as e:
            print(f"[!] Ошибка первичной сборки: {e}")

    # Запуск фонового вотчера
    watcher = threading.Thread(target=watch_and_rebuild, daemon=True)
    watcher.start()

    server_address = ("", port)
    httpd = HTTPServer(server_address, DknHandler)
    print(f"[*] Сервер dkn.su запущен: http://localhost:{port}")
    print(f"[*] Корневая директория: {SITE_DIR}")
    print("[*] Автопересборка (Watcher): ВКЛЮЧЕНА (следит за _posts, _layouts, CSS, JS, HTML)")
    print("[*] Live-Reload в браузере: ВКЛЮЧЕН (страница обновляется сама)")
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
