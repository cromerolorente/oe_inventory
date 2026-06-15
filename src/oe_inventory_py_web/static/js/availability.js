// Logic for the Availability screen (frmAvailability.html).

document.addEventListener('DOMContentLoaded', function () {
    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-availability').DataTable({ pageLength: 50, ordering: true, autoWidth: false });
    }
});
