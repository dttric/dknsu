#!/usr/bin/env python3
"""
dkn.su — Jekyll Static Site Generator / Builder
Собирает проект dknsu из _posts, _layouts и статических файлов в директорию _site/
"""

import os
import sys
import re
import json
import shutil
import subprocess

# Автоматическая установка зависимостей, если они отсутствуют в окружении (например, на Vercel)
for pkg, mod in [("pyyaml", "yaml"), ("markdown", "markdown")]:
    try:
        __import__(mod)
    except ImportError:
        print(f"[*] Установка недостающего модуля: {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import yaml
import markdown

# Настройка UTF-8 для вывода в Windows консоли
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(PROJECT_DIR, "_site")
POSTS_DIR = os.path.join(PROJECT_DIR, "_posts")
LAYOUTS_DIR = os.path.join(PROJECT_DIR, "_layouts")

def parse_frontmatter(content):
    """Разделяет YAML front matter и тело Markdown"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
                return metadata, body
            except Exception as e:
                print(f"[!] Предупреждение: ошибка разбора frontmatter YAML ({e})")
                return {}, content
    return {}, content

def load_layout(name):
    """Загружает шаблон из _layouts/"""
    path = os.path.join(LAYOUTS_DIR, f"{name}.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "{{ content }}"

def clean_liquid_tags(template):
    """Очищает оставшиеся Liquid тэги {% ... %} и {% endif %}"""
    return re.sub(r'\{%[^{}%]*%\}', '', template)

def render_template(template, context):
    """Замена Liquid/Jekyll тегов для сборки"""
    rendered = template
    for key, val in context.items():
        rendered = re.sub(r'\{\{\s*' + re.escape(key) + r'(\s*\|\s*[^}]+)?\s*\}\}', str(val), rendered)
    return clean_liquid_tags(rendered)

def build():
    print("[*] Сборка проекта dkn.su на Jekyll...")

    # 1. Создание _site/ и безопасная очистка файлов
    os.makedirs(SITE_DIR, exist_ok=True)
    for item in os.listdir(SITE_DIR):
        item_path = os.path.join(SITE_DIR, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
            else:
                os.remove(item_path)
        except Exception:
            pass

    os.makedirs(os.path.join(SITE_DIR, "blog"), exist_ok=True)

    # 2. Загрузка конфигурации
    config = {}
    config_path = os.path.join(PROJECT_DIR, "_config.yml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    # 3. Загрузка макетов
    default_layout_raw = load_layout("default")
    _, default_layout = parse_frontmatter(default_layout_raw)
    post_layout_raw = load_layout("post")
    _, post_layout = parse_frontmatter(post_layout_raw)

    # 4. Обработка постов
    posts = []
    md = markdown.Markdown(extensions=["extra", "codehilite"])

    if os.path.exists(POSTS_DIR):
        for fname in sorted(os.listdir(POSTS_DIR), reverse=True):
            if not fname.endswith(".md") or fname.startswith("_"):
                continue
            fpath = os.path.join(POSTS_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            meta, body_md = parse_frontmatter(content)
            # Пропускаем черновики и скрытые публикации
            if meta.get("published") is False:
                continue
            html_body = md.reset().convert(body_md)

            # Определяем дату и имя файла
            base_name = fname[:-3]
            # Абсолютный URL от корня сайта, чтобы избежать дублирования /blog/blog/...
            post_url = f"/blog/{base_name}"
            date_str = str(meta.get("date", ""))[:10]
            if not date_str and len(base_name) >= 10:
                date_str = base_name[:10]

            post_data = {
                "title": meta.get("title", base_name),
                "date": date_str,
                "category": meta.get("category", "article"),
                "tag": meta.get("tag", "Статья"),
                "author": meta.get("author", "dkn core"),
                "excerpt": meta.get("excerpt", body_md[:160]),
                "url": post_url,
                "content": html_body,
                "filename": base_name
            }
            posts.append(post_data)

            # Рендерим страницу отдельного поста
            post_context = {
                "page.title": post_data["title"],
                "page.date": post_data["date"],
                "page.category": post_data["category"],
                "page.tag": post_data["tag"],
                "page.author": post_data["author"],
                "site.url": "",
                "site.time": "2026",
                "content": html_body
            }
            rendered_post_body = render_template(post_layout, post_context)

            # Оборачиваем в default layout
            default_context = {
                "page.title": f"{post_data['title']} // dkn.su",
                "site.url": "",
                "site.time": "2026",
                "content": rendered_post_body
            }
            final_html = render_template(default_layout, default_context)

            # Сохраняем как blog/name.html
            out_post_path = os.path.join(SITE_DIR, "blog", f"{base_name}.html")
            with open(out_post_path, "w", encoding="utf-8") as out_f:
                out_f.write(final_html)

            # Также создаем blog/name/index.html для чистых URL на локальных серверах
            post_folder = os.path.join(SITE_DIR, "blog", base_name)
            os.makedirs(post_folder, exist_ok=True)
            with open(os.path.join(post_folder, "index.html"), "w", encoding="utf-8") as out_f:
                out_f.write(final_html)

    print(f"[+] Скомпилировано постов: {len(posts)}")

    # 5. Сборка blog.html и blog/index.html (Архив публикаций)
    blog_cards_html = []
    for p in posts:
        card = f"""
        <a href="{p['url']}" class="blog-card">
            <div class="news-meta font-monospace mb-2">
                <span class="tag-badge tag-{p['category']}">{p['tag']}</span>
                <span class="news-date"><i class="bi bi-calendar3"></i> {p['date']}</span>
                <span class="text-muted">// {p['author']}</span>
            </div>
            <h2 class="blog-card-title">{p['title']}</h2>
            <p class="blog-card-excerpt">{p['excerpt']}</p>
        </a>"""
        blog_cards_html.append(card)

    blog_content = f"""
    <div class="blog-header-section mb-4">
        <div class="d-flex justify-content-between align-items-center mb-2">
            <h1 class="h2 font-monospace fw-bold m-0">Публикации // Блог</h1>
            <span class="badge bg-secondary-subtle text-secondary font-monospace">JEKYLL ARCHIVE</span>
        </div>
        <p class="text-muted font-monospace">// статьи, релизы и технические отчеты группы dkn</p>
    </div>
    <div class="blog-list">
        {''.join(blog_cards_html)}
    </div>"""

    blog_context = {
        "page.title": "dkn.su // publications",
        "site.url": "",
        "site.time": "2026",
        "content": blog_content
    }
    final_blog_html = render_template(default_layout, blog_context)
    with open(os.path.join(SITE_DIR, "blog.html"), "w", encoding="utf-8") as f:
        f.write(final_blog_html)
    with open(os.path.join(SITE_DIR, "blog", "index.html"), "w", encoding="utf-8") as f:
        f.write(final_blog_html)
    print("[+] Собрана страница архива: _site/blog.html и _site/blog/index.html")

    # 6. Генерация _site/feed.json (первые 3 поста с красивыми ссылками)
    feed_data = {
        "articles": [
            {
                "id": f"post-{i+1}",
                "category": p["category"],
                "tag": p["tag"],
                "title": p["title"],
                "date": p["date"],
                "url": p["url"],
                "summary": p["excerpt"],
                "author": p["author"]
            }
            for i, p in enumerate(posts[:3])
        ]
    }
    with open(os.path.join(SITE_DIR, "feed.json"), "w", encoding="utf-8") as f:
        json.dump(feed_data, f, ensure_ascii=False, indent=2)
    print("[+] Сгенерирован feed.json (топ-3 поста)")

    # 7. Сборка _site/index.html (внедрение 3 последних постов)
    index_src_path = os.path.join(PROJECT_DIR, "index.html")
    with open(index_src_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    _, index_body = parse_frontmatter(index_content)

    top_posts = posts[:3]
    if top_posts:
        news_items_html = []
        for p in top_posts:
            item_html = f"""                        <a href="{p['url']}" class="news-item" data-category="{p['category']}">
                            <div class="news-meta font-monospace">
                                <span class="tag-badge tag-{p['category']}">{p['tag']}</span>
                                <span class="news-date"><i class="bi bi-calendar3"></i> {p['date']}</span>
                                <span class="text-muted">// {p['author']}</span>
                            </div>
                            <h3 class="news-title">{p['title']}</h3>
                            <p class="news-summary">{p['excerpt']}</p>
                        </a>"""
            news_items_html.append(item_html)
        rendered_news = "\n".join(news_items_html)
    else:
        rendered_news = """                        <div class="empty-feed-placeholder font-monospace text-center">
                            <i class="bi bi-inbox placeholder-icon"></i>
                            <div class="placeholder-text">// публикаций пока нет</div>
                            <div class="placeholder-subtext text-muted">новые посты появятся здесь после добавления в блог</div>
                        </div>"""

    # Заменяем содержимое контейнера новостей
    index_rendered = re.sub(
        r'(<div class="news-list" id="news-container">)(.*?)(</div>\s*</section>)',
        r'\1\n' + rendered_news.replace('\\', '\\\\') + r'\n                    \3',
        index_body,
        flags=re.DOTALL
    )

    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_rendered)
    print("[+] Собрана главная страница: _site/index.html (топ-3 поста)")

    # 8. Копирование остальных статических файлов
    static_files = [
        "style.css",
        "blog.css",
        "error.css",
        "app.js",
        "204.html",
        "404.html",
        "CNAME",
        "vercel.json",
        "serve.py",
        "start.bat"
    ]
    for sf in static_files:
        src = os.path.join(PROJECT_DIR, sf)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(SITE_DIR, sf))

    print(f"[+] Скопированы статические файлы: {', '.join(static_files)}")
    print("[OK] Сборка успешно завершена в директорию _site/!")

if __name__ == "__main__":
    build()
