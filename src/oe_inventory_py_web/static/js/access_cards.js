// Form logic for the Access Cards screen (frmAccessCards.html).

function currentCard() {
    return document.getElementById('input-card').value.trim();
}

function buscarTarjetaAjax() {
    const code = currentCard();
    if (!code) return;
    fetch(`/api/get-card/?card=${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillCard(res.data);
            } else {
                limpiarTarjeta();
                document.getElementById('input-card').value = code;
                Swal.fire({ title: 'OE Inventory', text: 'Card does not exist. Fill the fields and Save to create it.', icon: 'info', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching card:', err));
}

function fillCard(d) {
    document.getElementById('input-card').value = d.card || '';
    document.getElementById('input-fermax').value = d.fermax || '';
    document.getElementById('input-pin').value = d.pin || '';
    // The staff dropdown only lists active people; if the card is assigned to
    // someone inactive (e.g. already terminated), add that option on the fly
    // so the name is shown instead of an empty selection.
    const selStaff = document.getElementById('select-staff');
    if (d.staff_id && !selStaff.querySelector('option[value="' + d.staff_id + '"]')) {
        const opt = document.createElement('option');
        opt.value = d.staff_id;
        opt.textContent = d.staff_name || ('#' + d.staff_id);
        selStaff.appendChild(opt);
    }
    selStaff.value = d.staff_id || '';
    document.getElementById('select-state').value = d.state_id || '';
    document.getElementById('input-obs').value = d.obs || '';
    document.getElementById('textarea-notes').value = d.notes || '';
}

function limpiarTarjeta() {
    document.getElementById('form-card').reset();
    document.getElementById('input-card').value = '';
    document.getElementById('textarea-notes').value = '';
    document.querySelectorAll('.card-row').forEach(r => r.classList.remove('table-primary'));
}

// Clear the editable fields when the user types a new card code, keeping the
// card field itself (same behaviour as frmDevices / frmPrinters).
function limpiarCamposTarjeta() {
    document.getElementById('input-fermax').value = '';
    document.getElementById('input-pin').value = '';
    document.getElementById('select-staff').value = '';
    document.getElementById('select-state').value = '';
    document.getElementById('input-obs').value = '';
    document.getElementById('textarea-notes').value = '';
    document.querySelectorAll('.card-row').forEach(r => r.classList.remove('table-primary'));
}

function generarPin() {
    if (document.getElementById('input-pin').value) {
        Swal.fire({ title: 'OE Inventory', text: "You can't create another PIN.", icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    fetch('/api/card-pin/')
        .then(r => r.json())
        .then(res => { if (res.success) document.getElementById('input-pin').value = res.pin || ''; })
        .catch(err => console.error('Error generating PIN:', err));
}

function guardarTarjeta() {
    if (!currentCard() || !document.getElementById('input-fermax').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'Card code and Fermax MIF are required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    document.getElementById('input-action').value = 'save';
    document.getElementById('form-card').submit();
}

function convertirVisitante() {
    if (!currentCard()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load a card first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm('Convert this card to a VISITOR card?')) return;
    document.getElementById('input-action').value = 'release';
    document.getElementById('form-card').submit();
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-tarjetas').addEventListener('click', function (e) {
        const row = e.target.closest('tr.card-row');
        if (!row) return;
        document.getElementById('input-card').value = row.dataset.card;
        buscarTarjetaAjax();
    });
    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-tarjetas').DataTable({ pageLength: 25, ordering: true, autoWidth: false });
    }
    const pre = document.getElementById('preselected-card').value;
    if (pre) {
        document.getElementById('input-card').value = pre;
        buscarTarjetaAjax();
    }
});
