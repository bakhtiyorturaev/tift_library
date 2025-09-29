document.addEventListener('DOMContentLoaded', function() {
    // Sana va vaqt tanlovi
    flatpickr('.datetimepicker', {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        allowInput: true,
        minDate: "today",
        defaultDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
    });

    // Talaba tanlanganda ID va telefonni to'ldirish
    const fullNameInput = document.querySelector('#{{ member_form.full_name.id_for_label }}');
    const studentIdField = document.getElementById('student-id-field');
    const phoneField = document.getElementById('phone-field');

    fullNameInput.addEventListener('input', function() {
        const selectedOption = document.querySelector(`#member-list option[value="${this.value}"]`);
        if (selectedOption) {
            studentIdField.value = selectedOption.getAttribute('data-student-id');
            phoneField.value = selectedOption.getAttribute('data-phone');
        }
    });

    // Talaba ID bo'yicha avtomatik to'ldirish
    studentIdField.addEventListener('change', function() {
        if (this.value) {
            fetch(`/api/check-member/?student_id=${this.value}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        fullNameInput.value = data.full_name;
                        phoneField.value = data.phone;
                    }
                });
        }
    });
});