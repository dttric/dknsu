/**
 * dkn.su — Hub & Dashboard Script
 */

let activeFilter = 'all';

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    initFilters();
});

// Фильтрация существующих постов дашборда по рубрикам
function initFilters() {
    const buttons = document.querySelectorAll('.filter-btn');
    const container = document.getElementById('news-container');
    if (!container) return;

    // Собираем все отрендеренные карточки новостей (максимум 3)
    const items = Array.from(container.querySelectorAll('.news-item'));

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeFilter = btn.getAttribute('data-filter') || 'all';

            // Удаляем временное сообщение о пустой категории, если оно было создано
            const existingNotice = container.querySelector('.filter-empty-notice');
            if (existingNotice) {
                existingNotice.remove();
            }

            // Если постов в блоге изначально нет (показана стандартная заглушка)
            if (items.length === 0) return;

            let visibleCount = 0;
            items.forEach(item => {
                const category = item.getAttribute('data-category');
                if (activeFilter === 'all' || category === activeFilter) {
                    item.style.display = '';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });

            // Если по выбранному фильтру среди 3 последних постов ничего нет
            if (visibleCount === 0) {
                const notice = document.createElement('div');
                notice.className = 'empty-feed-placeholder filter-empty-notice font-monospace text-center py-4';
                notice.innerHTML = `
                    <i class="bi bi-funnel placeholder-icon fs-3"></i>
                    <div class="placeholder-text fs-6">// в категории «${escapeHtml(activeFilter)}» пока нет записей</div>
                `;
                container.appendChild(notice);
            }
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
