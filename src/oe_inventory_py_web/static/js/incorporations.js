// Form logic for the Incorporations screen (frmIncorporations.html).

function currentCode() {
    return document.getElementById('input-code').value.trim();
}

function syncCode() {
    document.getElementById('input-code-hidden').value = currentCode();
}

function setRadio(name, value) {
    const el = document.querySelector(`input[name="${name}"][value="${value || ''}"]`);
    if (el) el.checked = true;
}

function setCheck(id, on) {
    document.getElementById(id).checked = (on === 1 || on === true);
}

function buscarIncorporacionAjax() {
    const code = currentCode();
    if (!code) return;
    fetch(`/api/get-incorporation/?id=${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillIncorporation(res.data);
            } else {
                limpiarIncorporacion();
                document.getElementById('input-code').value = code;
                Swal.fire({ title: 'OE Inventory', text: 'Incorporation not found. Fill the fields and Save to create it.', icon: 'info', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching incorporation data:', err));
}

function fillIncorporation(d) {
    document.getElementById('input-code').value = d.id;
    document.getElementById('input-name').value = d.name || '';
    document.getElementById('input-email').value = d.email || '';
    document.getElementById('select-company').value = d.company_id || '';
    document.getElementById('input-department').value = d.department || '';
    document.getElementById('select-delegation').value = d.delegation_id || '';
    document.getElementById('input-date').value = d.date || '';
    document.getElementById('textarea-address').value = d.direccion || '';
    document.getElementById('textarea-notes').value = d.notes || '';
    setRadio('laptop', d.laptop);
    setRadio('headset', d.headset);
    setCheck('chk-phone', d.phone);
    setCheck('chk-screen', d.screen);
    setCheck('chk-mouse', d.mouse);
    setCheck('chk-keyboard', d.keyboard);
    document.getElementById('select-sweatshirt').value = d.sweatshirt_size || '';
    setCheck('chk-descartado', d.descartado);
    setCheck('chk-usbchub', d.usbchub);
    setCheck('chk-pdf', d.pdf);
    setCheck('chk-acad', d.acad);
    syncCode();
}

function limpiarIncorporacion() {
    document.getElementById('form-inc').reset();
    document.getElementById('input-code').value = '';
    document.getElementById('textarea-notes').value = '';
    syncCode();
}

function guardarIncorporacion() {
    const required = ['input-name', 'select-company', 'input-department', 'select-delegation', 'input-date'];
    if (required.some(id => !document.getElementById(id).value.trim())) {
        Swal.fire({ title: 'OE Inventory', text: 'Name, Company, Department, Delegation and Date are required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    document.getElementById('input-action').value = 'save';
    document.getElementById('form-inc').submit();
}

function enviarIncorporacion() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load an incorporation first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    Swal.fire({
        title: 'Send devices', input: 'text',
        inputLabel: 'Medium used to send the devices',
        showCancelButton: true, confirmButtonColor: '#FF48D8',
    }).then(res => {
        if (res.isConfirmed && res.value) {
            document.getElementById('input-agency').value = res.value;
            document.getElementById('input-action').value = 'send';
            syncCode();
            document.getElementById('form-inc').submit();
        }
    });
}

function recibirIncorporacion() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load an incorporation first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm('Do you really want to mark the receipt of the devices?')) return;
    document.getElementById('input-action').value = 'receive';
    syncCode();
    document.getElementById('form-inc').submit();
}

function preferenciasIncorporacion() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load an incorporation first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    const email = document.getElementById('input-email').value.trim();
    if (!email) {
        Swal.fire({ title: 'OE Inventory', text: 'This incorporation has no email address. Add one and Save first.', icon: 'warning', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm(`Send the editable preferences form to ${email}?`)) return;
    document.getElementById('input-action').value = 'preferences';
    syncCode();
    document.getElementById('form-inc').submit();
}

function completarIncorporacion() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a pending incorporation first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm('Do you really want to complete the incorporation? The person will be migrated to Staff.')) return;
    document.getElementById('input-action').value = 'complete';
    syncCode();
    document.getElementById('form-inc').submit();
}

function bindGridClicks(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    table.addEventListener('click', function (e) {
        const row = e.target.closest('tr.inc-row');
        if (!row) return;
        document.getElementById('input-code').value = row.dataset.id;
        buscarIncorporacionAjax();
    });
}

document.addEventListener('DOMContentLoaded', function () {
    bindGridClicks('tabla-pending');
    bindGridClicks('tabla-incorporated');

    if (window.jQuery && jQuery.fn.DataTable) {
        ['#tabla-pending', '#tabla-discarded', '#tabla-incorporated'].forEach(sel => {
            jQuery(sel).DataTable({ pageLength: 25, ordering: true, autoWidth: false });
        });
        // Fix column widths when a tab becomes visible.
        document.querySelectorAll('#incTabs button').forEach(btn => {
            btn.addEventListener('shown.bs.tab', () => {
                jQuery.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
            });
        });
    }

    const pre = document.getElementById('preselected-inc').value;
    if (pre) {
        document.getElementById('input-code').value = pre;
        buscarIncorporacionAjax();
    }
});
