document.addEventListener('DOMContentLoaded', function() {
    const nationalidField = document.getElementById('id_NATIONALID');
    const errorMessage = document.createElement('div');
    errorMessage.style.color = 'red';
    nationalidField.parentNode.appendChild(errorMessage);

    nationalidField.addEventListener('input', function() {
        const nationalid = nationalidField.value;
        errorMessage.textContent = '';  // Clear previous error message

        if (nationalid.length >= 10) {  // You can adjust this to your requirement
            fetch(`/check-nationalid/${nationalid}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        errorMessage.textContent = `${nationalid} : کدملی وارد شده در دیتابیس موجود است`;
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});