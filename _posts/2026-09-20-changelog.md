---
layout: post
title: "changelog // 20.09.2026"
date: 2026-09-20 20:06:00 +0300
category: release
tag: Релиз
author: dttric
excerpt: "отчет за 20 сентября: запуск dkn.su, переезд хаба на dttric.dkn.su и обновленная темная тема в RassUPK."
published: true

banner: false
---

---
### dkn.su

`dkn.su` был запущен на тестовом домене `dev.dkn.su` для теста<br>
как оказалось позже у вас к нему доступа наху нет так что да
<br><br>
ниже можете посмотреть что случилось:

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

### dttric/hub



<div class="commit-card">
    <div class="commit-card-header">
        <a href="https://github.com/dttric/hub/commit/99e1dce82829f49feff0a7c9862391bace39f4b9" target="_blank" class="commit-hash"><i class="bi bi-git"></i> 99e1dce</a>
        <h4 class="commit-card-title">Миграция хаба на поддомен dkn.su</h4>
    </div>
    <div class="commit-card-body">
        <p>Хаб перенесен на адрес <code>dttric.dkn.su</code> в рамках централизации доменной зоны. Старый адрес <code>dttric.github.io</code> сохраняется как редирект для бесшовного перехода.</p>
        <p class="text-muted small mb-0">// В связи с обновлением DNS-записей возможна кратковременная недоступность узла.</p>
    </div>
    <div class="commit-card-footer">
        <span>Статус: <strong>Сайт работает</strong></span>
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
