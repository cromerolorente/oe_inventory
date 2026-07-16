// Form logic for the Device Types maintenance screen (frmDevicesType.html).

function currentCode() {
    return document.getElementById('input-code-hidden').value.trim();
}

function fillType(id, name, used) {
    document.getElementById('input-code-hidden').value = id;
    document.getElementById('input-type').value = name || '';
    const inUse = (used === '1' || used === 1 || used === true);
    document.getElementById('input-type').readOnly = inUse;
    document.getElementById('btn-delete').style.opacity = inUse ? '0.4' : '1';
    document.getElementById('used-note').style.display = inUse ? 'block' : 'none';
}

function limpiarType() {
    document.getElementById('form-type').reset();
    document.getElementById('input-code-hidden').value = '';
    document.getElementById('input-type').readOnly = false;
    document.getElementById('btn-delete').style.opacity = '1';
    document.getElementById('used-note').style.display = 'none';
    document.querySelectorAll('.type-row').forEach(r => r.classList.remove('table-primary'));
}

function guardarType() {
    if (!document.getElementById('input-type').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'The description cannot be empty.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    document.getElementById('input-action').value = 'save';
    document.getElementById('form-type').submit();
}

function eliminarType() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Select a type from the list first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm('Do you want to delete this device type?')) return;
    document.getElementById('input-action').value = 'delete';
    document.getElementById('form-type').submit();
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-types').addEventListener('click', function (e) {
        const row = e.target.closest('tr.type-row');
        if (!row) return;
        document.querySelectorAll('.type-row').forEach(r => r.classList.remove('table-primary'));
        row.classList.add('table-primary');
        fillType(row.dataset.id, row.dataset.type, row.dataset.used);
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-types').DataTable({ pageLength: 25, ordering: true, autoWidth: false });
    }
});
