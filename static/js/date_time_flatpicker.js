document.addEventListener("DOMContentLoaded", function () {
    flatpickr(".datetimepicker", {
        enableTime: true,                // 🕒 vaqt qo'shadi
        time_24hr: true,                 // 24 soat format (00–23)
        dateFormat: "Y-m-d H:i",         // Sana + soat:daqiqani saqlash formati
        altInput: true,                  // Foydalanuvchiga chiroyli ko‘rinishi uchun
        altFormat: "d-m-Y H:i",          // Ko‘rsatiladigan format
        allowInput: true,

        locale: {
            weekdays: {
                shorthand: ['Ya', 'Du', 'Se', 'Cho', 'Pa', 'Ju', 'Sha'],
                longhand: [
                    'Yakshanba', 'Dushanba', 'Seshanba',
                    'Chorshanba', 'Payshanba', 'Juma', 'Shanba'
                ],
            },
            months: {
                shorthand: [
                    'Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyun',
                    'Iyul', 'Avg', 'Sen', 'Okt', 'Noy', 'Dek'
                ],
                longhand: [
                    'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
                    'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr'
                ],
            },
            firstDayOfWeek: 1
        }
    });
});
