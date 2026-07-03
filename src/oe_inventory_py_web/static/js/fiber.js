// Form logic for the Fiber Lines screen (frmFiberLines.html).

function currentCode() {
    return document.getElementById('input-code').value.trim();
}

function syncCode() {
    const code = currentCode();
    document.getElementById('input-code-hidden').value = code;
    document.getElementById('input-code-incidence').value = code;
}

function buscarFibraAjax() {
    const code = currentCode();
    if (!code) {
        Swal.fire({ title: 'OE Inventory', text: 'Type a fiber ID or use Find.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    fetch(`/api/get-fiber/?id=${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillFiber(res.data);
            } else {
                limpiarFibra();
                Swal.fire({ title: 'OE Inventory', text: 'Fiber line not found.', icon: 'warning', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching fiber data:', err));
}

function fillFiber(d) {
    document.getElementById('input-code').value = d.id;
    document.getElementById('input-description').value = d.description || '';
    document.getElementById('input-provider').value = d.provider || '';
    document.getElementById('select-delegation').value = d.delegation_id || '';
    document.getElementById('input-order').value = d.order || '';
    document.getElementById('input-service-code').value = d.service_code || '';
    document.getElementById('input-access').value = d.access || '';
    document.getElementById('input-router').value = d.router || '';
    document.getElementById('input-addressing').value = d.addressing || '';
    document.getElementById('input-wifi1').value = d.wifi1 || '';
    document.getElementById('input-wifi2').value = d.wifi2 || '';
    document.getElementById('check-active').checked = (d.active === 1);
    document.getElementById('input-start-date').value = d.start_date || '';
    document.getElementById('input-down-date').value = d.down_date || '';
    document.getElementById('input-ip').value = d.ip_fixed || '';
    document.getElementById('input-fee').value = (d.fee != null ? d.fee : 0);
    document.getElementById('textarea-notes').value = d.notes || '';
    syncCode();
    renderIncidences(d.incidences || []);
    fillWorkingCodes(d.working_codes || []);
}

function renderIncidences(list) {
    const tbody = document.getElementById('body-incidences');
    tbody.innerHTML = '';
    if (!list.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-3">No incidences.</td></tr>';
        return;
    }
    list.forEach(it => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${it.id_incidence}</td><td>${it.open_date || ''}</td>` +
            `<td>${it.open_description || ''}</td><td>${it.close_date || ''}</td>` +
            `<td>${it.close_description || ''}</td><td>${it.working_code || ''}</td>`;
        tbody.appendChild(tr);
    });
}

function fillWorkingCodes(codes) {
    const dl = document.getElementById('working-code-options');
    dl.innerHTML = '';
    codes.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        dl.appendChild(opt);
    });
}

function limpiarFibra() {
    document.getElementById('form-fiber').reset();
    document.getElementById('input-code').value = '';
    document.getElementById('textarea-notes').value = '';
    document.getElementById('body-incidences').innerHTML =
        '<tr><td colspan="6" class="text-center text-muted py-3">No fiber line loaded.</td></tr>';
    ocultarIncidencia();
    syncCode();
}

function guardarFibra() {
    if (!document.getElementById('input-description').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'The Description field is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!document.getElementById('input-start-date').value) {
        Swal.fire({ title: 'OE Inventory', text: 'A valid Start Date is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    document.getElementById('input-action').value = 'save';
    document.getElementById('form-fiber').submit();
}

function mostrarIncidencia() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a fiber line first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    document.getElementById('incidence-panel').style.display = 'block';
}

function ocultarIncidencia() {
    document.getElementById('incidence-panel').style.display = 'none';
}

function excelIncidencias() {
    const code = currentCode();
    if (!code) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a fiber line first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    window.location = `?export=incidences&fiber=${encodeURIComponent(code)}`;
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-fibra').addEventListener('click', function (e) {
        const row = e.target.closest('tr.fiber-row');
        if (!row) return;
        document.getElementById('input-code').value = row.dataset.id;
        bootstrap.Tab.getOrCreateInstance(document.getElementById('tab-general-btn')).show();
        buscarFibraAjax();
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-fibra').DataTable({ pageLength: 50, ordering: true, autoWidth: false });
    }

    const pre = document.getElementById('preselected-fiber').value;
    if (pre) {
        document.getElementById('input-code').value = pre;
        buscarFibraAjax();
    }
});
