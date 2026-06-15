// Form logic for the Licenses screen (frmLicenses.html).

function limpiarFormularioLicencia() {
    // Clear everything except the serial the user is typing.
    document.getElementById('select-company').value = '';
    document.getElementById('input-type').value = '';
    document.getElementById('input-origin').value = '';
    document.getElementById('input-date').value = '';
    document.getElementById('input-value').value = '0';
    document.getElementById('input-obs').value = '';
    document.getElementById('input-bill').value = '';
    document.getElementById('input-person').value = 'Unassigned';
    document.getElementById('textarea-notes').value = '';
    document.querySelectorAll('.license-row').forEach(r => r.classList.remove('table-primary'));
}

function fillLicense(d) {
    document.getElementById('input-serial').value = d.serial || '';
    document.getElementById('select-company').value = d.company_id || '';
    document.getElementById('input-type').value = d.type || '';
    document.getElementById('input-origin').value = d.origin || '';
    document.getElementById('input-date').value = d.date || '';
    document.getElementById('input-value').value = d.value || '0';
    document.getElementById('input-obs').value = d.obs || '';
    document.getElementById('input-bill').value = d.bill || '';
    document.getElementById('input-person').value = d.person || 'Unassigned';
    document.getElementById('textarea-notes').value = d.notes || '';
}

function buscarLicenciaAjax() {
    const input = document.getElementById('input-serial');
    if (!input || !input.value.trim()) return;
    const serial = input.value.trim();

    fetch(`/api/get-license/?serial_number=${encodeURIComponent(serial)}`)
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;
            if (data.exists) {
                fillLicense(data.data);
            } else {
                limpiarFormularioLicencia();
                document.getElementById('input-serial').value = serial;
                Swal.fire({
                    title: 'OE Inventory',
                    text: 'License not found. Fill the fields and press Save to create it.',
                    icon: 'info', confirmButtonColor: '#FF48D8',
                });
            }
        })
        .catch(err => console.error('Error fetching license data:', err));
}

function fillFromRow(row) {
    document.querySelectorAll('.license-row').forEach(r => r.classList.remove('table-primary'));
    row.classList.add('table-primary');
    const d = row.dataset;
    fillLicense({
        serial: d.serial, company_id: d.company, type: d.type, origin: d.origin,
        date: d.date, value: d.value, obs: d.obs, bill: d.bill, person: d.person, notes: d.notes,
    });
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-licencias').addEventListener('click', function (e) {
        const row = e.target.closest('tr.license-row');
        if (row) fillFromRow(row);
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-licencias').DataTable({ pageLength: 50, ordering: true, autoWidth: false });
    }
});
