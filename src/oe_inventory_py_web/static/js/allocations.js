// Form logic for the Allocations screen (frmAllocations.html).

// Set to true right before an internal submit (assign / manual generate) so the
// "leave the page" beacon below doesn't fire on those reloads.
let allocSubmitting = false;

function populateSerials(selectId, serials, emptyLabel) {
    const sel = document.getElementById(selectId);
    sel.innerHTML = '';
    const placeholder = document.createElement('option');
    placeholder.value = '';
    placeholder.textContent = serials.length ? '-- Select one --' : emptyLabel;
    sel.appendChild(placeholder);
    serials.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.textContent = s;
        sel.appendChild(opt);
    });
}

function searchAvailable(url, selectId, emptyLabel) {
    fetch(url)
        .then(r => r.json())
        .then(data => {
            if (data.success) populateSerials(selectId, data.serials || [], emptyLabel);
        })
        .catch(err => console.error('Error searching available items:', err));
}

function searchDevices() {
    const type = encodeURIComponent(document.getElementById('select-device-type').value);
    const brand = encodeURIComponent(document.getElementById('select-device-brand').value);
    searchAvailable(`/api/allocations-search/?kind=devices&type=${type}&brand=${brand}`,
        'select-device-serial', '-- No available devices --');
}

function searchLicenses() {
    const type = encodeURIComponent(document.getElementById('select-license-type').value);
    searchAvailable(`/api/allocations-search/?kind=licenses&type=${type}`,
        'select-license-serial', '-- No available licenses --');
}

function searchPhones() {
    // Phones use an <input> + <datalist> so the user can type and filter the
    // available serials as they go (instead of a plain dropdown).
    fetch('/api/allocations-search/?kind=phones')
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;
            const dl = document.getElementById('phone-options');
            dl.innerHTML = '';
            (data.serials || []).forEach(s => {
                const opt = document.createElement('option');
                opt.value = s;
                dl.appendChild(opt);
            });
        })
        .catch(err => console.error('Error searching available phones:', err));
}

const SERIAL_SELECT = {
    assign_device: 'select-device-serial',
    assign_license: 'select-license-serial',
    assign_phone: 'select-phone-serial',
};

function asignar(action) {
    if (!document.getElementById('select-staff').value) {
        Swal.fire({ title: 'OE Inventory', text: 'You must select a staff member first.', icon: 'warning', confirmButtonColor: '#FF48D8' });
        return;
    }
    const value = document.getElementById(SERIAL_SELECT[action]).value.trim();
    if (!value) {
        Swal.fire({ title: 'OE Inventory', text: 'Select an item to assign.', icon: 'warning', confirmButtonColor: '#FF48D8' });
        return;
    }
    // The phone field is typeable: only allow a serial that exists in the list
    // of available phones (the datalist). Otherwise block the assignment.
    if (action === 'assign_phone') {
        const available = Array.from(document.querySelectorAll('#phone-options option')).map(o => o.value);
        if (!available.includes(value)) {
            Swal.fire({ title: 'OE Inventory', text: 'That serial number is not in the list of available phones. Pick one from the list.', icon: 'error', confirmButtonColor: '#FF48D8' });
            return;
        }
    }
    allocSubmitting = true;
    document.getElementById('input-action').value = action;
    document.getElementById('form-alloc').submit();
}

// Generate ONE allocation document for the selected staff (groups all the items
// already assigned into a single PDF, instead of one per assignment).
function generarDocAsignacion() {
    if (!document.getElementById('select-staff').value) {
        Swal.fire({ title: 'OE Inventory', text: 'Select a staff member first.', icon: 'warning', confirmButtonColor: '#FF48D8' });
        return;
    }
    allocSubmitting = true;
    document.getElementById('input-action').value = 'generate_doc';
    document.getElementById('form-alloc').submit();
}

// Safety net: if the user leaves the screen with assignments not yet documented
// (didn't press "Generate document"), tell the server to generate it now.
// Skipped on internal reloads (assign / manual generate).
window.addEventListener('pagehide', function () {
    if (allocSubmitting) return;
    const form = document.getElementById('form-alloc');
    const token = form ? form.querySelector('[name="csrfmiddlewaretoken"]') : null;
    if (!form || !token) return;
    const data = new FormData();
    data.append('action', 'auto_doc');
    data.append('csrfmiddlewaretoken', token.value);
    navigator.sendBeacon(form.getAttribute('action'), data);
});

document.addEventListener('DOMContentLoaded', function () {
    // Phones are loaded up front (as in the desktop version).
    searchPhones();
});
