from django import forms
from django.utils.safestring import mark_safe
from django.forms.widgets import DateTimeInput
import jdatetime

class CustomJalaliAdminDateTimeWidget(DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['class'] = self.attrs.get('class', '') + ' vDateTimeField'
        # Custom time options
        self.time_choices = [
            ('now', 'Now'),
            ('08:00', '8am'),
            ('09:00', '9am'),
            ('12:00', 'Noon'),
            ('14:00', '2pm'),
        ]

    def render(self, name, value, attrs=None, renderer=None):
        # Convert value to Jalali if it's not None
        if value:
            # Ensure the value is a datetime object
            if isinstance(value, jdatetime.datetime):
                value = value.strftime('%Y-%m-%dT%H:%M')  # Format Jalali datetime to ISO format

        # Render the base HTML for the widget
        html = super().render(name, value, attrs, renderer)

        # Add custom JavaScript to change time options
        js = '''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const input = document.querySelector('input[name="{{ name }}"]');
            if (input) {
                input.addEventListener('focus', function() {
                    var timeOptions = ''' + str(self.time_choices) + ''';
                    var timeMenu = input.closest('.form-row').querySelector('.vDateTimeField .ui-timepicker');
                    if (timeMenu) {
                        timeMenu.innerHTML = '';
                        timeOptions.forEach(function(option) {
                            var optionElem = document.createElement('option');
                            optionElem.value = option[0];
                            optionElem.innerText = option[1];
                            timeMenu.appendChild(optionElem);
                        });
                    }
                });
            }
        });
        </script>
        '''
        # Return the rendered widget with injected JavaScript
        return mark_safe(html + js)

