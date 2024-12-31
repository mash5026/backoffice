document.addEventListener('DOMContentLoaded', function() {
    flatpickr(".jalali_date-time", {
        enableTime: true,         // Enable time selection
        dateFormat: "Y/m/d H:i:S",  // Jalali format with time
        time_24hr: true,         // Use 24-hour format for time
        locale: {
            firstDayOfWeek: 6,   // First day of week for Jalali calendar
            months: [
                "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
            ],
            weekdays: [
                "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه"
            ]
        },
        // Adjust these formats if necessary for your needs
    });
});

