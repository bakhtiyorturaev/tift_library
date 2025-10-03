document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("td.no-click").forEach(function (cell) {
        cell.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    });
});