django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
    $row.find('.select2').select2(); // دوباره‌سازی Select2 برای ردیف جدید
});