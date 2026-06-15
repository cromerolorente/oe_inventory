// Form logic for the Under Repair screen (frmUnderRepair.html).

let selectedRepairId = null;

function recibirReparacion() {
    if (!selectedRepairId) {
        Swal.fire({ title: 'OE Inventory', text: 'Select a pending device first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    Swal.fire({
        title: 'Receive from maintenance',
        input: 'text',
        inputLabel: 'Cost of the repair',
        showCancelButton: true,
        confirmButtonColor: '#FF48D8',
    }).then(res => {
        if (res.isConfirmed && res.value !== '') {
            document.getElementById('receive-id').value = selectedRepairId;
            document.getElementById('receive-value').value = res.value;
            document.getElementById('form-receive').submit();
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-pending').addEventListener('click', function (e) {
        const row = e.target.closest('tr.repair-row');
        if (!row) return;
        document.querySelectorAll('#tabla-pending tr').forEach(r => r.classList.remove('table-primary'));
        row.classList.add('table-primary');
        selectedRepairId = row.dataset.id;
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        ['#tabla-pending', '#tabla-repaired'].forEach(sel => {
            jQuery(sel).DataTable({ pageLength: 25, ordering: true, autoWidth: false });
        });
        document.querySelectorAll('#repairTabs button').forEach(btn => {
            btn.addEventListener('shown.bs.tab', () => {
                jQuery.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
            });
        });
    }
});
