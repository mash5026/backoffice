document.addEventListener('DOMContentLoaded', function () {
    const roleSelects = document.querySelectorAll('select[name$=role]');  // Select role dropdowns

    roleSelects.forEach(roleSelect => {
        roleSelect.addEventListener('change', function() {
            const selectedRole = this.value; // Get the selected value

            // Find all role dropdowns in the Officestaff inline
            const officestaffRoles = document.querySelectorAll('tr[data-inline="officestaff"] select[name$=role]');
            officestaffRoles.forEach(officestaffRole => {
                officestaffRole.value = selectedRole; // Set them to the selected role
            });
        });
    });
});