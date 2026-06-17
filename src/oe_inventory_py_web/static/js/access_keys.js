// Form logic for the Access Keys screen (frmAccessKeys.html).

function currentCode() {
    return document.getElementById('input-code').value.trim();
}

function syncCode() {
    document.getElementById('input-code-hidden').value = currentCode();
}

function buscarLlaveAjax() {
    const code = currentCode();
    if (!code) return;
    fetch(`/api/get-key/?id=${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillKey(res.data);
            } else {
                limpiarLlave();
                document.getElementById('input-code').value = code;
                Swal.fire({ title: 'OE Inventory', text: 'Key not found. Fill the fields and Save to create it.', icon: 'info', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching key:', err));
}

function fillKey(d) {
    document.getElementById('input-code').value = d.id;
    document.getElementById('select-company').value = d.company_id || '';
    document.getElementById('input-type').value = d.type || '';
    document.getElementById('select-staff').value = d.staff_id || '';
    document.getElementById('input-date').value = d.date || '';
    document.getElementById('textarea-notes').value = d.notes || '';
    syncCode();
}

// Clear the editable fields when the user types a new Key ID, keeping the ID
// field itself (same behaviour as the other forms).
function limpiarCamposLlave() {
    document.getElementById('select-company').value = '';
    document.getElementById('input-type').value = '';
    document.getElementById('select-staff').value = '';
    document.getElementById('input-date').value = '';
    document.getElementById('textarea-notes').value = '';
    syncCode();
    document.querySelectorAll('.key-row').forEach(r => r.classList.remove('table-primary'));
}

function limpiarLlave() {
    document.getElementById('form-key').reset();
    document.getElementById('input-code').value = '';
    document.getElementById('textarea-notes').value = '';
    syncCode();
    document.querySelectorAll('.key-row').forEach(r => r.classList.remove('table-primary'));
}

function guardarLlave() {
    if (!document.getElementById('input-type').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'You have to indicate a valid Type.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!document.getElementById('input-date').value) {
        Swal.fire({ title: 'OE Inventory', text: 'A valid Insert Date is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    document.getElementById('form-key').submit();
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-llaves').addEventListener('click', function (e) {
        const row = e.target.closest('tr.key-row');
        if (!row) return;
        document.getElementById('input-code').value = row.dataset.id;
        buscarLlaveAjax();
    });
    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-llaves').DataTable({ pageLength: 25, ordering: true, autoWidth: false });
    }
    const pre = document.getElementById('preselected-key').value;
    if (pre) {
        document.getElementById('input-code').value = pre;
        buscarLlaveAjax();
    }
});
