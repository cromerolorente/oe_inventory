// Form logic for the Mobile Lines (SIM cards) screen (frmMobileLines.html).

function currentNumber() {
    return document.getElementById('input-number').value.trim();
}

function showPanel(mode) {
    document.getElementById('panel-mobile').style.display = (mode === 'normal') ? 'block' : 'none';
    document.getElementById('panel-esim').style.display = (mode === 'esim') ? 'block' : 'none';
    document.getElementById('panel-m2m').style.display = (mode === 'm2m') ? 'block' : 'none';
}

function onToggleEsim() {
    if (document.getElementById('chk-esim').checked) {
        document.getElementById('chk-m2m').checked = false;
        showPanel('esim');
    } else {
        showPanel('normal');
    }
}

function onToggleM2m() {
    if (document.getElementById('chk-m2m').checked) {
        document.getElementById('chk-esim').checked = false;
        showPanel('m2m');
    } else {
        showPanel('normal');
    }
}

function buscarLineaAjax() {
    const number = currentNumber();
    if (!number) return;
    fetch(`/api/get-line/?number=${encodeURIComponent(number)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillLine(res.data);
            } else {
                limpiarLinea();
                document.getElementById('input-number').value = number;
                Swal.fire({ title: 'OE Inventory', text: 'Mobile line not found. Fill the fields and Save to create it.', icon: 'info', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching mobile line:', err));
}

function fillLine(d) {
    document.getElementById('input-number').value = d.number || '';
    document.getElementById('select-company').value = d.company_id || '';
    document.getElementById('input-origin').value = d.origin || '';
    document.getElementById('input-date').value = d.date || '';
    document.getElementById('input-pin').value = d.pin || '';
    document.getElementById('input-pin2').value = d.pin2 || '';
    document.getElementById('input-puk').value = d.puk || '';
    document.getElementById('input-puk2').value = d.puk2 || '';
    document.getElementById('input-card').value = d.card || '';
    document.getElementById('input-extension').value = d.extension || '';
    document.getElementById('input-obs').value = d.obs || '';
    document.getElementById('input-person').value = d.person || '';
    document.getElementById('input-device-sn').value = d.phone_serial || '';
    document.getElementById('textarea-notes').value = d.notes || '';
    document.getElementById('chk-esim').checked = (d.esim === 1);
    document.getElementById('chk-m2m').checked = (d.m2m === 1);

    const baja = document.getElementById('alert-baja');
    if (d.baja) {
        baja.textContent = `Attention! This line was deactivated on ${d.baja}`;
        baja.style.display = 'block';
    } else {
        baja.style.display = 'none';
    }

    showPanel(d.mode || 'normal');
    syncNumbers();
}

function limpiarLinea(clearNumber) {
    // Keep what the user is typing in the Number field: form.reset() wipes every
    // field (including Number), so on each keystroke (oninput) we restore it.
    // Only an explicit clear (clearNumber = true, the Clear button) empties it.
    const num = document.getElementById('input-number').value;
    document.getElementById('form-line').reset();
    if (!clearNumber) document.getElementById('input-number').value = num;
    document.getElementById('input-person').value = '';
    document.getElementById('input-device-sn').value = '';
    document.getElementById('textarea-notes').value = '';
    document.getElementById('alert-baja').style.display = 'none';
    showPanel('normal');
    syncNumbers();
    document.querySelectorAll('.line-row').forEach(r => r.classList.remove('table-primary'));
}

function syncNumbers() {
    const num = currentNumber();
    ['num-mobile', 'num-esim', 'num-m2m'].forEach(id => { document.getElementById(id).value = num; });
}

function guardarLinea() {
    if (!currentNumber()) {
        Swal.fire({ title: 'OE Inventory', text: 'A line Number is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    document.getElementById('input-action').value = 'save';
    document.getElementById('form-line').submit();
}

function liberarLinea() {
    if (!currentNumber()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a line first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm('Do you want to unassign this line from its phone?')) return;
    document.getElementById('input-action').value = 'release';
    document.getElementById('form-line').submit();
}

function cancelarLinea() {
    if (!currentNumber()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a line first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm('Do you want to cancel this line with the provider?')) return;
    document.getElementById('input-action').value = 'cancel';
    document.getElementById('form-line').submit();
}

document.addEventListener('DOMContentLoaded', function () {
    // Validate + sync the line number into the assignment forms before submit.
    ['form-assign-mobile', 'form-assign-esim', 'form-assign-m2m'].forEach(fid => {
        document.getElementById(fid).addEventListener('submit', function (e) {
            const num = currentNumber();
            if (!num) {
                e.preventDefault();
                Swal.fire({ title: 'OE Inventory', text: 'Load a line first.', icon: 'info', confirmButtonColor: '#FF48D8' });
                return;
            }
            this.querySelector('input[name="number"]').value = num;
            const sel = this.querySelector('select');
            if (!sel.value) {
                e.preventDefault();
                Swal.fire({ title: 'OE Inventory', text: 'Select a value to assign.', icon: 'warning', confirmButtonColor: '#FF48D8' });
            }
        });
    });

    document.getElementById('tabla-lineas').addEventListener('click', function (e) {
        const row = e.target.closest('tr.line-row');
        if (!row) return;
        document.querySelectorAll('.line-row').forEach(r => r.classList.remove('table-primary'));
        row.classList.add('table-primary');
        document.getElementById('input-number').value = row.dataset.number;
        buscarLineaAjax();
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-lineas').DataTable({ pageLength: 25, ordering: true, autoWidth: false });
    }

    const pre = document.getElementById('preselected-number').value;
    if (pre) {
        document.getElementById('input-number').value = pre;
        buscarLineaAjax();
    }
});
