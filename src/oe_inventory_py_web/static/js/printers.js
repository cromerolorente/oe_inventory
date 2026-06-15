// Form logic for the Printers screen (frmPrinters.html).

function limpiarImpresora(clearSerial) {
    if (clearSerial) document.getElementById('input-serial').value = '';
    document.getElementById('input-description').value = '';
    document.getElementById('input-provider').value = '';
    document.getElementById('select-delegation').value = '';
    document.getElementById('input-mps').value = '';
    document.getElementById('input-ip').value = '';
    document.getElementById('input-start-date').value = '';
    document.getElementById('input-down-date').value = '';
    document.getElementById('input-fee').value = '';
    document.getElementById('input-user').value = '';
    document.getElementById('input-password').value = '';
    document.getElementById('textarea-notes').value = '';
    document.querySelectorAll('.printer-row').forEach(r => r.classList.remove('table-primary'));
}

function fillPrinter(d) {
    document.getElementById('input-serial').value = d.serial || '';
    document.getElementById('input-description').value = d.description || '';
    document.getElementById('input-provider').value = d.provider || '';
    document.getElementById('select-delegation').value = d.delegation_id || '';
    document.getElementById('input-mps').value = d.mps || '';
    document.getElementById('input-ip').value = d.ip || '';
    document.getElementById('input-start-date').value = d.start_date || '';
    document.getElementById('input-down-date').value = d.down_date || '';
    document.getElementById('input-fee').value = d.fee || '';
    document.getElementById('input-user').value = d.user || '';
    document.getElementById('input-password').value = d.password || '';
    document.getElementById('textarea-notes').value = d.notes || '';
}

function buscarImpresoraAjax() {
    const input = document.getElementById('input-serial');
    if (!input || !input.value.trim()) return;
    const serial = input.value.trim();

    fetch(`/api/get-printer/?serial_number=${encodeURIComponent(serial)}`)
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;
            if (data.exists) {
                fillPrinter(data.data);
            } else {
                limpiarImpresora(false);
                document.getElementById('input-serial').value = serial;
                Swal.fire({
                    title: 'OE Inventory',
                    text: 'Printer not found. Fill the fields and press Save to create it.',
                    icon: 'info', confirmButtonColor: '#FF48D8',
                });
            }
        })
        .catch(err => console.error('Error fetching printer data:', err));
}

function guardarImpresora() {
    if (!document.getElementById('input-description').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'The Description field is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!document.getElementById('input-start-date').value) {
        Swal.fire({ title: 'OE Inventory', text: 'A valid Start Date is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    document.getElementById('form-printer').submit();
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-impresoras').addEventListener('click', function (e) {
        const row = e.target.closest('tr.printer-row');
        if (!row) return;
        document.getElementById('input-serial').value = row.dataset.serial;
        bootstrap.Tab.getOrCreateInstance(document.getElementById('tab-general-btn')).show();
        buscarImpresoraAjax();
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-impresoras').DataTable({ pageLength: 50, ordering: true, autoWidth: false });
    }

    const pre = document.getElementById('preselected-sn').value;
    if (pre) {
        document.getElementById('input-serial').value = pre;
        buscarImpresoraAjax();
    }
});
