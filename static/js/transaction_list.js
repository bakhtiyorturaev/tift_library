document.addEventListener('DOMContentLoaded', function() {
    // Faqat qidiruv formasini ushlash
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const form = e.target;
            const url = new URL(window.location.href);

            // Reset page parameter
            url.searchParams.delete('page');

            // Formadagi qiymatlarni URL query string ga qo‘shish
            new FormData(form).forEach((value, key) => {
                if (value) {
                    url.searchParams.set(key, value);
                } else {
                    url.searchParams.delete(key);
                }
            });

            // Sahifani yangilash
            window.location.href = url.toString();
        });
    }
});
