document.addEventListener('DOMContentLoaded', function() {

    // Toggle sidebar on mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.getElementById('sidebar').classList.toggle('active');
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Search form handling
function handleSearchFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const url = new URL(window.location.href);

    // Reset page parameter if exists
    url.searchParams.delete('page');

    // Update URL with form data
    new FormData(form).forEach((value, key) => {
        if (value) {
            url.searchParams.set(key, value);
        } else {
            url.searchParams.delete(key);
        }
    });

    window.location.href = url.toString();
}

// Attach search form handlers
document.querySelectorAll('.search-form').forEach(form => {
    form.addEventListener('submit', handleSearchFormSubmit);
});

// Clear search form
function clearSearchForm(formId) {
    document.getElementById(formId).reset();
    const url = new URL(window.location.href);
    url.search = '';
    window.location.href = url.toString();
}