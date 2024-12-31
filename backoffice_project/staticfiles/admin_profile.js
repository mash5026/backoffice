(function() {
    // Initialize the script
    function initScript($) {
        $(document).ready(function() {
            let isUpdating = false;

            function syncRole(event) {
                if (isUpdating) return;  // Prevent recursive updates

                isUpdating = true;
                const selectElement = $(event.target);
                const selectedRoleId = selectElement.val();
                console.log(`Selected Role ID: ${selectedRoleId}`);

                // Iterate over each formset container
                $('.js-inline-admin-formset').each(function() {
                    const formsetContainer = $(this);
                    console.log('Formset Container:', formsetContainer);

                    // Find all role selects within the officestaff set group
                    const officeInlines = formsetContainer.find('select[id^="id_officestaff_set-"][id$="-role"]');
                    console.log('Office Inlines:', officeInlines);

                    if (officeInlines.length) {
                        // Update roles in existing form rows
                        officeInlines.each(function() {
                            const $this = $(this);
                            if (!$this.val()) { // Check if the role is empty
                                $this.val(selectedRoleId).trigger('change');
                                console.log('Updated role in existing row:', this);
                            }
                        });

                        // Add new role to new form rows if they are empty
                        const emptyRoleSelects = formsetContainer.find('tr.empty-form select[id$="-role"]');
                        emptyRoleSelects.each(function() {
                            const $this = $(this);
                            if (!$this.val()) { // Check if the role is empty
                                $this.val(selectedRoleId).trigger('change');
                                console.log('Updated role in new row:', this);
                            }
                        });
                    } else {
                        console.warn('No office inlines found within:', formsetContainer);
                    }
                });

                isUpdating = false;
            }

            // Attach event listener to profilerole_set select elements
            $('select[id^="id_profilerole_set-"][id$="-role"]').on('change', syncRole);
        });
    }

    // Load jQuery and initialize script if not already loaded
    function loadJQuery(callback) {
        var script = document.createElement('script');
        script.src = "https://code.jquery.com/jquery-3.6.0.min.js";
        script.onload = function() {
            if (typeof jQuery === 'undefined') {
                console.error('jQuery failed to load.');
                return;
            }
            var $ = jQuery.noConflict(true);
            callback($);
        };
        document.head.appendChild(script);
    }

    if (typeof django === 'undefined' || typeof django.jQuery === 'undefined') {
        loadJQuery(initScript);
    } else {
        (function($) {  
            initScript($);
        })(django.jQuery);
    }
})();