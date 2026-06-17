// Form logic for the Visitors Access Cards screen (frmVisitorsAccessCards.html).

function currentCard() {
    return document.getElementById('input-card').value.trim();
}

function buscarVisitanteAjax() {
    const code = currentCard();
    if (!code) return;
    fetch(`/api/get-visitor-card/?card=${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillVisitor(res.data);
            } else {
                limpiarVisitante();
                document.getElementById('input-card').value = code;
                Swal.fire({ title: 'OE Inventory', text: 'Card not found. Fill the fields and Save to create it.', icon: 'info', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching visitor card:', err));
}

function fillVisitor(d) {
    document.getElementById('input-card').value = d.card || '';
    document.getElementById('input-fermax').value = d.fermax || '';
    document.getElementById('input-user').value = d.user || '';
    document.getElementById('select-state').value = d.state_id || '';
    document.getElementById('input-obs').value = d.obs || '';
    renderHistory(d.history || []);
}

function renderHistory(history) {
    const tbody = document.getElementById('body-history');
    tbody.innerHTML = '';
    if (!history.length) {
        tbody.innerHTML = '<tr><td colspan="2" class="text-center text-muted py-2">No history.</td></tr>';
        return;
    }
    history.forEach(h => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${h.id}</td><td>${(h.notes || '').replace(/</g, '&lt;')}</td>`;
        tbody.appendChild(tr);
    });
}

// Clear the editable fields when the user types a new card code, keeping the
// card field itself (same behaviour as the other forms).
function limpiarCamposVisitante() {
    document.getElementById('input-fermax').value = '';
    document.getElementById('input-user').value = '';
    document.getElementById('select-state').value = '';
    document.getElementById('input-obs').value = '';
    document.getElementById('body-history').innerHTML =
        '<tr><td colspan="2" class="text-center text-muted py-2">No card loaded.</td></tr>';
    document.querySelectorAll('.visitor-row').forEach(r => r.classList.remove('table-primary'));
}

function limpiarVisitante() {
    document.getElementById('form-visitor').reset();
    document.getElementById('input-card').value = '';
    renderHistory([]);
    document.getElementById('body-history').innerHTML =
        '<tr><td colspan="2" class="text-center text-muted py-2">No card loaded.</td></tr>';
    document.querySelectorAll('.visitor-row').forEach(r => r.classList.remove('table-primary'));
}

function guardarVisitante() {
    if (!currentCard() || !document.getElementById('input-fermax').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'The Card and Fermax MIF fields are mandatory.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    document.getElementById('form-visitor').submit();
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-visitantes').addEventListener('click', function (e) {
        const row = e.target.closest('tr.visitor-row');
        if (!row) return;
        document.getElementById('input-card').value = row.dataset.card;
        buscarVisitanteAjax();
    });
    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-visitantes').DataTable({ pageLength: 25, ordering: true, autoWidth: false });
    }
    const pre = document.getElementById('preselected-card').value;
    if (pre) {
        document.getElementById('input-card').value = pre;
        buscarVisitanteAjax();
    }
});
