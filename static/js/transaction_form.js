document.addEventListener('DOMContentLoaded', function () {
    console.log('DOMContentLoaded');

    const fullNameInput = document.getElementById('full-name-input');
    const studentIdField = document.getElementById('student-id-field');
    const phoneField = document.getElementById('phone-field');
    const datalist = document.getElementById('member-list');

    if (!fullNameInput || !studentIdField || !phoneField || !datalist) return;

    // ✅ Ism Familiya bo‘yicha tanlansa
    fullNameInput.addEventListener('change', function () {
        const val = this.value.trim();
        const option = Array.from(datalist.options).find(opt => opt.value === val);

        if (option) {
            studentIdField.value = option.dataset.studentId || "";
            phoneField.value = option.dataset.phone || ""; // faqat 9 raqam
        }
    });

    // ✅ Talaba ID bo‘yicha tanlansa
    studentIdField.addEventListener('change', function () {
        const val = this.value.trim();
        const option = Array.from(datalist.options).find(opt => opt.dataset.studentId === val);

        if (option) {
            fullNameInput.value = option.value || "";
            phoneField.value = option.dataset.phone || "";
        }
    });

    // ✅ Telefon raqami bo‘yicha tanlansa (faqat 9 raqam)
    phoneField.addEventListener('change', function () {
        const val = this.value.trim();
        const option = Array.from(datalist.options).find(opt => opt.dataset.phone === val);

        if (option) {
            fullNameInput.value = option.value || "";
            studentIdField.value = option.dataset.studentId || "";
        }
    });
});
