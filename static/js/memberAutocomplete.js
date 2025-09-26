// static/js/memberAutocomplete.js
function initializeMemberAutocomplete() {
    const fullNameInput = document.getElementById('full-name-input');
    if (!fullNameInput) return; // Agar element topilmasa funktsiyani to'xtatish

    const studentIdField = document.getElementById('student-id-field'); // Bu yerda siz template'dagi to'g'ri ID ni ishlatishingiz kerak
    const phoneField = document.getElementById('phone-field'); // Bu yerda siz template'dagi to'g'ri ID ni ishlatishingiz kerak
    const datalist = document.getElementById('member-list');
    let searchTimeout;

    // Datalist variantlarini yashirish/boshlash
    function filterOptions() {
        const searchTerm = fullNameInput.value.toLowerCase();
        const options = datalist.querySelectorAll('option');
        let hasMatches = false;

        options.forEach(option => {
            if (searchTerm.length < 2) {
                option.style.display = 'none';
                return;
            }

            if (option.value.toLowerCase().includes(searchTerm)) {
                option.style.display = 'block';
                hasMatches = true;
            } else {
                option.style.display = 'none';
            }
        });

        // Agar moslik topilsa, datalistni ko'rsatish
        if (hasMatches && searchTerm.length >= 2) {
            datalist.style.display = 'block';
        } else {
            datalist.style.display = 'none';
        }
    }

    // Input hodisasi
    fullNameInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);

        // 300ms kutish (debounce)
        searchTimeout = setTimeout(() => {
            filterOptions();

            // Tanlangan variant bo'yicha maydonlarni to'ldirish
            const selectedOption = document.querySelector(`#member-list option[value="${this.value}"]`);
            if (selectedOption && selectedOption.style.display === 'block') {
                if (studentIdField) studentIdField.value = selectedOption.getAttribute('data-student-id');
                if (phoneField) phoneField.value = selectedOption.getAttribute('data-phone');
            }
        }, 300);
    });

    // Inputdan focus yo'qolganda datalistni yashirish
    fullNameInput.addEventListener('blur', function() {
        setTimeout(() => {
            if (datalist) datalist.style.display = 'none';
        }, 200);
    });

    // Talaba ID bo'yicha avtomatik to'ldirish
    if (studentIdField) {
        studentIdField.addEventListener('change', function() {
            if (this.value) {
                fetch(`/api/check-member/?student_id=${this.value}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.exists) {
                            if (fullNameInput) fullNameInput.value = data.full_name;
                            if (phoneField) phoneField.value = data.phone;
                        }
                    });
            }
        });
    }
}

// DOM yuklanganidan so'ng funktsiyani chaqirish
document.addEventListener('DOMContentLoaded', initializeMemberAutocomplete);