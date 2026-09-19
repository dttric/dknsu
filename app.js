/**
 * dkn.su — Hub & Dashboard Script
 */

// Резервные данные на случай открытия через file:// без веб-сервера
const FALLBACK_DATA = {
    articles: [
        {
            id: "post-1",
            category: "release",
            tag: "Релиз",
            title: "Обновление инфраструктуры dkn.su и запуск дашборда",
            date: "2026-09-20",
            url: "/blog/2026-09-20-infrastructure-update",
            summary: "Развернут новый узел dkn.su. Переработана структура сервисов, внедрена модульная система виджетов и интеграция с Jekyll-блогом.",
            author: "dkn team"
        },
        {
            id: "post-2",
            category: "article",
            tag: "Статья",
            title: "Архитектура легковесных веб-сервисов на dknhttp",
            date: "2026-08-14",
            url: "/blog/2026-08-14-lightweight-web-services",
            summary: "Разбор принципов проектирования минималистичных HTTP-демонов и микросервисов для внутренних нужд группы.",
            author: "root"
        },
        {
            id: "post-3",
            category: "announcement",
            tag: "Объявление",
            title: "Формирование репозиториев и открытие новых веток",
            date: "2026-07-02",
            url: "/blog/2026-07-02-repositories-and-branches",
            summary: "Синхронизация проектов группы dkn, настройка вебхуков и публичных зеркал для открытых инструментов.",
            author: "dkn core"
        }
    ]
};

let currentArticles = [];
let activeFilter = 'all';

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initFilters();
    loadDashboardData();
});

// Загрузка данных (из feed.json или fallback)
async function loadDashboardData(callback) {
    try {
        const response = await fetch('/feed.json', { cache: 'no-store' });
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        const data = await response.json();
        renderData(data);
    } catch (err) {
        console.warn('Загрузка feed.json не удалась (возможно локальный file://), используются резервные данные:', err);
        renderData(FALLBACK_DATA);
    } finally {
        if (typeof callback === 'function') callback();
    }
}

// Отрисовка данных (берем первые 3 поста для издания)
function renderData(data) {
    if (data.articles) {
        currentArticles = data.articles.slice(0, 3);
        renderArticles(currentArticles, activeFilter);
    }
}

// Отрисовка новостей с учетом фильтра
function renderArticles(articles, filter) {
    const container = document.getElementById('news-container');
    if (!container) return;

    const filtered = filter === 'all' 
        ? articles 
        : articles.filter(item => item.category === filter);

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="text-muted font-monospace py-4 text-center">
                В этой категории пока нет записей.
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(item => `
        <a href="${escapeHtml(item.url || '/blog')}" class="news-item">
            <div class="news-meta font-monospace">
                <span class="tag-badge tag-${escapeHtml(item.category)}">${escapeHtml(item.tag || item.category)}</span>
                <span class="news-date"><i class="bi bi-calendar3"></i> ${escapeHtml(item.date)}</span>
                ${item.author ? `<span class="text-muted">// ${escapeHtml(item.author)}</span>` : ''}
            </div>
            <h3 class="news-title">${escapeHtml(item.title)}</h3>
            <p class="news-summary">${escapeHtml(item.summary)}</p>
        </a>
    `).join('');
}

// Обработка кликов по фильтрам категорий
function initFilters() {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeFilter = btn.getAttribute('data-filter');
            renderArticles(currentArticles, activeFilter);
        });
    });
}

// Безопасное экранирование строк
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
