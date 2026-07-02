// Form logic for the Mobile Phones screen (frmPhones.html).

function toggleUnderRepair(on) {
    document.getElementById('alert-under-repair').style.display = on ? 'flex' : 'none';
}

function limpiarFormularioTelefono() {
    // Clear everything except the serial the user is typing.
    document.getElementById('select-company').value = '';
    document.getElementById('input-brand').value = '';
    document.getElementById('input-model').value = '';
    document.getElementById('input-origin').value = '';
    document.getElementById('input-date').value = '';
    document.getElementById('input-value').value = '0';
    document.getElementById('input-imei').value = '';
    document.getElementById('input-obs').value = '';
    document.getElementById('input-bill').value = '';
    document.getElementById('input-number').value = '';
    document.getElementById('input-person').value = 'Unassigned';
    document.getElementById('textarea-notes').value = '';
    toggleUnderRepair(false);
    document.querySelectorAll('.phone-row').forEach(r => r.classList.remove('table-primary'));
}

function fillPhone(d) {
    document.getElementById('input-serial').value = d.serial || '';
    document.getElementById('select-company').value = d.company_id || '';
    document.getElementById('input-brand').value = d.brand || '';
    document.getElementById('input-model').value = d.model || '';
    document.getElementById('input-origin').value = d.origin || '';
    document.getElementById('input-date').value = d.date || '';
    document.getElementById('input-value').value = d.value || '0';
    document.getElementById('input-imei').value = d.imei || '';
    document.getElementById('input-obs').value = d.obs || '';
    document.getElementById('input-bill').value = d.bill || '';
    document.getElementById('input-number').value = d.number || '';
    document.getElementById('input-person').value = d.person || 'Unassigned';
    document.getElementById('textarea-notes').value = d.notes || '';
    toggleUnderRepair(!!d.under_repair);
}

function buscarTelefonoAjax() {
    const input = document.getElementById('input-serial');
    if (!input || !input.value.trim()) return;
    const serial = input.value.trim();

    fetch(`/api/get-phone/?serial_number=${encodeURIComponent(serial)}`)
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;
            if (data.exists) {
                fillPhone(data.data);
            } else {
                limpiarFormularioTelefono();
                document.getElementById('input-serial').value = serial;
                Swal.fire({
                    title: 'OE Inventory',
                    text: 'Phone not found. Fill the fields and press Save to create it.',
                    icon: 'info', confirmButtonColor: '#FF48D8',
                });
            }
        })
        .catch(err => console.error('Error fetching phone data:', err));
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-telefonos').addEventListener('click', function (e) {
        const row = e.target.closest('tr.phone-row');
        if (!row) return;
        document.querySelectorAll('.phone-row').forEach(r => r.classList.remove('table-primary'));
        row.classList.add('table-primary');
        document.getElementById('input-serial').value = row.dataset.serial;
        buscarTelefonoAjax();
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-telefonos').DataTable({ pageLength: 20, ordering: true, autoWidth: false });
    }

    const pre = document.getElementById('preselected-sn').value;
    if (pre) {
        document.getElementById('input-serial').value = pre;
        buscarTelefonoAjax();
    }
});
