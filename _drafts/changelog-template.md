---
# ==============================================================================
# ШАБЛОН ЧЕНДЖЛОГА / РЕЛИЗА ДЛЯ DKN.SU
# Для скрытия используйте: published: false
# ==============================================================================

layout: post
title: "Ченджлог // Релиз v1.1.0"
date: 2026-09-20 20:00:00 +0300
category: release                      # release подсвечивается зеленым на дашборде
tag: Релиз
author: dkn core
excerpt: "Обновление узла dkn.su: поддержка интерактивных ченджлогов, красивое дерево коммитов и новые компоненты дашборда."
published: false

# Универсальный баннер релиза ПО / ченджлога (ВИД 1)
banner: release
version: "v1.1.0"
status: "latest"
badge: "stable"
branch: "branch: test"

---

Краткое введение в релиз: что было сделано, почему это важно и какие основные изменения вошли в текущую итерацию.

---

### История изменений (Дерево коммитов)

<div class="commit-tree">
    <!-- Коммит с новой фичей (feat) -->
    <div class="commit-row">
        <a href="https://github.com/dttric/dknsu/commit/4502e04" target="_blank" class="commit-hash"><i class="bi bi-git"></i> 4502e04</a>
        <span class="commit-badge feat">feat</span>
        <span class="commit-msg">Добавлена бутстраповская анимация плейсхолдера для иконок соцсетей</span>
        <div class="commit-meta">
            <span class="commit-diff"><span class="diff-add">+22</span> <span class="diff-del">-23</span></span>
            <span><i class="bi bi-person"></i> dttric</span>
        </div>
    </div>

    <!-- Коммит с багфиксом (fix) -->
    <div class="commit-row">
        <a href="https://github.com/dttric/dknsu/commit/aa9913b" target="_blank" class="commit-hash"><i class="bi bi-git"></i> aa9913b</a>
        <span class="commit-badge fix">fix</span>
        <span class="commit-msg">Исправлена видимость круглых плейсхолдеров на темном фоне</span>
        <div class="commit-meta">
            <span class="commit-diff"><span class="diff-add">+42</span> <span class="diff-del">-4</span></span>
            <span><i class="bi bi-person"></i> dttric</span>
        </div>
    </div>

    <!-- Коммит с рефакторингом (refactor) -->
    <div class="commit-row">
        <a href="https://github.com/dttric/dknsu/commit/f624a74" target="_blank" class="commit-hash"><i class="bi bi-git"></i> f624a74</a>
        <span class="commit-badge refactor">refactor</span>
        <span class="commit-msg">Статическая генерация топ-3 постов в HTML без лишних AJAX-запросов</span>
        <div class="commit-meta">
            <span class="commit-diff"><span class="diff-add">+120</span> <span class="diff-del">-121</span></span>
            <span><i class="bi bi-person"></i> dttric</span>
        </div>
    </div>

    <!-- Коммит с оптимизацией (perf) -->
    <div class="commit-row">
        <span class="commit-hash"><i class="bi bi-git"></i> 8e21ab9</span>
        <span class="commit-badge perf">perf</span>
        <span class="commit-msg">Ускорена отрисовка анимации на GPU и уменьшен размер CSS</span>
        <div class="commit-meta">
            <span class="commit-diff"><span class="diff-add">+14</span> <span class="diff-del">-8</span></span>
            <span><i class="bi bi-person"></i> root</span>
        </div>
    </div>

    <!-- Коммит документации (docs) -->
    <div class="commit-row">
        <span class="commit-hash"><i class="bi bi-git"></i> 3c19df2</span>
        <span class="commit-badge docs">docs</span>
        <span class="commit-msg">Созданы подробные шаблоны для статей и ченджлогов</span>
        <div class="commit-meta">
            <span class="commit-diff"><span class="diff-add">+80</span> <span class="diff-del">-0</span></span>
            <span><i class="bi bi-person"></i> dkn core</span>
        </div>
    </div>

    <!-- Коммит обслуживания / инфраструктуры (chore / ci) -->
    <div class="commit-row">
        <span class="commit-hash"><i class="bi bi-git"></i> 1a84f01</span>
        <span class="commit-badge chore">chore</span>
        <span class="commit-msg">Настройка правил .gitignore и очистка временных файлов сборки</span>
        <div class="commit-meta">
            <span class="commit-diff"><span class="diff-add">+5</span> <span class="diff-del">-2</span></span>
            <span><i class="bi bi-person"></i> dkn core</span>
        </div>
    </div>
</div>

---

### Крупные изменения (Детальные карточки)

<!-- Подробная карточка важного коммита или фичи -->
<div class="commit-card">
    <div class="commit-card-header">
        <span class="commit-hash"><i class="bi bi-git"></i> 4502e04</span>
        <span class="commit-badge feat">feat</span>
        <h4 class="commit-card-title">Интеграция скелетон-анимации в панель навигации</h4>
    </div>
    <div class="commit-card-body">
        <p>Полностью переработан механизм отображения неактивных и будущих сервисов в сайдбаре:</p>
        <ul>
            <li>Иконка GitHub переведена в статус плейсхолдера с мягким пульсирующим свечением.</li>
            <li>Добавлены слоты для будущих сервисов группы в виде аккуратных контурных кругляшков.</li>
            <li>Все плейсхолдеры работают на аппаратном ускорении без лишней нагрузки на CPU.</li>
        </ul>
    </div>
    <div class="commit-card-footer">
        <span><i class="bi bi-person"></i> Автор: <strong>dttric</strong></span>
        <span>Изменения: <span class="diff-add">+22 строк</span>, <span class="diff-del">-23 строк</span> (2 файла)</span>
    </div>
</div>

---

### Пример дифф-блока кода

```diff
@@ -30,6 +30,12 @@
  <div class="social-row">
      <a href="https://t.me/dknprojects" target="_blank"><i class="bi bi-telegram"></i></a>
+     <span class="placeholder-glow">
+         <span class="social-item social-placeholder-icon"><i class="bi bi-github"></i></span>
+     </span>
  </div>
```
