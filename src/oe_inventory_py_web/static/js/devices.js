// Form logic for the Devices screen (frmDevices.html).

document.addEventListener('DOMContentLoaded', function () {

    const tableEl = document.getElementById('tabla-dispositivos');
    if (!tableEl) return;

    const ajaxUrl = tableEl.dataset.ajaxUrl || '';
    const staffFilter = tableEl.dataset.staffFilter || '';

    // 1. DataTables in SERVER-SIDE mode: the database does the search, ordering
    //    and pagination, so the screen only ever loads one page (~50 rows) at a
    //    time instead of the whole inventory.
    const table = $('#tabla-dispositivos').DataTable({
        serverSide: true,
        processing: true,
        pageLength: 50,
        order: [[0, 'asc']],
        autoWidth: false,
        ajax: {
            url: ajaxUrl,
            data: function (d) {
                // Carry the optional "only this staff's devices" filter.
                d.id_staff = staffFilter;
            }
        },
        columns: [
            { data: 'serial' },
            { data: 'type' },
            { data: 'brand' },
            { data: 'model' },
            { data: 'screen' },
            { data: 'hd' },
            { data: 'memory' },
            { data: 'imei' },
            {
                data: 'mobile', className: 'text-center',
                render: function (v) { return v ? '☑' : '☐'; }
            },
            { data: 'pin' },
            { data: 'origin' },
            { data: 'date' },
            { data: 'bill' },
            { data: 'staff' },
            {
                data: 'value', className: 'text-end',
                render: function (v) { return (v != null ? v : 0) + ' €'; }
            }
        ]
    });

    // Table is ready: restore the normal mouse pointer (set to 'wait' while loading).
    document.documentElement.style.cursor = '';

    // 2. Click a row -> load that device into the form. We reuse the existing
    //    /api/get-device/ endpoint (via buscarDispositivoAjax) so the rows
    //    themselves stay lightweight (no per-row data-* attributes needed).
    $('#tabla-dispositivos tbody').on('click', 'tr', function () {
        const rowData = table.row(this).data();
        if (!rowData) return;

        $('#tabla-dispositivos tbody tr').removeClass('table-primary');
        $(this).addClass('table-primary');

        const inputSerial = document.getElementById('input-serial');
        if (inputSerial) inputSerial.value = rowData.serial || '';
        buscarDispositivoAjax();
    });

});

function limpiarFormularioDispositivo() {
    console.log("Clearing the form because the SN changed...");

    // Sync the hidden key field.
    const inputClave = document.getElementById('input-clave');
    if (inputClave) inputClave.value = '';

    // Basic fields (EXCEPT input-serial itself, so we don't erase what the user is typing).
    if (document.getElementById('input-type')) document.getElementById('input-type').value = '';
    if (document.getElementById('input-brand')) document.getElementById('input-brand').value = '';
    if (document.getElementById('input-model')) document.getElementById('input-model').value = '';
    if (document.getElementById('select-company')) document.getElementById('select-company').value = '';
    if (document.getElementById('input-staff')) document.getElementById('input-staff').value = 'Unassigned';

    // Hardware
    if (document.getElementById('input-screen')) document.getElementById('input-screen').value = '';
    if (document.getElementById('input-hd')) document.getElementById('input-hd').value = '';
    if (document.getElementById('input-memory')) document.getElementById('input-memory').value = '';

    // Mobile network.
    if (document.getElementById('input-imei')) document.getElementById('input-imei').value = '';
    const checkMobile = document.getElementById('check-mobile');
    if (checkMobile) checkMobile.checked = false;
    if (document.getElementById('input-pin')) document.getElementById('input-pin').value = '';

    // Bills and dates.
    if (document.getElementById('input-origin')) document.getElementById('input-origin').value = '';
    if (document.getElementById('input-date')) document.getElementById('input-date').value = '';
    if (document.getElementById('input-bill')) document.getElementById('input-bill').value = '';
    if (document.getElementById('input-value')) document.getElementById('input-value').value = '0';

    // History / notes.
    const textareaNotes = document.querySelector('textarea[name="notes"]');
    if (textareaNotes) textareaNotes.value = '';

    // Remove any row highlighted in blue in the table.
    document.querySelectorAll('.device-row').forEach(r => r.classList.remove('table-primary'));
}


function buscarDispositivoAjax() {
    const serialInput = document.getElementById('input-serial');
    if (!serialInput || !serialInput.value.trim()) return;

    const serial = serialInput.value.trim();

    // Call the Django API passing the SN.
    fetch(`/api/get-device/?serial_number=${encodeURIComponent(serial)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Device found via AJAX:", data);

                // Sync the form's hidden key field.
                const inputClave = document.getElementById('input-clave');
                if (inputClave) inputClave.value = data.serial;

                // Fill the form exactly as on row click.
                if (document.getElementById('input-type')) document.getElementById('input-type').value = data.type;
                if (document.getElementById('input-brand')) document.getElementById('input-brand').value = data.brand;
                if (document.getElementById('input-model')) document.getElementById('input-model').value = data.model;
                if (document.getElementById('select-company')) document.getElementById('select-company').value = data.company;
                if (document.getElementById('input-staff')) document.getElementById('input-staff').value = data.staff;

                if (document.getElementById('input-screen')) document.getElementById('input-screen').value = data.screen;
                if (document.getElementById('input-hd')) document.getElementById('input-hd').value = data.hd;
                if (document.getElementById('input-memory')) document.getElementById('input-memory').value = data.memory;

                if (document.getElementById('input-imei')) document.getElementById('input-imei').value = data.imei;
                const checkMobile = document.getElementById('check-mobile');
                if (checkMobile) checkMobile.checked = (data.mobile === 'true');
                if (document.getElementById('input-pin')) document.getElementById('input-pin').value = data.pin;

                if (document.getElementById('input-origin')) document.getElementById('input-origin').value = data.origin;
                if (document.getElementById('input-date')) document.getElementById('input-date').value = data.date;
                if (document.getElementById('input-bill')) document.getElementById('input-bill').value = data.bill;
                if (document.getElementById('input-value')) document.getElementById('input-value').value = data.value;

                const textareaNotes = document.querySelector('textarea[name="notes"]');
                if (textareaNotes) textareaNotes.value = data.notes;

                // Optional: deselect any highlighted row to avoid confusion.
                document.querySelectorAll('.device-row').forEach(r => r.classList.remove('table-primary'));

            } else {
                // Not found: behave like Phones/Licenses — keep the serial the
                // user typed, clear the rest and invite them to create it.
                limpiarFormularioDispositivo();
                const inputSerial2 = document.getElementById('input-serial');
                if (inputSerial2) inputSerial2.value = serial;
                Swal.fire({
                    title: 'OE Inventory',
                    text: 'Device not found. Fill the fields and press Save to create it.',
                    icon: 'info',
                    confirmButtonColor: '#FF48D8',
                });
            }
        })
        .catch(error => {
            console.error("AJAX request error:", error);
            Swal.fire({ icon: 'error', title: 'Error', text: 'An error occurred while searching for the device.' });
        });
}
