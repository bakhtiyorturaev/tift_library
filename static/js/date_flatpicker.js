document.addEventListener("DOMContentLoaded", function () {
    flatpickr(".datepicker", {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "d-m-Y",
        allowInput: true,

        locale: {
            firstDayOfWeek: 1,
            weekdays: {
                shorthand: ['Ya', 'Du', 'Se', 'Cho', 'Pa', 'Ju', 'Sha'],
                longhand: [
                    'Yakshanba', 'Dushanba', 'Seshanba',
                    'Chorshanba', 'Payshanba', 'Juma', 'Shanba'
                ]
            },
            months: {
                shorthand: [
                    'Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyun',
                    'Iyul', 'Avg', 'Sen', 'Okt', 'Noy', 'Dek'
                ],
                longhand: [
                    'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
                    'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr'
                ]
            }
        }
    });
});
