/**
 * dkn.su — Hub & Dashboard Script
 */

let currentArticles = [];
let activeFilter = 'all';

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initFilters();
    loadDashboardData();
});

// Загрузка данных из feed.json
async function loadDashboardData(callback) {
    try {
        const response = await fetch('/feed.json', { cache: 'no-store' });
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        const data = await response.json();
        renderData(data);
    } catch (err) {
        console.warn('Загрузка feed.json не удалась, используются резервные данные:', err);
        renderData({ articles: [] });
    } finally {
        if (typeof callback === 'function') callback();
    }
}

// Отрисовка данных (правило: ровно 3 последних поста)
function renderData(data) {
    const rawArticles = Array.isArray(data.articles) ? data.articles : [];

    // Сортируем по дате (свежие сверху) и берем ровно 3 последних
    currentArticles = rawArticles
        .slice()
        .sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0))
        .slice(0, 3);

    renderArticles(currentArticles, activeFilter);
}

// Отрисовка постов в блок «Издание»
function renderArticles(articles, filter) {
    const container = document.getElementById('news-container');
    if (!container) return;

    // 1. Если постов в блоге вообще нет
    if (!articles || articles.length === 0) {
        container.innerHTML = `
            <div class="empty-feed-placeholder font-monospace text-center">
                <i class="bi bi-inbox placeholder-icon"></i>
                <div class="placeholder-text">// публикаций пока нет</div>
                <div class="placeholder-subtext text-muted">новые посты появятся здесь после добавления в блог</div>
            </div>
        `;
        return;
    }

    // 2. Фильтрация по рубрике
    const filtered = filter === 'all' 
        ? articles 
        : articles.filter(item => item.category === filter);

    // 3. Если по выбранному фильтру ничего не найдено
    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-feed-placeholder font-monospace text-center py-4">
                <i class="bi bi-funnel placeholder-icon fs-3"></i>
                <div class="placeholder-text fs-6">// в категории «${escapeHtml(filter)}» пока нет записей</div>
            </div>
        `;
        return;
    }

    // 4. Отрисовка карточек
    container.innerHTML = filtered.map(item => `
        <a href="${escapeHtml(item.url || '/blog')}" class="news-item">
            <div class="news-meta font-monospace">
                <span class="tag-badge tag-${escapeHtml(item.category || 'article')}">${escapeHtml(item.tag || item.category || 'статья')}</span>
                <span class="news-date"><i class="bi bi-calendar3"></i> ${escapeHtml(item.date || '')}</span>
                ${item.author ? `<span class="text-muted">// ${escapeHtml(item.author)}</span>` : ''}
            </div>
            <h3 class="news-title">${escapeHtml(item.title || 'Без названия')}</h3>
            <p class="news-summary">${escapeHtml(item.summary || '')}</p>
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
