// Form logic for the Orders screen (frmOrders.html).

function currentCode() {
    return document.getElementById('input-code').value.trim();
}

function syncCode() {
    document.getElementById('input-code-hidden').value = currentCode();
}

function setActionEnabled(id, enabled) {
    const btn = document.getElementById(id);
    btn.disabled = !enabled;
    btn.style.opacity = enabled ? '1' : '0.35';
}

function toggleActionButtons(d) {
    const canceled = d.cancelado === 1;
    const processed = d.tramitado === 1;
    const received = d.recibido === 1;
    const open = !canceled && !received;
    setActionEnabled('btn-cancel', open && !processed);
    setActionEnabled('btn-process', open && !processed);
    setActionEnabled('btn-receive', open && processed);
}

function buscarPedidoAjax() {
    const code = currentCode();
    if (!code) return;
    fetch(`/api/get-order/?id=${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillOrder(res.data);
            } else {
                limpiarPedido();
                document.getElementById('input-code').value = code;
                Swal.fire({ title: 'OE Inventory', text: 'Order not found. Fill the fields and Save to create it.', icon: 'info', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching order data:', err));
}

function fillOrder(d) {
    document.getElementById('input-code').value = d.id;
    document.getElementById('input-article').value = d.article || '';
    document.getElementById('input-uds').value = d.uds;
    document.getElementById('input-date').value = d.date || '';
    document.getElementById('textarea-notes').value = d.notes || '';
    syncCode();
    toggleActionButtons(d);
}

function limpiarPedido() {
    document.getElementById('form-order').reset();
    document.getElementById('input-code').value = '';
    document.getElementById('textarea-notes').value = '';
    syncCode();
    ['btn-cancel', 'btn-process', 'btn-receive'].forEach(id => setActionEnabled(id, false));
}

function guardarPedido() {
    if (!document.getElementById('input-article').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: "The 'Article' field cannot be empty.", icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!document.getElementById('input-date').value) {
        Swal.fire({ title: 'OE Inventory', text: 'A valid Date is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    document.getElementById('input-action').value = 'save';
    document.getElementById('form-order').submit();
}

function submitOrderAction(action, confirmText) {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load an order first.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    if (!confirm(confirmText)) return;
    syncCode();
    document.getElementById('input-action').value = action;
    document.getElementById('form-order').submit();
}

function cancelarPedido() { submitOrderAction('cancel', 'Do you want to cancel this order?'); }
function procesarPedido() { submitOrderAction('process', 'Do you want to process this order?'); }
function recibirPedido() { submitOrderAction('receive', 'Do you want to receive this order?'); }

document.addEventListener('DOMContentLoaded', function () {
    ['btn-cancel', 'btn-process', 'btn-receive'].forEach(id => setActionEnabled(id, false));

    ['tabla-pending', 'tabla-canceled', 'tabla-received'].forEach(tid => {
        const table = document.getElementById(tid);
        if (!table) return;
        table.addEventListener('click', function (e) {
            const row = e.target.closest('tr.order-row');
            if (!row) return;
            document.getElementById('input-code').value = row.dataset.id;
            buscarPedidoAjax();
        });
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        ['#tabla-pending', '#tabla-canceled', '#tabla-received'].forEach(sel => {
            jQuery(sel).DataTable({ pageLength: 25, ordering: true, autoWidth: false });
        });
        document.querySelectorAll('#ordersTabs button').forEach(btn => {
            btn.addEventListener('shown.bs.tab', () => {
                jQuery.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
            });
        });
    }

    const pre = document.getElementById('preselected-order').value;
    if (pre) {
        document.getElementById('input-code').value = pre;
        buscarPedidoAjax();
    }
});
