document.addEventListener('DOMContentLoaded', function() {
    // Initialize date pickers
    flatpickr('.datepicker', {
        dateFormat: "Y-m-d",
        allowInput: true
    });

    // Handle search form submission
    document.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault();
        const form = e.target;
        const url = new URL(window.location.href);

        // Reset page parameter
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
    });
});