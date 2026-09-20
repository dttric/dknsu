---
layout: post
title: "changelog // 20.09.2026"
date: 2026-09-20 20:06:00 +0300
category: release
tag: Релиз
author: dttric
excerpt: "отчет за 20 сентября: запуск dkn.su, переезд хаба на dttric.dkn.su и обновленная темная тема в RassUPK."
published: true
banner: release
version: "20.09.2026"
status: "latest"
badge: "production"
branch: "dknprojects"
---


### dkn.su

Развертывание и первый запуск основного узла `dkn.su` в изолированной тестовой ветке:

<div class="commit-tree">
    <div class="commit-row">
        <a href="https://github.com/dttric/dknsu/commit/b8e73156bb055dda30b6fd9afc35cd04c022eb20" target="_blank" class="commit-hash"><i class="bi bi-git"></i> b8e7315</a>
        <span class="commit-badge merge">merge</span>
        <span class="commit-msg">#2: ОБНОВЛЕНИЕ ЕБАТЬ</span>
        <div class="commit-meta">
            <span class="diff-add">+весь сайт</span>
            <span><i class="bi bi-person"></i> dttric</span>
        </div>
    </div>
</div>


---

### Часть 2: dkn.su & Hub // Релиз в прод и переезд

Слияние веток, открытие репозитория и перенос хаба на собственный поддомен:

<div class="commit-tree">
    <div class="commit-row">
        <span class="commit-hash"><i class="bi bi-git"></i> master</span>
        <span class="commit-badge feat">release</span>
        <span class="commit-msg">Слиты ветки <code>test</code> и <code>master</code> — сайт официально доступен</span>
        <div class="commit-meta">
            <span>dkn.su</span>
        </div>
    </div>
    <div class="commit-row">
        <span class="commit-hash"><i class="bi bi-unlock"></i> public</span>
        <span class="commit-badge chore">repo</span>
        <span class="commit-msg">Репозиторий проекта вновь переведен в публичный доступ</span>
        <div class="commit-meta">
            <span>github</span>
        </div>
    </div>
    <div class="commit-row">
        <span class="commit-hash"><i class="bi bi-signpost-split"></i> dns</span>
        <span class="commit-badge refactor">hub</span>
        <span class="commit-msg">Хаб переехал с <code>dttric.github.io</code> на <code>dttric.dkn.su</code></span>
        <div class="commit-meta">
            <span>редирект сохранен</span>
        </div>
    </div>
</div>

<div class="commit-card">
    <div class="commit-card-header">
        <span class="commit-hash"><i class="bi bi-hdd-network"></i> dttric.dkn.su</span>
        <span class="commit-badge feat">миграция</span>
        <h4 class="commit-card-title">Миграция хаба на поддомен dkn.su</h4>
    </div>
    <div class="commit-card-body">
        <p>Хаб перенесен на адрес <code>dttric.dkn.su</code> в рамках централизации доменной зоны. Старый адрес <code>dttric.github.io</code> сохраняется как редирект для бесшовного перехода. В связи с обновлением DNS-записей возможна кратковременная недоступность узла.</p>
    </div>
    <div class="commit-card-footer">
        <span>Статус: <strong>DNS Propagation</strong></span>
        <span>Зона: <strong>dkn.su</strong></span>
    </div>
</div>

---

### Часть 3: RassUPK // Обновление темной темы

Редизайн и исправление интерфейса расписания **RassUPK**:

<div class="commit-tree">
    <div class="commit-row">
        <span class="commit-hash"><i class="bi bi-palette2"></i> ui</span>
        <span class="commit-badge fix">fix</span>
        <span class="commit-msg">Исправлена и приведена в нормальный вид темная тема (мяу)</span>
        <div class="commit-meta">
            <span class="diff-add">+dark mode</span>
            <span>RassUPK</span>
        </div>
    </div>
</div>

<div class="commit-card">
    <div class="commit-card-header">
        <span class="commit-hash"><i class="bi bi-moon-stars"></i> theme</span>
        <span class="commit-badge style">дизайн</span>
        <h4 class="commit-card-title">Темная тема расписания занятий</h4>
    </div>
    <div class="commit-card-body">
        <ul>
            <li>Переработана контрастность расписания учебных пар и карточек дисциплин.</li>
            <li>Адаптирован календарь учебного года и селекторы недель/дней.</li>
            <li>Цветовая палитра синхронизирована с общей эстетикой dkn (темно-синий фон, неоновые акценты).</li>
        </ul>
    </div>
    <div class="commit-card-footer">
        <span>Модуль: <strong>RassUPK Web</strong></span>
        <span>Тема: <strong>Cyber Dark</strong></span>
    </div>
</div>
