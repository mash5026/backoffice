document.addEventListener('DOMContentLoaded', function() {
    function updateChildLocations(parentId) {
        var childLocationSelect = document.getElementById('id_location');
        childLocationSelect.innerHTML = '<option value="">Select Child Location</option>'; // Clear previous options

        if (parentId) {
            fetch(`/admin/get-child-locations/?parent_id=${parentId}`)
                .then(response => response.json())
                .then(data => {
                    data.locations.forEach(location => {
                        var option = document.createElement('option');
                        option.value = location.id;
                        option.text = location.name;
                        childLocationSelect.add(option);
                    });
                })
                .catch(error => console.error('Error fetching child locations:', error));
        }
    }

    var parentLocationSelect = document.getElementById('id_location');
    if (parentLocationSelect) {
        parentLocationSelect.addEventListener('change', function() {
            updateChildLocations(this.value);
        });
    }
});