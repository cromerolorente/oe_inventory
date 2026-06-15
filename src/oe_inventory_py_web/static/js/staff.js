// Form logic for the Staff screen (frmStaff.html).

let selectedItem = null;  // {id, serial} of the assigned-item row selected for release.
let staffItems = [];      // items currently assigned to the loaded staff member.

function fmtEU(n) {
    return Number(n || 0).toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function currentCode() {
    return document.getElementById('input-code').value.trim();
}

function syncCode() {
    const code = currentCode();
    document.getElementById('input-code-hidden').value = code;
    document.getElementById('input-code-doc').value = code;
}

// ---- Load a staff member via AJAX ----
function buscarStaffAjax() {
    const code = currentCode();
    if (!code) {
        Swal.fire({ title: 'OE Inventory', text: 'Type a staff ID or use Find.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    fetch(`/api/get-staff/?id=${encodeURIComponent(code)}`)
        .then(res => res.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillStaff(res.data);
            } else {
                limpiarStaff();
                Swal.fire({ title: 'OE Inventory', text: 'Staff not found or not available for your profile.', icon: 'warning', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching staff data:', err));
}

function fillStaff(data) {
    document.getElementById('input-code').value = data.id;
    document.getElementById('input-name').value = data.name || '';
    document.getElementById('input-department').value = data.department || '';
    document.getElementById('select-company').value = data.company_id || '';
    document.getElementById('select-delegation').value = data.delegation_id || '';
    document.getElementById('input-email').value = data.email || '';
    document.getElementById('input-fecha-inc').value = data.fecha_incorporacion || '';
    document.getElementById('input-fecha-baja').value = data.fecha_baja || '';
    document.getElementById('check-persona').checked = (data.persona_fisica === 1);
    document.getElementById('textarea-notes').value = data.notes || '';
    document.getElementById('lbl-devices').textContent = data.devices_count;
    document.getElementById('lbl-value').textContent = fmtEU(data.total_value);
    syncCode();
    staffItems = data.items || [];
    renderItems(staffItems);
    renderDocs(data.docs || [], data.id);
}

function renderItems(items) {
    selectedItem = null;
    const tbody = document.getElementById('body-staff-items');
    tbody.innerHTML = '';
    if (!items.length) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted py-3">No items assigned.</td></tr>';
        return;
    }
    items.forEach(it => {
        const tr = document.createElement('tr');
        tr.className = 'item-row';
        tr.style.cursor = 'pointer';
        tr.dataset.id = it.id;
        tr.dataset.serial = it.serial;
        tr.innerHTML = `<td>${it.id}</td><td>${it.serial}</td><td>${it.type}</td><td>${it.brand}</td>` +
            `<td>${it.model}</td><td>${it.origin}</td><td>${it.date}</td><td>${it.obs}</td>` +
            `<td class="text-end">${fmtEU(it.value)}</td>`;
        tbody.appendChild(tr);
    });
}

function renderDocs(docs, staffId) {
    const tbody = document.getElementById('body-docs');
    tbody.innerHTML = '';
    if (!docs.length) {
        tbody.innerHTML = '<tr><td class="text-center text-muted py-3">No documents.</td></tr>';
        return;
    }
    docs.forEach(name => {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.innerHTML = `<td><i class="bi bi-file-earmark-pdf text-danger"></i> ${name}</td>`;
        tr.addEventListener('click', () => {
            document.getElementById('doc-viewer').src = `/staff/doc/${staffId}/${encodeURIComponent(name)}/`;
        });
        tbody.appendChild(tr);
    });
}

function limpiarStaff() {
    selectedItem = null;
    document.getElementById('form-staff').reset();
    document.getElementById('input-code').value = '';
    document.getElementById('textarea-notes').value = '';
    document.getElementById('lbl-devices').textContent = '0';
    document.getElementById('lbl-value').textContent = '0,00';
    document.getElementById('body-staff-items').innerHTML =
        '<tr><td colspan="9" class="text-center text-muted py-3">No staff loaded.</td></tr>';
    document.getElementById('body-docs').innerHTML =
        '<tr><td class="text-center text-muted py-3">No staff loaded.</td></tr>';
    document.getElementById('doc-viewer').src = 'about:blank';
    syncCode();
}

// ---- Actions ----
function guardarStaff() {
    if (!document.getElementById('input-name').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'Name is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    document.getElementById('input-action').value = 'save';
    document.getElementById('form-staff').submit();
}

function terminarStaff() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a staff member first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    // Populate the modal with the items currently assigned to this person.
    const tbody = document.getElementById('body-terminate-items');
    tbody.innerHTML = '';
    if (!staffItems.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-2">No items assigned.</td></tr>';
    } else {
        staffItems.forEach(it => {
            const tr = document.createElement('tr');
            tr.innerHTML =
                `<td class="text-center"><input type="checkbox" class="form-check-input return-chk" value="${it.id}"></td>` +
                `<td>${it.id}</td><td>${it.serial || ''}</td><td>${it.type || ''}</td>` +
                `<td>${it.brand || ''}</td><td>${it.model || ''}</td>`;
            tbody.appendChild(tr);
        });
    }
    document.getElementById('chk-return-all').checked = false;
    new bootstrap.Modal(document.getElementById('terminateModal')).show();
}

function toggleAllReturns(master) {
    document.querySelectorAll('#body-terminate-items .return-chk').forEach(c => { c.checked = master.checked; });
}

function confirmarTerminate() {
    if (!confirm('Terminate this contract? The checked items will be returned to stock and a Terminate document will be generated.')) return;
    const ids = Array.from(document.querySelectorAll('#body-terminate-items .return-chk:checked')).map(c => c.value);
    document.getElementById('input-returned-items').value = ids.join(',');
    syncCode();
    document.getElementById('input-action').value = 'terminate';
    document.getElementById('form-staff').submit();
}

function liberarItem() {
    if (!selectedItem) {
        Swal.fire({ title: 'OE Inventory', text: 'Select an assigned item from the table first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    const name = document.getElementById('input-name').value;
    if (!confirm(`Do you want to unassign ${selectedItem.serial || selectedItem.id} from ${name}?`)) return;
    document.getElementById('input-item-id').value = selectedItem.id;
    document.getElementById('input-item-serial').value = selectedItem.serial;
    syncCode();
    document.getElementById('input-action').value = 'release';
    document.getElementById('form-staff').submit();
}

function generarDocStaff() {
    const code = currentCode();
    if (!code) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a staff member first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    window.open(`/staff/report/?staff=${encodeURIComponent(code)}`, '_blank');
}

function enviarMailStaff() {
    const code = currentCode();
    if (!code) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a staff member first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm('Send the inventory report by email to the People department?')) return;
    document.getElementById('input-email-staff').value = code;
    document.getElementById('form-email').submit();
}

function excelStaff() {
    const code = currentCode();
    if (!code) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a staff member first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    window.location = `/staff/?export=excel&staff=${encodeURIComponent(code)}`;
}

// ---- Wiring ----
document.addEventListener('DOMContentLoaded', function () {
    // Select an assigned item (for Release).
    document.getElementById('tabla-items').addEventListener('click', function (e) {
        const row = e.target.closest('tr.item-row');
        if (!row) return;
        document.querySelectorAll('#body-staff-items tr').forEach(r => r.classList.remove('table-primary'));
        row.classList.add('table-primary');
        selectedItem = { id: row.dataset.id, serial: row.dataset.serial };
    });

    // Click a staff row in the List tab -> load it in General.
    document.getElementById('tabla-staff').addEventListener('click', function (e) {
        const row = e.target.closest('tr.staff-row');
        if (!row) return;
        document.getElementById('input-code').value = row.dataset.id;
        bootstrap.Tab.getOrCreateInstance(document.getElementById('tab-general-btn')).show();
        buscarStaffAjax();
    });

    // DataTable on the staff list.
    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-staff').DataTable({ pageLength: 50, ordering: true, autoWidth: false });
    }

    // Auto-load a preselected staff member (after a save/release/upload redirect).
    const preselected = document.getElementById('preselected-staff').value;
    if (preselected) {
        document.getElementById('input-code').value = preselected;
        buscarStaffAjax();
    }
});
